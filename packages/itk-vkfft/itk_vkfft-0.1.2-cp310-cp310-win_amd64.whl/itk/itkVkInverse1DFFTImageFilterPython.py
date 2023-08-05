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
    from . import _itkVkInverse1DFFTImageFilterPython
else:
    import _itkVkInverse1DFFTImageFilterPython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkVkInverse1DFFTImageFilterPython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkVkInverse1DFFTImageFilterPython.SWIG_PyStaticMethod_New

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
import itk.itkInverse1DFFTImageFilterPython
import itk.itkImageToImageFilterBPython
import itk.itkImageToImageFilterCommonPython
import itk.pyBasePython
import itk.itkImageSourcePython
import itk.itkImagePython
import itk.itkSizePython
import itk.itkIndexPython
import itk.itkOffsetPython
import itk.itkMatrixPython
import itk.itkCovariantVectorPython
import itk.vnl_vector_refPython
import itk.stdcomplexPython
import itk.vnl_vectorPython
import itk.vnl_matrixPython
import itk.itkFixedArrayPython
import itk.itkVectorPython
import itk.vnl_matrix_fixedPython
import itk.itkPointPython
import itk.ITKCommonBasePython
import itk.itkImageRegionPython
import itk.itkSymmetricSecondRankTensorPython
import itk.itkRGBPixelPython
import itk.itkRGBAPixelPython
import itk.itkImageSourceCommonPython
import itk.itkVectorImagePython
import itk.itkVariableLengthVectorPython

def itkVkInverse1DFFTImageFilterICD2_New():
    return itkVkInverse1DFFTImageFilterICD2.New()

class itkVkInverse1DFFTImageFilterICD2(itk.itkInverse1DFFTImageFilterPython.itkInverse1DFFTImageFilterICD2):
    r"""Proxy of C++ itkVkInverse1DFFTImageFilterICD2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICD2___New_orig__)
    Clone = _swig_new_instance_method(_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICD2_Clone)
    GetDeviceID = _swig_new_instance_method(_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICD2_GetDeviceID)
    SetDeviceID = _swig_new_instance_method(_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICD2_SetDeviceID)
    __swig_destroy__ = _itkVkInverse1DFFTImageFilterPython.delete_itkVkInverse1DFFTImageFilterICD2
    cast = _swig_new_static_method(_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICD2_cast)

    def New(*args, **kargs):
        """New() -> itkVkInverse1DFFTImageFilterICD2

        Create a new object of the class itkVkInverse1DFFTImageFilterICD2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkVkInverse1DFFTImageFilterICD2.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkVkInverse1DFFTImageFilterICD2.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkVkInverse1DFFTImageFilterICD2.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkVkInverse1DFFTImageFilterICD2 in _itkVkInverse1DFFTImageFilterPython:
_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICD2_swigregister(itkVkInverse1DFFTImageFilterICD2)
itkVkInverse1DFFTImageFilterICD2___New_orig__ = _itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICD2___New_orig__
itkVkInverse1DFFTImageFilterICD2_cast = _itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICD2_cast


def itkVkInverse1DFFTImageFilterICD3_New():
    return itkVkInverse1DFFTImageFilterICD3.New()

class itkVkInverse1DFFTImageFilterICD3(itk.itkInverse1DFFTImageFilterPython.itkInverse1DFFTImageFilterICD3):
    r"""Proxy of C++ itkVkInverse1DFFTImageFilterICD3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICD3___New_orig__)
    Clone = _swig_new_instance_method(_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICD3_Clone)
    GetDeviceID = _swig_new_instance_method(_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICD3_GetDeviceID)
    SetDeviceID = _swig_new_instance_method(_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICD3_SetDeviceID)
    __swig_destroy__ = _itkVkInverse1DFFTImageFilterPython.delete_itkVkInverse1DFFTImageFilterICD3
    cast = _swig_new_static_method(_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICD3_cast)

    def New(*args, **kargs):
        """New() -> itkVkInverse1DFFTImageFilterICD3

        Create a new object of the class itkVkInverse1DFFTImageFilterICD3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkVkInverse1DFFTImageFilterICD3.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkVkInverse1DFFTImageFilterICD3.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkVkInverse1DFFTImageFilterICD3.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkVkInverse1DFFTImageFilterICD3 in _itkVkInverse1DFFTImageFilterPython:
_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICD3_swigregister(itkVkInverse1DFFTImageFilterICD3)
itkVkInverse1DFFTImageFilterICD3___New_orig__ = _itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICD3___New_orig__
itkVkInverse1DFFTImageFilterICD3_cast = _itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICD3_cast


