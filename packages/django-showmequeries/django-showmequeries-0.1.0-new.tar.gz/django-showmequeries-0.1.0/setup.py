from setuptools import setup
from querycount import __version__

tarball_url = "https://github.com/kaajavi/django-showmequeries/tarball/{0}".format(__version__)
url = "https://github.com/kaajavi/django-showmequeries"

from pathlib import Path

here = Path(__file__).parent
long_description = (here / "README.rst").read_text()

setup(
    name="django-showmequeries",
    version=__version__,
    original_author="Brad Montgomery",
    author="Javier Guignard",
    author_email="kaajavi@gmail.com",
    description=("Middleware that Prints statics of DB queries to the runserver console."),
    install_requires=[],
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url=url,
    license="MIT",
    keywords="django querycount queries database performance",
    packages=[
        "querycount",
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        "Topic :: Utilities",
    ],
)
