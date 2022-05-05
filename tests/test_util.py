"""
tests/test_util
---------------

Tests functionality in the aerisweather_api_v1.util module.
"""

from typing import Any, Dict

from aerisweather_api_v1.util import JsonObjectWalker, optisclose, str_to_bool

import pytest


@pytest.fixture
def json_object_walker() -> JsonObjectWalker:
    """
    Creates a :py:class:`JsonObjectWalker` for testing.
    """
    return JsonObjectWalker()


@pytest.fixture
def obj() -> Dict[str, Any]:
    """
    Creates a test dictionary suitable for walking via the :py:class:`JsonObjectWalker`.
    """
    return {
        "response": [
            {
                "id": "testObj",
                "loc": {
                    "long": -93.20,
                    "lat": 45.40,
                },
                "place": {
                    "name": "east bethel",
                    "state": "mn",
                    "country": "us",
                },
                "profile": {
                    "tz": "America/Chicago",
                },
                "data": {
                    "d": {
                        "1": {
                            "2": {
                                "s": "Hello, Nested World!",
                                "l": [1, 1, 2, 3, 5],
                                "i": 3,
                            },
                        },
                    },
                    "l": [
                        0,
                        "Hello, List!",
                        {
                            "k": "List/Dict Value",
                        },
                    ],
                    "i": 2,
                    "f": 3.14,
                    "s": "Hello, World!",
                },
            }
        ]
    }


class TestOptIsClose:
    """
    Tests the functionality of :py:func:`optisclose`.
    """

    def test_a_and_b_are_none(self) -> None:
        """
        Tests that when:
            ``a`` = ``None``
            ``b`` = ``None``

        ``optisclose`` returns ``True``.
        """
        assert optisclose(None, None)

    def test_a_is_none_b_is_float(self) -> None:
        """
        Tests that when:
            a = ``None``
            b = some ``float``

        ``optisclose`` returns ``False``.
        """
        assert not optisclose(None, 3.14)

    def test_a_is_float_b_is_none(self) -> None:
        """
        Tests that when:
            a = some ``float``
            b = ``None``

        ``optisclose`` returns ``False``.
        """
        assert not optisclose(3.14, None)

    def test_a_and_b_equal(self) -> None:
        """
        Tests that when ``a`` and ``b`` are equal, ``optisclose`` returns ``True``.
        """
        assert optisclose(3.14, 3.14)

    def test_increased_rel_tol(self) -> None:
        """
        Tests that setting ``rel_tol`` appropriately increases the permissible float delta.
        """
        # sanity check: these should not compare equally
        assert not optisclose(0.8, 1.0)
        assert not optisclose(0.8, 1.5)

        # 0.8 and 1.0 should compare equally with a large enough value of rel_tol
        assert optisclose(0.8, 1.0, rel_tol=0.25)

        # but 0.8 and 1.5 still will not compare equally
        assert not optisclose(0.8, 1.5, rel_tol=0.25)

    def test_increased_abs_tol(self) -> None:
        """
        Tests that setting ``abs_tol`` appropriately increases the permissible float delta.
        """
        # sanity check: these should not compare equally
        assert not optisclose(0.8, 1.0)
        assert not optisclose(0.8, 1.5)

        # 0.8 and 1.0 should compare equally with a large enough value of rel_tol
        assert optisclose(0.8, 1.0, abs_tol=0.25)

        # but 0.8 and 1.5 still will not compare equally
        assert not optisclose(0.8, 1.5, abs_tol=0.25)


class TestStrToBool:
    """
    Tests the functionality of :py:func:`str_to_bool`.
    """

    @pytest.mark.parametrize("val", ["true", "t", "1", "yes", "y"])
    def test_str_truthy_values_to_bool(self, val: str) -> None:
        """
        Tests that values string values indicating truth are converted to ``True``.
        """
        assert str_to_bool(val)

    @pytest.mark.parametrize("val", ["false", "f", "0", "no", "n"])
    def test_str_falsy_values_to_bool(self, val: str) -> None:
        """
        Tests that values string values indicating false are converted to ``False``.
        """
        assert not str_to_bool(val)

    @pytest.mark.parametrize("val", ["1000", "0001", "maybe", "yep", "nope", "yea, no", "tf"])
    def test_str_non_bool_values_raise_error(self, val: str) -> None:
        """
        Tests that values string values indicating false are converted to ``False``.
        """
        with pytest.raises(ValueError):
            str_to_bool(val)


class TestJsonObjectWalker:
    """
    Tests the functionality of :py:class:`JsonObjectWalker`.
    """

    def test_retrieve_nested(self, json_object_walker: JsonObjectWalker, obj: Dict[str, Any]) -> None:
        """
        Tests walking nested dictionaries to retrieve a non-collection object.
        """
        json_object_walker.set_object(obj["response"][0], "TestObject")

        assert json_object_walker("data", "d", "1", "2", "s") == "Hello, Nested World!"

    def test_retrieve_list(self, json_object_walker: JsonObjectWalker, obj: Dict[str, Any]) -> None:
        """
        Tests walking an object to retrieve an entire list and each of its individual elements.
        """
        json_object_walker.set_object(obj["response"][0], "TestObject")

        assert json_object_walker("data", "d", "1", "2", "l") == [1, 1, 2, 3, 5]
        assert json_object_walker("data", "d", "1", "2", "l", 0) == 1
        assert json_object_walker("data", "d", "1", "2", "l", 1) == 1
        assert json_object_walker("data", "d", "1", "2", "l", 2) == 2
        assert json_object_walker("data", "d", "1", "2", "l", 3) == 3
        assert json_object_walker("data", "d", "1", "2", "l", 4) == 5

    def test_retrieve_dict(self, json_object_walker: JsonObjectWalker, obj: Dict[str, Any]) -> None:
        """
        Tests walking an object to retrieve an entire dict and each of its individual elements.
        """
        json_object_walker.set_object(obj, "TestObject")

        assert json_object_walker("response", 0, "place") == {
            "name": "east bethel",
            "state": "mn",
            "country": "us",
        }
        assert json_object_walker("response", 0, "place", "name") == "east bethel"
        assert json_object_walker("response", 0, "place", "state") == "mn"
        assert json_object_walker("response", 0, "place", "country") == "us"

    def test_retrieve_item_from_non_collection(self, json_object_walker: JsonObjectWalker, obj: Dict[str, Any]) -> None:
        """
        Tests that attempting to retrieve an item from a non-collection type (e.g. int) raises an error.
        """
        json_object_walker.set_object(obj["response"][0], "TestObject")

        with pytest.raises(ValueError):
            json_object_walker("data", "s", 1)

    def test_retrieve_nonexistent_item(self, json_object_walker: JsonObjectWalker, obj: Dict[str, Any]) -> None:
        """
        Tests that attempting to retrieve a nonexistent key raises an error.
        """
        json_object_walker.set_object(obj["response"][0], "TestObject")

        with pytest.raises(ValueError):
            json_object_walker("data", "d", "NotARealKey")
