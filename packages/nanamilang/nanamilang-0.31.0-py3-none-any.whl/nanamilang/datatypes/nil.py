"""NanamiLang Nil Data Type Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from .base import Base
from .string import String
from ._exports import export


class Nil(Base):
    """NanamiLang Nil Type"""

    _hashed = hash('nil')
    name: str = 'Nil'
    _expected_type = str
    _python_reference: str
    purpose = 'To mark as a nil'

    def format(self, **_) -> str:
        """NanamiLang Nil, format() method implementation"""

        return 'nil'

    def origin(self) -> str:
        """NanamiLang Nil, origin() method implementation"""

        return self._python_reference

    @export()
    def nominal(self) -> String:
        """NanamiLang Nil, nominal() method implementation"""

        return String(self.name)

    def reference(self) -> None:
        """NanamiLang Nil, reference() method implementation"""

        return None

    def to_py_str(self) -> str:
        """NanamiLang Nil, to_py_str() method implementation"""

        return ''

    # We redefine self.reference() method to return Python 3 NoneType
