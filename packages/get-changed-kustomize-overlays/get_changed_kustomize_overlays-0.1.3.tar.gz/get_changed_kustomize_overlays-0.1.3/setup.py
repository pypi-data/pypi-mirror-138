import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="get_changed_kustomize_overlays",
    version="0.1.3",
    author="Gal Shinder",
    author_email="galsh1304@gmail.com",
    description="A tool that helps you to test only those kustomize overlays that were affected by a merge in your CI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/galshi/get-changed-kustomize-overlays",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
