import setuptools

with open("README.md", "r") as long_desc:
    long_description = long_desc.read()

setuptools.setup(
    name="attribute_dict",
    version="1.0.0",
    author="JoBrad",
    author_email="",
    description="A subclass of dict that allows object-style access to its entries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JoBrad/attribute_dict",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    test_suite='nose2.collector.collector',
)