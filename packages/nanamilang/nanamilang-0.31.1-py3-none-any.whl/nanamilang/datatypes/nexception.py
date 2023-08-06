"""NanamiLang NException Data Type Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from typing import Tuple, List

from .base import Base
from .string import String
from .hashmap import HashMap
from .keyword import Keyword
from ._exports import export

from nanamilang import shortcuts


class NException(Base):
    """NanamiLang NException Type"""

    _cs: list = None  # <- call stack
    _core_traceback: list = None
    _exception: Exception
    _expected_type = HashMap
    name: str = 'NException'
    _position: tuple = ('<unknown>', 1, 1)
    _python_reference: HashMap
    purpose = 'Encapsulate Python 3 Exception'

    def __init__(self, reference: Tuple[Exception,
                                        Tuple, List]) -> None:
        """Initialize a new NException instance"""

        shortcuts.ASSERT_COLL_LENGTH_EQUALS_TO(
            reference,
            3,
            message='NException: reference should be a triplet'
        )
        # To avoid trapping into ValueError, let's assert length

        self._exception, self._position, self._cs = reference
        # remember _what_ the error has been occurred and __where__

        self._cs.reverse()  # <- to read this later in reverse order

        self._position_message = ':'.join(map(str, self._position))
        # compile position message and store in self._position_message

        reference = HashMap(
            (
                Keyword('message'),
                String(self._exception.__str__()),
                Keyword('name'),
                String(self._exception.__class__.__name__),
             ),
        )
        # turn reference into a nanamilang.datatypes.HashMap instance

        super().__init__(reference)
        # and then we can call Base.__init__() through Python super()

        self._core_traceback = []

        _t = self._exception.__traceback__
        while _t is not None:
            _f = _t.tb_frame.f_code.co_filename
            self._core_traceback.append(
                shortcuts.aligned('at', f'{_f}:{_t.tb_lineno}', 70)
            )
            _t = _t.tb_next
        # store self._traceback (because could be used in self.format)

    def to_py_str(self) -> str:
        """NanamiLang Exception, to_py_str method"""

        return self.get(Keyword('name')).to_py_str()

    def position(self) -> tuple:
        """NanamiLang NException, self._position getter"""

        return self._position

    def exception(self) -> Exception:
        """NanamiLang NException, self,_exception getter"""

        return self._exception

    def get(self, key: Keyword) -> Base:
        """NanamiLang NException, get() method implementation"""

        shortcuts.ASSERT_IS_CHILD_OF(
            key,
            Keyword,
            message='NException.get: the "key" must be a Keyword'
        )

        return self._python_reference.get(key)

    def hashed(self) -> int:
        """NanamiLang NException, hashed() method implementation"""

        # Override hashed() to return the _reference.hashed() value
        return self._python_reference.hashed()

    @export()
    def nominal(self) -> String:
        """NanamiLang NException nominal() method implementation"""

        return String(self.name)

    def format(self, **kwargs) -> str:
        """NanamiLang NException, format() method implementation"""

        _max = 70
        _1space = ' '
        _2spaces = '  '

        _include_traceback = kwargs.get('include_traceback', False)
        if _include_traceback:
            _ = ['  ' + x for x in self._core_traceback]
            _with_traceback = '\n' + '\n'.join(_) + '\n'
        else:
            _with_traceback = shortcuts.aligned('', '<traceback hidden>', _max)

        _src = kwargs.get('src', '')
        if not _src:
            _with_e_highlight = '\n  '
        else:
            _with_e_highlight = f'\n{_2spaces}{_src}\n{_2spaces}{(self._position[2] - 1) * " "}^\n{_2spaces}'

        n_ref = self._python_reference.get(Keyword("name")).reference()
        m_ref = self._python_reference.get(Keyword("message")).reference()

        _nm_separator = _1space if len(self._position_message) + len(n_ref) + len(m_ref) < _max else '\n' + _2spaces

        return f'\n  at {self._position_message}{_with_e_highlight}{n_ref}:{_nm_separator}{m_ref}\n{_with_traceback}'
