"""NanamiLang AST CLass"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from functools import wraps
from typing import List

from nanamilang.spec import Spec
from nanamilang import datatypes
from nanamilang.token import Token
from nanamilang.builtin import BuiltinFunctions
from nanamilang.shortcuts import ASSERT_IS_CHILD_OF
from nanamilang.shortcuts import ASSERT_COLLECTION_NOT_EMPTY
from nanamilang.shortcuts import ASSERT_EVERY_COLLECTION_ITEM_IS_CHILD_OF


def handle(exceptions: tuple, m_name: str, cs: list):
    """
    NanamiLang AST, handle exceptions:
    1. If exception has been suddenly raised
    2. Try to determine position where it happened
    3. Create & return datatypes.MException instance

    :param m_name: currently evaluating module name
    :param exceptions: tuple of exceptions to handle
    :param cs: call stack of nanamilang macros/functions
    """

    def wrapped(_fn):
        @wraps(_fn)
        def function(*args, **kwargs):
            try:
                return _fn(*args, **kwargs)
            except exceptions as exception:
                # At least __try__ to
                # determine error occurrence position
                # First, lets make it in the cheapest way ever
                position = getattr(exception, '_position', None)
                # Non-custom exception obviously doesn't contain
                # _position; as we're working with s-expressions,
                # assume that exception occurred at the f/m call.
                if not position:
                    tree: list = args[1]
                    maybe_token: Token = tree[0]
                    if isinstance(maybe_token, Token):
                        position = maybe_token.position()
                # We tried so hard ... but position still is None
                if not position:
                    position = (m_name, 1, 1)
                # Guessing position is freaking hell, to be honest ...
                return datatypes.NException((exception, position, cs))

        return function

    return wrapped


class ASTBuildInvalidInput(Exception):
    """
    NML AST Build Error: Invalid input
    """

    def __str__(self):
        """NanamiLang ASTBuildInvalidInput"""

        # Do not scare AST._create() please :(
        return 'Unable to create an AST from input'


class ASTBuildInvalidToken(Exception):
    """
    NML AST Build Error: Invalid token
    """

    _token: Token
    _position: tuple

    def __str__(self):
        """NanamiLang ASTBuildInvalidToken"""

        return self._token.reason()

    def __init__(self, token: Token, *args):
        """NanamiLang ASTBuildInvalidToken"""

        self._token = token
        self._position = token.position()

        super(ASTBuildInvalidToken).__init__(*args)


class ASTEvalNotFoundInThisContent(Exception):
    """
    NML AST Eval Error: Not found in this content
    """

    _name: str
    _position: tuple

    def __init__(self, token: Token, *args):
        """NanamiLang ASTEvalNotFoundInThisContent"""

        # token.dt().origin() is the actual identifier name
        self._name = token.dt().origin()
        self._position = token.position()

        super(ASTEvalNotFoundInThisContent).__init__(*args)

    def __str__(self):
        """NanamiLang ASTEvalNotFoundInThisContent"""

        return f"There's no '{self._name}' in this context"


class ASTEvalIsNotAFunctionDataType(Exception):
    """
    NML AST Eval Error: Not a function data type
    """

    _name: str
    _position: tuple

    def __init__(self, token: Token, *args):
        """NanamiLang ASTEvalIsNotAFunctionDataType"""

        # Would be either a name of (re)defined identifier,
        # or name of the data type user has tried to call()
        self._name = token.dt().origin() or token.dt().name
        self._position = token.position()

        super(ASTEvalIsNotAFunctionDataType).__init__(*args)

    def __str__(self):
        """NanamiLang ASTEvalIsNotAFunctionDataType"""

        return f'"{self._name}" is not a Function Data Type'


class ASTEvalInvalidDotExprArity(Exception):
    """
    NML AST Eval Error: Invalid dot-expr arity
    """

    _name: str
    _position: tuple

    def __init__(self, token: Token, *args):
        """NanamiLang ASTEvalInvalidDotExprArity"""

        # Would be either a name of (re)defined identifier,
        # or name of the data type user has tried to call()
        self._name = token.dt().origin() or token.dt().name
        self._position = token.position()

        super(ASTEvalInvalidDotExprArity).__init__(*args)

    def __str__(self):
        """NanamiLang ASTEvalInvalidDotExprArity"""

        return f'{self._name}: invalid dot-expression arity'


class ASTEvalNotExportedMethod(Exception):
    """
    NML AST Eval Error: Method wasn't exported (or missing)
    """

    _name: str
    _position: tuple

    def __init__(self, token: Token, *args):
        """NanamiLang ASTEvalNotExportedMethod"""

        # Would be either a name of (re)defined identifier,
        # or name of the data type user has tried to call()
        self._name = token.dt().origin() or token.dt().name
        self._position = token.position()

        super(ASTEvalNotExportedMethod).__init__(*args)

    def __str__(self):
        """NanamiLang ASTEvalNotExportedMethod"""

        return f'Unable to call method named "{self._name}"'


class AST:
    """
    NanamiLang AST (abstract syntax tree)
    """

    _call_stack = None
    _m_name: str = None
    _tokenized: List[Token] = None
    _wood: List[List[Token] or Token] = None

    def __init__(self, tokenized: List[Token], m_name: str) -> None:
        """
        Initialize a new NanamiLang AST instance

        :param m_name: the module name to built AST for
        :param tokenized: collection of Token instances
        """

        ASSERT_IS_CHILD_OF(m_name, str,
                           'AST: module name needs to be a string')
        ASSERT_COLLECTION_NOT_EMPTY(
            m_name, 'AST: module name could not be an empty string')

        ASSERT_IS_CHILD_OF(tokenized, list,
                           'AST: token instances needs to be a list')
        ASSERT_COLLECTION_NOT_EMPTY(
            tokenized, 'AST: at least 1 token instance was expected')
        ASSERT_EVERY_COLLECTION_ITEM_IS_CHILD_OF(
            tokenized,
            Token,
            'AST: each tokens instances list item needs to be Token')

        self._m_name = m_name
        self._tokenized = tokenized

        self._call_stack = []  # <--- initialize nanamilang call stack

        # If something went wrong while building a tree -> NException!
        try:
            self._wood = self._create()
        except (Exception,) as _:
            exc_traceback = _.__traceback__
            self._wood = [Token(
                Token.NException,
                (ASTBuildInvalidInput().with_traceback(exc_traceback),
                 (m_name, 1, 1), self._call_stack)
            )]

    @staticmethod
    def dot(name, inst, args) -> (None
                                  or datatypes.Base):
        """NanamiLang AST, handle a dot-expression"""

        method = getattr(inst, name, None)
        if not method:
            return None

        exported = getattr(method, 'exported', False)
        if not exported:
            return None

        # export() should cover method with nml specs!
        method_specs = getattr(method, 'specs', False)

        Spec.validate(f'{inst}.{name}',
                      args, method_specs)
        # Spec.validate() could raise an Exception :))

        return method(*args)  # < return method result

    def cs(self) -> list:
        """NanamiLang AST, self._cs getter"""

        return self._call_stack

    def wood(self) -> list:
        """NanamiLang AST, self._wood getter"""

        return self._wood

    def _create(self) -> Token or List[Token] or list:
        """NanamiLang AST, create an actual wood of trees"""

        # Initially was written by @buzzer13 (https://gitlab.com/buzzer13)

        items = []
        stack = [items]

        for token in self._tokenized:

            if token.type() == Token.ListBegin:

                wired = []
                stack[-1].append(wired)
                stack.append(wired)

            elif token.type() == Token.ListEnd:

                stack.pop()

            elif token.type() == Token.Invalid:

                # Propagate Invalid token as a NException
                return [Token(
                    Token.NException,
                    (ASTBuildInvalidToken(token),
                        token.position(), self._call_stack)
                )]

            else:

                stack[-1].append(token)

        return items  # <- and each of them can be just a Token, or a form

    def evaluate(self, me) -> tuple:
        """NanamiLang AST, evaluate entire NanamiLang module recursively"""

        @handle((Exception,), self._m_name, self._call_stack)
        def recursive(environment: dict,
                      token_or_form: Token or List[Token]) -> datatypes.Base:
            if not token_or_form:
                return datatypes.Nil('nil')
            if isinstance(token_or_form, Token):
                return recursive(environment, [Token(Token.Identifier, 'identity'),
                                               token_or_form])  # <- tmp solution :D
            args: List[datatypes.Base] = []
            identifier: List[Token] or Token
            rest: List[Token or List[Token]]
            identifier, *rest = token_or_form
            # If identifier is a Macro, handle it ...
            if isinstance(identifier, Token):
                if isinstance(identifier.dt(), datatypes.Macro):
                    self._call_stack.append({'kind': 'mc', 'args': [],
                                             'name': identifier.dt().origin()})
                    return recursive(
                        environment,
                        identifier.dt().reference()(rest, environment, me, recursive))
            # Start collecting arguments for a Function call ...
            for part in rest:
                if isinstance(part, Token):
                    # If token is Identifier, try to handle bindings ...
                    if part.type() == part.Identifier:
                        defined = environment.get(part.dt().origin(),
                                                  me.get(part.dt().origin()))
                        # If token was initially marked as an Undefined ...
                        # check whether it has been defined somewhere above ...
                        if isinstance(part.dt(), datatypes.Undefined):
                            if not defined:
                                raise ASTEvalNotFoundInThisContent(part)
                        if isinstance(defined, datatypes.NException):
                            return defined  # <- propagate possible exception
                        args.append(defined if defined is not None else part.dt())
                        # If token was NOT initially marked as an Undefined
                        # add its bundled data type to arg list, add a 'defined' otherwise
                    else:
                        if isinstance(part.dt(), datatypes.NException):
                            return part.dt()  # <- propagate possible exception
                        args.append(part.dt())
                    # If it is something different from Identifier, add its bundled datatype
                else:
                    # Since we use handle() decorator, it can return
                    # an NException data type instance, so handle it ..
                    result_or_nexception = recursive(environment, part)
                    if isinstance(result_or_nexception, datatypes.NException):
                        return result_or_nexception
                    # Don't add NException to args, return it instead (exception-propagation)
                    args.append(result_or_nexception)
                    # If nothing critical happened -> append a 'result_or_nexception' to args
            # Finally, we almost ready to handle a Function call
            if isinstance(identifier, list):
                # Since we use handle() decorator, it can return
                # an NException data type instance, so handle it ..
                result_or_nexception = recursive(environment, identifier)
                if isinstance(result_or_nexception, datatypes.NException):
                    return result_or_nexception
                # Do not call NException reference, return it instead (exception-propagation)
                if isinstance(result_or_nexception, datatypes.Function):
                    return result_or_nexception.reference()(args)
                if isinstance(result_or_nexception, datatypes.Keyword):
                    return BuiltinFunctions.get_func(args + [result_or_nexception])
                raise ASTEvalIsNotAFunctionDataType(identifier[0])
                # If nothing critical happened -> call 'result_or_exception'.reference(args).
            if identifier.type() == identifier.Keyword:
                self._call_stack.append({
                    'kind': 'fn',
                    'name': 'get', 'args': args + [identifier.dt()]
                })
                return BuiltinFunctions.get_func(args + [identifier.dt()])
            if identifier.type() == identifier.Identifier:
                maybe_dot_started = identifier.dt().origin()
                if maybe_dot_started.startswith('.'):
                    if len(args) < 1:
                        raise ASTEvalInvalidDotExprArity(identifier)
                    ret = self.dot(maybe_dot_started[1:], args[0], args[1:])
                    if ret is not None:
                        return ret
                    raise ASTEvalNotExportedMethod(identifier)  # <- not exported, or missing
                defined = environment.get(identifier.dt().origin(), me.get(identifier.dt().origin()))
                if isinstance(identifier.dt(), datatypes.Undefined):
                    if not defined:
                        raise ASTEvalNotFoundInThisContent(identifier)
                dt = defined or identifier.dt()
                if isinstance(dt, datatypes.Function):
                    self._call_stack.append({
                        'name': dt.origin(), 'kind': 'fn', 'args': args
                    })
                    return dt.reference()(args)
                if isinstance(dt, datatypes.Keyword):
                    self._call_stack.append({
                        'name': 'get', 'kind': 'fn', 'args': args + [dt]
                    })
                    return BuiltinFunctions.get_func(args + [dt])
            raise ASTEvalIsNotAFunctionDataType(identifier)
            # If user tries to call Keyword or a Function, handle it, otherwise raise Exception

        return tuple(recursive({}, _tree) for _tree in self.wood())
        # Iterate through wood of trees, collect results, and return them to AST.evaluate(...) caller
