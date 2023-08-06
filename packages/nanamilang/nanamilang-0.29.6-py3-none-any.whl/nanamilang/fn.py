"""NanamiLang Fn Handler Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from copy import copy

from nanamilang import destruct
from nanamilang import datatypes
from nanamilang.spec import Spec
from nanamilang.token import Token


class Fn:
    """NanamiLang Fn Handler Class"""

    _function_body_token_or_form: list
    _environment: dict = None
    _recursive_evaluate_function = None
    _function_name: str = None
    _function_parameters_form: list = None
    _number_of_function_params: int = None
    _nanamilang_function_spec: list = None

    def __init__(self,
                 function_body_token_or_form: list,
                 environment: dict,
                 recursive_evaluate_function,
                 function_name: str,
                 function_parameters_form: list,
                 nanamilang_function_spec: list = None) -> None:
        """NanamiLang Fn Handler, initialize a new Fn instance"""

        self._function_body_token_or_form = function_body_token_or_form
        self._environment = copy(environment)  # <- 'closure' capturing
        self._recursive_evaluate_function = recursive_evaluate_function
        self._function_name = function_name
        self._function_parameters_form = function_parameters_form[1:]
        self._number_of_function_params = len(self._function_parameters_form)
        self._nanamilang_function_spec = nanamilang_function_spec or []  # <- will be extended
        self._nanamilang_function_spec.append([Spec.ArityIs, self._number_of_function_params])

    def env(self) -> dict:
        """NanamiLang Fn Handler, self._environment private getter"""

        return self._environment

    def generate_meta__forms(self) -> list:
        """NanamiLang Fn Handler, generate function meta data :: forms"""

        parameter_names = []
        for parameter_token_or_form in self._function_parameters_form:
            if isinstance(parameter_token_or_form, Token):
                parameter_names.append(parameter_token_or_form.dt().origin())
            if isinstance(parameter_token_or_form, list):
                parameter_names.append('[vector or hashmap]')
        return [f'({self._function_name} {parameter_names})']

    def handle(self, args: tuple) -> datatypes.Base:
        """NanamiLang Fn Handler, handle function evaluation using local closure and merged specs"""

        Spec.validate(self._function_name, args, self._nanamilang_function_spec)

        current_eval_env = copy(self._environment)  # <- prevent function 'closure' mutation

        for parameter_token_or_form, fn_arg in zip(self._function_parameters_form, args):
            current_eval_env.update(destruct.Destructuring(parameter_token_or_form).destruct(fn_arg))

        return self._recursive_evaluate_function(current_eval_env, self._function_body_token_or_form)
