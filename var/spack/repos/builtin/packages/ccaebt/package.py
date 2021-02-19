# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ccaebt(MakefilePackage):
    """Code Comprehension Assistance for Evidence-Based performance Tuning"""

    homepage = "https://github.com/ebt-hpc/cca/"
    git      = "https://github.com/ebt-hpc/cca.git"

    version('1.0', commit='2c71a14c684c67f6125bbcd70248348dadf10994')

    depends_on('gmp')
    depends_on('zlib')

    depends_on('redland-bindings', type='run')
    depends_on('virtuoso', type='run')

    depends_on('py-psutil', type='run')
    depends_on('py-sympy', type='run')
    depends_on('py-msgpack', type='run')
    depends_on('py-pygit2', type='run')
    depends_on('py-gensim', type='run')
    depends_on('py-scikit-learn', type='run')
    depends_on('py-pyodbc', type='run')
    # depends on manually installed opam and packages

    patch('ccaebt_common.patch')

    def edit(self, spec, prefix):
        scpath = join_path('cca', 'scripts', 'siteconf.py')
        copath = join_path('cca', 'ebtutil', 'conf.py')
        vipath = join_path('cca', 'ebtutil', 'virtuoso_ini.py')

        prefixd = prefix.data
        prefixv = spec['virtuoso'].prefix
        filter_file('/opt/cca', prefix, scpath)
        filter_file('/opt/cca', prefix, copath)
        filter_file('/var/lib/cca', prefixd, scpath)
        filter_file('/var/lib/cca', prefixd, copath)
        filter_file('/opt/virtuoso', prefixv, scpath)
        filter_file('/opt/virtuoso', prefixv, vipath)

    def build(self, spec, prefix):
        with working_dir('src'):
            make(parallel=False)

    def install(self, spec, prefix):
        spath = join_path('src', 'ast', 'analyzing')
        install_tree('cca', prefix)
        mkdirp(prefix.bin)
        install_tree(join_path(spath, 'bin'), prefix.bin)
        mkdirp(prefix.etc)
        install_tree(join_path(spath, 'etc'), prefix.etc)
        install('LICENSE', prefix)
        dpath = prefix.modules
        mkdirp(dpath)
        install(join_path(spath, 'langs', 'astml', 'Mastml_p.cmxs'), dpath)
        install(join_path(spath, 'langs', 'cpp', 'Mcpp_p.cmxs'), dpath)
        install(join_path(spath, 'langs', 'fortran', 'Mfortran_p.cmxs'), dpath)

    def test(self):
        test_dir = self.test_suite.current_test_data_dir
        pythonexe = join_path(self.spec['python'].prefix.bin, 'python')
        pypath = join_path(self.spec.prefix.ebtutil, 'outline.py')
        # C
        opts = [pypath, join_path(test_dir, 'ctest')]
        expected = ['rsdft: 0.532741']
        self.run_test(pythonexe, options=opts, expected=expected)
        # Fortran77
        opts = [pypath, join_path(test_dir, 'ftest')]
        expected = ['rsdft: 0.613510']
        self.run_test(pythonexe, options=opts, expected=expected)
        # Fortran90
        opts = [pypath, join_path(test_dir, 'f90')]
        expected = ['rsdft: 0.613510']
        self.run_test(pythonexe, options=opts, expected=expected)
