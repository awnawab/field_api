set(CMAKE_C_COMPILER nvc)
set(CMAKE_Fortran_COMPILER nvfortran)
set(CMAKE_CXX_COMPILER nvc++)

set( OpenACC_Fortran_FLAGS "-acc=gpu -gpu=cc90,lineinfo,fastmath,rdc" )

if(NOT DEFINED CMAKE_CUDA_ARCHITECTURES)
  set(CMAKE_CUDA_ARCHITECTURES 90)
endif()
