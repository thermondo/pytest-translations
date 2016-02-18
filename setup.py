from setuptools import setup

from pytest_translations import __version__, __doc__

setup(
    name='pytest-translations',
    description='Test your translation files',
    long_description=__doc__,
    author='Thermondo GmbH',
    author_email='syphar@fastmail.fm',
    version=__version__,
    py_modules=['pytest_translations'],
    license='MIT',
    url='https://github.com/thermondo/pytest-translations',
    download_url='https://github.com/thermondo/pytest-translations',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'pytest11': [
            'pytest_translations = pytest_translations',
        ]
    },
    install_requires=[
        'py>=1.3.0',
        'polib>=1.0.5',
        'pyenchant>=1.6.0',
    ]
)
