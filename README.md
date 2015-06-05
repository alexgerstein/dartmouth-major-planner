Find the courses that fit.

## Description
Webapp for Dartmouth students to plan their courses for their time at Dartmouth. Instead of individually looking up the courses that you want to take and checking for conflicts. The app scrapes all course catalogue pages and provides a simple interface to select the classes _you_ want to take.

Currently at [www.dartplan.com](http://www.dartplan.com). DartmouthID required.

## Statuses
[![Build Status](https://travis-ci.org/alexgerstein/dartmouth-major-planner.svg?branch=master)](https://travis-ci.org/alexgerstein/dartmouth-major-planner)
[![Coverage Status](https://coveralls.io/repos/alexgerstein/dartmouth-major-planner/badge.svg?branch=master)](https://coveralls.io/r/alexgerstein/dartmouth-major-planner?branch=master)

## Installation
1. Clone repo to computer
2. Install all requirements from requirements.txt

	Virtual environment (preferred):
	1. Create a virtual environment: ```virtualenv flask```
	2. Install requirements: ```flask/bin/pip install -r requirements.txt```
	3. Activate virtual environment: ```. flask/bin/activate```

	System-wide (not the best option): ```sudo pip install -r requirements.txt```

## Run Locally
1. Start up a local server: ```python manage.py server```
2. Start up the scraper: ```python manage.py scrape [--all]``` NOTE: ```--all``` scrapes old ORCs as well as the current ORC and Timetable.

## Tests
* To run the basic unittests, run ```python manage.py tests```.

## License
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
