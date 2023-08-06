from setuptools import setup, find_packages

__version__ = '0.6.2'

setup(
    name = 'metalearn',
    packages = find_packages(include=['metalearn', 'metalearn.*']),
    version = __version__,
    description = 'A package to aid in metalearning',
    author = 'Roland Laboulaye, Brandon Schoenfeld, Casey Davis',
    author_email = 'rlaboulaye@gmail.com, bjschoenfeld@gmail.com, caseykdavis@gmail.com',
    url = 'https://github.com/byu-dml/metalearn',
    download_url = 'https://github.com/byu-dml/metalearn/archive/{}.tar.gz'.format(__version__),
    keywords = ['metalearning', 'machine learning', 'metalearn'],
    license='MIT',
    install_requires = [
        'numpy',
        'scikit-learn<=0.22.2.post1',
        'pandas',
    ],
    classifiers = [
        'Programming Language :: Python :: 3'
    ],
    include_package_data=True,
)
