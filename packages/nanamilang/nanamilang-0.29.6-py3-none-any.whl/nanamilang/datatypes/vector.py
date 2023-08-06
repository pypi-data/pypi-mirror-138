"""NanamiLang Vector Data Type Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from nanamilang import shortcuts
from ._exports import export
from .base import Base
from .string import String
from .collection import Collection
from .integernumber import IntegerNumber


class Vector(Collection):
    """NanamiLang Vector Data Type Class"""

    name: str = 'Vector'
    _expected_type = tuple
    _default = tuple()
    _python_reference: tuple
    purpose = 'Implements Vector of NanamiLang Base data types'

    @export()
    def last(self) -> Base:
        """NanamiLang Vector, return a last vector element"""

        return self.get(IntegerNumber(-1))  # <- Python3 trick

    @export()
    def first(self) -> Base:
        """NanamiLang Vector, return a first vector element"""

        return self.get(IntegerNumber(0))

    @export()
    def second(self) -> Base:
        """NanamiLang Vector, return a second vector element"""

        return self.get(IntegerNumber(1))

    @export()
    def range(self,
              _from_: IntegerNumber,
              _to_:   IntegerNumber) -> Base:
        """
        NanamiLang Vector, range() implementation
        Takes _from_, _to_ and returns a new Vector
        """

        return self.__class__(tuple(map(IntegerNumber,
                                        range(_from_.reference(),
                                              _to_.reference()))))

    def get(self, by: IntegerNumber, default: Base = None) -> Base:
        """NanamiLang Vector, get() implementation"""

        if not default:
            default = self._nil

        shortcuts.ASSERT_IS_CHILD_OF(
            by,
            IntegerNumber,
            message='Vector.get: an index must be an IntegerNumber'
        )

        return shortcuts.get(self.reference(), by.reference(), default)

    def to_py_str(self) -> str:
        """NanamiLang Vector, to_py_str() method implementation"""

        return '[' + ' '.join([f'\\"{i.to_py_str()}\\"'
                               if isinstance(i, String)
                               else i.to_py_str() for i in self.items()]) + ']'

    def format(self, **_) -> str:
        """NanamiLang Vector, format() method re-implementation"""

        # There is no sense to iterate over self.items() when we can return '[]'
        if self._collection_contains_nothing.truthy():
            return '[]'
        return '[' + f'{", ".join((i.format() for i in self.reference()))}' + ']'
