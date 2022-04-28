"""
aerisweather/util
-----------------

Contains miscellaneous utility code.
"""

from math import isclose
from typing import Any, Dict, Optional, Union


_NO_DEFAULT = object()

JsonKey = Union[str, int]

#: Normalized string values that can be interpreted as ``True``.
_true_values = {"true", "t", "1", "yes", "y"}

#: Normalized string values that can be interpreted as ``False``.
_false_values = {"false", "f", "0", "no", "n"}


def optisclose(
    a: Optional[float], b: Optional[float], rel_tol: Optional[float] = None, abs_tol: Optional[float] = None
) -> bool:
    """
    Returns ``True`` if ``a`` and ``b`` are floating point numbers of approximate equality, or
    both are ``None``. Returns ``False`` otherwise.

    This function wraps Python's :py:func:`math.isclose`, but allows for ``a`` and ``b`` to
    be ``None``.
    """
    if a is None and b is None:
        return True
    elif a is None or b is None:
        return False

    kwargs = dict()
    if rel_tol is not None:
        kwargs["rel_tol"] = rel_tol
    if abs_tol is not None:
        kwargs["abs_tol"] = abs_tol

    return isclose(a, b, **kwargs)


def str_to_bool(s: str) -> bool:
    """
    Attempts to interpret the string ``s`` as a boolean value. If ``s``
    does not appear to be a valid boolean, raises a :py:class:`ValueError`.

    :param s: the string to interpret as a boolean
    :return: the boolean interpretation of ``s``
    """
    normalized_s = s.strip().lower()
    if normalized_s in _true_values:
        return True
    elif normalized_s in _false_values:
        return False
    raise ValueError(f"could not interpret '{s}' as a boolean")


class JsonObjectWalker:
    """
    Class that helps walk deserialized JSON objects.

    The purpose is to ensure that there are clear error messages when
    constructing object models from JSON, without having to write
    excessive error handling logic for missing dictionary elements.
    """

    def __init__(self) -> None:
        self.o: Dict[Any, Any] = dict()
        self.exc_type = ValueError
        self.missing_msg = "missing required property {prop}; can't access {full_prop}"
        self.non_collection_msg = "property {prop} is not dict or list; can't access {full_prop}"

    def set_object(self, o: Dict[Any, Any], object_type: str) -> None:
        """
        Sets the JSON object to be walked.

        :param o: the JSON object whose elements will be walked
        :param object_type: a description of what the object represents; used in error messages
        """
        self.o = o
        self.object_type = object_type

    def __call__(self, *args: JsonKey, default: Any = _NO_DEFAULT) -> Any:
        r"""
        Walks the object previously set by ``set_object``, returning the value
        at the provided path. If the path cannot be walked fully, ``default``
        is returned if it is specified. Otherwise, an exception is raised.

        :param \*args: attributes of the object to walk (i.e. dictionary keys and list indices)
        :param default: the default value to return if the object path cannot be walked
        """
        try:
            result = self._walk(*args)
        except self.exc_type as e:
            if default is not _NO_DEFAULT:
                result = default
            else:
                raise e
        return result

    def _walk(self, *args: JsonKey) -> Any:
        r"""
        Walks the object previously set by ``set_object``, returning the value
        at the provided path. Raises an exception if the path cannot be
        walked fully.

        :param \*args: attributes of the object to walk (i.e. dictionary keys and list indices)
        """
        current = self.o
        full_prop = ".".join(str(i) for i in args)
        prop = list()
        for i in args:
            if not isinstance(current, (dict, list)):
                raise self.exc_type(self.non_collection_msg.format(prop=".".join(prop), full_prop=full_prop))
            try:
                prop.append(i)
                current = current[i]
            except (IndexError, KeyError):
                raise self.exc_type(self.missing_msg.format(prop=".".join(str(i) for i in prop), full_prop=full_prop))
        return current
