import setuptools

import pyasesm

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyasesm",
    version=pyasesm.__version__,
    author="Dawid Czarnecki",
    author_email="dawid@pz.pl",
    description="ArcSight ESM Active List connection library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dawid-czarnecki/pyasesm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        'Environment :: Console',
        "Operating System :: OS Independent",
        'Intended Audience :: Science/Research',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Information Technology',
        'Topic :: Security',
        'Topic :: Internet',
    ],
    install_requires=['requests', 'simplejson']
)