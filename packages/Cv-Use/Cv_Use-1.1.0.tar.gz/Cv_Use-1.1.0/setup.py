import setuptools

with open("README.md", "r",encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name="Cv_Use",
  version="1.1.0",
  author="ChenShuai-Zhang",
  author_email="aeuna@qq.com",
  description="This is a self-use, simple, module for operating opencv",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)
