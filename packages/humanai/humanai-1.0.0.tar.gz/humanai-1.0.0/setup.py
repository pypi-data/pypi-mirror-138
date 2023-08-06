from setuptools import find_packages, setup
setup(
    name='humanai',
    packages=find_packages(),
    version='1.0.0',
    description='Turns common questions into human responses.',
    author='Me',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner', 'Brainshop'],
    test_suite='tests',
)