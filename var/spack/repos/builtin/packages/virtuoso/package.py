# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Virtuoso(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/openlink/virtuoso-opensource"
    url      = "https://github.com/openlink/virtuoso-opensource/archive/v7.2.5.1.tar.gz"
    # url      = "https://github.com/openlink/virtuoso-opensource/archive/develop/7.tar.gz"

    version('7.2.5.1', sha256='3e4807e94098b8265f8cf00867d1215bb1e9d0d274878e59a420742d2de471c2')
    # version('7', sha256='30b58ac00a03c58d1564a001695ab02aede49d4df634f77e84ae08ec9986b9c9')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    depends_on('gperf')
    depends_on('readline')
    depends_on('openssl@1.0.2u', type=('build', 'link', 'run'))

    patch('virt_rpc.patch')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')

    def configure_args(self):
        args = []
        args.append('--with-layout=opt')
        args.append('--with-readline=/usr')
        args.append('--program-transform-name=s/isql/isql-v/')
        args.append('--disable-dbpedia-vad')
        args.append('--disable-demo-vad')
        args.append('--enable-fct-vad')
        args.append('--enable-ods-vad')
        args.append('--disable-sparqldemo-vad')
        args.append('--disable-tutorial-vad')
        args.append('--enable-isparql-vad')
        args.append('--enable-rdfmappers-vad')
        return args
