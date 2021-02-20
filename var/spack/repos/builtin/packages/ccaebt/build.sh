#!/bin/sh
export WORKDIR=`pwd`/ocamlwork
export BUILDDIR=`pwd`/src

# 0. directory
mkdir -p $WORKDIR


# 1. ocaml (for opam)
cd $WORKDIR
curl -OL http://caml.inria.fr/pub/distrib/ocaml-4.11/ocaml-4.11.1.tar.gz
tar xf ocaml-4.11.1.tar.gz
cd ocaml-4.11.1
./configure --prefix=$WORKDIR/ocaml
make
make install
export PATH=$PATH:$WORKDIR/ocaml/bin

# 2.opam
cd $WORKDIR
curl -OL https://github.com/ocaml/opam/releases/download/2.0.7/opam-full-2.0.7.tar.gz
tar xf opam-full-2.0.7.tar.gz
cd opam-full-2.0.7
./configure --prefix=$WORKDIR/opam
make lib-ext
make
make install

# 3.ocaml (for packages)
export PATH=$PATH:$WORKDIR/opam/bin
export OPAMROOT=$WORKDIR/work
#export OPAMROOT=/tmp
#OPAMROOT must be shorter than 38 bytes
opam init --disable-sandboxing --disable-completion --no-setup --bare
opam switch create ocaml-base-compiler.4.11.1
eval $(opam env)

# 4.modules
opam install -b -y camlzip cryptokit csv git-unix menhir ocamlnet pxp ulex uuidm
eval $(opam env)

# 5.volt
cd $WORKDIR
curl -OL https://github.com/codinuum/volt/archive/master.tar.gz
tar xf master.tar.gz
cd volt-master
sh configure
make all
make install

# 6.parser
cd $BUILDDIR
make

