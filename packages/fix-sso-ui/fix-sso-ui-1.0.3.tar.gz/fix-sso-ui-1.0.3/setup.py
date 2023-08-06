import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
  name = 'fix-sso-ui',         # How you named your package folder (MyLib)
  packages = ['fix_sso_ui'],   # Chose the same as "name"
  version = '1.0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Forked from https://github.com/RistekCSUI/django-sso-ui originally made by fatanugraha, temp. uploaded fix for public access',   # Give a short description about your library
  author="Fata Nugraha",
  author_email="fatanugraha@outlook.com",
  url = 'https://github.com/stevensim226/django-sso-ui',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/stevensim226/django-sso-ui/archive/refs/tags/v1.0.1.tar.gz',    # I explain this later on
  install_requires=["python-cas", "django", "six"],
  classifiers=[
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
  ],
)
