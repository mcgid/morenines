from setuptools import setup, find_packages

setup(
    name='morenines',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mn = morenines.main:main'
        ]
    },
)
