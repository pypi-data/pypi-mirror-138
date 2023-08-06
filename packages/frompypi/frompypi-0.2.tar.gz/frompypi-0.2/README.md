This module enables installing and importing any PyPI package simply by:

    from pypi import packagename

Use underscore instead of dash, if found in package name. When package contains multiple
top-level modules it attempts to choose the most similar to the name of the package itself.

Note: does not support "import pypi.something" or "import pypi.something as somethingelse"
