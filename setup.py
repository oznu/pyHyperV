from distutils.core import setup

setup(
    name='pyHyperV',
    version='0.0.2',
    author='oznu',
    author_email='dev@oz.nu',
    packages=['pyHyperV'],
    url='https://github.com/oznu/pyHyperV',
    license='Apache License',
    description='A simple client for calling HyperV orchestator runbooks in python',
    long_description=open('README.rst').read(),
    install_requires=[
        "requests >= 2.0.0",
        "requests_ntlm"
    ],
)
