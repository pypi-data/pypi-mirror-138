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
    from . import _itkBModeImageFilterPython
else:
    import _itkBModeImageFilterPython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkBModeImageFilterPython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkBModeImageFilterPython.SWIG_PyStaticMethod_New

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
import itk.itkFrequencyDomain1DImageFilterPython
import itk.itkFrequencyDomain1DFilterFunctionPython
import itk.ITKCommonBasePython
import itk.pyBasePython
import itk.itkImageRegionPython
import itk.itkSizePython
import itk.itkIndexPython
import itk.itkOffsetPython
import itk.itkCurvilinearArraySpecialCoordinatesImagePython
import itk.itkVectorPython
import itk.vnl_vector_refPython
import itk.stdcomplexPython
import itk.vnl_vectorPython
import itk.vnl_matrixPython
import itk.itkFixedArrayPython
import itk.itkSimpleDataObjectDecoratorPython
import itk.itkArrayPython
import itk.itkCovariantVectorPython
import itk.itkRGBPixelPython
import itk.itkRGBAPixelPython
import itk.itkSpectra1DSupportWindowImageFilterPython
import itk.itkImageSourceCommonPython
import itk.itkImageToImageFilterCommonPython
import itk.itkImagePython
import itk.itkMatrixPython
import itk.vnl_matrix_fixedPython
import itk.itkPointPython
import itk.itkSymmetricSecondRankTensorPython
import itk.ITKIOImageBaseBasePython
import itk.itkImageSourcePython
import itk.itkVectorImagePython
import itk.itkVariableLengthVectorPython
import itk.itkImageToImageFilterAPython

def itkBModeImageFilterCASCID2CASCID2CASCcomplexID2_New():
    return itkBModeImageFilterCASCID2CASCID2CASCcomplexID2.New()

class itkBModeImageFilterCASCID2CASCID2CASCcomplexID2(itk.itkCurvilinearArraySpecialCoordinatesImagePython.itkCastImageFilterCASCID2CASCID2_Superclass_Superclass):
    r"""Proxy of C++ itkBModeImageFilterCASCID2CASCID2CASCcomplexID2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkBModeImageFilterPython.itkBModeImageFilterCASCID2CASCID2CASCcomplexID2___New_orig__)
    Clone = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterCASCID2CASCID2CASCcomplexID2_Clone)
    SetDirection = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterCASCID2CASCID2CASCcomplexID2_SetDirection)
    GetDirection = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterCASCID2CASCID2CASCcomplexID2_GetDirection)
    SetFrequencyFilter = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterCASCID2CASCID2CASCcomplexID2_SetFrequencyFilter)
    __swig_destroy__ = _itkBModeImageFilterPython.delete_itkBModeImageFilterCASCID2CASCID2CASCcomplexID2
    cast = _swig_new_static_method(_itkBModeImageFilterPython.itkBModeImageFilterCASCID2CASCID2CASCcomplexID2_cast)

    def New(*args, **kargs):
        """New() -> itkBModeImageFilterCASCID2CASCID2CASCcomplexID2

        Create a new object of the class itkBModeImageFilterCASCID2CASCID2CASCcomplexID2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkBModeImageFilterCASCID2CASCID2CASCcomplexID2.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkBModeImageFilterCASCID2CASCID2CASCcomplexID2.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkBModeImageFilterCASCID2CASCID2CASCcomplexID2.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkBModeImageFilterCASCID2CASCID2CASCcomplexID2 in _itkBModeImageFilterPython:
_itkBModeImageFilterPython.itkBModeImageFilterCASCID2CASCID2CASCcomplexID2_swigregister(itkBModeImageFilterCASCID2CASCID2CASCcomplexID2)
itkBModeImageFilterCASCID2CASCID2CASCcomplexID2___New_orig__ = _itkBModeImageFilterPython.itkBModeImageFilterCASCID2CASCID2CASCcomplexID2___New_orig__
itkBModeImageFilterCASCID2CASCID2CASCcomplexID2_cast = _itkBModeImageFilterPython.itkBModeImageFilterCASCID2CASCID2CASCcomplexID2_cast


def itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2_New():
    return itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2.New()

class itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2(itk.itkCurvilinearArraySpecialCoordinatesImagePython.itkCastImageFilterCASCIF2CASCIF2_Superclass_Superclass):
    r"""Proxy of C++ itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkBModeImageFilterPython.itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2___New_orig__)
    Clone = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2_Clone)
    SetDirection = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2_SetDirection)
    GetDirection = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2_GetDirection)
    SetFrequencyFilter = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2_SetFrequencyFilter)
    __swig_destroy__ = _itkBModeImageFilterPython.delete_itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2
    cast = _swig_new_static_method(_itkBModeImageFilterPython.itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2_cast)

    def New(*args, **kargs):
        """New() -> itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2

        Create a new object of the class itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2 in _itkBModeImageFilterPython:
_itkBModeImageFilterPython.itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2_swigregister(itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2)
itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2___New_orig__ = _itkBModeImageFilterPython.itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2___New_orig__
itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2_cast = _itkBModeImageFilterPython.itkBModeImageFilterCASCIF2CASCIF2CASCcomplexIF2_cast


def itkBModeImageFilterID2ID2_New():
    return itkBModeImageFilterID2ID2.New()

class itkBModeImageFilterID2ID2(itk.itkImageToImageFilterAPython.itkImageToImageFilterID2ID2):
    r"""Proxy of C++ itkBModeImageFilterID2ID2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkBModeImageFilterPython.itkBModeImageFilterID2ID2___New_orig__)
    Clone = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterID2ID2_Clone)
    SetDirection = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterID2ID2_SetDirection)
    GetDirection = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterID2ID2_GetDirection)
    SetFrequencyFilter = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterID2ID2_SetFrequencyFilter)
    __swig_destroy__ = _itkBModeImageFilterPython.delete_itkBModeImageFilterID2ID2
    cast = _swig_new_static_method(_itkBModeImageFilterPython.itkBModeImageFilterID2ID2_cast)

    def New(*args, **kargs):
        """New() -> itkBModeImageFilterID2ID2

        Create a new object of the class itkBModeImageFilterID2ID2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkBModeImageFilterID2ID2.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkBModeImageFilterID2ID2.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkBModeImageFilterID2ID2.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkBModeImageFilterID2ID2 in _itkBModeImageFilterPython:
_itkBModeImageFilterPython.itkBModeImageFilterID2ID2_swigregister(itkBModeImageFilterID2ID2)
itkBModeImageFilterID2ID2___New_orig__ = _itkBModeImageFilterPython.itkBModeImageFilterID2ID2___New_orig__
itkBModeImageFilterID2ID2_cast = _itkBModeImageFilterPython.itkBModeImageFilterID2ID2_cast


def itkBModeImageFilterID3ID3_New():
    return itkBModeImageFilterID3ID3.New()

class itkBModeImageFilterID3ID3(itk.itkImageToImageFilterAPython.itkImageToImageFilterID3ID3):
    r"""Proxy of C++ itkBModeImageFilterID3ID3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkBModeImageFilterPython.itkBModeImageFilterID3ID3___New_orig__)
    Clone = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterID3ID3_Clone)
    SetDirection = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterID3ID3_SetDirection)
    GetDirection = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterID3ID3_GetDirection)
    SetFrequencyFilter = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterID3ID3_SetFrequencyFilter)
    __swig_destroy__ = _itkBModeImageFilterPython.delete_itkBModeImageFilterID3ID3
    cast = _swig_new_static_method(_itkBModeImageFilterPython.itkBModeImageFilterID3ID3_cast)

    def New(*args, **kargs):
        """New() -> itkBModeImageFilterID3ID3

        Create a new object of the class itkBModeImageFilterID3ID3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkBModeImageFilterID3ID3.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkBModeImageFilterID3ID3.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkBModeImageFilterID3ID3.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkBModeImageFilterID3ID3 in _itkBModeImageFilterPython:
