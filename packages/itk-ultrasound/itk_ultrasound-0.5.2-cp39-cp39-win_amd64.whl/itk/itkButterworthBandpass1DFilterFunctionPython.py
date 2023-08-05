# This file was automatically generated by SWIG (http://www.swig.org).
# Version 4.0.2
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.


import collections

from sys import version_info as _version_info
if _version_info < (3, 7, 0):
    raise RuntimeError("Python 3.7 or later required")


from . import _UltrasoundPython



from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError("Python 2.7 or later required")

# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _itkButterworthBandpass1DFilterFunctionPython
else:
    import _itkButterworthBandpass1DFilterFunctionPython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkButterworthBandpass1DFilterFunctionPython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkButterworthBandpass1DFilterFunctionPython.SWIG_PyStaticMethod_New

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "thisown":
            self.this.own(value)
        elif name == "this":
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


import collections.abc
import itk.ITKCommonBasePython
import itk.pyBasePython
class listIndex2(collections.abc.MutableSequence):
    r"""Proxy of C++ std::list< itk::Index< 2 > > class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    iterator = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_iterator)
    def __iter__(self):
        return self.iterator()
    __nonzero__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2___nonzero__)
    __bool__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2___bool__)
    __len__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2___len__)
    __getslice__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2___getslice__)
    __setslice__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2___setslice__)
    __delslice__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2___delslice__)
    __delitem__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2___delitem__)
    __getitem__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2___getitem__)
    __setitem__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2___setitem__)
    pop = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_pop)
    append = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_append)
    empty = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_empty)
    size = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_size)
    swap = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_swap)
    begin = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_begin)
    end = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_end)
    rbegin = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_rbegin)
    rend = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_rend)
    clear = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_clear)
    get_allocator = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_get_allocator)
    pop_back = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_pop_back)
    erase = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_erase)

    def __init__(self, *args):
        r"""
        __init__(self) -> listIndex2
        __init__(self, other) -> listIndex2

        Parameters
        ----------
        other: std::list< itk::Index< 2 > > const &

        __init__(self, size) -> listIndex2

        Parameters
        ----------
        size: std::list< itk::Index< 2 > >::size_type

        __init__(self, size, value) -> listIndex2

        Parameters
        ----------
        size: std::list< itk::Index< 2 > >::size_type
        value: std::list< itk::Index< 2 > >::value_type const &

        """
        _itkButterworthBandpass1DFilterFunctionPython.listIndex2_swiginit(self, _itkButterworthBandpass1DFilterFunctionPython.new_listIndex2(*args))
    push_back = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_push_back)
    front = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_front)
    back = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_back)
    assign = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_assign)
    resize = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_resize)
    insert = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_insert)
    pop_front = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_pop_front)
    push_front = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_push_front)
    reverse = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex2_reverse)
    __swig_destroy__ = _itkButterworthBandpass1DFilterFunctionPython.delete_listIndex2

# Register listIndex2 in _itkButterworthBandpass1DFilterFunctionPython:
_itkButterworthBandpass1DFilterFunctionPython.listIndex2_swigregister(listIndex2)

class listIndex3(collections.abc.MutableSequence):
    r"""Proxy of C++ std::list< itk::Index< 3 > > class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    iterator = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_iterator)
    def __iter__(self):
        return self.iterator()
    __nonzero__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3___nonzero__)
    __bool__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3___bool__)
    __len__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3___len__)
    __getslice__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3___getslice__)
    __setslice__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3___setslice__)
    __delslice__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3___delslice__)
    __delitem__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3___delitem__)
    __getitem__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3___getitem__)
    __setitem__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3___setitem__)
    pop = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_pop)
    append = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_append)
    empty = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_empty)
    size = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_size)
    swap = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_swap)
    begin = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_begin)
    end = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_end)
    rbegin = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_rbegin)
    rend = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_rend)
    clear = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_clear)
    get_allocator = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_get_allocator)
    pop_back = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_pop_back)
    erase = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_erase)

    def __init__(self, *args):
        r"""
        __init__(self) -> listIndex3
        __init__(self, other) -> listIndex3

        Parameters
        ----------
        other: std::list< itk::Index< 3 > > const &

        __init__(self, size) -> listIndex3

        Parameters
        ----------
        size: std::list< itk::Index< 3 > >::size_type

        __init__(self, size, value) -> listIndex3

        Parameters
        ----------
        size: std::list< itk::Index< 3 > >::size_type
        value: std::list< itk::Index< 3 > >::value_type const &

        """
        _itkButterworthBandpass1DFilterFunctionPython.listIndex3_swiginit(self, _itkButterworthBandpass1DFilterFunctionPython.new_listIndex3(*args))
    push_back = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_push_back)
    front = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_front)
    back = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_back)
    assign = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_assign)
    resize = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_resize)
    insert = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_insert)
    pop_front = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_pop_front)
    push_front = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_push_front)
    reverse = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex3_reverse)
    __swig_destroy__ = _itkButterworthBandpass1DFilterFunctionPython.delete_listIndex3

# Register listIndex3 in _itkButterworthBandpass1DFilterFunctionPython:
_itkButterworthBandpass1DFilterFunctionPython.listIndex3_swigregister(listIndex3)

