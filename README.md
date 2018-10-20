# Corridor Obstacle Avoidance
Simplified problem of identifying an obstacle in a corridor using signal processing techniques and
determining if should turn left or right.

Graphical Explanation of the problem:
![Depth Map](img/Explanation.png?raw=true "Explanation")

### Input

From an Original Image, using various techniques we can generate a Depth Map. The original Image could look like:
![Original Image](img/original.png?raw=true "Original Image")

Provided a depth map such as the one below:
![Depth Map](img/index.png?raw=true "Depth Map")

Determines clearance on left and right such as the image below:

![Depth Map](img/index6.png?raw=true "Clearance Detection")

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
