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
    from . import _itkAnalyticSignalImageFilterPython
else:
    import _itkAnalyticSignalImageFilterPython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkAnalyticSignalImageFilterPython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkAnalyticSignalImageFilterPython.SWIG_PyStaticMethod_New

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
import itk.itkImageToImageFilterBPython
import itk.itkImageRegionPython
import itk.ITKCommonBasePython
import itk.pyBasePython
import itk.itkSizePython
import itk.itkIndexPython
import itk.itkOffsetPython
import itk.itkImagePython
import itk.itkRGBPixelPython
import itk.itkFixedArrayPython
import itk.itkVectorPython
import itk.vnl_vector_refPython
import itk.stdcomplexPython
import itk.vnl_vectorPython
import itk.vnl_matrixPython
import itk.itkMatrixPython
import itk.vnl_matrix_fixedPython
import itk.itkPointPython
import itk.itkCovariantVectorPython
import itk.itkSymmetricSecondRankTensorPython
import itk.itkRGBAPixelPython
import itk.itkVectorImagePython
import itk.itkVariableLengthVectorPython
import itk.itkImageToImageFilterCommonPython
import itk.itkImageSourcePython
import itk.itkImageSourceCommonPython
import itk.itkFrequencyDomain1DImageFilterPython
import itk.itkCurvilinearArraySpecialCoordinatesImagePython
import itk.ITKIOImageBaseBasePython
import itk.itkSpectra1DSupportWindowImageFilterPython
import itk.itkSimpleDataObjectDecoratorPython
import itk.itkArrayPython
import itk.itkFrequencyDomain1DFilterFunctionPython

def itkAnalyticSignalImageFilterID2ICD2_New():
    return itkAnalyticSignalImageFilterID2ICD2.New()

class itkAnalyticSignalImageFilterID2ICD2(itk.itkImageToImageFilterBPython.itkImageToImageFilterID2ICD2):
    r"""Proxy of C++ itkAnalyticSignalImageFilterID2ICD2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID2ICD2___New_orig__)
    Clone = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID2ICD2_Clone)
    GetDirection = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID2ICD2_GetDirection)
    SetDirection = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID2ICD2_SetDirection)
    SetFrequencyFilter = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID2ICD2_SetFrequencyFilter)
    __swig_destroy__ = _itkAnalyticSignalImageFilterPython.delete_itkAnalyticSignalImageFilterID2ICD2
    cast = _swig_new_static_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID2ICD2_cast)

    def New(*args, **kargs):
        """New() -> itkAnalyticSignalImageFilterID2ICD2

        Create a new object of the class itkAnalyticSignalImageFilterID2ICD2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkAnalyticSignalImageFilterID2ICD2.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkAnalyticSignalImageFilterID2ICD2.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkAnalyticSignalImageFilterID2ICD2.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkAnalyticSignalImageFilterID2ICD2 in _itkAnalyticSignalImageFilterPython:
_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID2ICD2_swigregister(itkAnalyticSignalImageFilterID2ICD2)
itkAnalyticSignalImageFilterID2ICD2___New_orig__ = _itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID2ICD2___New_orig__
itkAnalyticSignalImageFilterID2ICD2_cast = _itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID2ICD2_cast


def itkAnalyticSignalImageFilterID3ICD3_New():
    return itkAnalyticSignalImageFilterID3ICD3.New()

class itkAnalyticSignalImageFilterID3ICD3(itk.itkImageToImageFilterBPython.itkImageToImageFilterID3ICD3):
    r"""Proxy of C++ itkAnalyticSignalImageFilterID3ICD3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID3ICD3___New_orig__)
    Clone = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID3ICD3_Clone)
    GetDirection = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID3ICD3_GetDirection)
    SetDirection = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID3ICD3_SetDirection)
    SetFrequencyFilter = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID3ICD3_SetFrequencyFilter)
    __swig_destroy__ = _itkAnalyticSignalImageFilterPython.delete_itkAnalyticSignalImageFilterID3ICD3
    cast = _swig_new_static_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID3ICD3_cast)

    def New(*args, **kargs):
        """New() -> itkAnalyticSignalImageFilterID3ICD3

        Create a new object of the class itkAnalyticSignalImageFilterID3ICD3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkAnalyticSignalImageFilterID3ICD3.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkAnalyticSignalImageFilterID3ICD3.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkAnalyticSignalImageFilterID3ICD3.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkAnalyticSignalImageFilterID3ICD3 in _itkAnalyticSignalImageFilterPython:
