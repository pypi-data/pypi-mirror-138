"""NanamiLang HashSet Data Type Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from typing import ValuesView
from nanamilang import shortcuts

from .base import Base
from .string import String
from ._imdict import ImDict
from .boolean import Boolean
from .collection import Collection


class HashSet(Collection):
    """NanamiLang HashSet Data Type Class"""

    name: str = 'HashSet'
    _expected_type = dict
    _default = {}
    _python_reference: dict
    purpose = 'Implements HashSet of NanamiLang Base data types'

    def _init__chance_to_process_and_override(self, reference) -> dict:
        """NanamiLang HashSet, process and override HashMap reference"""

        # Here we can complete HashSet structure initialization procedure

        return ImDict({element.hashed(): element for element in reference})

    def get(self, by: Base, default: Base = None) -> Base:
        """NanamiLang HashSet, get() implementation"""

        if not default:
            default = self._nil

        shortcuts.ASSERT_IS_CHILD_OF(
            by,
            Base,
            message='HashSet.get: by is not Base derived'
        )

        return self.reference().get(by.hashed(), default)

    def items(self) -> ValuesView:
        """NanamiLang HashSet, items() method implementation"""

        return self.reference().values()

    def contains(self, element) -> Boolean:
        """NanamiLang HashSet, contains? method implementation"""

        return Boolean(element.hashed() in self.reference().keys())

    def to_py_str(self) -> str:
        """NanamiLang HashSet, to_py_str() method implementation"""

        return '#{' + ' '.join([f'\\"{i.to_py_str()}\\"'
                                if isinstance(i, String)
                                else i.to_py_str() for i in self.items()]) + '}'

    def format(self, **_) -> str:
        """NanamiLang HashSet, format() method implementation"""

        # There is no sense to iterate over self.items() when we just can return a '#{}'
        if self._collection_contains_nothing.truthy():
            return '#{}'
        return '#{' + f'{", ".join((v.format() for v in self.reference().values()))}' + '}'
