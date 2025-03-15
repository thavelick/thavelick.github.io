---
slug: til/nosetests_only_recurses_subfolders_that_are_modules
categories: til, blog
title: TIL: nosetests - Only Recurses Sub-folders That Are Modules
publish_date: 2022-09-25
---
In a project I work on, we organize tests under a `tests` folder.  Within that
folder, of course, we have several levels of sub-folders. Recently I had a
problem where some newer tests weren't being run with our build. It turns out
that `nosetests` only recurses into subfolders that are modules. Thus, to fix
the problem, I had to add an empty `__init__.py` file to the subfolder that
contained the tests that weren't being run.

To prevent this from happening again, I added the following little meta-test to
our test suite:

```python
import os
import unittest

class TestEnsureAllTestFoldersAreModules(unittest.TestCase):
    def test_ensure_all_test_folders_are_modules(self):
        # nosetests won't run tests in folders that don't have an __init__.py
        # file, so make sure that all the sub-folders under tests/, recursively,
        # have an __init__.py file. Only check folders that contain a test_*.py
        # file as some folders like __pycache__ don't contain actual tests.

        for root, dirs, files in os.walk('tests'):
            if any([f.startswith('test_') and f.endswith(".py") for f in files]):
                self.assertTrue(
                    '__init__.py' in files,
                    '{} does not have an __init__.py file'.format(root)
                )
```

## Resources
* https://stackoverflow.com/questions/19852548/run-nosetests-in-all-subdirectories
* https://docs.python.org/3.11/library/os.html#os.walk
