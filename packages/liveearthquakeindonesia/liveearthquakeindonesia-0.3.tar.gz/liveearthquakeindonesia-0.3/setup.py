"""
https://packaging.python.org/en/latest/tutorials/packaging-projects/
Markdown guide
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="liveearthquakeindonesia",
    version="0.3",
    author="Rizal Mustofa",
    author_email="rizalmustofa31@gmail.com",
    description="The package will get the latest earthquake from BMKG",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rizalmustofa31/Latest-Indonesia-Earhquake",
    project_urls={
        "Website": "https://github.com/rizalmustofa31",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"
    ],
    # package_dir={"": "src"},
    # packages=setuptools.find_packages(where="src"),
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
