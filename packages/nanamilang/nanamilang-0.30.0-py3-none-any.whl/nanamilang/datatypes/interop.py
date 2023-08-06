"""NanamiLang Python 3 Interop Classes"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from .nil import Nil
from .base import Base
from .string import String
from .vector import Vector
from .symbol import Symbol
from .boolean import Boolean
from .keyword import Keyword
from ._exports import export
from nanamilang import shortcuts
from .floatnumber import FloatNumber
from .integernumber import IntegerNumber


class Py3Inst(Base):
    """NanamiLang data type which wraps Python 3 inst"""

    name = 'Py3Inst'
    _expected_type = object
    _object_name: str = None
    _python_reference = object
    purpose = 'Allows you to encapsulate a Python3 inst'

    def __init__(self, reference) -> None:
        """Initialize new NanamiLang Py3Inst instance"""

        self._object_name = reference.__class__.__name__

        super().__init__(reference)

    def _set_hash(self, reference) -> None:
        """NanamiLang Py3Inst, override '_set_hash()'"""

        self._hashed = String(reference.__str__()).hashed()

    def get(self,
            symbol: Keyword, default=None
            ) -> ('Py3Inst' or 'Py3Object' or Nil):
        """NanamiLang Py3Inst, returns Py3Inst or Py3Object"""

        if not default:
            default = Nil('nil')

        shortcuts.ASSERT_IS_CHILD_OF(
            symbol,
            Keyword,
            message='Py3Inst.get: symbol name is not a Keyword'
        )

        name = shortcuts.demangle(symbol.reference())

        attribute = getattr(self.reference(), name, None)

        # For now, we implicitly dispatch Py3Inst & Py3Object
        # depending on existence of the '__call__()' attribute

        return (Py3Object(attribute)
                if hasattr(attribute, '__call__')
                else Py3Inst(attribute)) if attribute else default

    @export()
    def nominal(self) -> String:
        """NanamiLang Py3Inst, 'nominal()' method implementation"""

        return String(self.name)

    def format(self, **_) -> str:
        """NanamiLang Py3Inst, 'format()' method implementation"""

        return f'<{self._object_name}>'

    def to_py_str(self) -> str:
        """NanamiLang Py3Inst, 'to_py_str()' method implementation"""

        return self.format()

    @export()
    def cast(self, to: Keyword) -> Base:
        """NanamiLang Py3Inst, cast Py3Inst tp NanamiLang data type"""

        # As for now, we only support simple data types to cast into

        shortcuts.ASSERT_IS_CHILD_OF(
            to,
            Keyword,
            message='Py3Inst.cast: type name to cast to is not a Keyword'
        )

        conv = lambda: self.reference().decode('utf-8') \
            if isinstance(self.reference(), bytes) else str(self.reference())

        if to.reference() == 'to-string':
            return String(conv())
        if to.reference() == 'to-symbol':
            return Symbol(conv())
        if to.reference() == 'to-keyword':
            return Keyword(conv())
        if to.reference() == 'to-boolean':
            return Boolean(bool(self.reference()))
        if to.reference() == 'to-float-number':
            return FloatNumber(float(self.reference()))
        if to.reference() == 'to-integer-number':
            return IntegerNumber(int(self.reference()))
        if (to.reference() == 'to-nanamilang' and
                issubclass(self.reference().__class__, (Base,))):
            return self.reference()  # <- check whether is Base Data Type

        raise AssertionError('Py3Inst.cast: could not cast self.reference()')


class Py3Object(Base):
    """NanamiLang data type which wraps Python 3 object"""

    name = 'Py3Object'
    _expected_type = object
    _object_name: str = None
    _python_reference = object
    purpose = 'Allows you to encapsulate a Python3 object'

    def __init__(self, reference) -> None:
        """Initialize new NanamiLang Py3Object instance"""

        self._object_name = reference.__name__

        super().__init__(reference)

    def _set_hash(self, reference) -> None:
        """NanamiLang Py3Object, override '_set_hash()'"""

        self._hashed = String(reference.__name__).hashed()

    def get(self,
            symbol: Keyword, default=None
            ) -> ('Py3Inst' or 'Py3Object' or Nil):
        """NanamiLang Py3Object, returns Py3Inst or Py3Object"""

        if not default:
            default = Nil('nil')

        shortcuts.ASSERT_IS_CHILD_OF(
            symbol,
            Keyword,
            message='Py3Object.get: symbol name is not a Keyword'
        )

        name = shortcuts.demangle(symbol.reference())

        attribute = getattr(self.reference(), name, None)

        # For now, we implicitly dispatch Py3Inst & Py3Object
        # depending on existence of the '__call__()' attribute

        return (Py3Object(attribute)
                if hasattr(attribute, '__call__')
                else Py3Inst(attribute)) if attribute else default

    @export()
    def nominal(self) -> String:
        """NanamiLang Py3Object, 'nominal()' method implementation"""

        return String(self.name)

    def format(self, **_) -> str:
        """NanamiLang Py3Object, 'format()' method implementation"""

        return f'<{self._object_name}>'

    def to_py_str(self) -> str:
        """NanamiLang Py3Object, 'to_py_str()' method implementation"""

        return self.format()

    @export()
    def instantiate(self, args: Vector) -> Py3Inst:
        """NanamiLang Py3Object, 'instantiate()' method implementation"""

        shortcuts.ASSERT_IS_CHILD_OF(
            args,
            Vector,
            message='Py3Object.instantiate: instantiate args argument is not a Vector'
        )

        return Py3Inst(self.reference()(*[item.reference() for item in args.items()]))
