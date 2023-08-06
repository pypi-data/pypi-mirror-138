from setuptools import setup, find_packages

setup(
  name="dankware",
  version="1.2",
  author="SirDank",
  author_email="SirDankenstein@protonmail.com",
  description="Python module with various features.",
  long_description=open("README.md").read(),
  long_description_content_type="text/markdown",
  url="https://github.com/SirDankenstien/dankware",
  project_urls={
    "GitHub": "https://github.com/SirDankenstien/dankware",
    "Bug Tracker": "https://github.com/SirDankenstien/dankware/issues",
  },
  license="MIT",
  keywords="dankware",
  classifiers = [
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  "Development Status :: 5 - Production/Stable",
  "Intended Audience :: Education"
  ],
  package_dir={"": "."},
  packages=find_packages(where="."),
  install_requires=['alive-progress', 'colorama']
)