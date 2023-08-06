import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bmkgdashboard",
    version="0.8",
    author="Sencho Parameswara",
    author_email="senchoparameswara@gmail.com",
    description="this package is src for BMKG indonesian earthquake live and last articlee",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sencho-masteringpy/bmkg-dashboard",
    project_urls={
        "MyWeb": "https://senchooo.com",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],
    packages=["bmkgdashboard"],
    python_requires=">=3.6"
)
