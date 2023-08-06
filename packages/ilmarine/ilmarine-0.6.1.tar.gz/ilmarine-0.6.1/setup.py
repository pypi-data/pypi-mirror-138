import pathlib
import sys
from distutils.core import setup
from distutils.command.install import install as _install

class install(_install):
    def run(self):
        print("Wrong repo from public pypi")
        sys.exit(1)
        _install.run(self)

HERE = pathlib.Path(__file__).parent

setup(
    cmdclass={'install': install},
    name="ilmarine",
    version="0.6.1",
    description="ilmarine package for the internal pypi",
    long_description="ilmarine package for the internal pypi",
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["ilmarine"],
    include_package_data=True,
)