_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID3ICD3_swigregister(itkAnalyticSignalImageFilterID3ICD3)
itkAnalyticSignalImageFilterID3ICD3___New_orig__ = _itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID3ICD3___New_orig__
itkAnalyticSignalImageFilterID3ICD3_cast = _itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID3ICD3_cast


def itkAnalyticSignalImageFilterID4ICD4_New():
    return itkAnalyticSignalImageFilterID4ICD4.New()

class itkAnalyticSignalImageFilterID4ICD4(itk.itkImageToImageFilterBPython.itkImageToImageFilterID4ICD4):
    r"""Proxy of C++ itkAnalyticSignalImageFilterID4ICD4 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID4ICD4___New_orig__)
    Clone = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID4ICD4_Clone)
    GetDirection = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID4ICD4_GetDirection)
    SetDirection = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID4ICD4_SetDirection)
    SetFrequencyFilter = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID4ICD4_SetFrequencyFilter)
    __swig_destroy__ = _itkAnalyticSignalImageFilterPython.delete_itkAnalyticSignalImageFilterID4ICD4
    cast = _swig_new_static_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID4ICD4_cast)

    def New(*args, **kargs):
        """New() -> itkAnalyticSignalImageFilterID4ICD4

        Create a new object of the class itkAnalyticSignalImageFilterID4ICD4 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkAnalyticSignalImageFilterID4ICD4.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkAnalyticSignalImageFilterID4ICD4.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkAnalyticSignalImageFilterID4ICD4.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkAnalyticSignalImageFilterID4ICD4 in _itkAnalyticSignalImageFilterPython:
_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID4ICD4_swigregister(itkAnalyticSignalImageFilterID4ICD4)
itkAnalyticSignalImageFilterID4ICD4___New_orig__ = _itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID4ICD4___New_orig__
itkAnalyticSignalImageFilterID4ICD4_cast = _itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterID4ICD4_cast


def itkAnalyticSignalImageFilterIF2ICF2_New():
    return itkAnalyticSignalImageFilterIF2ICF2.New()

class itkAnalyticSignalImageFilterIF2ICF2(itk.itkImageToImageFilterBPython.itkImageToImageFilterIF2ICF2):
    r"""Proxy of C++ itkAnalyticSignalImageFilterIF2ICF2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF2ICF2___New_orig__)
    Clone = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF2ICF2_Clone)
    GetDirection = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF2ICF2_GetDirection)
    SetDirection = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF2ICF2_SetDirection)
    SetFrequencyFilter = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF2ICF2_SetFrequencyFilter)
    __swig_destroy__ = _itkAnalyticSignalImageFilterPython.delete_itkAnalyticSignalImageFilterIF2ICF2
    cast = _swig_new_static_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF2ICF2_cast)

    def New(*args, **kargs):
        """New() -> itkAnalyticSignalImageFilterIF2ICF2

        Create a new object of the class itkAnalyticSignalImageFilterIF2ICF2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkAnalyticSignalImageFilterIF2ICF2.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkAnalyticSignalImageFilterIF2ICF2.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkAnalyticSignalImageFilterIF2ICF2.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkAnalyticSignalImageFilterIF2ICF2 in _itkAnalyticSignalImageFilterPython:
_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF2ICF2_swigregister(itkAnalyticSignalImageFilterIF2ICF2)
itkAnalyticSignalImageFilterIF2ICF2___New_orig__ = _itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF2ICF2___New_orig__
itkAnalyticSignalImageFilterIF2ICF2_cast = _itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF2ICF2_cast


def itkAnalyticSignalImageFilterIF3ICF3_New():
    return itkAnalyticSignalImageFilterIF3ICF3.New()

