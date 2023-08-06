from setuptools import setup, find_packages

setup(
    name="Choam",
    version="0.1.9",
    description="Python project scaffolder/manager",
    packages=find_packages(),
    keywords=['package', 'manager'],
    install_requires=['typing', 'toml', 'importlib', 'choam', 'fire', 'findimports'],
    project_urls={
        'Source': 'https://github.com/cowboycodr/choam'
    },
)