def itkVkInverse1DFFTImageFilterICF2_New():
    return itkVkInverse1DFFTImageFilterICF2.New()

class itkVkInverse1DFFTImageFilterICF2(itk.itkInverse1DFFTImageFilterPython.itkInverse1DFFTImageFilterICF2):
    r"""Proxy of C++ itkVkInverse1DFFTImageFilterICF2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICF2___New_orig__)
    Clone = _swig_new_instance_method(_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICF2_Clone)
    GetDeviceID = _swig_new_instance_method(_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICF2_GetDeviceID)
    SetDeviceID = _swig_new_instance_method(_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICF2_SetDeviceID)
    __swig_destroy__ = _itkVkInverse1DFFTImageFilterPython.delete_itkVkInverse1DFFTImageFilterICF2
    cast = _swig_new_static_method(_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICF2_cast)

    def New(*args, **kargs):
        """New() -> itkVkInverse1DFFTImageFilterICF2

        Create a new object of the class itkVkInverse1DFFTImageFilterICF2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkVkInverse1DFFTImageFilterICF2.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkVkInverse1DFFTImageFilterICF2.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkVkInverse1DFFTImageFilterICF2.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkVkInverse1DFFTImageFilterICF2 in _itkVkInverse1DFFTImageFilterPython:
_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICF2_swigregister(itkVkInverse1DFFTImageFilterICF2)
itkVkInverse1DFFTImageFilterICF2___New_orig__ = _itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICF2___New_orig__
itkVkInverse1DFFTImageFilterICF2_cast = _itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICF2_cast


def itkVkInverse1DFFTImageFilterICF3_New():
    return itkVkInverse1DFFTImageFilterICF3.New()

class itkVkInverse1DFFTImageFilterICF3(itk.itkInverse1DFFTImageFilterPython.itkInverse1DFFTImageFilterICF3):
    r"""Proxy of C++ itkVkInverse1DFFTImageFilterICF3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICF3___New_orig__)
    Clone = _swig_new_instance_method(_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICF3_Clone)
    GetDeviceID = _swig_new_instance_method(_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICF3_GetDeviceID)
    SetDeviceID = _swig_new_instance_method(_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICF3_SetDeviceID)
    __swig_destroy__ = _itkVkInverse1DFFTImageFilterPython.delete_itkVkInverse1DFFTImageFilterICF3
    cast = _swig_new_static_method(_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICF3_cast)

    def New(*args, **kargs):
        """New() -> itkVkInverse1DFFTImageFilterICF3

        Create a new object of the class itkVkInverse1DFFTImageFilterICF3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkVkInverse1DFFTImageFilterICF3.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkVkInverse1DFFTImageFilterICF3.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkVkInverse1DFFTImageFilterICF3.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkVkInverse1DFFTImageFilterICF3 in _itkVkInverse1DFFTImageFilterPython:
_itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICF3_swigregister(itkVkInverse1DFFTImageFilterICF3)
itkVkInverse1DFFTImageFilterICF3___New_orig__ = _itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICF3___New_orig__
itkVkInverse1DFFTImageFilterICF3_cast = _itkVkInverse1DFFTImageFilterPython.itkVkInverse1DFFTImageFilterICF3_cast


from itk.support import helpers
import itk.support.types as itkt
from typing import Sequence, Tuple, Union

@helpers.accept_array_like_xarray_torch
def vk_inverse1_dfft_image_filter(*args: itkt.ImageLike,  device_id: int=..., direction: int=...,**kwargs)-> itkt.ImageSourceReturn:
    """Functional interface for VkInverse1DFFTImageFilter"""
    import itk

    kwarg_typehints = { 'device_id':device_id,'direction':direction }
    specified_kwarg_typehints = { k:v for (k,v) in kwarg_typehints.items() if kwarg_typehints[k] is not ... }
    kwargs.update(specified_kwarg_typehints)

    instance = itk.VkInverse1DFFTImageFilter.New(*args, **kwargs)
    return instance.__internal_call__()

def vk_inverse1_dfft_image_filter_init_docstring():
    import itk
    from itk.support import template_class

    filter_class = itk.VkFFTBackend.VkInverse1DFFTImageFilter
    vk_inverse1_dfft_image_filter.process_object = filter_class
    is_template = isinstance(filter_class, template_class.itkTemplate)
    if is_template:
        filter_object = filter_class.values()[0]
    else:
        filter_object = filter_class

    vk_inverse1_dfft_image_filter.__doc__ = filter_object.__doc__




