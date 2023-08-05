from pathlib import Path
from setuptools import setup


long_description = (Path(__file__).parent / "README.md").read_text()

setup(
    name='abstractTrade-simpleTrade',
    version='0.1.3',
    license='MIT',
    author="Joao Paulo Euko",
    long_description=long_description,
    long_description_content_type='text/markdown'
)
