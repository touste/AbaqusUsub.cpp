#coding=utf8

########################################################################
###                                                                  ###
### Created by Martin Genet, 2008-2015                               ###
###                                                                  ###
### Laboratoire de Mécanique et de Technologie (LMT), Cachan, France ###
### Lawrence Berkeley National Laboratory, California, USA           ###
### University of California at San Francisco, USA                   ###
### Swiss Federal Institute of Technology (ETH), Zurich, Switzerland ###
###                                                                  ###
########################################################################

import glob

usub_cpp_file = open("usub.cpp", "w")

usub_cpp_file.write('''\
// Generated by usub.cpp.py.

#ifndef usub_cpp
#define usub_cpp

#include <stdio.h>
#include <string.h>

''')

if (glob.glob("UEXTERNALDB/uexternaldb.cpp")):
    usub_cpp_file.write('''\
#include "UEXTERNALDB/uexternaldb.cpp"

''')

usub_cpp_file.write('''\
#include "umat_data.h"

''')

umats = glob.glob("UMAT_C_*")
for umat in umats:
    usub_cpp_file.write('''\
#include "''' + umat + '''/umat.cpp"
''')

usub_cpp_file.write('''\

/**
 *
 * This is the general UMat function.
 * Depending on the name of the material model chosen in ABAQUS, the specific UMat function is executed.
 * Before that, a UMatData structure is created, that contains all data given by ABAQUS, but reinterpreted in C++ types (names are conserved).
 *
 */

extern "C" void umat_(
    double *stress,
    double *statev,
    double *ddsdde,
    double *sse,
    double *spd,
    double *scd,
    double *rpl,
    double *ddsddt,
    double *drplde,
    double *drpldt,
    double *stran,
    double *dstran,
    double *time,
    double *dtime,
    double *temp,
    double *dtemp,
    double *predef,
    double *dpred,
    char   *cmname,
    int    *ndi,
    int    *nshr,
    int    *ntens,
    int    *nstatv,
    double *props,
    int    *nprops,
    double *coords,
    double *drot,
    double *pnewdt,
    double *celent,
    double *dfgrd0,
    double *dfgrd1,
    int    *noel,
    int    *npt,
    int    *layer,
    int    *kspt,
    int    *kstep,
    int    *kinc,
    short   cmname_len)
{
''')

for umat in umats:
    usub_cpp_file.write('''\
    if (strncmp(cmname, "'''+umat+'''", '''+str(len(umat))+''') == 0)
    {
        UMatData<'''+umat.lower()+'''::ndim, '''+umat.lower()+'''::nvec, '''+umat.lower()+'''::npro, '''+umat.lower()+'''::nsta> umat_data(stress, statev, ddsdde, sse, spd, scd, rpl, ddsddt, drplde, drpldt, stran, dstran, time, dtime, temp, dtemp, predef, dpred, cmname,  ndi, nshr, ntens, nstatv, props, nprops, coords, drot, pnewdt, celent, dfgrd0, dfgrd1, noel, npt, layer, kspt, kstep, kinc, cmname_len);

        '''+umat.lower()+'''::umat(umat_data);
    }
''')

usub_cpp_file.write('''\

} // void umat_

#endif // # ifndef usub_cpp
''')
