from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='md_citeproc',
    version='0.2.2',
    description='Citeproc extension for Python-Markdown',
    license="GPLv3",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://md-citeproc.readthedocs.io',
    project_urls={
        'Documentation': 'https://md-citeproc.readthedocs.io',
        'Source Code': 'https://gitlab.com/dinuthehuman/md_citeproc',
        'Issue Tracker': 'https://gitlab.com/dinuthehuman/md_citeproc/-/issues'
    },
    author='Martin Obrist',
    author_email='dev@obrist.email',
    classifiers=[
        'Development Status :: 3 - Alpha',
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
    install_requires=['jinja2', 'Markdown'],
    setup_requires=['wheel'],
    extras_require={
        'dev': ['gitpython', 'mkdocs', 'mkdocstrings', 'twine', 'pytest', 'nose', 'invoke']
    },
    include_package_data=True
)
