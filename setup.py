from setuptools import setup, find_packages

setup(
    name='crypto-backtest',
    version='0.0.5',
    description='BullionBear backtest framework',
    author='yitech',
    author_email='coastq22889@icloud.com',
    packages=find_packages(include=['backtest', 'backtest.*']),
    install_requires=[
        'pydantic',
        'pydantic-settings',
        'python-dateutil'
    ],
)
