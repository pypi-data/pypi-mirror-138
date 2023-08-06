"""NanamiLang String Data Type CLass"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from .base import Base
from ._exports import export


class String(Base):
    """NanamiLang String Data Type"""

    name: str = 'String'
    _expected_type = str
    _python_reference: str
    purpose = 'Encapsulate Python 3 str'

    def truthy(self) -> bool:
        """NanamiLang String, truthy() method implementation"""

        return True

    def format(self, **_) -> str:
        """NanamiLang String, format() method implementation"""

        return f'"{self.reference()}"'

    @export()
    def nominal(self) -> Base:
        """NanamiLang String, nominal() method implementation"""

        return String(self.name)

    def to_py_str(self) -> str:
        """NanamiLang String, to_py_str() method implementation"""

        return self.reference()

    # We redefine 'self.truthy()' to validate empty strings as well
