# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openrasmol(MakefilePackage):
    """RasMol is a molecular graphics program intended for the
       visualisation of proteins, nucleic acids and small molecules."""

    homepage = "http://www.openrasmol.org/"
    url      = "https://sourceforge.net/projects/openrasmol/files/RasMol/RasMol_2.7.5/RasMol-2.7.5.2.tar.gz"

    version('2.7.5.2', sha256='b975e6e69d5c6b161a81f04840945d2f220ac626245c61bcc6c56181b73a5718')

    depends_on('imake', type='build')
    depends_on('wget', type='build')
    depends_on('libx11')
    depends_on('libxpm')
    depends_on('libxext')
    depends_on('libxi')

    patch('rasmol_noqa.patch')

    def edit(self, spec, prefix):
        im = join_path('src', 'Imakefile')
        filter_file('releases-noredirect', 'releases', im)

    def build(self, spec, prefix):
        with working_dir('src'):
            bash = which('bash')
            bash('./build_all.sh')

    def install(self, spec, prefix):
        with working_dir('src'):
            bash = which('bash')
            bash('./rasmol_install.sh', '--prefix={0}'.format(prefix))
