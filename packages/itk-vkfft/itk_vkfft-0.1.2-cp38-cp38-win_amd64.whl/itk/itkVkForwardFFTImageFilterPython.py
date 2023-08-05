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
    from . import _itkVkForwardFFTImageFilterPython
else:
    import _itkVkForwardFFTImageFilterPython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkVkForwardFFTImageFilterPython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkVkForwardFFTImageFilterPython.SWIG_PyStaticMethod_New

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
import itk.itkForwardFFTImageFilterPython
import itk.itkImageToImageFilterBPython
import itk.itkImageRegionPython
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

def itkVkForwardFFTImageFilterID2_New():
    return itkVkForwardFFTImageFilterID2.New()

class itkVkForwardFFTImageFilterID2(itk.itkForwardFFTImageFilterPython.itkForwardFFTImageFilterID2ICD2):
    r"""Proxy of C++ itkVkForwardFFTImageFilterID2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterID2___New_orig__)
    Clone = _swig_new_instance_method(_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterID2_Clone)
    GetDeviceID = _swig_new_instance_method(_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterID2_GetDeviceID)
    SetDeviceID = _swig_new_instance_method(_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterID2_SetDeviceID)
    __swig_destroy__ = _itkVkForwardFFTImageFilterPython.delete_itkVkForwardFFTImageFilterID2
    cast = _swig_new_static_method(_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterID2_cast)

    def New(*args, **kargs):
        """New() -> itkVkForwardFFTImageFilterID2

        Create a new object of the class itkVkForwardFFTImageFilterID2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkVkForwardFFTImageFilterID2.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkVkForwardFFTImageFilterID2.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkVkForwardFFTImageFilterID2.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkVkForwardFFTImageFilterID2 in _itkVkForwardFFTImageFilterPython:
_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterID2_swigregister(itkVkForwardFFTImageFilterID2)
itkVkForwardFFTImageFilterID2___New_orig__ = _itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterID2___New_orig__
itkVkForwardFFTImageFilterID2_cast = _itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterID2_cast


def itkVkForwardFFTImageFilterID3_New():
    return itkVkForwardFFTImageFilterID3.New()

class itkVkForwardFFTImageFilterID3(itk.itkForwardFFTImageFilterPython.itkForwardFFTImageFilterID3ICD3):
    r"""Proxy of C++ itkVkForwardFFTImageFilterID3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterID3___New_orig__)
    Clone = _swig_new_instance_method(_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterID3_Clone)
    GetDeviceID = _swig_new_instance_method(_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterID3_GetDeviceID)
    SetDeviceID = _swig_new_instance_method(_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterID3_SetDeviceID)
    __swig_destroy__ = _itkVkForwardFFTImageFilterPython.delete_itkVkForwardFFTImageFilterID3
    cast = _swig_new_static_method(_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterID3_cast)

    def New(*args, **kargs):
        """New() -> itkVkForwardFFTImageFilterID3

        Create a new object of the class itkVkForwardFFTImageFilterID3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkVkForwardFFTImageFilterID3.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkVkForwardFFTImageFilterID3.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkVkForwardFFTImageFilterID3.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkVkForwardFFTImageFilterID3 in _itkVkForwardFFTImageFilterPython:
_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterID3_swigregister(itkVkForwardFFTImageFilterID3)
itkVkForwardFFTImageFilterID3___New_orig__ = _itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterID3___New_orig__
itkVkForwardFFTImageFilterID3_cast = _itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterID3_cast


def itkVkForwardFFTImageFilterIF2_New():
    return itkVkForwardFFTImageFilterIF2.New()

