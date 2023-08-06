"""NanamiLang Formatter Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from typing import List

from nanamilang import datatypes
from nanamilang.token import Token
from nanamilang.shortcuts import (
    ASSERT_IS_CHILD_OF,
    ASSERT_COLLECTION_NOT_EMPTY,
    ASSERT_EVERY_COLLECTION_ITEM_IS_CHILD_OF
)


class Formatter:
    """NanamiLang Formatter"""

    _tokenized: List[Token] = None

    def __init__(self, tokenized: List[Token]) -> None:
        """
        Initialize a new NanamiLang Formatter instance

        :param tokenized: collection of Token instances
        """

        ASSERT_IS_CHILD_OF(
            tokenized,
            list, 'Formatter: the tokens list needs to be a list.')
        ASSERT_COLLECTION_NOT_EMPTY(
            tokenized, 'Formatter: at least one token is required')
        ASSERT_EVERY_COLLECTION_ITEM_IS_CHILD_OF(
            tokenized, Token, 'Formatter: nothing but Tokens here')
        # Also, this will prevent from attempt to format built tree

        self._tokenized = tokenized

    def format(self) -> str:
        """NanamiLang Formatter, format() given tokens list as a single NanamiLang source code line"""

        # I have plans to re-implement Formatter.format() in order to support source code prettifying.

        def space(idx: int, token: Token) -> str:
            if idx > 0:
                curr_is_data_type = token.type() in Token.data_types
                curr_is_list_begin = token.type() == Token.ListBegin
                prev_is_list_end = self._tokenized[idx - 1].type() == Token.ListEnd
                prev_is_data_type = self._tokenized[idx - 1].type() in Token.data_types
                prev_is_either_data_type_or_list_end = prev_is_data_type or prev_is_list_end

                if prev_is_either_data_type_or_list_end and (curr_is_data_type or curr_is_list_begin):
                    return ' '
            return ''

        def symbol(token: Token) -> str:
            if token.type() in [Token.ListBegin, Token.ListEnd]:
                return {Token.ListBegin: '(', Token.ListEnd: ')'}.get(token.type())
            if token.type() in Token.data_types:
                dt = token.dt()
                return dt.origin() if isinstance(dt, datatypes.Undefined) else dt.format()
            return ''

        return ''.join([f'{space(idx, token)}{symbol(token)}' for idx, token in enumerate(self._tokenized)])
