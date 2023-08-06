import pathlib
import setuptools

long_description = (pathlib.Path(__file__).parent / "README.md").read_text()

setuptools.setup(
    name='abstractTradeSimpleT',
    version='0.1.7',
    license='MIT',
    author="Joao Paulo Euko",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['lib'],
    install_requires=[],
    extra_requires={
        "dev": []
    }
)
