import os.path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='copydoc',
    version='1.0.9',
    author='NPR Visuals',
    author_email='nprapps@npr.org',
    url='https://github.com/nprapps/copydoc/',
    description='Parse Google docs for use in content management',
    long_description=read('README.rst'),
    py_modules=('copydoc',),
    license="MIT License",
    keywords='google gdocs',
    install_requires=[
        'beautifulsoup4==4.4.1'
    ],
    extras_require={
        'dev': [
            'Sphinx==1.3.1',
            'nose2==0.5.0',
            'tox==2.3.1',
            'flake8==3.5.0'
        ]
    },
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    )
)
