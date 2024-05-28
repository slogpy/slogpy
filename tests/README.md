# slogpy testing
slogpy uses Poetry and has several dependencies included for development.

## Running the tests
* Start from the install location
* Make sure you have created the virtual environment
(this typically only needs to be done once, but doesn't hurt to do again)
    * ```poetry install```
* Now you have to be in the virtual environment
    * ```poetry shell```
* Run all of the tests using pytest
    * ```pytest tests```

## Getting Code Coverage of the tests
* Make sure you are in the virtual environment
    * ```poetry shell```
* Run the tests while also getting code coverage
    * ```coverage run -m pytest tests```
* Get the code coverage report
    * ```coverage report```
