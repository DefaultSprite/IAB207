# IAB207 Assignment
Event website implementing Flask, Bootstrap, HTML and CSS for assignment.

## TODO List
 - [ ] Set up base website
 - [ ] Distribute Tasks 

## Setting up a virtual environment
Setting up a virtual environment can be useful as different projects will most likely require different version packages.
Isolating your project so that it only requires certain packages can be beneficial, and in this case I would suggest it,
but it isn't mandatory.

It is similar to how we set up the python anywhere server, and serves a similar purpose.

---

**Setting up the Virtual Environment** <br>
Make sure you are in the project directory in where in the console it should end in `IAB207/` and type the following to
create a virtual environment.
```
python -m venv .venv
cd .venv/Scripts
.\Activate.ps1
```
It is highly probable that you will get an error of some sort. For that you can refer here
https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy?view=powershell-7.3

For a quick and easy way of enabling scripts in powershell.
```Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser```

After that execute this command to install all the required packages
```
pip install -r requirements.txt
```
and you're done!

## Getting Submodule Files
Navigate to the parent directory of the submodule then,
```
git submodule init
git submodule update
```
This way you can get all of the example code.