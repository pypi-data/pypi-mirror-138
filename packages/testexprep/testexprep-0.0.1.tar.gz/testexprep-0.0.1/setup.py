import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testexprep",
    version="0.0.1",
    author="Ginan-Team",
    author_email="rmaj@frontiersi.com.au",
    description="Testing installation of External Package from GitHub repo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ronaldmaj/testexprep",
    project_urls={"Bug Tracker": "https://github.com/ronaldmaj/testexprep/issues"},
    license="MIT",
    packages=["testexprep"],
    install_requires=["unlzw"],
)
