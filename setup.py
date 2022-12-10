from setuptools import setup

REQUIREMENTS = [
    "credentials",
    "Pillow",
    "tweepy",
    "tweet_capture"
]

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience ::  Creators",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: French",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.9",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

setup(
    name="contentconvertor",
    version="0.0.1",
    description="Converts content from Twitter to a png image that can be uploaded to Instagram",
    long_description="Converts content from Twitter to a png image that can be uploaded to Instagram",
    author="Léo Leducq",
    author_email="iziatask@gmail.com",
    url="github.com/leoleducq/Content-Convertor",
    packages=["contentconvertor"],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    python_requires=">=3.9",
)