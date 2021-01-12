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

        prefixd = join_path(prefix, 'data')
        prefixv = spec['virtuoso'].prefix
        filter_file('/opt/cca', prefix, scpath)
        filter_file('/opt/cca', prefix, copath)
        filter_file('/var/lib/cca', prefixd, scpath)
        filter_file('/var/lib/cca', prefixd, copath)
        filter_file('/opt/virtuoso', prefixv, scpath)
        filter_file('/opt/virtuoso', prefixv, vipath)

    def build(self, spec, prefix):
        with working_dir('./src'):
            make()

    def install(self, spec, prefix):
        install_tree('cca', prefix)
        dpath = join_path(prefix, 'bin')
        mkdirp(dpath)
        install_tree('src/ast/analyzing/bin', dpath)
        dpath = join_path(prefix, 'etc')
        mkdirp(dpath)
        install_tree('src/ast/analyzing/etc', dpath)
        install('LICENSE', prefix)
        dpath = join_path(prefix, 'modules')
        mkdirp(dpath)
        #install('src/ast/analyzing/langs/fortran/Mfortran_p.cmxs', dpath)
        install('LICENSE', dpath)
