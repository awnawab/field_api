! (C) Copyright 2026- ECMWF.
! (C) Copyright 2026- Meteo-France.
!
! This software is licensed under the terms of the Apache Licence Version 2.0
! which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
! In applying this licence, ECMWF does not waive the privileges and immunities
! granted to it by virtue of its status as an intergovernmental organisation
! nor does it submit to any jurisdiction.

PROGRAM IS_MAP_DEVPTR_BY_DEFAULT

  USE FIELD_DEFAULTS_MODULE, ONLY : INIT_MAP_DEVPTR
  USE FIELD_ABORT_MODULE

  IMPLICIT NONE

  WRITE (*, *) "MAP DEVICE POINTERS BY DEFAULT", INIT_MAP_DEVPTR

  IF (.NOT. INIT_MAP_DEVPTR) THEN
    ! This is not a real error; it lets CTest verify the configured default.
    CALL FIELD_ABORT ("DEVICE POINTER MAPPING IS DISABLED BY DEFAULT")
  ENDIF

END PROGRAM IS_MAP_DEVPTR_BY_DEFAULT
