from setuptools import setup, find_packages


PACKAGE = 'pytest_translations'
VERSION = __import__(PACKAGE).__version__
DOC = __import__(PACKAGE).__doc__

setup(
    name='pytest-translations',
    description='Test your translation files',
    long_description=__doc__,
    author='Thermondo GmbH',
    author_email='denis.cornehl@gmail.com',
    version=VERSION,
    packages=find_packages(),
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
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'pytest11': [
            'pytest_translations = pytest_translations',
        ]
    },
    install_requires=[
        'polib>=1.0.5',
        'pyenchant>=1.6.0',
    ],
    zip_safe=False,
)
