from setuptools import find_packages, setup

def read_requirements():
    with open("requirements.txt") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name='PythonCore',
    version='0.1.0',
    description='DAR Python Core',
    author='DAR Data Services',
    packages=find_packages(),
    install_requires=read_requirements(),
)