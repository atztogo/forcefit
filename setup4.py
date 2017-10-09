from distutils.core import setup, Extension
#from setuptools import setup, Extension
import platform
import numpy
import platform
import os

from setup import (extension_spglib, extension_phonopy,
                   packages_phonopy, scripts_phonopy)
from setup3 import (extension_lapackepy, extension_phono3py,
                    packages_phono3py, scripts_phono3py)

include_dirs_numpy = [numpy.get_include()]
include_dirs_lapacke = ['../lapacke/include']
include_dirs = ['c/harmonic_h', 'c/anharmonic_h']
include_dirs += include_dirs_numpy + include_dirs_lapacke

extra_link_args = ['-lgomp',]

if platform.system() == 'Darwin':
    include_dirs += ['/opt/local/include',]
    extra_link_args += ['/opt/local/lib/libopenblas.a']
else:
    extra_link_args += ['-llapacke', '-llapack', '-lblas']

extension_phono4py = Extension(
    'anharmonic._phono4py',
    include_dirs=include_dirs,
    extra_compile_args=['-fopenmp'],
    extra_link_args=extra_link_args,
    sources=['c/_phono4py.c',
             'c/harmonic/dynmat.c',
             'c/harmonic/lapack_wrapper.c',
             'c/harmonic/phonoc_array.c',
             'c/harmonic/phonoc_utils.c',
             'c/anharmonic/phonon3/fc3.c',
             'c/anharmonic/phonon4/fc4.c',
             'c/anharmonic/phonon4/real_to_reciprocal.c',
             'c/anharmonic/phonon4/frequency_shift.c'])

extension_forcefit = Extension(
    'anharmonic._forcefit',
    include_dirs=include_dirs,
    extra_compile_args=['-fopenmp'],
    extra_link_args=extra_link_args,
    sources=['c/_forcefit.c',
             'c/harmonic/lapack_wrapper.c'])

packages_phono4py = ['anharmonic.phonon4',
                     'force_fit']
scripts_phono4py = ['scripts/phono4py',
                    'scripts/force-fit']


if __name__ == '__main__':
    version = ''
    with open("phonopy/version.py") as w:
        for line in w:
            if "__version__" in line:
                version = line.split()[2].strip('\"')

    # To deploy to pypi by travis-CI
    nanoversion = ''
    if os.path.isfile("__nanoversion__.txt"):
        with open('__nanoversion__.txt') as nv:
            for line in nv:
                nanoversion = '%.4s' % (line.strip())
                break
            if nanoversion:
                nanoversion = '.' + nanoversion

    if all([x.isdigit() for x in version.split('.')]):
        setup(name='phono4py',
              version=(version + nanoversion),
              description='This is the phono4py module.',
              author='Atsushi Togo',
              author_email='atz.togo@gmail.com',
              url='http://atztogo.github.io/phono3py/',
              packages=(packages_phonopy +
                        packages_phono3py +
                        packages_phono4py),
              scripts=(scripts_phonopy +
                       scripts_phono3py +
                       scripts_phono4py),
              ext_modules=[extension_spglib,
                           extension_lapackepy,
                           extension_phonopy,
                           extension_phono3py,
                           extension_phono4py])
    else:
        print("Phono4py version number could not be retrieved.")
