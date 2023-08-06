import setuptools
import subprocess


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

_result = subprocess.run("src/fastapi_sysunicorns/version.py", encoding="utf-8", stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True, shell=True)
version = f"{_result.stdout}".replace("\n","")

setuptools.setup(
    name="fastapi-sysunicorns-helper",
    version=version,
    author="miragecentury",
    author_email="victorien.vanroye@gmail.com",
    description="Utility Package for FastApi Python Application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/public-sysunicorns-info/fastapi_sysunicorns_helper",
    project_urls={
        "Bug Tracker": "https://github.com/public-sysunicorns-info/fastapi_sysunicorns_helper/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        "pydantic >= 1.9.0, <2.0.0",
        "fastapi >= 0.73.0, <1.0.0",
        "dependency-injector >= 4.0, <5.0"
    ]
)