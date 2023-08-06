import os
import subprocess
import platform

from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext

pylena_version = "0.1.0"

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        super().__init__(name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class ConanCMakeBuildExtension(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(["conan", "--version"])
        except OSError:
            raise RuntimeError("Conan should be installed to build the extension")
        try:
            out = subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError("CMake should be installed to build the extension")
        for ext in self.extensions:
            self.build(ext)

    def build(self, ext):
        ext_dir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        ext_dir = os.path.join(ext_dir, "pylena")

        version_file = open(os.path.join(ext_dir, "version.py"), mode='w')
        print("version = \"{}\"".format(pylena_version), file=version_file)
        version_file.close()

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        output_arg = "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={}".format(ext_dir) if platform.system() != "Windows" else "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_Release={}".format(ext_dir)
        subprocess.run(["conan", "remote", "add", "lrde-public", "https://artifactory.lrde.epita.fr/artifactory/api/conan/lrde-public", "--force"])
        res = subprocess.run(['conan', 'install', ext.sourcedir, '-s', 'compiler.cppstd=20', '-s', 'compiler.libcxx=libstdc++11', '-e', 'CXXFLAGS=', '-e', 'CFLAGS=', '--build', 'missing'], cwd=self.build_temp)
        if res.returncode:
            raise RuntimeError("Unable to run conan")
        cmake_command =  ['cmake', ext.sourcedir, output_arg]
        if "PYTHON_EXECUTABLE" in os.environ:
            cmake_command.append("-DPYTHON_EXECUTABLE={}".format(os.environ["PYTHON_EXECUTABLE"])) # To detect the correct Python version with several pyenv python version
        res = subprocess.run(cmake_command, cwd=self.build_temp)
        if res.returncode:
            raise RuntimeError("Unable to run config cmake")
        if not self.dry_run:
            res = subprocess.run(['cmake', '--build', '.'], cwd=self.build_temp)
            if res.returncode:
                raise RuntimeError("Unable to build the package")

# Definitiely waiting for PEP 621 to be supported by setuptools

CLASSIFIERS = """\
    License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)
    Operating System :: POSIX :: Linux
    Programming Language :: C++
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3 :: Only
    Programming Language :: Python :: Implementation :: CPython
    Topic :: Scientific/Engineering :: Image Processing
"""

setup(
    name="pylena",
    version=pylena_version,
    url="https://gitlab.lrde.epita.fr/olena/pylena",
    author="EPITA Research and Development Laboratory (LRDE)",
    author_email="baptiste.esteban@lrde.epita.fr",
    platforms=["Linux"],
    description="Image processing library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MPLv2",
    classifiers = [clf for clf in CLASSIFIERS.split('\n') if clf], # From https://github.com/numpy/numpy/blob/a2d91e6f5b3b2e192ae741798844e306a7854e85/setup.py#L446
    install_requires=["numpy"],
    extras_require={
        "packaging": ["auditwheel"],
        "doc": ["sphinx", "sphinx_rtd_theme", "sphinx_gallery", "scikit-image", "matplotlib"],
        "tests": ["pytest"]
    },
    packages=find_packages(exclude=["tests", "doc"]),
    ext_modules=[CMakeExtension("pylena_cxx")],
    cmdclass={
        'build_ext': ConanCMakeBuildExtension,
    }
)
