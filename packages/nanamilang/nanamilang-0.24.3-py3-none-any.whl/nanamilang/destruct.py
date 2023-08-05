"""NanamiLang Collection Destructuring"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from nanamilang.token import Token
from nanamilang.datatypes import Nil
from nanamilang.datatypes import Base
from nanamilang.datatypes import String
from nanamilang.datatypes import Keyword
from nanamilang.datatypes import Collection
from nanamilang.datatypes import IntegerNumber
from nanamilang.datatypes import Vector, HashMap
from nanamilang.shortcuts import (
    NML_M_ITERATE_AS_PAIRS,
    NML_M_FORM_IS_A_VECTOR, NML_M_FORM_IS_A_HASHMAP
)


class Destructuring:
    """Allows to destructure Vectors and HashMaps"""

    # Destructuring('a').destruct('1')
    # -> {'a': 1}

    # Destructuring('a').destruct([1 2])
    # -> {'a': [1 2]}

    # Destructuring([a b]).destruct([1 2])
    # -> {'a': 1, 'b': 2}

    # Destructuring({:keys [a b]}).destruct({:a 1})
    # -> {'a': 1, 'b': nil}

    # Destructuring({:strs [a b]}).destruct({"a" 1})
    # -> {'a': 1, 'b': nil}

    _nil: Nil = Nil('nil')
    _target_token_or_form: list or Token

    def __init__(self, target_token_or_form: list):
        """Initialize a new Destructuring instance"""

        self._target_token_or_form = target_token_or_form

    def destruct(self,
                 any_valid_data_type: Base or Collection) -> dict:
        """Destruct given collection, then return environment dict"""

        if isinstance(self._target_token_or_form, Token):
            any_valid_data_type: Base

            assert issubclass(any_valid_data_type.__class__,
                              (Base,)), (
                'destructuring: right-side needs to be Base Data Type'
            )
            return self._single_token_destructure(any_valid_data_type)
        if isinstance(self._target_token_or_form, list):
            any_valid_data_type: Collection
            assert issubclass(any_valid_data_type.__class__,
                              (Collection,)), (
                'destructuring: right-side needs to be a Collection Type'
            )
            return self._collection_form_destructure(any_valid_data_type)
        return {}  # <-------------- return an empty dictionary otherwise

    def _hashmap_strs_destruct(self, strs: list,
                               collection: Collection) -> dict:
        """When we need to extract strs from the given HashMap"""

        return {s: collection.get(String(s), self._nil) for s in strs}

    def _hashmap_keys_destruct(self, keys: list,
                               collection: Collection) -> dict:
        """When we need to extract keys from the given HashMap"""

        return {k: collection.get(Keyword(k), self._nil) for k in keys}

    def _vector_form_destructure(self, collection: Collection) -> dict:
        """When self._target_token_or_form is actually a Vector form"""

        assert isinstance(collection, Vector), (
            'destructuring: right-side needs to be a Vector'
        )

        environ = {}
        for idx, idn in enumerate(
                NML_M_ITERATE_AS_PAIRS(self._target_token_or_form)):
            idn: Token
            assert isinstance(idn, Token), (
                'destructuring: each element needs to be a Token'
            )
            assert idn.type() == Token.Identifier, (
                'destructuring: each element needs to be an Identifier'
            )
            idx = IntegerNumber(idx)  # <-- cast 'idx' to IntegerNumber
            environ[idn.dt().origin()] = collection.get(idx, self._nil)

        return environ

    def _hashmap_form_destructure(self, collection: Collection) -> dict:
        """When self._target_token_or_form is actually a HashMap form"""

        assert isinstance(collection, HashMap), (
            'destructuring: right-side needs to be a Hashmap'
        )

        hashmap_form = tuple(
            self._target_token_or_form[1:])
        assert len(hashmap_form) == 2, (
            'destructuring: wrong HashMap form arity'
        )
        kind: Token
        vector_form: list
        kind, vector_form = hashmap_form
        assert isinstance(kind, Token), (
            'destructuring: kind needs to be a Token'
        )
        assert kind.type() == Token.Keyword, (
            'destructuring: kind needs to be a Keyword'
        )
        assert NML_M_FORM_IS_A_VECTOR(vector_form), (
            'destructuring: Vector form needs to be a Vector'
        )
        identifiers = []
        for idn in NML_M_ITERATE_AS_PAIRS(vector_form):
            idn: Token
            assert isinstance(idn, Token), (
                'destructuring: each element needs to be a Token'
            )
            assert idn.type() == Token.Identifier, (
                'destructuring: each element needs to be an Identifier'
            )
            identifiers.append(idn.dt().origin())
        assert kind.dt().reference() in ['strs', 'keys'], (
            'destructuring: an unknown HashMap destructuring operation'
        )
        if kind.dt().reference() == 'strs':
            return self._hashmap_strs_destruct(identifiers, collection)
        if kind.dt().reference() == 'keys':
            return self._hashmap_keys_destruct(identifiers, collection)
        return {}  # <------------ return an empty dictionary otherwise

    def _single_token_destructure(self, any_valid_data_type: Base) -> dict:
        """When self._target_token_or_form is actually a Token instance"""

        self._target_token_or_form: Token
        assert self._target_token_or_form.type() == Token.Identifier, (
            'destructuring: the left-side needs to be an Identifier'
        )
        return {self._target_token_or_form.dt().origin(): any_valid_data_type}

    def _collection_form_destructure(self, collection: Collection) -> dict:
        """When self._target_token_or_form is actually a collection form"""

        if NML_M_FORM_IS_A_VECTOR(self._target_token_or_form):
            return self._vector_form_destructure(collection)  # <- if Vector
        if NML_M_FORM_IS_A_HASHMAP(self._target_token_or_form):
            return self._hashmap_form_destructure(collection)  # <- if HashMap

        return {}  # <------------------- return an empty dictionary otherwise
