"""NanamiLang Collection Data Type Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from functools import reduce
from typing import Generator

from ._exports import export

from .nil import Nil
from .base import Base
from .string import String
from .boolean import Boolean
from .integernumber import IntegerNumber


class Collection(Base):
    """NanamiLang Collection Type Base Class"""

    name = 'Collection'
    _nil = Nil('nil')
    _hashed = _nil.hashed()
    _default = None
    _nil__hashed_val = _hashed
    _length: IntegerNumber = IntegerNumber(0)
    _collection_contains_nothing: Boolean = Boolean(True)

    def get(self, by: Base, default: Base) -> Base:
        """
        NanamiLang Collection Type Base Class
        virtual get() method
        """

        raise NotImplementedError  # <- it means: 'virtual method'

    def to_py_str(self) -> str:
        """NanamiLang Collection virtual to_py_str() implementation"""

        raise NotImplementedError

    @export()
    def empty(self) -> Boolean:
        """
        NanamiLang Collection Type Base Class
        empty() method implementation
        """

        return self._collection_contains_nothing

    @export()
    def nominal(self) -> String:
        """NanamiLang Collection, nominal() method implementation"""

        return String(self.name)

    @staticmethod
    def _init__chance_to_process_and_override(reference):
        """
        NanamiLang Collection Type Base Class
        Give it a chance to process, override a raw passed reference
        """

        return reference

    def _init__assertions_on_non_empty_reference(self,
                                                 reference) -> None:
        """
        NanamiLang Collection Type Base Class
        Allows to define assertions to run on passed *raw* reference
        """

        self._init_assert_only_base(reference)

    @staticmethod
    def _init__count_length(ref: tuple) -> int:
        """NanamiLang Collection Type Base Class, return ref count"""

        return len(ref)

    @export()
    def count(self) -> IntegerNumber:
        """NanamiLang Collection Type Base Class, get self._length"""

        return self._length

    def items(self) -> Generator:
        """NanamiLang Collection Type Base Class, return a Generator"""

        # By default, we treat _python_reference as the plain structure
        return self._python_reference

    def _set_hash(self, reference) -> None:
        """NanamiLang Collection Type Base Class, disable _set_hash()"""

    def __init__(self, reference) -> None:
        """NanamiLang Collection Type Base Class, initialize new instance"""

        possibly_overridden = self._default
        if reference:
            self._init__assertions_on_non_empty_reference(reference)
            self._hashed = reduce(
                lambda e, n: e + n, map(lambda e: e.hashed(), reference)
            ) + hash(self.name)  # hackish, but it works anyway, maybe we can keep this
            possibly_overridden = self._init__chance_to_process_and_override(reference)
            self._length = IntegerNumber(self._init__count_length(possibly_overridden))
            self._collection_contains_nothing = Boolean(not bool(self._length.reference()))

        super().__init__(possibly_overridden)

        # Call Base.__init__ through super() to finish Base NanamiLang type initialization.

    @staticmethod
    def contains(_) -> Boolean:
        """NanamiLang Collection, contains? virtual method"""

        # If not redefined, returns False (i.e.: Vector __should not__ redefine this method)

        return Boolean(False)

    def truthy(self) -> bool:
        """NanamiLang Collection, truthy() method implementation"""

        return True
        # We redefine self.truthy() method to always return True even if collection is empty
