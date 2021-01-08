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

    def build(self, spec, prefix):
        with working_dir('./src'):
            make()

    def install(self, spec, prefix):
        install_tree('cca/*', prefix)
        install_tree('src/ast/analyzing/bin', prefix)
        install_tree('src/ast/analyzing/etx', prefix)
        install('LICENSE', prefix)
        mpath = join_path(prefix, 'module')
        mkdirp(mpath)
        install('src/ast/analyzing/langs/fortran/Mfortran_p.cmxs', mpath)
