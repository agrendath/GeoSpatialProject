
# INFOH509

## Easy Boarding
This project aims to provide a solution to guide passengers to the best place on a platform to board the carriage of their choice.

Passengers are often faced with uncertainty when waiting for their train on a platform. They often lack information about

- The side of the platform from which the train will arrive and depart.
- The length of the train in relation to the platform.
- The specific features of each carriage, such as first class, PRM carriages, bicycle carriages, the quiet zone, etc.
- How to avoid certain parts of the train if the arrival platform is shorter than the length of the train.
- All these uncertainties can lead to confusion and even delays in boarding, especially on crowded platforms.

## Installation

1. Clone the repository :

    ```
    git clone https://github.com/agrendath/GeoSpatialProject.git
    ```

2. Access the project file :

    ```
    cd GeoSpatialProject
    ```

3. Install the dependencies :

    ```
    pip install -r requirements.txt
    ```
   
## Usage

To start the project you can run `python app.py`.
And then go to the url indicated: http://127.0.0.1:5000/

By default, the information displayed is that for the departures of voice 2 in Brussels North.
You can change this by modifying this part of the code in the index.py file
and the function of the same name.

````python
def index():
    station = "Brussels North"
    station_overpass_name = "Bruxelles-Nord - Brussel-Noord"
    platform = 2
````

## Contributors

Vilain Léandre
Jadot Jérôme
Lefranc Antoine
Leal Mendo