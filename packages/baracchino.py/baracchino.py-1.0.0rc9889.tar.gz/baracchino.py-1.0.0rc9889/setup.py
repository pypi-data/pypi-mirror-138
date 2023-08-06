import os
import platform
from setuptools import setup
import re, subprocess
req = """
requests
aiohttp
"""

with open('baracchino/__init__.py') as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

if version.endswith(('a', 'b', 'rc')):
    # append version identifier based on commit count
    try:

        p = os.popen(" ".join(['git', 'describe', '--always']))
        version += p.read()[:-1].replace('a', "").replace('b', "").replace('c', "").replace('d', "").replace('e', "").replace('f', "").replace('g', "").replace('h', "").replace("i", "")
        print(version)
    except Exception:
        import traceback
        traceback.print_exc()
        print(Exception())
requirements = []
print(f"Using version {version}")
requirements = req.splitlines()
setup(name="baracchino.py", version=f"{version}", packages=["baracchino"], license="MIT", install_requires=requirements, classifiers=['Development Status :: 5 - Production/Stable',
                                                                                                                          'License :: OSI Approved :: MIT License',
                                                                                                                          'Intended Audience :: Developers',
                                                                                                                          'Natural Language :: English',
                                                                                                                          'Operating System :: OS Independent',
                                                                                                                          'Programming Language :: Python :: 3.8',
                                                                                                                          'Programming Language :: Python :: 3.9',
                                                                                                                          'Topic :: Internet',
                                                                                                                          'Topic :: Software Development :: Libraries',
                                                                                                                          'Topic :: Software Development :: Libraries :: Python Modules',
                                                                                                                          'Topic :: Utilities',
                                                                                                                          'Typing :: Typed'])
