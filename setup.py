from setuptools import setup, find_packages


def get_description():
    return "Data definitions for Red Hat's content delivery network"


def get_long_description():
    with open("README.md") as f:
        text = f.read()

    # Long description is everything after README's initial heading
    idx = text.find("\n\n")
    return text[idx:]


def get_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    name="cdn-definitions",
    version="3.4.1",
    author="Rohan McGovern",
    author_email="rmcgover@redhat.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/release-engineering/cdn-definitions",
    license="GNU General Public License",
    description=get_description(),
    include_package_data=True,
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    install_requires=get_requirements(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={
        "Documentation": "https://release-engineering.github.io/cdn-definitions/",
        "Changelog": "https://github.com/release-engineering/cdn-definitions/blob/master/CHANGELOG.md",
    },
)
