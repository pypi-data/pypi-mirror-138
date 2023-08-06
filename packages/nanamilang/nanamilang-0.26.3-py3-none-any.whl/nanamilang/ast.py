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
                # First, let's make it in the cheapest way ever:
                position = getattr(exception, '_position', None)
                # Non-custom exception obviously doesn't contain
                # _position; as we're working with s-expressions,
                # assume that exception occurred at the form start.
                if not position:
                    tree: list = args[1]
                    maybe_token: Token = tree[0]
                    if isinstance(maybe_token, Token):
                        position = maybe_token.position()
                # We tried so hard ... but position is still unknown
                if not position:
                    position = (m_name, 1, 1)
                # So we use a mock position triplet (1 line & 1 char).
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

        self._call_stack = []

        self._m_name = m_name
        self._tokenized = tokenized

        # If something went wrong, cast occurred exception into custom
        # NException instance, and only store NException Token in wood
        try:
            self._wood = self._create()
        except (Exception,) as _:
            exc_traceback = _.__traceback__
            self._wood = [Token(
                Token.NException,
                (ASTBuildInvalidInput().with_traceback(exc_traceback),
                 (m_name, 1, 1), self._call_stack))]

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

        # export() should cover method with spec rules
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

        return items  # <- finally, return built AST based on tokens input

    def evaluate(self, me) -> tuple:
        """NanamiLang AST, evaluate entire NanamiLang module recursively"""

        @handle((Exception,), self._m_name, self._call_stack)
        def recursive(environment: dict,
                      token_or_form: Token or List[Token]) -> datatypes.Base:
            if not token_or_form:
                return datatypes.Nil('nil')
            if isinstance(token_or_form, Token):
                return recursive(environment, [Token(Token.Identifier, 'identity'),
                                               token_or_form])  # <- this is just temporary solution
            args: List[datatypes.Base] = []
            identifier_token_or_form: List[Token] or Token
            rest: List[Token or List[Token]]
            identifier_token_or_form, *rest = token_or_form
            # If identifier_token_or_form is a Token.Identifier pointing to Macro, handle macro call
            if isinstance(identifier_token_or_form, Token):
                if isinstance(identifier_token_or_form.dt(), datatypes.Macro):
                    self._call_stack.append({'kind': 'mc', 'args': [],
                                             'name': identifier_token_or_form.dt().origin()})
                    return recursive(
                        environment,
                        identifier_token_or_form.dt().reference()(rest, environment, me, recursive))
            # Start collecting args list for a Function call. Each expression form will be evaluated
            for part_token_or_form in rest:
                if isinstance(part_token_or_form, Token):
                    # If token is Identifier, try to lookup for the local, then global user bindings
                    if part_token_or_form.type() == part_token_or_form.Identifier:
                        user_bound = environment.get(part_token_or_form.dt().origin(),
                                                     me.get(part_token_or_form.dt().origin()))
                        # If identifier was marked as Undefined and wasn't bound, raise an exception
                        if isinstance(part_token_or_form.dt(), datatypes.Undefined):
                            if not user_bound:
                                raise ASTEvalNotFoundInThisContent(part_token_or_form)
                        # If user bound data type is actually an exception raised earlier, propagate
                        if isinstance(user_bound, datatypes.NException):
                            return user_bound
                        args.append(user_bound or part_token_or_form.dt())
                        # If user bound data type does not exist, add token bundled data type to the
                        # Function call args list, add a user bound data type to args list otherwise
                    else:
                        # If data type is actually an exception that we have raised above, propagate
                        if isinstance(part_token_or_form.dt(), datatypes.NException):
                            return part_token_or_form.dt()
                        args.append(part_token_or_form.dt())
                        # If token isn't an Identifier, add token bundled data type to the args list
                else:
                    # If the next part is actually an expression form, evaluate it recursively first
                    result_or_nexception = recursive(environment, part_token_or_form)
                    # If exception has been occurred during expression form evaluation, propagate it
                    if isinstance(result_or_nexception, datatypes.NException):
                        return result_or_nexception
                    args.append(result_or_nexception)
                    # If nothing expression form has been evaluated to normal data type, add to args
            # Finally, we almost ready to handle a Function call. But we need to handle expressions.
            if isinstance(identifier_token_or_form, list):
                # Like a Function argument, expression form needs to be recursively evaluated first.
                result_or_nexception = recursive(environment, identifier_token_or_form)
                # And of course, if expression form has been evaluated to an exception, propagate it
                if isinstance(result_or_nexception, datatypes.NException):
                    return result_or_nexception
                # And, if an expression form has been evaluated to a Function data type, handle call
                if isinstance(result_or_nexception, datatypes.Function):
                    return result_or_nexception.reference()(args)
                # Also, let's handle casting Keyword to a Function call using 'get' builtin function
                if isinstance(result_or_nexception, datatypes.Keyword):
                    return BuiltinFunctions.get_func(args + [result_or_nexception])
                raise ASTEvalIsNotAFunctionDataType(Token(Token.Proxy, result_or_nexception))
                # If expression form has not been evaluated to a Function or a Keyword data type, we
                # will raise ASTEvalIsNotAFunctionDataType, using casting evaluation result to proxy
            # As said earlier, we make it possible for a user to cast Keyword to a Function call, so
            if identifier_token_or_form.type() == identifier_token_or_form.Keyword:
                self._call_stack.append({
                    'kind': 'fn',
                    'name': 'get', 'args': args + [identifier_token_or_form.dt()]
                })
                return BuiltinFunctions.get_func(args + [identifier_token_or_form.dt()])
            # And yes, here we also need to check whether identifier token is pointing to user bound
            if identifier_token_or_form.type() == identifier_token_or_form.Identifier:
                # Here, we make it possible for a user to call a possibly @exported data type method
                maybe_dot_started = identifier_token_or_form.dt().origin()
                if maybe_dot_started.startswith('.'):
                    if len(args) < 1:
                        # If dot-expression arity is wrong, we will raise ASTEvalInvalidDotExprArity
                        raise ASTEvalInvalidDotExprArity(identifier_token_or_form)
                    dot_expression_result = self.dot(maybe_dot_started[1:], args[0], args[1:])
                    if dot_expression_result is not None:
                        return dot_expression_result
                    # But if method wasn't exported or doesn't exist, raise ASTEvalNotExportedMethod
                    raise ASTEvalNotExportedMethod(identifier_token_or_form)
                # Here, we also need to handle possible both user local and global bound data types:
                user_bound = environment.get(identifier_token_or_form.dt().origin(),
                                             me.get(identifier_token_or_form.dt().origin()))
                # If the Identifier was initially marked as Undefined, raise exception if not bound.
                if isinstance(identifier_token_or_form.dt(), datatypes.Undefined):
                    if not user_bound:
                        raise ASTEvalNotFoundInThisContent(identifier_token_or_form)
                # Here we store data type to dispatch it later (dispatch Function/Keyword data type)
                d_type = user_bound or identifier_token_or_form.dt()
                # If it is a Function, simply call it using the collected function arguments vector.
                if isinstance(d_type, datatypes.Function):
                    self._call_stack.append({'name': d_type.origin(), 'kind': 'fn', 'args': args})
                    return d_type.reference()(args)
                # If it is a Keyword, call builtin 'get' function passing store data type as 1st arg
                if isinstance(d_type, datatypes.Keyword):
                    self._call_stack.append({'name': 'get', 'kind': 'fn', 'args': args + [d_type]})
                    return BuiltinFunctions.get_func(args + [d_type])
                # Well, this is how AST.evaluate().recursive() function handles built AST evaluation
            raise ASTEvalIsNotAFunctionDataType(identifier_token_or_form)
            # Also, we handle a non-Function data type call by raising ASTEvalIsNotAFunctionDataType

        return tuple(recursive({}, _tree) for _tree in self.wood())
        # Iterating through wood of trees, evaluate each tree, and return collected tuple of results
