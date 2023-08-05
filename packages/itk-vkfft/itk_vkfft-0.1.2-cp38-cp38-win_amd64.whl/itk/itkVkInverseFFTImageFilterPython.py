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
    from . import _itkVkInverseFFTImageFilterPython
else:
    import _itkVkInverseFFTImageFilterPython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkVkInverseFFTImageFilterPython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkVkInverseFFTImageFilterPython.SWIG_PyStaticMethod_New

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
import itk.itkInverseFFTImageFilterPython
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

def itkVkInverseFFTImageFilterICD2_New():
    return itkVkInverseFFTImageFilterICD2.New()

class itkVkInverseFFTImageFilterICD2(itk.itkInverseFFTImageFilterPython.itkInverseFFTImageFilterICD2ID2):
    r"""Proxy of C++ itkVkInverseFFTImageFilterICD2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICD2___New_orig__)
    Clone = _swig_new_instance_method(_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICD2_Clone)
    GetDeviceID = _swig_new_instance_method(_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICD2_GetDeviceID)
    SetDeviceID = _swig_new_instance_method(_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICD2_SetDeviceID)
    __swig_destroy__ = _itkVkInverseFFTImageFilterPython.delete_itkVkInverseFFTImageFilterICD2
    cast = _swig_new_static_method(_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICD2_cast)

    def New(*args, **kargs):
        """New() -> itkVkInverseFFTImageFilterICD2

        Create a new object of the class itkVkInverseFFTImageFilterICD2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkVkInverseFFTImageFilterICD2.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkVkInverseFFTImageFilterICD2.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkVkInverseFFTImageFilterICD2.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkVkInverseFFTImageFilterICD2 in _itkVkInverseFFTImageFilterPython:
_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICD2_swigregister(itkVkInverseFFTImageFilterICD2)
itkVkInverseFFTImageFilterICD2___New_orig__ = _itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICD2___New_orig__
itkVkInverseFFTImageFilterICD2_cast = _itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICD2_cast


def itkVkInverseFFTImageFilterICD3_New():
    return itkVkInverseFFTImageFilterICD3.New()

class itkVkInverseFFTImageFilterICD3(itk.itkInverseFFTImageFilterPython.itkInverseFFTImageFilterICD3ID3):
    r"""Proxy of C++ itkVkInverseFFTImageFilterICD3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICD3___New_orig__)
    Clone = _swig_new_instance_method(_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICD3_Clone)
    GetDeviceID = _swig_new_instance_method(_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICD3_GetDeviceID)
    SetDeviceID = _swig_new_instance_method(_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICD3_SetDeviceID)
    __swig_destroy__ = _itkVkInverseFFTImageFilterPython.delete_itkVkInverseFFTImageFilterICD3
    cast = _swig_new_static_method(_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICD3_cast)

    def New(*args, **kargs):
        """New() -> itkVkInverseFFTImageFilterICD3

        Create a new object of the class itkVkInverseFFTImageFilterICD3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkVkInverseFFTImageFilterICD3.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkVkInverseFFTImageFilterICD3.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkVkInverseFFTImageFilterICD3.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkVkInverseFFTImageFilterICD3 in _itkVkInverseFFTImageFilterPython:
_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICD3_swigregister(itkVkInverseFFTImageFilterICD3)
itkVkInverseFFTImageFilterICD3___New_orig__ = _itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICD3___New_orig__
itkVkInverseFFTImageFilterICD3_cast = _itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICD3_cast


def itkVkInverseFFTImageFilterICF2_New():
    return itkVkInverseFFTImageFilterICF2.New()

class itkVkInverseFFTImageFilterICF2(itk.itkInverseFFTImageFilterPython.itkInverseFFTImageFilterICF2IF2):
    r"""Proxy of C++ itkVkInverseFFTImageFilterICF2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICF2___New_orig__)
    Clone = _swig_new_instance_method(_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICF2_Clone)
    GetDeviceID = _swig_new_instance_method(_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICF2_GetDeviceID)
    SetDeviceID = _swig_new_instance_method(_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICF2_SetDeviceID)
    __swig_destroy__ = _itkVkInverseFFTImageFilterPython.delete_itkVkInverseFFTImageFilterICF2
    cast = _swig_new_static_method(_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICF2_cast)

    def New(*args, **kargs):
        """New() -> itkVkInverseFFTImageFilterICF2

        Create a new object of the class itkVkInverseFFTImageFilterICF2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkVkInverseFFTImageFilterICF2.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkVkInverseFFTImageFilterICF2.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkVkInverseFFTImageFilterICF2.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkVkInverseFFTImageFilterICF2 in _itkVkInverseFFTImageFilterPython:
_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICF2_swigregister(itkVkInverseFFTImageFilterICF2)
itkVkInverseFFTImageFilterICF2___New_orig__ = _itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICF2___New_orig__
itkVkInverseFFTImageFilterICF2_cast = _itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICF2_cast


def itkVkInverseFFTImageFilterICF3_New():
    return itkVkInverseFFTImageFilterICF3.New()

class itkVkInverseFFTImageFilterICF3(itk.itkInverseFFTImageFilterPython.itkInverseFFTImageFilterICF3IF3):
    r"""Proxy of C++ itkVkInverseFFTImageFilterICF3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICF3___New_orig__)
    Clone = _swig_new_instance_method(_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICF3_Clone)
    GetDeviceID = _swig_new_instance_method(_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICF3_GetDeviceID)
    SetDeviceID = _swig_new_instance_method(_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICF3_SetDeviceID)
    __swig_destroy__ = _itkVkInverseFFTImageFilterPython.delete_itkVkInverseFFTImageFilterICF3
    cast = _swig_new_static_method(_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICF3_cast)

    def New(*args, **kargs):
        """New() -> itkVkInverseFFTImageFilterICF3

        Create a new object of the class itkVkInverseFFTImageFilterICF3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkVkInverseFFTImageFilterICF3.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkVkInverseFFTImageFilterICF3.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkVkInverseFFTImageFilterICF3.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkVkInverseFFTImageFilterICF3 in _itkVkInverseFFTImageFilterPython:
_itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICF3_swigregister(itkVkInverseFFTImageFilterICF3)
itkVkInverseFFTImageFilterICF3___New_orig__ = _itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICF3___New_orig__
itkVkInverseFFTImageFilterICF3_cast = _itkVkInverseFFTImageFilterPython.itkVkInverseFFTImageFilterICF3_cast


from itk.support import helpers
import itk.support.types as itkt
from typing import Sequence, Tuple, Union

@helpers.accept_array_like_xarray_torch
def vk_inverse_fft_image_filter(*args: itkt.ImageLike,  device_id: int=...,**kwargs)-> itkt.ImageSourceReturn:
    """Functional interface for VkInverseFFTImageFilter"""
    import itk

    kwarg_typehints = { 'device_id':device_id }
    specified_kwarg_typehints = { k:v for (k,v) in kwarg_typehints.items() if kwarg_typehints[k] is not ... }
    kwargs.update(specified_kwarg_typehints)

    instance = itk.VkInverseFFTImageFilter.New(*args, **kwargs)
    return instance.__internal_call__()

def vk_inverse_fft_image_filter_init_docstring():
    import itk
    from itk.support import template_class

    filter_class = itk.VkFFTBackend.VkInverseFFTImageFilter
    vk_inverse_fft_image_filter.process_object = filter_class
    is_template = isinstance(filter_class, template_class.itkTemplate)
    if is_template:
        filter_object = filter_class.values()[0]
    else:
        filter_object = filter_class

    vk_inverse_fft_image_filter.__doc__ = filter_object.__doc__




