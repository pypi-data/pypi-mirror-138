import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nikebotandroid",
    version="0.0.1",
    author="olega obini",
    author_email="author@example.com",
    description="A retail automation bot for the mobile Nike app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olegaobini/nikebot",
    project_urls={
        "Bug Tracker": "https://github.com/olegaobini/nikebot/issues",
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
