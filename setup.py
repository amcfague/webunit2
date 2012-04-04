try:
    from setuptools import setup, find_packages
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = None

setup(
    name='webunit2',
    version='0.2.2',
    description='Eases the testing of web services.',
    license="GPL",
    long_description=long_description,
    author='Andrew McFague',
    author_email='redmumba@gmail.com',
    maintainer='Andrew McFague',
    maintainer_email='redmumba@gmail.com',
    url='https://github.com/amcfague/webunit2',
    zip_safe=True,
    packages=find_packages(exclude=["ez_setup", "tests"]),
    install_requires=[
        "httplib2",
        "poster",
    ],
    test_suite='nose.collector',
    tests_require=[
        "mock",
        "nose",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Software Development :: Testing",
    ],
)
