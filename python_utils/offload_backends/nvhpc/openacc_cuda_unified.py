# (C) Copyright 2026- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.


__all__ = ['NVHPCOpenACCUnifiedCUDA']

from offload_backends.nvhpc.openacc_cuda import NVHPCOpenACCCUDA


class NVHPCOpenACCUnifiedCUDA(NVHPCOpenACCCUDA):
    """NVHPC OpenACC/CUDA backend for full CUDA Unified Memory."""

    # Keep data-sharing attributes such as PRIVATE on compute constructs, but
    # omit clauses which request host/device allocation, mapping, or movement.
    _data_attributes = ['private']

    @classmethod
    def c_devptr_decl(cls, symbols):
        """Declare a pointer valid in the unified host/device address space."""

        return f"TYPE(C_PTR) :: {','.join(symbols)}"

    @classmethod
    def devptr_c_loc(cls, symbol):
        """Return the C address of unified or explicitly allocated memory."""

        return f"C_LOC({symbol})"

    @classmethod
    def host_data(cls, symbols):
        return ""

    @classmethod
    def end_host_data(cls):
        return ""

    @classmethod
    def create(cls, symbols):
        return ""

    @classmethod
    def delete(cls, symbols):
        return ""

    @classmethod
    def attach(cls, ptr):
        return ""

    @classmethod
    def detach(cls, ptr):
        return ""

    @classmethod
    def declare(cls, symbols):
        return ""

    @classmethod
    def update_device(cls, data):
        return ""

    @classmethod
    def update_host(cls, data):
        return ""

    @classmethod
    def data(cls, **kwargs):
        return ""

    @classmethod
    def end_data(cls):
        return ""

    @classmethod
    def data_deviceptr(cls, symbols):
        return ""

    @classmethod
    def end_data_deviceptr(cls):
        return ""

    @classmethod
    def memcpy_async_intf(cls):
        """C_PTR-compatible interfaces for contiguous CUDA copies."""

        intf = """
  INTEGER(C_INT) FUNCTION CUDA_MEMCPY_C (DST, SRC, SIZ, KDIR) BIND(C, NAME='cudaMemcpy')
    IMPORT :: C_PTR, C_SIZE_T, C_INT
    TYPE(C_PTR), VALUE :: DST, SRC
    INTEGER(C_SIZE_T), VALUE :: SIZ
    INTEGER(C_INT), VALUE :: KDIR
  END FUNCTION CUDA_MEMCPY_C

  INTEGER(C_INT) FUNCTION CUDA_MEMCPY_ASYNC_C (DST, SRC, SIZ, KDIR, STREAM) BIND(C, NAME='cudaMemcpyAsync')
    IMPORT :: C_PTR, C_SIZE_T, C_INT, C_INTPTR_T
    TYPE(C_PTR), VALUE :: DST, SRC
    INTEGER(C_SIZE_T), VALUE :: SIZ
    INTEGER(C_INT), VALUE :: KDIR
    INTEGER(C_INTPTR_T), VALUE :: STREAM
  END FUNCTION CUDA_MEMCPY_ASYNC_C
  """

        return intf.split('\n')

    @classmethod
    def memcpy_2D_intf(cls):
        """C_PTR-compatible interfaces for two-dimensional CUDA copies."""

        intf = """
  INTEGER(C_INT) FUNCTION CUDA_MEMCPY_2D_C (DST, DST_PITCH, SRC, SRC_PITCH, WIDTH, HEIGHT, KDIR) &
    BIND(C, NAME='cudaMemcpy2D')
    IMPORT :: C_PTR, C_SIZE_T, C_INT
    TYPE(C_PTR), VALUE :: DST, SRC
    INTEGER(C_SIZE_T), VALUE :: DST_PITCH, SRC_PITCH, WIDTH, HEIGHT
    INTEGER(C_INT), VALUE :: KDIR
  END FUNCTION CUDA_MEMCPY_2D_C

  INTEGER(C_INT) FUNCTION CUDA_MEMCPY_2D_ASYNC_C (DST, DST_PITCH, SRC, SRC_PITCH, WIDTH, HEIGHT, KDIR, STREAM) &
    BIND(C, NAME='cudaMemcpy2DAsync')
    IMPORT :: C_PTR, C_SIZE_T, C_INT, C_INTPTR_T
    TYPE(C_PTR), VALUE :: DST, SRC
    INTEGER(C_SIZE_T), VALUE :: DST_PITCH, SRC_PITCH, WIDTH, HEIGHT
    INTEGER(C_INT), VALUE :: KDIR
    INTEGER(C_INTPTR_T), VALUE :: STREAM
  END FUNCTION CUDA_MEMCPY_2D_ASYNC_C
  """

        return intf.split('\n')

    @classmethod
    def memcpy_to_device(cls, dev, host_ptr, size, return_val="ISTAT", **kwargs):
        return (f"{return_val} = CUDA_MEMCPY_C({dev}, C_LOC({host_ptr}), {size}, "
                "CUDAMEMCPYDEFAULT)")

    @classmethod
    def memcpy_to_device_async(cls, dev, host_ptr, size, stream, return_val="ISTAT", **kwargs):
        return (f"{return_val} = CUDA_MEMCPY_ASYNC_C({dev}, C_LOC({host_ptr}), {size}, "
                f"CUDAMEMCPYDEFAULT, {stream})")

    @classmethod
    def memcpy_from_device(cls, dev, host_ptr, size, return_val="ISTAT", **kwargs):
        return (f"{return_val} = CUDA_MEMCPY_C(C_LOC({host_ptr}), {dev}, {size}, "
                "CUDAMEMCPYDEFAULT)")

    @classmethod
    def memcpy_from_device_async(cls, dev, host_ptr, size, stream, return_val="ISTAT", **kwargs):
        return (f"{return_val} = CUDA_MEMCPY_ASYNC_C(C_LOC({host_ptr}), {dev}, {size}, "
                f"CUDAMEMCPYDEFAULT, {stream})")

    @classmethod
    def memcpy_2D(cls, src, src_pitch, dst, dst_pitch, width, height, kdir, return_val="ISTAT"):
        return (f"{return_val} = CUDA_MEMCPY_2D_C({dst}, {dst_pitch}, {src}, {src_pitch}, "
                f"{width}, {height}, CUDAMEMCPYDEFAULT)")

    @classmethod
    def memcpy_2D_async(cls, src, src_pitch, dst, dst_pitch, width, height, stream, kdir,
                        return_val="ISTAT"):
        return (f"{return_val} = CUDA_MEMCPY_2D_ASYNC_C({dst}, {dst_pitch}, {src}, {src_pitch}, "
                f"{width}, {height}, CUDAMEMCPYDEFAULT, {stream})")
