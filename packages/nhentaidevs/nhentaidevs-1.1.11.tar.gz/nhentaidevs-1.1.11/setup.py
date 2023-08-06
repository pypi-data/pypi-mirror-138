from setuptools import setup, find_packages

with open("README.md", "r") as f:
    LONG_DESC = f.read()

setup(
    name='nhentaidevs',
    version='1.1.11',
    description="Mini Nhentai Doujins Scraper/Downloader.",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    author="John Lester Dev :>",
    author_email="johnlesterincbusiness@gmail.com",
    url="https://pypi.org/project/nhentaidevs",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "beautifulsoup4",
        "coloredevs",
        "requests",
        "pickle-mixin",
        "click",
        "tqdm"
    ],
    keywords=[
        'nhentai',
        'download',
        'images',
        'doujinshi',
        'cli',
        'scraper'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
)
