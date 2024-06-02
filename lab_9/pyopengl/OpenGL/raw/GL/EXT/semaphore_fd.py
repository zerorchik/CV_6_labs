'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_EXT_semaphore_fd'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_EXT_semaphore_fd',error_checker=_errors._error_checker)
GL_HANDLE_TYPE_OPAQUE_FD_EXT=_C('GL_HANDLE_TYPE_OPAQUE_FD_EXT',0x9586)
@_f
@_p.types(None,_cs.GLuint,_cs.GLenum,_cs.GLint)
def glImportSemaphoreFdEXT(semaphore,handleType,fd):pass