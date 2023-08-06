import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cloudformer",
    version="0.0.2",
    author="Aziz Kurbanov",
    author_email="azizbek@gmail.com",
    description="Automated IaaS and Paas provisioner for cloud solutions running on managed kubernetes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sqe/cloudformer",
    project_urls={
        "Bug Tracker": "https://github.com/sqe/cloudformer/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)