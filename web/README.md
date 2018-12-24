## Web Interface

[![Build Status](https://travis-ci.org/CameronDevine/StateMint.svg?branch=master)](https://travis-ci.org/CameronDevine/StateMint)

To allow easy use the functionality in StateMint a web interface was created.
This interface allows students and other to take advantage of this tool without the need to install Python or Mathematica.
An example of this interface is running [here](statemint.stmartin.edu).

### Usage

This interface uses the Python StateMint [package](../python/README.md) in an AWS Lambda function to perform the symbolic mathematics.
Equations can be entered in text boxes on the webpage, then the Lambda function is used to find the result which can be displayed in multiple forms for copying into Python, Mathematica, Matlab or LaTeX.
These systems can also be saved or downloaded for later modification or use.

### Installation

To make copy of this interface, start our by creating an Amazon AWS account.
Next, make sure Python's `pip` is installed.
Finally run `make` in this directory.
If not done previously this will prompt you to set up the AWS CLI, see [this link](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) for details.
When the command has completed successfully, copy the contents of the `HTML` directory to your favorite static web host.
