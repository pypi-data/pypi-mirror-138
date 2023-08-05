import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="merge_csv_xjg",
    version="0.0.3",
    author="Joaquim Gomez",
    description="Merge two CSV files with pandas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JoaquimXG/csv-merge",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={ 'console_scripts': ['merge_csv = merge_csv.__main__:main' ] },
    install_requires=['pandas', 'numpy', 'click'],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)