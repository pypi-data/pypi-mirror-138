from setuptools import setup
import re

with open('cowsay/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

readme = ''
with open('README.md') as f:
    readme = f.read()

packages = [
    'cowsay',
    'cowsay.lib',
    'cowsay.lib.cows'
]

setup(
    name = "cowsay-py",
    version = version,
    packages = packages,
    license = 'MIT',
    author = "Ovlic",
    description = "Python module for cowsay",
    long_description = readme,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ovlic/cowsay_py",
    project_urls = {
        "Bug Tracker": "https://github.com/ovlic/cowsay_py/issues",
    },
    classifiers = {
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    },
    include_package_data=True,
    python_requires = '>=3.6',
)