from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup
from setuptools import find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name="quantestpy",
    version="0.1.0",
    license="Apache 2.0",
    description="Software for testing quantum computing programs.",
    author="Quantestpy Development Team",
    url="https://github.com/QuantestPy/quantestpy",
    packages=find_packages(),
    py_modules=[splitext(basename(path))[0]
                for path in glob("quantestpy/*.py")],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=_requires_from_file("requirements.txt")
)
