from setuptools import setup

name = "types-pyflakes"
description = "Typing stubs for pyflakes"
long_description = '''
## Typing stubs for pyflakes

This is a PEP 561 type stub package for the `pyflakes` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `pyflakes`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/pyflakes. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `9150db52a6280c7a40f1a8029f5b390314ba0dda`.
'''.lstrip()

setup(name=name,
      version="2.4.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pyflakes.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pyflakes-stubs'],
      package_data={'pyflakes-stubs': ['__init__.pyi', 'api.pyi', 'checker.pyi', 'messages.pyi', 'reporter.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