_itkBModeImageFilterPython.itkBModeImageFilterID3ID3_swigregister(itkBModeImageFilterID3ID3)
itkBModeImageFilterID3ID3___New_orig__ = _itkBModeImageFilterPython.itkBModeImageFilterID3ID3___New_orig__
itkBModeImageFilterID3ID3_cast = _itkBModeImageFilterPython.itkBModeImageFilterID3ID3_cast


def itkBModeImageFilterID4ID4_New():
    return itkBModeImageFilterID4ID4.New()

class itkBModeImageFilterID4ID4(itk.itkImageToImageFilterAPython.itkImageToImageFilterID4ID4):
    r"""Proxy of C++ itkBModeImageFilterID4ID4 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkBModeImageFilterPython.itkBModeImageFilterID4ID4___New_orig__)
    Clone = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterID4ID4_Clone)
    SetDirection = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterID4ID4_SetDirection)
    GetDirection = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterID4ID4_GetDirection)
    SetFrequencyFilter = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterID4ID4_SetFrequencyFilter)
    __swig_destroy__ = _itkBModeImageFilterPython.delete_itkBModeImageFilterID4ID4
    cast = _swig_new_static_method(_itkBModeImageFilterPython.itkBModeImageFilterID4ID4_cast)

    def New(*args, **kargs):
        """New() -> itkBModeImageFilterID4ID4

        Create a new object of the class itkBModeImageFilterID4ID4 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkBModeImageFilterID4ID4.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkBModeImageFilterID4ID4.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkBModeImageFilterID4ID4.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkBModeImageFilterID4ID4 in _itkBModeImageFilterPython:
_itkBModeImageFilterPython.itkBModeImageFilterID4ID4_swigregister(itkBModeImageFilterID4ID4)
itkBModeImageFilterID4ID4___New_orig__ = _itkBModeImageFilterPython.itkBModeImageFilterID4ID4___New_orig__
itkBModeImageFilterID4ID4_cast = _itkBModeImageFilterPython.itkBModeImageFilterID4ID4_cast


def itkBModeImageFilterIF2IF2_New():
    return itkBModeImageFilterIF2IF2.New()

class itkBModeImageFilterIF2IF2(itk.itkImageToImageFilterAPython.itkImageToImageFilterIF2IF2):
    r"""Proxy of C++ itkBModeImageFilterIF2IF2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkBModeImageFilterPython.itkBModeImageFilterIF2IF2___New_orig__)
    Clone = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterIF2IF2_Clone)
    SetDirection = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterIF2IF2_SetDirection)
    GetDirection = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterIF2IF2_GetDirection)
    SetFrequencyFilter = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterIF2IF2_SetFrequencyFilter)
    __swig_destroy__ = _itkBModeImageFilterPython.delete_itkBModeImageFilterIF2IF2
    cast = _swig_new_static_method(_itkBModeImageFilterPython.itkBModeImageFilterIF2IF2_cast)

    def New(*args, **kargs):
        """New() -> itkBModeImageFilterIF2IF2

        Create a new object of the class itkBModeImageFilterIF2IF2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkBModeImageFilterIF2IF2.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkBModeImageFilterIF2IF2.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkBModeImageFilterIF2IF2.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkBModeImageFilterIF2IF2 in _itkBModeImageFilterPython:
_itkBModeImageFilterPython.itkBModeImageFilterIF2IF2_swigregister(itkBModeImageFilterIF2IF2)
itkBModeImageFilterIF2IF2___New_orig__ = _itkBModeImageFilterPython.itkBModeImageFilterIF2IF2___New_orig__
itkBModeImageFilterIF2IF2_cast = _itkBModeImageFilterPython.itkBModeImageFilterIF2IF2_cast


def itkBModeImageFilterIF3IF3_New():
    return itkBModeImageFilterIF3IF3.New()

