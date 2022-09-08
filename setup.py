from setuptools import setup


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name="quantestpy",
    version="0.1.0",
    license="Apache 2.0",
    description="Software for testing quantum computing programs.",
    author="Quantestpy Development Team",
    url="https://github.com/QuantestPy/quantestpy",
    packages=["quantestpy"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=_requires_from_file("requirements.txt")
)
