import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="indonesia-earthquake",
    version="0.0.3",
    author="Arsenius Anom Permadi",
    author_email="anom@broanom.com",
    description="the latest earthquake from BMKG | Indonesia",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anompermadi/latest_indonesia_earthquake.git",
    project_urls={
        "Website": "https://www.broanom.com/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
