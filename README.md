# State Model RnD

This library is used to take the elemental equations and constraint equations of a system and find a differential equation in a standard form. This script is a port from a Mathematica notebook with the same functionality but was ported to allow it to be run using an AWS Lambda function, allowing anyone to run the code without having Python/sympy or Mathematica installed.

## Installation

State Model RnD can be run a python library on your computer or with the `StateModelLambda.py` file it can be deployed as an AWS Lambda function. the instructions for both installations are below.

### Local Installation
StateModelRnD can be installed on a local machine using the steps below.

1. Clone the git repository to a local directory.
2. Make sure sympy is installed. The easiest way to do this is with `pip` using the command, `pip install sympy`.
3. Move the `StateModelRnD.py` file to a location where `python` will be able to find it.

### AWS Lambda Installation
The Python implementation of State Model RnD was originally written to work with AWS Lambda. The following steps will allow you to integrate State Model RnD into your website.

1. Create an AWS account at [https://aws.amazon.com/](https://aws.amazon.com/ "Amazon AWS").
2. Clone the git repository to a directory on your machine.
3. Either use the provided zip file and skip to step 8, or create your own using the steps below.
4. Download `sympy` and `mpmath` to this directory using, `pip download sympy mpmath`.
5. Extract the contents of the compressed files.
6. Copy the `sympy` directory found inside the `sympy-1.0` folder to the same directory as the `StateModelRnD.py` and `StateModelLambda.py` files. Do the same for mpmath.
7. Combine together in a zip file `StateModelRnD.py`, `StateModelLambda.py`, the `sympy-1.0` directory, and the `mpmath-0.19` directory. (Note: these versions are as of April 12, 2017)
8. Go to [https://aws.amazon.com/](https://aws.amazon.com/ "Amazon AWS"), sign into the console, and go to the AWS Lambda console.
9. Click "Create a Lambda function".
10. Select the Blank Function blueprint.
11. Click on the dashed outline box and select "API Gateway" as the trigger.
12. Give the API the name "StateModelRnD". Name the deployment stage, I chose "beta". Finally, chose Open for the security.
13. Name the Lambda function. I chose "StateModelRnD" again. Add a description if you wish, and select "Python 2.7" as the runtime.
14. Select "Upload a .ZIP file" under lambda code, and upload the zip file you created in step 5.
15. For the handler enter `StateModelLambda.handler`.
16. Under "Role" select Create a custom role. When the new tab opens save the existing code by clicking Allow, which should be similar to,
~~~~
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
~~~~
17. Under Advanced settings change the memory to 768 MB and the timeout to 10 seconds.
18. Press next and on the next page review the settings and click Create function.
19. Under Actions choose "Configure test event" and enter the code below, and click "save and test". If any errors come up during this test let me know.
~~~~
{"queryStringParameters": {
  "InVars": "vS",
  "StVarElEqns": "vMB' = 1/MB * fMB, vMW' = 1/MW * fMW, fKS' = KS * vKS, fKT' = KT * vKT",
  "OtherElEqns": "fBS = BS * vBS, fBT = BT * vBT",
  "Constraints": "fMB = fKS + fBS, fMW = fKT + fBT - fKS - fBS, vKS = vMW - vMB, vKT = vS - vMW, vBS = vMW - vMB, vBT = vS - vMW",
  "OutputVars": "vMB vMW fKS fKT fBS fBT",
  "OutputType": "Equation"
}
}
~~~~
20. Navigate to the AWS API Gateway console, and select the StateModelRnD API.
21. Under Actions select Create Method. Then select POST and click the checkmark.
22. For Integration type choose Lambda Function. Check the Use Lambda Proxy integration box. Select the region your Lambda function was created in, and enter the name of your Lambda function. Click save.
23. Click "Integration Request" and make sure that "Use Lambda Proxy integration" is checked.
24. Click "Method Response" then "Add Response". Enter 400 as the status, then under 400 click "Add Header" and enter `Access-Control-Allow-Origin`. Then click "Add Response Model", and enter `application/json` as the content type and select Empty for the model.
25. Select the "Any" method and click Actions, Delete Method.
26. Click Actions, Enable CORS, and accept the default values.
27. Click Actions, Deploy API, and select the stage name you entered in step 11.
28. Click SDK Generation and select JavaScript as the platform, then click Generate SDK. Download this zip file to the same folder as the rest of your files and unzip it.
29. Copy the `StateModelRnD.html` and `StateModelRnD.js` files into the `apiGateway-js-sdk` folder.
30. Edit the `StateModelRnD.html` file to add your preferred styling.
31. Upload the `StateModelRnD.html`, `StateModelRnD.js`, `apigClient.js` files and the `lib` directory to your webserver of choice.

## Credits

Original Mathematica Notebook: Joseph Garbini

Python/sympy port: Cameron Devine
