import setuptools as SetUpToolS

with open("README.md", "r",encoding="UTF-8") as fh:
  long_description = fh.read()

SetUpToolS.setup(
  name="civilmod",
  version="0.92.52",
  author="nlvac97",
  author_email="ehcemc@outlook.com",
  description="Classic",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://nlvac97.github.io",
  packages=SetUpToolS.find_packages(),
  requires=[
      ],
  install_requires=[
      ],
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)
