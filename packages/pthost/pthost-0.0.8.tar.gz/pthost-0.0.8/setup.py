import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pthost",
    description="Default vhost tester",
    version="0.0.8",
    url="https://www.penterep.com/",
    author="Penterep",
    author_email="info@penterep.com",
    license="GPLv3+",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Environment :: Console"
    ],
    python_requires = '>=3.6',
    install_requires=["ptlibs>=0.0.3", "requests", "tldextract"],
    entry_points = {'console_scripts': ['pthost = pthost.pthost:main']},
    long_description=long_description,
    long_description_content_type="text/markdown",
)