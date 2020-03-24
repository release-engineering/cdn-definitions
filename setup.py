from setuptools import setup


def get_description():
    return "Data definitions for Red Hat's content delivery network"


def get_long_description():
    with open("README.md") as f:
        text = f.read()

    # Long description is everything after README's initial heading
    idx = text.find("\n\n")
    return text[idx:]


setup(
    name="cdn-definitions",
    version="0.1.0",
    author="Rohan McGovern",
    author_email="rmcgover@redhat.com",
    packages=["cdn_definitions"],
    url="https://github.com/release-engineering/cdn-definitions",
    license="GNU General Public License",
    description=get_description(),
    include_package_data=True,
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
