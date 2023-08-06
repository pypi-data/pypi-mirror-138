"""NanamiLang Callable Data Type Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from .base import Base
from .string import String
from .vector import Vector
from .hashmap import HashMap
from ._exports import export


class Callable(Base):
    """NanamiLang Callable Data Type Class"""

    name = 'Callable'
    _expected_type = dict
    _python_reference: dict

    @export()
    def meta(self) -> HashMap:
        """NanamiLang Callable, meta() method implementation"""

        _meta_ = self.reference().meta
        _forms_ = tuple(String(_) for _ in _meta_.get('forms'))

        return HashMap(
            (String('forms'), Vector(_forms_),
             String('kind'), String(_meta_.get('kind')),
             String('name'), String(_meta_.get('name')),
             String('docstring'), String(_meta_.get('docstring'))))

    def origin(self) -> str:
        """NanamiLang Callable, origin() method implementation"""

        return self.format()

    def truthy(self) -> bool:
        """NanamiLang Callable, truthy() method implementation"""

        return True

    @export()
    def nominal(self) -> String:
        """NanamiLang Callable, nominal() method implementation"""

        return String(self.name)

    def to_py_str(self) -> str:
        """NanamiLang Callable, to_py_str() method implementation"""

        return self.format()

    # We redefine truthy() method to always return True for Callable
