# This file was automatically generated by SWIG (http://www.swig.org).
# Version 4.0.2
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.


import collections

from sys import version_info as _version_info
if _version_info < (3, 7, 0):
    raise RuntimeError("Python 3.7 or later required")


from . import _VkFFTBackendPython



from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError("Python 2.7 or later required")

# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _itkVkComplexToComplex1DFFTImageFilterPython
else:
    import _itkVkComplexToComplex1DFFTImageFilterPython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkVkComplexToComplex1DFFTImageFilterPython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkVkComplexToComplex1DFFTImageFilterPython.SWIG_PyStaticMethod_New

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
import itk.itkComplexToComplex1DFFTImageFilterPython
import itk.itkImageToImageFilterBPython
import itk.itkImageRegionPython
import itk.itkIndexPython
import itk.itkSizePython
import itk.itkOffsetPython
import itk.itkImagePython
import itk.stdcomplexPython
import itk.itkFixedArrayPython
import itk.itkRGBPixelPython
import itk.itkPointPython
import itk.itkVectorPython
import itk.vnl_vector_refPython
import itk.vnl_vectorPython
import itk.vnl_matrixPython
import itk.itkSymmetricSecondRankTensorPython
import itk.itkMatrixPython
import itk.itkCovariantVectorPython
import itk.vnl_matrix_fixedPython
import itk.itkRGBAPixelPython
import itk.itkImageSourcePython
import itk.itkVectorImagePython
import itk.itkVariableLengthVectorPython
import itk.itkImageSourceCommonPython
import itk.itkImageToImageFilterCommonPython

def itkVkComplexToComplex1DFFTImageFilterICD2_New():
    return itkVkComplexToComplex1DFFTImageFilterICD2.New()

class itkVkComplexToComplex1DFFTImageFilterICD2(itk.itkComplexToComplex1DFFTImageFilterPython.itkComplexToComplex1DFFTImageFilterICD2):
    r"""Proxy of C++ itkVkComplexToComplex1DFFTImageFilterICD2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICD2___New_orig__)
    Clone = _swig_new_instance_method(_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICD2_Clone)
    GetDeviceID = _swig_new_instance_method(_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICD2_GetDeviceID)
    SetDeviceID = _swig_new_instance_method(_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICD2_SetDeviceID)
    __swig_destroy__ = _itkVkComplexToComplex1DFFTImageFilterPython.delete_itkVkComplexToComplex1DFFTImageFilterICD2
    cast = _swig_new_static_method(_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICD2_cast)

    def New(*args, **kargs):
        """New() -> itkVkComplexToComplex1DFFTImageFilterICD2

        Create a new object of the class itkVkComplexToComplex1DFFTImageFilterICD2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkVkComplexToComplex1DFFTImageFilterICD2.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkVkComplexToComplex1DFFTImageFilterICD2.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkVkComplexToComplex1DFFTImageFilterICD2.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkVkComplexToComplex1DFFTImageFilterICD2 in _itkVkComplexToComplex1DFFTImageFilterPython:
_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICD2_swigregister(itkVkComplexToComplex1DFFTImageFilterICD2)
itkVkComplexToComplex1DFFTImageFilterICD2___New_orig__ = _itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICD2___New_orig__
itkVkComplexToComplex1DFFTImageFilterICD2_cast = _itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICD2_cast


def itkVkComplexToComplex1DFFTImageFilterICD3_New():
    return itkVkComplexToComplex1DFFTImageFilterICD3.New()

class itkVkComplexToComplex1DFFTImageFilterICD3(itk.itkComplexToComplex1DFFTImageFilterPython.itkComplexToComplex1DFFTImageFilterICD3):
    r"""Proxy of C++ itkVkComplexToComplex1DFFTImageFilterICD3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICD3___New_orig__)
    Clone = _swig_new_instance_method(_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICD3_Clone)
    GetDeviceID = _swig_new_instance_method(_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICD3_GetDeviceID)
    SetDeviceID = _swig_new_instance_method(_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICD3_SetDeviceID)
    __swig_destroy__ = _itkVkComplexToComplex1DFFTImageFilterPython.delete_itkVkComplexToComplex1DFFTImageFilterICD3
    cast = _swig_new_static_method(_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICD3_cast)

    def New(*args, **kargs):
        """New() -> itkVkComplexToComplex1DFFTImageFilterICD3

        Create a new object of the class itkVkComplexToComplex1DFFTImageFilterICD3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkVkComplexToComplex1DFFTImageFilterICD3.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkVkComplexToComplex1DFFTImageFilterICD3.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkVkComplexToComplex1DFFTImageFilterICD3.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkVkComplexToComplex1DFFTImageFilterICD3 in _itkVkComplexToComplex1DFFTImageFilterPython:
_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICD3_swigregister(itkVkComplexToComplex1DFFTImageFilterICD3)
itkVkComplexToComplex1DFFTImageFilterICD3___New_orig__ = _itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICD3___New_orig__
itkVkComplexToComplex1DFFTImageFilterICD3_cast = _itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICD3_cast


