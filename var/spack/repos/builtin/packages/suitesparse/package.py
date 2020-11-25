# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Suitesparse(Package):
    """SuiteSparse: A Suite of Sparse matrix packages"""

    homepage = "http://www.suitesparse.com"
    url      = "https://github.com/PetterS/SuiteSparse/archive/master.tar.gz"

    version('master', sha256='62de43ed4ca21cf85de43e1587c0f6fdb67cd6326fcb5cc60b1d58b0f4b112ab')

    depends_on('metis@4.0.3')
    depends_on('blas')

    def install(self, spec, prefix):
        # patch SuiteSparse_config/SuiteSparse_config.mk
        c = join_path('SuiteSparse_config', 'SuiteSparse_config.mk')
        #  Fortran
        filter_file(
            r'^F77 .+',
            'F77 = {0}'.format(spack_f77),
            c
        )
        if spec.satisfies('%fj'):
            filter_file(
                r'^F77FLAGS .+',
                'F77FLAGS = $(FFLAGS) -O0 -X7',
                c
            )

        #  Install PATH
        filter_file(
            r'^INSTALL_LIB .+',
            'INSTALL_LIB = {0}'.format(prefix.lib),
            c
        )
        filter_file(
            r'^INSTALL_INCLUDE .+',
            'INSTALL_INCLUDE = {0}'.format(prefix.include),
            c
        )
        #  BLAS/LAPACK
        if spec['blas'].name == 'openblas':
            pblas = 'BLAS = -lopenblas'
            if spec.satisfies('%gcc'):
                pblas += ' -lgfortran'
            plapack = 'LAPACK = -lopenblas'
            filter_file(
                r'^BLAS .+',
                pblas,
                c
            )
            filter_file(
                r'^LAPACK .+',
                plapack,
                c
            )
        #  METIS
        filter_file(
            r'^METIS_PATH .+',
            'METIS_PATH = {0}'.format(spec['metis'].prefix.include),
            c
        )
        metisa = join_path(spec['metis'].prefix.lib, 'libmetis.a')
        filter_file(
            r'^METIS .+',
            'METIS = {0}'.format(metisa),
            c
        )
        # Patch makefile
        m = join_path('CHOLMOD', 'Lib', 'Makefile')
        filter_file(
            '$(METIS_PATH)/Lib',
            '$(METIS_PATH)',
            m,
            String=True
        )

        # make
        make()
        # test UMFPACK
        with working_dir("UMFPACK"):
            mkdirp('Demo/tmp')
            make('hb', parallel=False)
        # Install
        mkdirp(prefix.lib)
        mkdirp(prefix.include)
        make('install')
