from setuptools import setup, find_packages

setup(
    name="tls-verify",
    version="1.2.0",
    author='Christopher Langton',
    author_email='chris@langton.cloud',
    description="Validate the security of your TLS connections so that they deserve your trust.",
    long_description="""# tls-verify
Abandoned, see [trivialscan](https://pypi.org/project/trivialscan/)""",
    long_description_content_type="text/markdown",
    url="https://gitlab.com/trivialsec/trivialscan",
    project_urls={
        "Source": "https://gitlab.com/trivialsec/trivialscan",
        "Documentation": "https://gitlab.com/trivialsec/trivialscan/-/blob/main/docs/0.index.md",
        "Tracker": "https://gitlab.com/trivialsec/trivialscan/-/issues",
    },
    classifiers=[
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
    include_package_data=True,
    install_requires=[
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",

)
