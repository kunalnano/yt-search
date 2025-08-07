from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="yt-search-terminal",
    version="1.0.0",
    author="Al Sharma",
    author_email="",
    description="Algorithm-free YouTube search in your terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kunalnano/yt-search",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "yt-search=yt_search.main:main",
            "yts=yt_search.main:main",
        ],
    },
    keywords="youtube search terminal cli algorithm-free",
    project_urls={
        "Bug Reports": "https://github.com/kunalnano/yt-search/issues",
        "Source": "https://github.com/kunalnano/yt-search",
    },
)