class itkAnalyticSignalImageFilterIF3ICF3(itk.itkImageToImageFilterBPython.itkImageToImageFilterIF3ICF3):
    r"""Proxy of C++ itkAnalyticSignalImageFilterIF3ICF3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF3ICF3___New_orig__)
    Clone = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF3ICF3_Clone)
    GetDirection = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF3ICF3_GetDirection)
    SetDirection = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF3ICF3_SetDirection)
    SetFrequencyFilter = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF3ICF3_SetFrequencyFilter)
    __swig_destroy__ = _itkAnalyticSignalImageFilterPython.delete_itkAnalyticSignalImageFilterIF3ICF3
    cast = _swig_new_static_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF3ICF3_cast)

    def New(*args, **kargs):
        """New() -> itkAnalyticSignalImageFilterIF3ICF3

        Create a new object of the class itkAnalyticSignalImageFilterIF3ICF3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkAnalyticSignalImageFilterIF3ICF3.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkAnalyticSignalImageFilterIF3ICF3.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkAnalyticSignalImageFilterIF3ICF3.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkAnalyticSignalImageFilterIF3ICF3 in _itkAnalyticSignalImageFilterPython:
_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF3ICF3_swigregister(itkAnalyticSignalImageFilterIF3ICF3)
itkAnalyticSignalImageFilterIF3ICF3___New_orig__ = _itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF3ICF3___New_orig__
itkAnalyticSignalImageFilterIF3ICF3_cast = _itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF3ICF3_cast


def itkAnalyticSignalImageFilterIF4ICF4_New():
    return itkAnalyticSignalImageFilterIF4ICF4.New()

class itkAnalyticSignalImageFilterIF4ICF4(itk.itkImageToImageFilterBPython.itkImageToImageFilterIF4ICF4):
    r"""Proxy of C++ itkAnalyticSignalImageFilterIF4ICF4 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF4ICF4___New_orig__)
    Clone = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF4ICF4_Clone)
    GetDirection = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF4ICF4_GetDirection)
    SetDirection = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF4ICF4_SetDirection)
    SetFrequencyFilter = _swig_new_instance_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF4ICF4_SetFrequencyFilter)
    __swig_destroy__ = _itkAnalyticSignalImageFilterPython.delete_itkAnalyticSignalImageFilterIF4ICF4
    cast = _swig_new_static_method(_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF4ICF4_cast)

    def New(*args, **kargs):
        """New() -> itkAnalyticSignalImageFilterIF4ICF4

        Create a new object of the class itkAnalyticSignalImageFilterIF4ICF4 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkAnalyticSignalImageFilterIF4ICF4.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkAnalyticSignalImageFilterIF4ICF4.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkAnalyticSignalImageFilterIF4ICF4.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkAnalyticSignalImageFilterIF4ICF4 in _itkAnalyticSignalImageFilterPython:
_itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF4ICF4_swigregister(itkAnalyticSignalImageFilterIF4ICF4)
itkAnalyticSignalImageFilterIF4ICF4___New_orig__ = _itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF4ICF4___New_orig__
itkAnalyticSignalImageFilterIF4ICF4_cast = _itkAnalyticSignalImageFilterPython.itkAnalyticSignalImageFilterIF4ICF4_cast


from itk.support import helpers
import itk.support.types as itkt
from typing import Sequence, Tuple, Union

@helpers.accept_array_like_xarray_torch
def analytic_signal_image_filter(*args: itkt.ImageLike,  direction: int=..., frequency_filter=...,**kwargs)-> itkt.ImageSourceReturn:
    """Functional interface for AnalyticSignalImageFilter"""
    import itk

    kwarg_typehints = { 'direction':direction,'frequency_filter':frequency_filter }
    specified_kwarg_typehints = { k:v for (k,v) in kwarg_typehints.items() if kwarg_typehints[k] is not ... }
    kwargs.update(specified_kwarg_typehints)

    instance = itk.AnalyticSignalImageFilter.New(*args, **kwargs)
    return instance.__internal_call__()

def analytic_signal_image_filter_init_docstring():
    import itk
    from itk.support import template_class

    filter_class = itk.Ultrasound.AnalyticSignalImageFilter
    analytic_signal_image_filter.process_object = filter_class
    is_template = isinstance(filter_class, template_class.itkTemplate)
    if is_template:
        filter_object = filter_class.values()[0]
    else:
        filter_object = filter_class

    analytic_signal_image_filter.__doc__ = filter_object.__doc__




