from setuptools import setup, find_packages

packages = find_packages()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cricketapi",
    version='1.0.2',
    author = 'Roanuz Softwares Private Ltd',
    author_email = 'contact@roanuz.com',
    description="Roanuz Sports SDK For New V5 APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache License 2.0',
    url="https://github.com/roanuz/cricketapi-sdk",
    packages=packages,
    package_data={packages[0]: ['py.typed']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests'
    ],
    extras_require={
    }
)


