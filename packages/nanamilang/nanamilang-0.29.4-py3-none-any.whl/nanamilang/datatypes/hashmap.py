"""NanamiLang HashMap Data Type Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from typing import Generator
from nanamilang import shortcuts

from .base import Base
from .string import String
from .vector import Vector
from ._imdict import ImDict
from .boolean import Boolean
from .collection import Collection


class HashMap(Collection):
    """NanamiLang HashMap Data Type Class"""

    name: str = 'HashMap'
    _expected_type = dict
    _default = {}
    _python_reference: dict
    purpose = 'Implement HashMap of NanamiLang Base data types'

    def _init__assertions_on_non_empty_reference(self,
                                                 reference) -> None:
        """NanamiLang HashMap, assert: raw reference coll is even"""

        self._init_assert_only_base(reference)
        self._init_assert_ref_length_must_be_even(reference)
        # make-hashmap already takes care, but we must ensure anyway

    def _init__chance_to_process_and_override(self, reference) -> dict:
        """NanamiLang HashMap, process and override HashSet reference"""

        # Here we can complete HashMap structure initialization procedure

        partitioned = shortcuts.plain2partitioned(reference)
        return ImDict({key.hashed(): (key, val) for key, val in partitioned})

    def get(self, by: Base, default: Base = None) -> Base:
        """NanamiLang HashMap, get() implementation"""

        if not default:
            default = self._nil

        shortcuts.ASSERT_IS_CHILD_OF(
            by,
            Base,
            message='HashMap.get: by is not Base derived'
        )

        return shortcuts.get(self.reference().get(by.hashed(), ()), 1, default)

    def items(self) -> Generator:
        """NanamiLang HashMap, items() method implementation"""

        return (Vector(elem) for elem in self.reference().values())

    def contains(self, element) -> Boolean:
        """NanamiLang HashMap, contains? method implementation"""

        return Boolean(element.hashed() in self.reference().keys())

    def to_py_str(self) -> str:
        """NanamiLang HashMap, to_py_str() method implementation"""

        return '{' + ' '.join([(f'\\"{k.to_py_str()}\\"'
                                if isinstance(k, String)
                                else k.to_py_str()) +
                               ' ' +
                               (f'\\"{v.to_py_str()}\\"'
                                if isinstance(v, String)
                                else v.to_py_str()) for k, v in self.reference().values()]) + '}'

    def format(self, **_) -> str:
        """NanamiLang HashMap, format() method implementation"""

        # There is no sense to iterate over self.items() when we just can return  a '{}'
        if self._collection_contains_nothing.truthy():
            return '{}'
        return '{' + f'{", ".join([f"{k.format()} {v.format()}" for k, v in self.reference().values()])}' + '}'
