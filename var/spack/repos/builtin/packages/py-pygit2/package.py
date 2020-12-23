# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPygit2(PythonPackage):
    """Pygit2 is a set of Python bindings to the libgit2 shared library,
    libgit2 implements the core of Git.
    """

    homepage = "http://www.pygit2.org/"
    url      = "https://github.com/libgit2/pygit2/archive/v1.3.0.tar.gz"

    version('1.3.0', sha256='1ffbbbfc2f85694b8f395a616ab930e57b2df9d50781e8ba84603d293ae70462')

    extends('python')
    depends_on('py-setuptools', type='build')
    # Version must match with libgit2
    # See: http://www.pygit2.org/install.html
    depends_on('libgit2@1.1:1.1.99', when='@1.4:')
    depends_on('libgit2@1.0:1.0.99', when='@1.1:1.3.99')
    depends_on('libgit2@0.28:0.28.99', when='@:1.0.99')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-cffi', type=('build', 'run'))
    depends_on('py-cached-property', type=('run'))

    def setup_build_environment(self, env):
        spec = self.spec
        # http://www.pygit2.org/install.html
        env.set('LIBGIT2', spec['libgit2'].prefix)
        env.set('LIBGIT2_LIB', spec['libgit2'].prefix.lib)
