"""NanamiLang Builtin- Macros/Functions classes"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

import functools
from typing import List
from copy import deepcopy
from functools import reduce

from nanamilang.destruct import Destructuring
from nanamilang.spec import Spec
from nanamilang.token import Token
from nanamilang import fn, datatypes, loader
from nanamilang.shortcuts import (
    NML_M_ASSERT_COLL_FORM_ITEMS_COUNT_IS,
    NML_M_ASSERT_COLL_FORM_ITEMS_COUNT_IS_EVEN,
    NML_M_ASSERT_FORM_IS_A_VECTOR,
    NML_M_ASSERT_FORM_IS_A_HASHMAP,
    NML_M_ITERATE_AS_PAIRS, ASSERT_DICT_CONTAINS_KEYS,
    dashcase2capitalcase, plain2partitioned, randstr, get
)


def nanamilang_vector_to_spec_rules(vector: datatypes.Vector):
    """Recursively convert Vector coll to valid Spec rules list"""

    def recursively_processed(dt):
        if isinstance(dt, datatypes.String):
            return datatypes.DataType.resolve(dt.reference())
        if isinstance(dt, datatypes.Keyword):
            return dashcase2capitalcase(dt.reference())
        if isinstance(dt, datatypes.Vector):
            return [recursively_processed(i) for i in dt.items()]
        return None  # <- unreachable, but to make Pylint happy :)

    return [recursively_processed(item) for item in vector.items()]


def meta(data: dict):
    """
    NanamiLang, apply metadata to the handler function
    'name': function or macro LISP name (to access as)
    'forms': possible function or macro possible forms
    'docstring': what function or macro actually does?
    May contain 'spec' attribute, but could be omitted

    :param data: a function metadata Python dictionary
    """

    def wrapped(_fn):
        @functools.wraps(_fn)
        def function(*args, **kwargs):

            spec = data.get('spec')
            if spec:
                Spec.validate(data.get('name'), args[0], spec)

            return _fn(*args, **kwargs)

        ASSERT_DICT_CONTAINS_KEYS(data,
                                  {'name', 'forms', 'docstring'},
                                  'function meta must have "name", "forms" and "docstring" keys!')

        if 'BuiltinMacro' in function.__qualname__:
            data.update({'kind': 'macro'})
        elif 'BuiltinFunctions' in function.__qualname__:
            data.update({'kind': 'function'})  # <- do not require a meta data to contain kind key

        function.meta = data

        return function

    return wrapped  # <- register builtin function/macro handle to access it inside the NanamiLang


class BuiltinMacros:
    """NanamiLang Builtin Macros"""

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': 'do',
           'forms': ['(do form1 form2 ... formN)'],
           'docstring': 'Run all given forms, returns last evaluation result'})
    def do_macro(tree: list, local_env: dict, _, eval_function) -> list or Token:
        """
        Builtin 'do' macro implementation

        :param tree: a form given to this macro
        :param local_env: local environment during expr eval
        :param _: unused argument, but I need to mention it here
        :param eval_function: reference to recursive eval function
        :return: the modified or new source tree as it would be expected
        """

        evaluated = Token(Token.Nil, 'nil')

        for token_or_form in tree:
            evaluated = eval_function(local_env, token_or_form)
            if isinstance(evaluated, datatypes.NException):
                return Token(Token.Proxy, evaluated)  # <---- propagate possibly created NException instance

        return Token(Token.Proxy, evaluated)  # <--------------------------------- return the last evaluated

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': '->',
           'forms': ['(-> form1 form2 ... formN)'],
           'docstring': 'Each next form wraps previous one'})
    def first_threading_macro(tree: list, *_: tuple) -> list or Token:
        """
        Builtin '->' macro implementation

        :param tree: a form given to this macro
        :param _: unused argument, but I need to mention it here
        :return: the modified or new source tree as it would be expected
        """

        if not len(tree) > 1:
            return tree[-1]  # <------------------------------ if tree contains only one item, return it

        tree = deepcopy(tree)

        for idx, tof in enumerate(tree):
            if len(tree) - 1 != idx:
                next_tof = tree[idx + 1]
                if isinstance(next_tof, list):
                    tree[idx + 1].insert(1, tof)
                else:
                    tree[idx + 1] = [next_tof, tof]

        return tree[-1]  # <----------------------------- will return the last form of the modified tree

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': '->>',
           'forms': ['(->> form1 form2 ... formN)'],
           'docstring': 'Each next form wraps previous one'})
    def last_threading_macro(tree: list, *_: tuple) -> list or Token:
        """
        Builtin '->>' macro implementation

        :param tree: a form given to this macro
        :param _: unused argument, but I need to mention it here
        :return: the modified or new source tree as it would be expected
        """

        if not len(tree) > 1:
            return tree[-1]  # <------------------------------ if tree contains only one item, return it

        tree = deepcopy(tree)

        for idx, tof in enumerate(tree):
            if len(tree) - 1 != idx:
                next_tof = tree[idx + 1]
                if isinstance(next_tof, list):
                    tree[idx + 1].append(tof)
                else:
                    tree[idx + 1] = [next_tof, tof]

        return tree[-1]  # <----------------------------- will return the last form of the modified tree

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 3]],
           'name': 'if',
           'forms': ['(if cond then-branch else-branch)'],
           'docstring': 'Returns then/else branch depending on the condition'})
    def if_macro(tree: list, local_env: dict, _, eval_function) -> list or Token:
        """
        Builtin 'if' macro implementation

        :param tree: a form given to this macro
        :param local_env: local environment during expr eval
        :param _: unused argument, but I need to mention it here
        :param eval_function: reference to recursive eval function
        :return: the modified or new source tree as it would be expected
        """

        cond, then_branch, else_branch = tree

        evaluated = eval_function(local_env, cond)
        if isinstance(evaluated, datatypes.NException):
            return Token(Token.Proxy, evaluated)  # <---- propagate possibly created NException instance

        return then_branch if evaluated.truthy() is True else else_branch  # return corresponding branch

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityEven]],
           'name': 'cond',
           'forms': ['(cond cond1 expr1 ... condN exprN)'],
           'docstring': 'Allows you to describe your condition-expression pairs'})
    def cond_macro(tree: list, local_env: dict, _, eval_function) -> list or Token:
        """
        Builtin 'cond' macro implementation

        :param tree: a form given to this macro
        :param local_env: local environment during expr eval
        :param _: unused argument, but I need to mention it here
        :param eval_function: reference to recursive eval function
        :return: the modified or new source tree as it would be expected
        """

        for [cond, expr] in plain2partitioned(tree):

            evaluated = eval_function(local_env, cond)
            if isinstance(evaluated, datatypes.NException):
                return Token(Token.Proxy, evaluated)  # <-------- propagate possible NException instance

            if evaluated.truthy():
                return expr  # <----- return expression if corresponding evaluated condition is truthy()

        return Token(Token.Nil, 'nil')  # <- if nothing has been supplied to macro, return nil data type

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': 'comment',
           'forms': ['(comment ...)'],
           'docstring': 'Allows you to replace entire form with a Nil'})
    def comment_macro(*_: tuple) -> list or Token:
        """
        Builtin 'comment' macro implementation

        :param _: unused argument, but I need to mention it here
        :return: the modified or new source tree as it would be expected
        """

        return Token(Token.Nil, 'nil')  # <- as it was said in docstring, we just return a Nil data type

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityVariants, [1, 2, 3]]],
           'name': 'fn',
           'forms': ['(fn [p1 p2 ...])',
                     '(fn [p1 p2 ...] body)',
                     '(fn fn-name [p1 p2 ...] body)'],
           'docstring': 'Allows to define anonymous, maybe named, function'})
    def fn_macro(tree: list, local_env: dict, _, eval_function) -> list or Token:
        """
        Builtin 'fn' macro implementation

        :param tree: a form given to this macro
        :param local_env: local environment during expr eval
        :param _: unused argument, but I need to mention it here
        :param eval_function: reference to recursive eval function
        :return: the modified or new source tree as it would be expected
        """

        name_token, parameters_form, body_token_or_form = None, [], None

        if len(tree) == 1:
            parameters_form, body_token_or_form = tree + [Token(Token.Nil, 'nil')]
        elif len(tree) == 2:
            parameters_form, body_token_or_form = tree
        else:
            name_token, parameters_form, body_token_or_form = tree
            assert isinstance(name_token, Token),        'fn: name needs to be a token, not a form'
            assert name_token.type() == Token.Identifier,      'fn: name needs to be an Identifier'

        NML_M_ASSERT_FORM_IS_A_VECTOR(parameters_form,  'fn: parameters form needs to be a Vector')

        fn_name = name_token.dt().origin() if name_token else randstr()

        fni = fn.Fn(body_token_or_form, local_env, eval_function, fn_name, parameters_form)
        fn_handle = lambda args: fni.handle(tuple(args))  # <- we cannot call fni.handle() directly

        fn_handle.meta = {
            'name': fn_name, 'docstring': '',
            'kind': 'function', 'forms': fni.generate_meta__forms()
        }

        payload = {fn_name: datatypes.Function({'function_name': fn_name, 'function_reference': fn_handle})}

        local_env.update(payload)  # <----- update local environment, thus AST will be aware of our function
        fni.env().update(payload)  # <----- and also we need to update function closure for the same purpose

        return Token(Token.Identifier, fn_name)  # <-- gonna return locally defined NanamiLang function name

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': 'or',
           'forms': ['(or expr1 expr2 ... exprN)'],
           'docstring': 'Returns nil by default, last if everything is falsie'})
    def or_macro(tree: list, local_env: dict, _, eval_function) -> list or Token:
        """
        Builtin 'or' macro implementation

        :param tree: a form given to this macro
        :param local_env: local environment during expr eval
        :param _: unused argument, but I need to mention it here
        :param eval_function: reference to recursive eval function
        :return: the modified or new source tree as it would be expected
        """

        if not tree:
            return Token(Token.Nil, 'nil')  # <------------------------------ by default, gonna return nil data type

        for condition in tree:

            evaluated = eval_function(local_env, condition)
            if isinstance(evaluated, datatypes.NException) or evaluated.truthy():
                return Token(Token.Proxy, evaluated)  # <------------------ return if its NException or a truthy one

        return tree[-1]  # <- like in Clojure and other LISP engines: everything is falsie - return the last element

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': 'and',
           'forms': ['(and expr1 expr2 ... exprN)'],
           'docstring': 'Returns true by default, last if everything is truthy'})
    def and_macro(tree: list, local_env: dict, _, eval_function) -> list or Token:
        """
        Builtin 'and' macro implementation

        :param tree: a form given to this macro
        :param local_env: local environment during expr eval
        :param _: unused argument, but I need to mention it here
        :param eval_function: reference to recursive eval function
        :return: the modified or new source tree as it would be expected
        """

        if not tree:
            return Token(Token.Boolean, True)  # <-------------------------- by default, gonna return true data type

        for cond in tree:

            evaluated = eval_function(local_env, cond)
            if isinstance(evaluated, datatypes.NException) or not evaluated.truthy():
                return Token(Token.Proxy, evaluated)  # <------------------ return if its NException or a falsie one

        return tree[-1]  # <- like in Clojure and other LISP engines: everything is truthy - return the last element

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2]],
           'name': 'def',
           'forms': ['(def binding dtype)'],
           'docstring': 'Allows to define global binding and access it later'})
    def def_macro(tree: list, local_env: dict, module_env, eval_function) -> list or Token:
        """
        Builtin 'def' macro implementation

        :param tree: a form given to this macro
        :param local_env: local environment during expr eval
        :param module_env: module environment we are free to modify
        :param eval_function: reference to recursive eval function
        :return: modified or new source tree as it would be expected
        """

        binding_token, dtype_token_or_form = tree

        assert not isinstance(binding_token, list),                                'def: binding could not be a form'
        assert binding_token.type() == Token.Identifier,                     'def: binding needs to be an Identifier'

        evaluated = eval_function(local_env, dtype_token_or_form)
        if isinstance(evaluated, datatypes.NException):
            return Token(Token.Proxy, evaluated)  # <----------------- propagate possibly created NException instance

        name = binding_token.dt().origin()

        module_env.set(name, evaluated)

        return Token(Token.Identifier, name)  # <- as it would be expected, def returns globally defined binding name

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityVariants, [2, 3, 4, 5]]],
           'name': 'defn',
           'forms': ['(defn name [p1 p2 ...])',
                     '(defn name [p1 p2 ...] body)',
                     '(defn name docstring [p1 p2 ...] body)',
                     '(defn name docstring spec [p1 p2 ...] body)'],
           'docstring': 'Allows to define named, maybe documented, spec-covered, function'})
    def defn_macro(tree: list, local_env: dict, module_env, eval_function) -> list or Token:
        """
        Builtin 'defn' macro implementation

        :param tree: a form given to this macro
        :param local_env: local environment during expr eval
        :param module_env: module environment we are free to modify
        :param eval_function: reference to recursive eval function
        :return: modified or new source tree as it would be expected
        """

        __defs__ = None, None, [], [], None
        name_token, docstring_token, spec_form, parameters_form, body_token_or_form = __defs__

        if len(tree) == 2:
            name_token, parameters_form, body_token_or_form = tree + [Token(Token.Nil, 'nil')]
        elif len(tree) == 3:
            name_token, parameters_form, body_token_or_form = tree
        elif len(tree) == 4:
            name_token, docstring_token, parameters_form, body_token_or_form = tree
        else:
            name_token, docstring_token, spec_form, parameters_form, body_token_or_form = tree

        assert isinstance(name_token, Token),                   'defn: name needs to be a token, not a form'
        assert name_token.type() == Token.Identifier,                    'defn: name needs to be Identifier'

        if docstring_token:
            assert isinstance(docstring_token, Token),     'defn: docstring needs to be a token, not a form'
            assert docstring_token.type() == Token.String,            'defn: docstring needs to be a String'

        ####################################################################################################

        spec_list = []

        if spec_form:
            NML_M_ASSERT_FORM_IS_A_HASHMAP(spec_form,               'defn: spec form needs to be a HashMap')
            NML_M_ASSERT_COLL_FORM_ITEMS_COUNT_IS_EVEN(spec_form,   'defn: spec form needs to be a HashMap')

            evaluated = eval_function(local_env, spec_form)
            if isinstance(evaluated, datatypes.NException):
                return Token(Token.Proxy, evaluated)  # <- thus, we propagate a possible NException instance

            spec_list = nanamilang_vector_to_spec_rules(evaluated.get(datatypes.Keyword('nanamilang-spec')))

        #####################################################################################################

        NML_M_ASSERT_FORM_IS_A_VECTOR(parameters_form, 'defn: function parameters form needs to be a Vector')

        fn_name = name_token.dt().origin()

        fni = fn.Fn(body_token_or_form, local_env, eval_function, fn_name, parameters_form, spec_list)
        fn_handle = lambda args: fni.handle(tuple(args))  # <- sadly, we can not call fni.handle() in direct way

        fn_handle.meta = {
            'name': fn_name, 'docstring': docstring_token.dt().reference() if docstring_token else '',
            'kind': 'function', 'forms': fni.generate_meta__forms()
        }

        module_env.set(fn_name, datatypes.Function({'function_name': fn_name, 'function_reference': fn_handle}))

        return Token(Token.Identifier, fn_name)  # <- as it would be expected, defn return globally defined func name

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1]],
           'name': 'require',
           'forms': ['(require \'module-name)'],
           'docstring': 'Allows to require a module in current dir or in \'NANAMILANG_PATH\''})
    def require_macro(tree: list, local_env: dict, module_env, eval_function) -> list or Token:
        """
        Builtin 'require' macro implementation

        :param tree: a form given to this macro
        :param local_env: local environment during expr eval
        :param module_env: module environment we are free to modify
        :param eval_function: reference to recursive eval function
        :return: modified or new source tree as it would be expected
        """

        module_name_token_or_form = tree[0]

        evaluated = eval_function(local_env, module_name_token_or_form)
        if isinstance(evaluated, datatypes.NException):
            return Token(Token.Proxy, evaluated)  # <--------------------------- propagate possibly created NException

        assert isinstance(evaluated, datatypes.Symbol),                       'require: module name needs to be Symbol'

        loader.Loader.load(evaluated.reference(), module_env)  # <---------------------- load requested module by name

        return Token(Token.Nil, 'nil')  # <- a module could be 'imported' or not, we gonna return Nil type in any case

    ##################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2]],
           'name': 'for',
           'forms': ['(for [identifier coll] body-token-or-form)'],
           'docstring': 'Iterates through an evaluated Vector collection'})
    def for_macro(tree: list, local_env: dict, _, eval_function) -> list or Token:
        """
        Builtin 'for' macro implementation

        :param tree: a form given to this macro
        :param local_env: local environment during expr eval
        :param _: unused argument, but I need to mention it here
        :param eval_function: reference to recursive eval function
        :return: modified or new source tree as it would be expected
        """

        identifier_coll_vector_form, body_token_or_form = tree

        NML_M_ASSERT_FORM_IS_A_VECTOR(identifier_coll_vector_form,        'for: first argument needs to be a Vector')

        NML_M_ASSERT_COLL_FORM_ITEMS_COUNT_IS(identifier_coll_vector_form, 2,
                                              'for: incorrect Vector form arity: expected exactly: identifier, coll')

        identifier_token, coll_token_or_form = tuple(NML_M_ITERATE_AS_PAIRS(identifier_coll_vector_form))

        assert identifier_token.type() == Token.Identifier,               'for: identifier needs to be an Identifier'

        evaluated = eval_function(local_env, coll_token_or_form)
        if isinstance(evaluated, datatypes.NException):
            return Token(Token.Proxy, evaluated)  # ---------------- propagate a possibly created NException instance

        assert isinstance(evaluated, datatypes.Vector),                              'for: coll needs to be a Vector'

        _ = []

        for an_item in evaluated.items():
            local_env[identifier_token.dt().origin()] = an_item
            _evaluated = eval_function(local_env, body_token_or_form)
            if isinstance(_evaluated, datatypes.NException):
                return Token(Token.Proxy, _evaluated)  # <------------ propagate possibly created NException instance
            _.append(_evaluated)

        _resulting_vector_data_type = datatypes.Vector(tuple(_))

        return Token(Token.Proxy, _resulting_vector_data_type)  # <- for-cycle will return resulted vector collection

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityVariants, [1, 2]]],
           'name': 'let',
           'forms': ['(let [b1 v1 ...])',
                     '(let [b1 v1 ...] body-token-or-form)'],
           'docstring': 'Allows to define local bindings and access them later'})
    def let_macro(tree: list, local_env: dict, _, eval_function) -> list or Token:
        """
        Builtin 'let' macro implementation

        :param tree: a form given to this macro
        :param local_env: local environment during expr eval
        :param _: unused argument, but I need to mention it here
        :param eval_function: reference to recursive eval function
        :return: modified or new source tree as it would be expected
        """

        if len(tree) == 1:
            bindings_form, body_token_or_form = tree + [Token(Token.Nil, 'nil')]
        else:
            bindings_form, body_token_or_form = tree

        NML_M_ASSERT_FORM_IS_A_VECTOR(bindings_form,                      'let: bindings form needs to be a Vector')
        NML_M_ASSERT_COLL_FORM_ITEMS_COUNT_IS_EVEN(bindings_form,             'let: bindings form needs to be even')

        for [idn_token_or_form, dtype_token_or_form] in NML_M_ITERATE_AS_PAIRS(bindings_form, 2):
            evaluated = eval_function(local_env, dtype_token_or_form)
            if isinstance(evaluated, datatypes.NException):
                return Token(Token.Proxy, evaluated)  # <------------ propagate possibly created NException instance
            local_env.update(Destructuring(idn_token_or_form).destruct(evaluated))  # <-- populate local environment

        return body_token_or_form  # <- we just return body or token form there as is, without any modifications made

    #################################################################################################################


class BuiltinFunctions:
    """NanamiLang Builtin Functions"""

    #################################################################################################################

    @staticmethod
    def install(fn_meta: dict, fn_callback) -> bool:
        """
        Allows others installing their own functions.
        For example: let the REPL install (exit) function

        :param fn_meta: required function meta information
        :param fn_callback: installed function callback reference
        :return: whether function has been successfully installed
        """

        fn_meta.update({'kind': 'function'})
        reference_key = f'{fn_meta.get("name")}_func'
        maybe_existing = getattr(BuiltinFunctions, reference_key, None)
        if maybe_existing:
            delattr(BuiltinFunctions, reference_key)

        setattr(BuiltinFunctions, reference_key, fn_callback)
        getattr(BuiltinFunctions, reference_key, None).meta = fn_meta
        return bool(getattr(BuiltinFunctions, reference_key, None).meta == fn_meta)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1]],
           'name': 'identity',
           'forms': ['(identity something)'],
           'docstring': 'Returns something as it is'})
    def identity_func(args: List[datatypes.Base]) -> datatypes.Base:
        """
        Builtin 'identity' function implementation

        :param args: incoming 'identity' function arguments (only 1)
        :return: datatypes.Base

        """

        return args[0]
        # 'identity' function is required for internal purposes (for example, AST requires it). Can be used elsewhere

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.ArgumentsTypeChainVariants, [[datatypes.Collection,
                                                        datatypes.Base]]]],
           'name': 'contains?',
           'forms': ['(contains? collection element)'],
           'docstring': 'Checks whether collection contains element or not'})
    def contains_func(args: List[datatypes.Base]) -> datatypes.Boolean:
        """
        Builtin 'contains?' function implementation

        :param args: incoming 'contains?' function arguments (coll, element).
        :return: datatypes.Boolean
        """

        collection: datatypes.Collection
        element: datatypes.Base

        collection, element = args

        return collection.contains(element)
        # Since Collections use Boolean to represent Python 3 boolean, there is no need to explicitly cast the result

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1],
                    [Spec.EachArgumentTypeIs, datatypes.Function]],
           'name': 'wrapped',
           'forms': ['(wrapped function)'],
           'docstring': 'Returns wrapped Function'})
    def wrapped_func(args: List[datatypes.Function]) -> datatypes.Py3Object:
        """
        Builtin 'wrapped' function implementation

        :param args: incoming 'wrapped' function arguments (a Function Type)
        :return: datatypes.Py3Object

        """

        function: datatypes.Function = args[0]

        def nml(_arg) -> datatypes.Base:

            if isinstance(_arg, bool):   # <--------------------------------------------------- ------------- Boolean
                return datatypes.Boolean(_arg)
            if isinstance(_arg, int):    # <----------------------------------------------------------- IntegerNumber
                return datatypes.IntegerNumber(_arg)
            if isinstance(_arg, str):    # <------------------------------------------------------- String (from str)
                return datatypes.String(_arg)
            if isinstance(_arg, bytes):  # <----------------------------------------------------- String (from bytes)
                return datatypes.String(_arg.decode('utf-8'))
            return datatypes.Nil('nil')  # <--------------------------------------------------------- Nil (otherwise)

        return datatypes.Py3Object(lambda *_args, **kwargs: function.reference()(tuple(map(nml, _args))).reference())

        # This function will return specially formed Py3Object to call a NanamiLang function handler inside a Python3

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityVariants, [2, 3]],
                    [Spec.ArgumentsTypeChainVariants, [[datatypes.HashSet, datatypes.Base],
                                                       [datatypes.HashSet, datatypes.Base, datatypes.Base],
                                                       [datatypes.Vector, datatypes.IntegerNumber],
                                                       [datatypes.Vector, datatypes.IntegerNumber, datatypes.Base],
                                                       [datatypes.HashMap, datatypes.Base],
                                                       [datatypes.HashMap, datatypes.Base, datatypes.Base],
                                                       [datatypes.Py3Inst, datatypes.Keyword],
                                                       [datatypes.Py3Inst, datatypes.Keyword, datatypes.Base],
                                                       [datatypes.Py3Object, datatypes.Keyword],
                                                       [datatypes.Py3Object, datatypes.Keyword, datatypes.Base]]]],
           'name': 'get',
           'forms': ['(get collection-or-interop-data-type by)',
                     '(get collection-or-interop-data-type by by-default)'],
           'docstring': 'Returns collection element (by key, index, or element), Py3Object or Py3Inst'})
    def get_func(args: List[datatypes.Base]) -> datatypes.Base:
        """
        Builtin 'get' function implementation

        :param args: incoming 'get' function arguments (collection/interop datatype, key, index, element).
        :return: datatypes.Base
        """

        collection_or_interop_data_type: datatypes.Collection or datatypes.Py3Object or datatypes.Py3Inst
        by: datatypes.Base
        by_default: datatypes.Base

        collection_or_interop_data_type, by, by_default = args if len(args) == 3 else args + [datatypes.Nil('nil')]

        return collection_or_interop_data_type.get(by, default=by_default)
        # Function can take 2 or 3 arguments, optional third argument is a 'default' value, which is a Nil by default

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': 'str',
           'forms': ['(str e1 e2 ... eX)'],
           'docstring': 'Returns all the elements as a String'})
    def str_func(args: List[datatypes.Base]) -> datatypes.String:
        """
        Builtin 'str' function implementation

        :param args: incoming 'str' function arguments (elements).
        :return: datatypes.Vector
        """

        return datatypes.String(''.join([x.to_py_str() for x in args]))
        # Using each element to_py_str() method in order to build a str

    #################################################################################################################

    @staticmethod
    @meta({'spec': None,
           'name': 'make-vector',
           'forms': ['(make-vector e1 e2 ... eX)'],
           'docstring': 'Creates a Vector data structure'})
    def make_vector_func(args: List[datatypes.Base]) -> datatypes.Vector:
        """
        Builtin 'make-vector' function implementation

        :param args: incoming 'make-vector' function arguments (elements).
        :return: datatypes.Vector
        """

        return datatypes.Vector(tuple(args))
        # Let the Collection.__init__() handle Vector structure construction

    #################################################################################################################

    @staticmethod
    @meta({'spec': None,
           'name': 'make-hashset',
           'forms': ['(make-hashset e1 e2 ... eX)'],
           'docstring': 'Creates a HashSet data structure'})
    def make_set_func(args: List[datatypes.Base]) -> datatypes.HashSet:
        """
        Builtin 'make-hashset' function implementation

        :param args: incoming 'make-hashset' function arguments (elements).
        :return: datatypes.HashSet
        """

        return datatypes.HashSet(tuple(args))
        # Let the Collection.__init__() handle HashSet structure construction

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityEven]],
           'name': 'make-hashmap',
           'forms': ['(make-hashmap k1 v2 ... kX vX)'],
           'docstring': 'Creates a HashMap data structure'})
    def make_hashmap_func(args: List[datatypes.Base]) -> datatypes.HashMap:
        """
        Builtin 'make-hashmap' function implementation

        :param args: incoming 'make-hashmap' function arguments (elements).
        :return: datatypes.HashMap
        """

        return datatypes.HashMap(tuple(args))
        # Let the Collection.__init__() handle HashMap structure construction

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1],
                    [Spec.EachArgumentTypeIs, datatypes.HashMap]],
           'name': 'import',
           'forms': ['(import {:name ... :refer [...]})'],
           'docstring': 'Returns Python 3 module wrapped as a Py3Object'})
    def py3_import_func(args: List[datatypes.HashMap]) -> datatypes.Py3Object or datatypes.Nil:
        """
        Builtin 'make-hashmap' function implementation

        :param args: incoming 'import' function arguments (a hashmap with name and refer keys).
        :return: datatypes.Py3Object
        """

        module_description: datatypes.HashMap = args[0]

        nil = datatypes.Nil('nil')

        module_name: datatypes.String or datatypes.Nil
        module_name = module_description.get(datatypes.Keyword('name'), nil)

        if isinstance(module_name, datatypes.Nil):
            return nil

        if not isinstance(module_name, datatypes.String):
            return nil

        module_name = module_name.reference()

        module_symbols: datatypes.Vector or datatypes.Nil
        module_symbols = module_description.get(datatypes.Keyword('refer'), nil)

        if isinstance(module_symbols, datatypes.Nil):
            return nil

        if not isinstance(module_symbols, datatypes.Vector):
            return nil

        module_symbols = [keyword.reference() for keyword in module_symbols.items()]

        return datatypes.Py3Object(__import__(module_name, fromlist=module_symbols, level=0))

        # Returns an imported Python 3 module wrapped using Nanamilang Py3Object data type or Nil

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1]],
           'name': 'not',
           'forms': ['(not something)'],
           'docstring': 'Returns something truth inverted'})
    def not_func(args: List[datatypes.Base]) -> datatypes.Boolean:
        """
        Builtin 'not' function implementation

        :param args: incoming 'not' function arguments
        :return: datatypes.String
        """

        return datatypes.Boolean(not args[0].truthy())
        # All NanamiLang Data Types require their truthy() retval to be explicitly cast into NanamiLang Boolean type.

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': '=',
           'forms': ['(= s1 s2 ... sX)'],
           'docstring': 'Returns false once current does not equal next'})
    def eq_func(args: List[datatypes.Base]) -> datatypes.Boolean:
        """
        Builtin '=' function implementation

        :param args: incoming '=' function arguments (any known data types)
        :return: datatypes.Boolean
        """

        _ne = False
        for idx, curr in enumerate(args):
            _next = get(args, idx + 1, None)
            if not _next:
                break
            _ne = curr.hashed() == _next.hashed()
            if not _ne:
                break

        return datatypes.Boolean(_ne)  # once '_ne == False', exit the function, cause there is no sense to continue.

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '>',
           'forms': ['(> n1 n2 ... nX)'],
           'docstring': 'Returns false once current less than next'})
    def greater_than_func(args: List[datatypes.Numeric]) -> datatypes.Boolean:
        """
        Builtin '>' function implementation

        :param args: incoming '>' function arguments (only numeric values allowed)
        :return: datatypes.Boolean
        """

        _gt = False
        for idx, curr in enumerate(args):
            _next = get(args, idx + 1, None)
            if not _next:
                break
            _gt = curr.reference() > _next.reference()
            if not _gt:
                break

        return datatypes.Boolean(_gt)  # once '_gt == False', exit the function, cause there is no sense to continue.

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '<',
           'forms': ['(< n1 n2 ... nX)'],
           'docstring': 'Returns false once current greater than next'})
    def less_than_func(args: List[datatypes.Numeric]) -> datatypes.Boolean:
        """
        Builtin '<' function implementation

        :param args: incoming '<' function arguments (only numeric values allowed)
        :return: datatypes.Boolean
        """

        _lt = False
        for idx, curr in enumerate(args):
            _next = get(args, idx + 1, None)
            if not _next:
                break
            _lt = curr.reference() < _next.reference()
            if not _lt:
                break

        return datatypes.Boolean(_lt)  # once '_lt == False', exit the function, cause there is no sense to continue.

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '>=',
           'forms': ['(>= n1 n2 ... nX)'],
           'docstring': 'Returns false once current less-than-equals next'})
    def greater_than_eq_func(args: List[datatypes.Numeric]) -> datatypes.Boolean:
        """
        Builtin '>=' function implementation

        :param args: incoming '>=' function arguments (only numeric data types allowed)
        :return: datatypes.Boolean
        """

        _gte = False
        for idx, curr in enumerate(args):
            _next = get(args, idx + 1, None)
            if not _next:
                break
            _gte = curr.reference() >= _next.reference()
            if not _gte:
                break

        return datatypes.Boolean(_gte)  # once '_gte == False', exit the function since there is no sense to continue

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '<=',
           'forms': ['(<= n1 n2 ... nX)'],
           'docstring': 'Returns false once current greater-than-equals next'})
    def less_than_eq_func(args: List[datatypes.Numeric]) -> datatypes.Boolean:
        """
        Builtin '<=' function implementation

        :param args: incoming '>=' function arguments (numeric data types only allowed)
        :return: datatypes.Boolean
        """

        _lte = False
        for idx, curr in enumerate(args):
            _next = get(args, idx + 1, None)
            if not _next:
                break
            _lte = curr.reference() <= _next.reference()
            if not _lte:
                break

        return datatypes.Boolean(_lte)  # once '_lte == False', exit the function cause there is no sense to continue

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '+',
           'forms': ['(+ n1 n2 ... nX)'],
           'docstring': 'Applies "+" operation to passed numbers'})
    def add_func(args: List[datatypes.Numeric]) -> datatypes.Numeric:
        """
        Builtin '+' function implementation

        :param args: incoming '+' function arguments (only numeric here)
        :return: either datatypes.IntegerNumber or datatypes.FloatNumber
        """

        result = reduce(lambda _, x: _ + x, map(lambda n: n.reference(), args))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '-',
           'forms': ['(- n1 n2 ... nX)'],
           'docstring': 'Applies "-" operation to passed numbers'})
    def sub_func(args: List[datatypes.Numeric]) -> datatypes.Numeric:
        """
        Builtin '-' function implementation

        :param args: incoming '-' function arguments (only numeric here)
        :return: either datatypes.IntegerNumber or datatypes.FloatNumber
        """

        result = reduce(lambda _, x: _ - x, map(lambda n: n.reference(), args))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '*',
           'forms': ['(* n1 n2 ... nX)'],
           'docstring': 'Applies "*" operation to passed numbers'})
    def mul_func(args: List[datatypes.Numeric]) -> datatypes.Numeric:
        """
        Builtin '*' function implementation

        :param args: incoming '*' function arguments (only numeric here)
        :return: either datatypes.IntegerNumber or datatypes.FloatNumber
        """

        result = reduce(lambda _, x: _ * x, map(lambda n: n.reference(), args))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': '/',
           'forms': ['(/ n1 n2 ... nX)'],
           'docstring': 'Applies "/" operation to passed numbers'})
    def divide_func(args: List[datatypes.Numeric]) -> datatypes.Numeric:
        """
        Builtin '/' function implementation

        :param args: incoming '/' function arguments (only numeric here)
        :return: either datatypes.IntegerNumber or datatypes.FloatNumber
        """

        result = reduce(lambda _, x: _ / x, map(lambda n: n.reference(), args))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeIs, datatypes.Numeric]],
           'name': 'mod',
           'forms': ['(mod n1 n2 ... nX)'],
           'docstring': 'Applies "mod" operation to passed numbers'})
    def modulo_func(args: List[datatypes.Numeric]) -> datatypes.Numeric:
        """
        Builtin 'mod' function implementation

        :param args: incoming 'mod' function arguments (only numeric here)
        :return: either datatypes.IntegerNumber or a datatypes.FloatNumber
        """

        result = reduce(lambda _, x: _ % x, map(lambda n: n.reference(), args))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.ArgumentsTypeChainVariants, [[datatypes.Function, datatypes.Collection],
                                                       [datatypes.Keyword, datatypes.Collection]]]],
           'name': 'map',
           'forms': ['(map function collection)'],
           'docstring': 'Allows to map collection elements with the passed (anonymous) function or Keyword-Fn'})
    def map_func(args: List[datatypes.Base]) -> datatypes.Vector or datatypes.NException:
        """
        Builtin 'map' function implementation

        :param args: incoming 'map' function arguments   (collection and maybe anonymous function or keyword-fn)
        :return: datatypes.Vector
        """

        function: datatypes.Function or datatypes.Keyword
        collection: datatypes.Collection

        function, collection = args

        if isinstance(function, datatypes.Keyword):
            k = function
            function = datatypes.Function(
                {'function_name': randstr(),
                 'function_reference': lambda _a_: BuiltinFunctions.get_func(_a_ + [k])})

        _ = []
        for element in collection.items():
            res = function.reference()([element])
            if isinstance(res, datatypes.NException):
                return res  # <------------------------------ if we ran into NException, we need to propagate it
            _.append(res)

        return datatypes.Vector(tuple(_))  # <------ return a resulting vector of the mapped collection elements

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.ArgumentsTypeChainVariants, [[datatypes.Function, datatypes.Collection],
                                                       [datatypes.Keyword, datatypes.Collection]]]],
           'name': 'filter',
           'forms': ['(filter function collection)'],
           'docstring': 'Allows to filter collection elements with the passed (anonymous) function or Keyword-Fn'})
    def filter_func(args: List[datatypes.Base]) -> datatypes.Vector or datatypes.NException:
        """
        Builtin 'filter' function implementation

        :param args: incoming 'filter' function arguments (collection and maybe anonymous function or a keyword-fn)
        :return: datatypes.Vector
        """

        function: datatypes.Function or datatypes.Keyword
        collection: datatypes.Collection

        function, collection = args

        if isinstance(function, datatypes.Keyword):
            k = function
            function = datatypes.Function(
                {'function_name': randstr(),
                 'function_reference': lambda _a_: BuiltinFunctions.get_func(_a_ + [k])})

        _ = []
        for element in collection.items():
            res = function.reference()([element])
            if isinstance(res, datatypes.NException):
                return res  # <--------------------------------- if we ran into NException, we need to propagate it
            if res.truthy():
                _.append(element)

        return datatypes.Vector(tuple(_))  # <------- return a resulting vector of the filtered collection elements

        #############################################################################################################
