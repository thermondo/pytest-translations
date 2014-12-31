from setuptools import setup

setup(
    name='pytest-translations',
    description='Test your translation files',
    author='Denis Cornehl',
    author_email='syphar@fastmail.fm',
    version='0.1.0',
    py_modules=['pytest_translations'],
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
