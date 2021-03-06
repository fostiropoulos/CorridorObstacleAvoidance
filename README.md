# Corridor Obstacle Avoidance
Simplified problem of identifying an obstacle in a corridor using signal processing techniques and
determining if should turn left or right.

Graphical Explanation of the problem:
![Depth Map](img/Explanation.png?raw=true "Explanation")

### Input

From an Original Image, using various techniques we can generate a Depth Map. The original Image could look like:
<p align="center">
  <img src="img/original.png">
</p>
Provided a depth map such as the one below:
<p align="center">
  <img src="img/index.png">
</p>

Determines clearance on left and right such as the image below:
<p align="center">
  <img src="img/index6.png">
</p>
Observe the left green and right orange line, the clearance is for an infinitely tall object, hence the lines stop and take into consideration the uneven width of the object into calculating the clearance. The clearance then is the minimum distance between the object and corridor.


### EDA

`CorridorAvoidanceEDA.ipynb`

### Python Utility Requirements

python 3.x

`pip install -r requirements.txt`


### Usage

`python find_clearance.py filename`

### Output

` [right/left] [clearance in m] `
