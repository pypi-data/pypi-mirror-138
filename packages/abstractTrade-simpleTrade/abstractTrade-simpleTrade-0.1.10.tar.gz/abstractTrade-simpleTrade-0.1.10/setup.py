import pathlib
import setuptools

long_description = (pathlib.Path(__file__).parent / "README.md").read_text()

setuptools.setup(
    name='abstractTrade-simpleTrade',
    version='0.1.10',
    license='MIT',
    author="Joao Paulo Euko",
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'abstractTrade-simpleTrade': 'abstractTrade-simpleTrade'},
    packages=setuptools.find_packages(),
    install_requires=[],
)
