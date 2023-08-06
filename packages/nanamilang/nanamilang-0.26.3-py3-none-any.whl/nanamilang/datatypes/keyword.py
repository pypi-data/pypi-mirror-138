"""NanamiLang Keyword Data Type Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from .base import Base
from .string import String
from ._exports import export


class Keyword(Base):
    """NanamiLang Keyword Data Type"""

    name: str = 'Keyword'
    _expected_type = str
    _python_reference: str
    purpose = 'Encapsulate Python 3 str'

    @export()
    def nominal(self) -> String:
        """NanamiLang Keyword nominal() method implementation"""

        return String(self.name)

    def format(self, **_) -> str:
        """NanamiLang Keyword, format() method implementation"""

        return f':{self._python_reference}'

    def to_py_str(self) -> str:
        """NanamiLang Keyword, to_py_str() method implementation"""

        return self.format()

    def _additional_assertions_on_init(self, reference) -> None:
        """NanamiLang Keyword, _additional_assertions_on_init() method implementation"""

        self._init_assert_ref_could_not_be_empty(reference)
        # Since Keyword encapsulates a Python 3 str, ensure that the string is not empty
