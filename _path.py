# generated from rosidl_generator_py/resource/_idl.py.em
# with input from custom_interfaces:msg/Path.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100


class Metaclass_Path(type):
    """Metaclass of message 'Path'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Path(metaclass=Metaclass_Path):
    """Message class 'Path'."""

    __slots__ = [
        '_waypoints',
    ]

    _fields_and_field_types = {
        'waypoints': 'sequence<custom_interfaces/HelperLatLon>',
    }

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.waypoints = kwargs.get('waypoints', [])

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.waypoints != other.waypoints:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def waypoints(self):
        """Message field 'waypoints'."""
        return self._waypoints

    @waypoints.setter
    def waypoints(self, value):
        self._waypoints = value
