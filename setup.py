from setuptools import find_packages, setup

setup(
    name="changelog",
    version="0.0.1",
    description="Changelog automation hook",
    long_description_content_type="text/markdown",
    url="https://github.com/UBtrNvME/changelog",
    packages=find_packages(),
    scripts=[],
    classifiers=["Programming Language :: Python :: 3"],
    install_requires=[
        "moto",
        "pytest==6.2.4",
    ],
    python_requires="==3.10.0",
    include_package_data=True,
    zip_safe=False,
)
