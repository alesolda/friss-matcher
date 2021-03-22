# Copyright (C) 2021 Ale Solda

from setuptools import setup

__version__ = "1.0.0"

install_requires = [
    "Django==3.1.7",
    "django-extensions==3.1.1",
    "djangorestframework==3.12.2",
    "fuzzywuzzy==0.18.0",
    "uvicorn==0.13.4",
]

dependency_links = []

packages = [
    "friss_matcher",
    "friss_matcher.match",
    "friss_matcher.match.migrations",
]


setup(
    name="friss-matcher",
    version=__version__,
    license="Alejandro Solda (C)",
    description="Friss Matcher",
    author="Alejandro Solda",
    author_email="43531535+alesolda@users.noreply.github.com",
    package_dir={"": "src"},
    packages=packages,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Alejandro Solda (C)",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
    ],
    keywords=[
        "friss",
        "match",
        "matcher",
    ],
    python_requires=">=3.9",
    install_requires=install_requires,
    setup_requires=[
        "wheel",
    ],
    entry_points={
        "console_scripts": [
            "friss-matcher = friss_matcher.__main__:main",
        ]
    },
)
