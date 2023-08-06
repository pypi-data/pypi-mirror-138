import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="titanscraper",
    version="0.0.20",
    description="A web scraping library that makes web-scraping easy",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/emileKing/titanscraper",
    author="Emile DJIDA GONGDEBIYA",
    author_email="djidadevacc@gmail.com",
    license="MIT",
    packages=["titanscraper"],
    include_package_data=True,
    install_requires=["beautifulsoup4==4.10.0", "xmltodict==0.12.0", "lxml", "requests==2.26.0"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)