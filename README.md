# Python URL shortener REST API

### Main features:
- POST to /shorten json in the format {"url": "url_to_shorten"} in order to get a short url for it.
- On GET request to /<short_url>, user will be redirected to the full url.
- Added limit of 5 POST request per day for ip+user agent combination.
- In order to "protect" against multiple requests from the same agents, from the 6th POST request user will be redirected to a website that delays 5 seconds before returning a response.

### Install dependencies:
Execute `pip install -r requirements.txt`

### How to run tests:
Execute `pytest`

### How to Run:
Execute `flask run`

### Improvements:
* user_attempts should be persisted so that it works even after service restart and also prevent it from being locked
* Change db to increase parallel request possibilities
* Move away from flask dev server to a production suitable one
* Containerize and put a load balancer in front
* Add UI
* Add factory pattern for app/db creation
