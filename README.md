# iReporterApi

[![Build Status](https://travis-ci.org/ringtho/iReporterApi.svg?branch=develop)](https://travis-ci.org/ringtho/iReporterApi) [![Coverage Status](https://coveralls.io/repos/github/ringtho/iReporterApi/badge.svg?branch=develop)](https://coveralls.io/github/ringtho/iReporterApi?branch=develop)  [![Maintainability](https://api.codeclimate.com/v1/badges/adefe911915e872403c5/maintainability)](https://codeclimate.com/github/ringtho/iReporterApi/maintainability)


## Overview
Corruption is a huge bane to Africa’s development. African countries must develop novel and localised solutions that will curb this menace, hence the birth of iReporter. iReporter enables any/every citizen to bring any form of corruption to the notice of appropriate authorities and the general public. Users can also report on things that needs government intervention.

This iReporter Api serves to create, edit, delete and retrieve redflag incidents that have been already created.
The endpoints are deployed at [iReporter Heroku](https://sringtho.herokuapp.com)

# Features

A user can:

- get all redflags in the database
- get a particular redflag in the database using its id
- edit the location of a particular redflag
- edit the comment of a particular redflag
- delete a particular redflag

## API Description ##
The ireporter API is implemented in flask, a python microframework. Version 1 of the API is hosted on Heroku and can be accessed at https://sringtho.herokuapp.com.
The corresponding endpoints and their functionalities are described below

|Endpoint                                       | Function                          
|-----------------------------------------------|----------------------------------------------
|POST /api/v1/red-flags                         | adds a redflag to the database(list)
|GET /api/v1/red-flags                          | retrieves all redflags stored in the database
|GET /api/v1/red-flags/<red_flag_id>            | retrives a particular redflag based on its id
|PATCH /api/v1/red-flags/<red_flag_id>/location | edit the location of a particular redflag 
|PATCH /api/v1/red-flags/<red_flag_id>/comment  | edit the comment of a particular redflag
|DELETE /api/v1/red-flags                       | deletes a particular redflag

When using the API and example of the input data for creating a redflag is shown below:
```javascript
{
   	"createdBy": 1,
	"types": "redflag",
	"location": "arua",
	"status": "rejected",
	"images": ["pog.png", "redflag.jpg"]
	"videos": ["vid.mp4","corrupt.mkv"],
	"comment": "smith"
	
}
```
NOTE:
* CeatedBy should by all means be an integer and is a required field

## Installation Instructions
To run the API, follow these steps:
* Clone this repository onto your computer
* Install python3 and postman
* Navigate to the repository root (fast-food-fast) and create a virtual environment
```
$ cd ireporterApi
$ virtualenv venv
```
* Activate the virtual environment and install dependencies in requirements.txt
```
$ source venv/bin/activate
$ pip install -r requirements.txt
```
* Run the app.py script
```
$ python app.py
```
* Test the API endpoints using Postman

## Contributors
* Ringtho J. Smith - *sringtho@gmail.com*



