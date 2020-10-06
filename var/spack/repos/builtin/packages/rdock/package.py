# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os

class Rdock(Package):
    """rDock is a fast and versatile Open Source docking program 
    that can be used to dock small molecules against proteins and 
    nucleic acids. """

    homepage = "https://rdock.sourceforge.net/"
    url      = "https://sourceforge.net/projects/rdock/files/rDock_2013.1_src.tar.gz"

    version('2013.1', sha256='e716998c3f8a2a70205a8d30ba22675bfdb1764d13c858645138c5eadf2a37e9')

    depends_on('popt')
    depends_on('cppunit')
    depends_on('openbabel', type='run')
    depends_on('py-numpy', type='run')
    
    patch('rdockcommon.patch')
    patch('fjconst.patch', when='%fj')

    phases = ['build', 'install']

    def build(self, spec, prefix):
        # compiler path
        mpath = 'build/tmakelib/linux-g++-64/tmake.conf'
        filter_file('/usr/bin/gcc', spack_cc, mpath, string=True)
        filter_file('/usr/bin/g++', spack_cxx, mpath, string=True)
        # compiler option
        if not spec.target.family == 'x86_64':
            filter_file('-m64', '', mpath, string=True)
            filter_file('-pipe', '', mpath, string=True)

        # build
        with working_dir("build"):
            make('linux-g++-64')
            #make('linux-g++-64-debug')

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def check_build(self):
        with working_dir("build"):
            make('test', parallel=False)

    def install(self, spec, prefix):
        install_tree('.', prefix)

    def setup_run_environment(self, env):
        env.set('RBT_ROOT', self.prefix)