class itkBModeImageFilterIF3IF3(itk.itkImageToImageFilterAPython.itkImageToImageFilterIF3IF3):
    r"""Proxy of C++ itkBModeImageFilterIF3IF3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkBModeImageFilterPython.itkBModeImageFilterIF3IF3___New_orig__)
    Clone = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterIF3IF3_Clone)
    SetDirection = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterIF3IF3_SetDirection)
    GetDirection = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterIF3IF3_GetDirection)
    SetFrequencyFilter = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterIF3IF3_SetFrequencyFilter)
    __swig_destroy__ = _itkBModeImageFilterPython.delete_itkBModeImageFilterIF3IF3
    cast = _swig_new_static_method(_itkBModeImageFilterPython.itkBModeImageFilterIF3IF3_cast)

    def New(*args, **kargs):
        """New() -> itkBModeImageFilterIF3IF3

        Create a new object of the class itkBModeImageFilterIF3IF3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkBModeImageFilterIF3IF3.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkBModeImageFilterIF3IF3.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkBModeImageFilterIF3IF3.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkBModeImageFilterIF3IF3 in _itkBModeImageFilterPython:
_itkBModeImageFilterPython.itkBModeImageFilterIF3IF3_swigregister(itkBModeImageFilterIF3IF3)
itkBModeImageFilterIF3IF3___New_orig__ = _itkBModeImageFilterPython.itkBModeImageFilterIF3IF3___New_orig__
itkBModeImageFilterIF3IF3_cast = _itkBModeImageFilterPython.itkBModeImageFilterIF3IF3_cast


def itkBModeImageFilterIF4IF4_New():
    return itkBModeImageFilterIF4IF4.New()

class itkBModeImageFilterIF4IF4(itk.itkImageToImageFilterAPython.itkImageToImageFilterIF4IF4):
    r"""Proxy of C++ itkBModeImageFilterIF4IF4 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkBModeImageFilterPython.itkBModeImageFilterIF4IF4___New_orig__)
    Clone = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterIF4IF4_Clone)
    SetDirection = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterIF4IF4_SetDirection)
    GetDirection = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterIF4IF4_GetDirection)
    SetFrequencyFilter = _swig_new_instance_method(_itkBModeImageFilterPython.itkBModeImageFilterIF4IF4_SetFrequencyFilter)
    __swig_destroy__ = _itkBModeImageFilterPython.delete_itkBModeImageFilterIF4IF4
    cast = _swig_new_static_method(_itkBModeImageFilterPython.itkBModeImageFilterIF4IF4_cast)

    def New(*args, **kargs):
        """New() -> itkBModeImageFilterIF4IF4

        Create a new object of the class itkBModeImageFilterIF4IF4 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkBModeImageFilterIF4IF4.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkBModeImageFilterIF4IF4.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkBModeImageFilterIF4IF4.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkBModeImageFilterIF4IF4 in _itkBModeImageFilterPython:
_itkBModeImageFilterPython.itkBModeImageFilterIF4IF4_swigregister(itkBModeImageFilterIF4IF4)
itkBModeImageFilterIF4IF4___New_orig__ = _itkBModeImageFilterPython.itkBModeImageFilterIF4IF4___New_orig__
itkBModeImageFilterIF4IF4_cast = _itkBModeImageFilterPython.itkBModeImageFilterIF4IF4_cast


from itk.support import helpers
import itk.support.types as itkt
from typing import Sequence, Tuple, Union

@helpers.accept_array_like_xarray_torch
def b_mode_image_filter(*args: itkt.ImageLike,  direction: int=..., frequency_filter=...,**kwargs)-> itkt.ImageSourceReturn:
    """Functional interface for BModeImageFilter"""
    import itk

    kwarg_typehints = { 'direction':direction,'frequency_filter':frequency_filter }
    specified_kwarg_typehints = { k:v for (k,v) in kwarg_typehints.items() if kwarg_typehints[k] is not ... }
    kwargs.update(specified_kwarg_typehints)

    instance = itk.BModeImageFilter.New(*args, **kwargs)
    return instance.__internal_call__()

def b_mode_image_filter_init_docstring():
    import itk
    from itk.support import template_class

    filter_class = itk.Ultrasound.BModeImageFilter
    b_mode_image_filter.process_object = filter_class
    is_template = isinstance(filter_class, template_class.itkTemplate)
    if is_template:
        filter_object = filter_class.values()[0]
    else:
        filter_object = filter_class

    b_mode_image_filter.__doc__ = filter_object.__doc__




