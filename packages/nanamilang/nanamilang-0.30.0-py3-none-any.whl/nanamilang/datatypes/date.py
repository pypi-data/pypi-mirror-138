"""NanamiLang Date Data Type Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

import datetime
from .base import Base
from .string import String
from ._exports import export


class Date(Base):
    """NanamiLang Date Data Type"""

    name: str = 'Date'
    _expected_type = datetime.datetime
    _python_reference: datetime.datetime
    purpose = 'Encapsulate Python 3 datetime.datetime class'

    @export()
    def nominal(self) -> String:
        """NanamiLang Date, nominal() method implementation"""

        return String(self.name)

    def to_py_str(self) -> str:
        """NanamiLang Date, to_py_str() method implementation"""

        return self.format()

    def format(self, **_) -> str:
        """NanamiLang Date, format() method re-implementation"""

        return f'#{self._python_reference.year}-{self._python_reference.month}-{self._python_reference.day}'
