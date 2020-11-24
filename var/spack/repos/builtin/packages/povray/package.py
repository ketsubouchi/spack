# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Povray(AutotoolsPackage):
    """The Persistence of Vision Raytracer is a high-quality, Free
    Software tool for creating stunning three-dimensional graphics."""

    homepage = "http://www.povray.org"
    url      = "https://github.com/POV-Ray/povray/archive/3.7-stable.tar.gz"

    version('3.7', sha256='2d047577494a20f8019cb0cbbec01fac5e5f64953f716858a7cc857cb1ca7c34')

    depends_on('boost+date_time+thread')
    depends_on('zlib')
    depends_on('libpng')
    depends_on('jpeg')
    depends_on('libtiff')
    depends_on('openexr')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        with working_dir("unix"):
            bash('./prebuild.sh')

    def configure_args(self):
        configure_args = []
        configure_args.append('COMPILED_BY=Spack' + spack_version)
        configure_args.append('--with-boost-thread=boost_thread-mt')
        return configure_args
