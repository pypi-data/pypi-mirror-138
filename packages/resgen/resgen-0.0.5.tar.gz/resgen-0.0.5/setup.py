import pathlib

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r",  encoding="utf-16") as fh:
    requirements = fh.read()

setup(
    name='resgen',
    version='0.0.5',
    entry_points='''
        [console_scripts]
        resgen=resgen:main
    ''',
    author='Udendu Abasili',
    description='This package was made to help generate responsive images in bulk',
    url='https://github.com/udabasili/responsive-image-gen',
    email='udbasili@yahoo.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    py_modules=['resgen', 'app'],
    packages=find_packages(),
    install_requires=[requirements],
    python_requires='>=3.2',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='responsive images python web development developer response_images_gen responsive images generator',
    download_url='https://github.com/udabasili/responsive-image-gen/archive/refs/tags/1.0.0.tar.gz'
)
