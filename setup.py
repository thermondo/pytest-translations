from setuptools import setup

setup(
    name='pytest-translations',
    description='Test your translation files',
    long_description=open("README.rst").read(),
    author='Denis Cornehl',
    author_email='syphar@fastmail.fm',
    version='0.1.0',
    py_modules=['pytest_translations'],
    license='MIT',
    url='https://github.com/thermondo/pytest-translations',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points={
        'pytest11': [
            'pytest_translations = pytest_translations',
        ]
    },
    install_requires=[
        'py>=1.3.0',
        'polib>=1.0.5',
    ]
)
