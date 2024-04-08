/*
 * Handle different Fortran conventions.
 */

#if defined(NO_APPEND_FORTRAN)
#if defined(UPPERCASE_FORTRAN)
#define F_FUNC(f,F) F
#else
#define F_FUNC(f,F) f
#endif
#else
#if defined(UPPERCASE_FORTRAN)
#define F_FUNC(f,F) F##_
#else
#define F_FUNC(f,F) f##_
#endif
#endif

#define qh_dgetrf F_FUNC(dgetrf,DGETRF)
#define qh_dgecon F_FUNC(dgecon,DGECON)
#define qh_dgetrs F_FUNC(dgetrs,DGETRS)

#define qhull_misc_lib_check() QHULL_LIB_CHECK

#include "libqhull_r/libqhull_r.h"

int qh_new_qhull_scipy(qhT *qh, int dim, int numpoints, coordT *points, boolT ismalloc,
                       char *qhull_cmd, FILE *outfile, FILE *errfile, coordT* feaspoint);

