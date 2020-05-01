import setuptools

from git2gitee import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="git2gitee",
    version=__version__,
    author="Mikele",
    author_email="blive200@gmail.com",
    description="import github repo to gitee, then clone to local",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toyourheart163/git2gitee",
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['git2gitee = git2gitee:cmd']
    },
    python_requires='>=3.6',
)