def itkVkComplexToComplex1DFFTImageFilterICF2_New():
    return itkVkComplexToComplex1DFFTImageFilterICF2.New()

class itkVkComplexToComplex1DFFTImageFilterICF2(itk.itkComplexToComplex1DFFTImageFilterPython.itkComplexToComplex1DFFTImageFilterICF2):
    r"""Proxy of C++ itkVkComplexToComplex1DFFTImageFilterICF2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICF2___New_orig__)
    Clone = _swig_new_instance_method(_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICF2_Clone)
    GetDeviceID = _swig_new_instance_method(_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICF2_GetDeviceID)
    SetDeviceID = _swig_new_instance_method(_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICF2_SetDeviceID)
    __swig_destroy__ = _itkVkComplexToComplex1DFFTImageFilterPython.delete_itkVkComplexToComplex1DFFTImageFilterICF2
    cast = _swig_new_static_method(_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICF2_cast)

    def New(*args, **kargs):
        """New() -> itkVkComplexToComplex1DFFTImageFilterICF2

        Create a new object of the class itkVkComplexToComplex1DFFTImageFilterICF2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkVkComplexToComplex1DFFTImageFilterICF2.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkVkComplexToComplex1DFFTImageFilterICF2.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkVkComplexToComplex1DFFTImageFilterICF2.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkVkComplexToComplex1DFFTImageFilterICF2 in _itkVkComplexToComplex1DFFTImageFilterPython:
_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICF2_swigregister(itkVkComplexToComplex1DFFTImageFilterICF2)
itkVkComplexToComplex1DFFTImageFilterICF2___New_orig__ = _itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICF2___New_orig__
itkVkComplexToComplex1DFFTImageFilterICF2_cast = _itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICF2_cast


def itkVkComplexToComplex1DFFTImageFilterICF3_New():
    return itkVkComplexToComplex1DFFTImageFilterICF3.New()

class itkVkComplexToComplex1DFFTImageFilterICF3(itk.itkComplexToComplex1DFFTImageFilterPython.itkComplexToComplex1DFFTImageFilterICF3):
    r"""Proxy of C++ itkVkComplexToComplex1DFFTImageFilterICF3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICF3___New_orig__)
    Clone = _swig_new_instance_method(_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICF3_Clone)
    GetDeviceID = _swig_new_instance_method(_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICF3_GetDeviceID)
    SetDeviceID = _swig_new_instance_method(_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICF3_SetDeviceID)
    __swig_destroy__ = _itkVkComplexToComplex1DFFTImageFilterPython.delete_itkVkComplexToComplex1DFFTImageFilterICF3
    cast = _swig_new_static_method(_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICF3_cast)

    def New(*args, **kargs):
        """New() -> itkVkComplexToComplex1DFFTImageFilterICF3

        Create a new object of the class itkVkComplexToComplex1DFFTImageFilterICF3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkVkComplexToComplex1DFFTImageFilterICF3.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkVkComplexToComplex1DFFTImageFilterICF3.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkVkComplexToComplex1DFFTImageFilterICF3.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkVkComplexToComplex1DFFTImageFilterICF3 in _itkVkComplexToComplex1DFFTImageFilterPython:
_itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICF3_swigregister(itkVkComplexToComplex1DFFTImageFilterICF3)
itkVkComplexToComplex1DFFTImageFilterICF3___New_orig__ = _itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICF3___New_orig__
itkVkComplexToComplex1DFFTImageFilterICF3_cast = _itkVkComplexToComplex1DFFTImageFilterPython.itkVkComplexToComplex1DFFTImageFilterICF3_cast


from itk.support import helpers
import itk.support.types as itkt
from typing import Sequence, Tuple, Union

@helpers.accept_array_like_xarray_torch
def vk_complex_to_complex1_dfft_image_filter(*args: itkt.ImageLike,  device_id: int=..., transform_direction=..., direction: int=...,**kwargs)-> itkt.ImageSourceReturn:
    """Functional interface for VkComplexToComplex1DFFTImageFilter"""
    import itk

    kwarg_typehints = { 'device_id':device_id,'transform_direction':transform_direction,'direction':direction }
    specified_kwarg_typehints = { k:v for (k,v) in kwarg_typehints.items() if kwarg_typehints[k] is not ... }
    kwargs.update(specified_kwarg_typehints)

    instance = itk.VkComplexToComplex1DFFTImageFilter.New(*args, **kwargs)
    return instance.__internal_call__()

def vk_complex_to_complex1_dfft_image_filter_init_docstring():
    import itk
    from itk.support import template_class

    filter_class = itk.VkFFTBackend.VkComplexToComplex1DFFTImageFilter
    vk_complex_to_complex1_dfft_image_filter.process_object = filter_class
    is_template = isinstance(filter_class, template_class.itkTemplate)
    if is_template:
        filter_object = filter_class.values()[0]
    else:
        filter_object = filter_class

    vk_complex_to_complex1_dfft_image_filter.__doc__ = filter_object.__doc__




