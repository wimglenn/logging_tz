import re
import sys
from setuptools import setup


with open("README.rst") as f:
    long_description = f.read()


def get_version():
    with open('logging_tz.py') as f:
        [version] = re.findall(r"\n__version__ = '([0-9\.]*)'\n", f.read())
    return version


if sys.version_info > (3, 2):
    raise Exception("You don't need this, the built-in logging.Formatter should just work")


test_deps = ['pytest', 'freezegun', 'mock']


setup(
    name='logging_tz',
    version=get_version(),
    author='Wim Glenn',
    author_email='hey@wimglenn.com',
    url='https://github.com/wimglenn/logging_tz',
    py_modules=['logging_tz'],
    description='Specify the UTC offset in Python 2 logging datefmt',
    long_description=long_description,
    install_requires=['pytz', 'tzlocal'],
    extras_require={'dev': test_deps},
    setup_requires=['pytest-runner'] + test_deps,
    tests_require=test_deps,
    classifiers=[
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries',
        'Intended Audience :: Developers',
        'Topic :: System :: Logging',
    ],
)