class itkVkForwardFFTImageFilterIF2(itk.itkForwardFFTImageFilterPython.itkForwardFFTImageFilterIF2ICF2):
    r"""Proxy of C++ itkVkForwardFFTImageFilterIF2 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterIF2___New_orig__)
    Clone = _swig_new_instance_method(_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterIF2_Clone)
    GetDeviceID = _swig_new_instance_method(_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterIF2_GetDeviceID)
    SetDeviceID = _swig_new_instance_method(_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterIF2_SetDeviceID)
    __swig_destroy__ = _itkVkForwardFFTImageFilterPython.delete_itkVkForwardFFTImageFilterIF2
    cast = _swig_new_static_method(_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterIF2_cast)

    def New(*args, **kargs):
        """New() -> itkVkForwardFFTImageFilterIF2

        Create a new object of the class itkVkForwardFFTImageFilterIF2 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkVkForwardFFTImageFilterIF2.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkVkForwardFFTImageFilterIF2.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkVkForwardFFTImageFilterIF2.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkVkForwardFFTImageFilterIF2 in _itkVkForwardFFTImageFilterPython:
_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterIF2_swigregister(itkVkForwardFFTImageFilterIF2)
itkVkForwardFFTImageFilterIF2___New_orig__ = _itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterIF2___New_orig__
itkVkForwardFFTImageFilterIF2_cast = _itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterIF2_cast


def itkVkForwardFFTImageFilterIF3_New():
    return itkVkForwardFFTImageFilterIF3.New()

class itkVkForwardFFTImageFilterIF3(itk.itkForwardFFTImageFilterPython.itkForwardFFTImageFilterIF3ICF3):
    r"""Proxy of C++ itkVkForwardFFTImageFilterIF3 class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __New_orig__ = _swig_new_static_method(_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterIF3___New_orig__)
    Clone = _swig_new_instance_method(_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterIF3_Clone)
    GetDeviceID = _swig_new_instance_method(_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterIF3_GetDeviceID)
    SetDeviceID = _swig_new_instance_method(_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterIF3_SetDeviceID)
    __swig_destroy__ = _itkVkForwardFFTImageFilterPython.delete_itkVkForwardFFTImageFilterIF3
    cast = _swig_new_static_method(_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterIF3_cast)

    def New(*args, **kargs):
        """New() -> itkVkForwardFFTImageFilterIF3

        Create a new object of the class itkVkForwardFFTImageFilterIF3 and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkVkForwardFFTImageFilterIF3.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkVkForwardFFTImageFilterIF3.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkVkForwardFFTImageFilterIF3.__New_orig__()
        from itk.support import template_class
        template_class.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkVkForwardFFTImageFilterIF3 in _itkVkForwardFFTImageFilterPython:
_itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterIF3_swigregister(itkVkForwardFFTImageFilterIF3)
itkVkForwardFFTImageFilterIF3___New_orig__ = _itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterIF3___New_orig__
itkVkForwardFFTImageFilterIF3_cast = _itkVkForwardFFTImageFilterPython.itkVkForwardFFTImageFilterIF3_cast


from itk.support import helpers
import itk.support.types as itkt
from typing import Sequence, Tuple, Union

@helpers.accept_array_like_xarray_torch
def vk_forward_fft_image_filter(*args: itkt.ImageLike,  device_id: int=...,**kwargs)-> itkt.ImageSourceReturn:
    """Functional interface for VkForwardFFTImageFilter"""
    import itk

    kwarg_typehints = { 'device_id':device_id }
    specified_kwarg_typehints = { k:v for (k,v) in kwarg_typehints.items() if kwarg_typehints[k] is not ... }
    kwargs.update(specified_kwarg_typehints)

    instance = itk.VkForwardFFTImageFilter.New(*args, **kwargs)
    return instance.__internal_call__()

def vk_forward_fft_image_filter_init_docstring():
    import itk
    from itk.support import template_class

    filter_class = itk.VkFFTBackend.VkForwardFFTImageFilter
    vk_forward_fft_image_filter.process_object = filter_class
    is_template = isinstance(filter_class, template_class.itkTemplate)
    if is_template:
        filter_object = filter_class.values()[0]
    else:
        filter_object = filter_class

    vk_forward_fft_image_filter.__doc__ = filter_object.__doc__




