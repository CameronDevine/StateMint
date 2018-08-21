# State Model RnD

[![Build Status](https://travis-ci.org/CameronDevine/StateModelRnD.svg?branch=master)](https://travis-ci.org/CameronDevine/StateModelRnD)
[![PyPI](https://img.shields.io/pypi/v/StateModelRnD.svg)](https://pypi.org/project/StateModelRnD/)
[![License](https://img.shields.io/github/license/CameronDevine/StateModelRnD.svg)](../blob/master/LICENSE)


This library is used to take the elemental equations and constraint equations of a system and find a differential equation in a standard form. This script is a port from a Mathematica notebook with the same functionality but was ported to allow it to be run using an AWS Lambda function, allowing anyone to run the code without having Python/sympy or Mathematica installed.

## Installation

State Model RnD can be run a python library on your computer or with the `StateModelLambda.py` file it can be deployed as an AWS Lambda function. the instructions for both installations are below.

### Local Installation

StateModelRnD can be installed on a local machine using the steps below.

1. Clone the git repository to a local directory.
2. Make sure sympy is installed. The easiest way to do this is with `pip` using the command, `pip install sympy`.
3. Move the `StateModelRnD.py` file to a location where `python` will be able to find it.

### AWS Lambda Installation

The Python implementation of State Model RnD was originally written to work with AWS Lambda. An installer script has been created to simplify this procedure.

1. Clone the git repository.
2. Create an AWS account at [https://aws.amazon.com/](https://aws.amazon.com/ "Amazon AWS").
3. Install Python 2, [https://www.python.org/downloads/](https://www.python.org/downloads/ "Python downloads").
4. Install Boto3 by running `pip install boto3`.
5. Configure Boto3 as per [http://boto3.readthedocs.io/en/latest/guide/quickstart.html#configuration](http://boto3.readthedocs.io/en/latest/guide/quickstart.html#configuration "Boto3 Configuration").
6. Run the installer Python script located at `installer/install.py`.
7. Upload the files in the `HTML` directory to your webserver of choice.

Steps 6 and 7 can be repeated after running `git pull` to update the Lambda function and other AWS settings.

### Manual AWS Lambda Installation

The AWS Lambda function can also be installed manually. Instructions on how to do this are located in the `MANUAL_INSTALL.md` file.

## Credits

Original Mathematica Notebook: Joseph Garbini

Python/sympy port: Cameron Devine
