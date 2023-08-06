from setuptools import setup
import os

VERSION = "0.2"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="strip-hidden-form-values",
    description="CLI tool for stripping hidden form values from an HTML document",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/strip-hidden-form-values",
    project_urls={
        "Issues": "https://github.com/simonw/strip-hidden-form-values/issues",
        "CI": "https://github.com/simonw/strip-hidden-form-values/actions",
        "Changelog": "https://github.com/simonw/strip-hidden-form-values/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["strip_hidden_form_values"],
    entry_points="""
        [console_scripts]
        strip-hidden-form-values=strip_hidden_form_values.cli:cli
    """,
    install_requires=["click"],
    extras_require={"test": ["pytest"]},
    python_requires=">=3.6",
)
