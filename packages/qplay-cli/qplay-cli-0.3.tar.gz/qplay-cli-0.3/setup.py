from setuptools import setup, find_packages

setup(
    name="qplay-cli",
    version='0.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'retrying',
    ],
    entry_points='''
        [console_scripts]
        quantplay=qplay_cli.main:quantplay
    ''',
)