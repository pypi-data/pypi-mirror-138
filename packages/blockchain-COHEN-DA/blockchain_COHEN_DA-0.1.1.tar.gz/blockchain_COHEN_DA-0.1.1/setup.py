import setuptools

setuptools.setup(
    name='blockchain_COHEN_DA',
    version='0.1.1',
    author='COHEN DA',
    author_email='DIS-ASSURANCE-CRYPTO@cohencpa.com',
    description='Transaction parsing for blockchains',
    package_dir={'blockchain':'blockchain'},
    packages=setuptools.find_packages()
)