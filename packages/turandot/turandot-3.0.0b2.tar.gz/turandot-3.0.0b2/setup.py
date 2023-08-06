import pathlib
from distutils.core import setup
from setuptools import find_packages


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    name='turandot',
    version='3.0.0b2',
    description='Turandot Markdown Converter',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="GPLv3",
    author='Martin Obrist',
    author_email='dev@obrist.email',
    url='https://turandot.readthedocs.io',
    project_urls={
        'Documentation': 'https://turandot.readthedocs.io',
        'Source Code': 'https://gitlab.com/dinuthehuman/turandot',
        'Issue Tracker': 'https://gitlab.com/dinuthehuman/turandot/-/issues'
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Text Processing :: Markup :: Markdown',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='markdown, citeproc',
    packages=find_packages(where='.', exclude=['tests', 'tasks']),
    python_requires='>=3.9, <4',
    include_package_data=True,
    setup_requires=['wheel'],
    install_requires=[
        "beautifulsoup4",
        "Mako",
        "Markdown",
        "python-frontmatter",
        "requests",
        "urllib3",
        "weasyprint>=53.0",
        "cssselect2",
        "jinja2",
        "markdown-katex",
        "colour",
        "peewee",
        "lxml",
        "pyyaml",
        "Pygments",
        "ruamel.yaml",
        "md_citeproc"
    ],
    extras_require={
        'tk': [
            'bidict',
            'tkhtmlview'
        ],
        'gtk': [
            'pygobject'
        ],
        'dev': ['gitpython', 'mkdocs', 'mkdocstrings', 'twine', 'pytest', 'nose', 'invoke'],
        'optional': ["gitpython", "qrcode"]
    }
)
