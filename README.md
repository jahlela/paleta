## Synopsis

Paleta is a programmatic color palette generator that uses k-means clustering to return the dominant color palette in an image. It also has user profiles with secure logins.

## Stack

Python backend, PostgreSQL database, Flask server, SQLalchemy, Jinja templating

## Features
* Submit Image
    * Users can submit any image URL to get a palette
![N|Solid](https://cloud.githubusercontent.com/assets/6724153/20730509/2c145dce-b63b-11e6-8f71-e6997e462b88.png)
* User Profile 
    * Review and remove images
![N|Solid](https://cloud.githubusercontent.com/assets/6724153/20730507/2af62e40-b63b-11e6-9b3b-a6f9767bce00.png)

* Image Gallery
    * Browse all images in the project
    * Add images to profile
![N|Solid](https://cloud.githubusercontent.com/assets/6724153/20730515/2ec9047a-b63b-11e6-92fa-8a92bb8e7088.png)

* Search for images by similar color
    *   Search for images with a similar color in their palette
![N|Solid](https://cloud.githubusercontent.com/assets/6724153/20730511/2d71d4d0-b63b-11e6-9dea-041ef37adc88.png)


## Installation

Install the dependencies and start the server.

```sh
$ cd paleta
$ pip install virtualenv
$ virtualenv env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
(env) $ python server.py
```

## Tests

There are tests covering all routes and the k-means computations.

## Contributors

Please feel free to fork this project or to submit pull requests.

## License

This project is licensed under the terms of the MIT license.