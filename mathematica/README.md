# State
State is a Mathematica package for assisting in the derivation of the equations of state for a dynamic system. It was originally developed by Joseph L. Garbini at the University of Washington, who continues to contribute to its development, along with Rico A.R. Picone of Saint Martin's University and Cameron N. Devine.

## Installation
Clone or download the repository. 

To fully install, copy the `State.m` Mathematica package file to a directory in your Mathematica *path* (to see which directories are in your path, evaluate `$Path` in a Mathematica notebook). It is recommended to use the path that is returned by Mathematica when you evaluate `FileNameJoin[{$UserBaseDirectory, "Applications"}]`.

Another option for full installation is to 

- open Mathematica, 
- select `File > Install...`, 
- select `Package` from the `Type of Item to Install` menu,
- select `State.m` from the `Source > File...` dialog, and
- select `OK`.

Once `State` is fully installed, it can be loaded into a Mathematica notebook with the command

    <<State`

The package can also be loaded from the working directory, which can be set to the notebook's directory with the command

    SetDirectory[NotebookDirectory[]];

If `State.m` is then placed in the same directory as the notebook, it can be loaded with the same command (``<<State` ``) without requiring full installation.

## Getting started
There are example notebooks that show applications. Open the notebooks in Mathematica and run them. They work without fully installing the package.