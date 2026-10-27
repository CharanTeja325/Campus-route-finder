# Smart Campus Route Finder

## Overview

Smart Campus Route Finder is a Python project that finds the shortest walking route between different locations in a college campus using the **A* (A-Star) Search Algorithm**. The application provides an interactive interface where users can select a starting point and destination to view the shortest path on a campus map.

## Features

* Find the shortest route between campus buildings.
* Visual campus map.
* Displays total distance.
* Estimates walking time.
* Shows the number of nodes explored.

## Technologies Used

* Python
* Streamlit
* Matplotlib

## Algorithm

This project uses the **A*** algorithm.

**Formula:**

```
f(n) = g(n) + h(n)
```

* **g(n):** Distance travelled from the start.
* **h(n):** Estimated distance to the destination.

The algorithm finds the shortest path efficiently using a heuristic approach.

## How to Run

Install the required packages:

```bash
pip install streamlit matplotlib
```

Run the application:

```bash
streamlit run app.py
```

## Future Improvements

* Live GPS support
* Mobile application
* More campus locations
* Multiple route options

B.Tech - Computer Science and Engineering