class listIndex4(collections.abc.MutableSequence):
    r"""Proxy of C++ std::list< itk::Index< 4 > > class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    iterator = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_iterator)
    def __iter__(self):
        return self.iterator()
    __nonzero__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4___nonzero__)
    __bool__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4___bool__)
    __len__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4___len__)
    __getslice__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4___getslice__)
    __setslice__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4___setslice__)
    __delslice__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4___delslice__)
    __delitem__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4___delitem__)
    __getitem__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4___getitem__)
    __setitem__ = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4___setitem__)
    pop = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_pop)
    append = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_append)
    empty = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_empty)
    size = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_size)
    swap = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_swap)
    begin = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_begin)
    end = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_end)
    rbegin = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_rbegin)
    rend = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_rend)
    clear = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_clear)
    get_allocator = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_get_allocator)
    pop_back = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_pop_back)
    erase = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_erase)

    def __init__(self, *args):
        r"""
        __init__(self) -> listIndex4
        __init__(self, other) -> listIndex4

        Parameters
        ----------
        other: std::list< itk::Index< 4 > > const &

        __init__(self, size) -> listIndex4

        Parameters
        ----------
        size: std::list< itk::Index< 4 > >::size_type

        __init__(self, size, value) -> listIndex4

        Parameters
        ----------
        size: std::list< itk::Index< 4 > >::size_type
        value: std::list< itk::Index< 4 > >::value_type const &

        """
        _itkButterworthBandpass1DFilterFunctionPython.listIndex4_swiginit(self, _itkButterworthBandpass1DFilterFunctionPython.new_listIndex4(*args))
    push_back = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_push_back)
    front = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_front)
    back = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_back)
    assign = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_assign)
    resize = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_resize)
    insert = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_insert)
    pop_front = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_pop_front)
    push_front = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_push_front)
    reverse = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.listIndex4_reverse)
    __swig_destroy__ = _itkButterworthBandpass1DFilterFunctionPython.delete_listIndex4

# Register listIndex4 in _itkButterworthBandpass1DFilterFunctionPython:
_itkButterworthBandpass1DFilterFunctionPython.listIndex4_swigregister(listIndex4)


def itkButterworthBandpass1DFilterFunction_Superclass_New():
    return itkButterworthBandpass1DFilterFunction_Superclass.New()

class itkButterworthBandpass1DFilterFunction_Superclass(itk.ITKCommonBasePython.itkObject):
    r"""Proxy of C++ itkButterworthBandpass1DFilterFunction_Superclass class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_Superclass___New_orig__)
    Clone = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_Superclass_Clone)
    EvaluateIndex = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_Superclass_EvaluateIndex)
    SetSignalSize = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_Superclass_SetSignalSize)
    GetSignalSize = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_Superclass_GetSignalSize)
    SetUseCache = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_Superclass_SetUseCache)
    GetUseCache = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_Superclass_GetUseCache)
    EvaluateFrequency = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_Superclass_EvaluateFrequency)
    __swig_destroy__ = _itkButterworthBandpass1DFilterFunctionPython.delete_itkButterworthBandpass1DFilterFunction_Superclass
    cast = _swig_new_static_method(_itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_Superclass_cast)

    def New(*args, **kargs):
        """New() -> itkButterworthBandpass1DFilterFunction_Superclass

        Create a new object of the class itkButterworthBandpass1DFilterFunction_Superclass and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkButterworthBandpass1DFilterFunction_Superclass.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkButterworthBandpass1DFilterFunction_Superclass.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkButterworthBandpass1DFilterFunction_Superclass.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkButterworthBandpass1DFilterFunction_Superclass in _itkButterworthBandpass1DFilterFunctionPython:
_itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_Superclass_swigregister(itkButterworthBandpass1DFilterFunction_Superclass)
itkButterworthBandpass1DFilterFunction_Superclass___New_orig__ = _itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_Superclass___New_orig__
itkButterworthBandpass1DFilterFunction_Superclass_cast = _itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_Superclass_cast


def itkButterworthBandpass1DFilterFunction_New():
    return itkButterworthBandpass1DFilterFunction.New()

class itkButterworthBandpass1DFilterFunction(itkButterworthBandpass1DFilterFunction_Superclass):
    r"""Proxy of C++ itkButterworthBandpass1DFilterFunction class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction___New_orig__)
    Clone = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_Clone)
    SetUpperFrequency = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_SetUpperFrequency)
    GetUpperFrequency = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_GetUpperFrequency)
    SetLowerFrequency = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_SetLowerFrequency)
    GetLowerFrequency = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_GetLowerFrequency)
    SetOrder = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_SetOrder)
    GetOrder = _swig_new_instance_method(_itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_GetOrder)
    __swig_destroy__ = _itkButterworthBandpass1DFilterFunctionPython.delete_itkButterworthBandpass1DFilterFunction
    cast = _swig_new_static_method(_itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_cast)

    def New(*args, **kargs):
        """New() -> itkButterworthBandpass1DFilterFunction

        Create a new object of the class itkButterworthBandpass1DFilterFunction and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkButterworthBandpass1DFilterFunction.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkButterworthBandpass1DFilterFunction.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkButterworthBandpass1DFilterFunction.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkButterworthBandpass1DFilterFunction in _itkButterworthBandpass1DFilterFunctionPython:
_itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_swigregister(itkButterworthBandpass1DFilterFunction)
itkButterworthBandpass1DFilterFunction___New_orig__ = _itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction___New_orig__
itkButterworthBandpass1DFilterFunction_cast = _itkButterworthBandpass1DFilterFunctionPython.itkButterworthBandpass1DFilterFunction_cast



