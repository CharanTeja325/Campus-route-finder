import heapq
import math

import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Smart Campus Route Finder", page_icon="🎓")

# ---- Campus map: building name -> (x, y) coordinates in metres ----
# Replace these with your own college's buildings and positions.
BUILDINGS = {
    "Main Gate": (0, 0),
    "Admin Block": (100, 40),
    "Library": (220, 60),
    "CS Department": (300, 160),
    "Canteen": (150, 150),
    "Auditorium": (260, 10),
    "Hostel": (80, 260),
    "Sports Ground": (200, 280),
    "Medical Center": (30, 130),
}

# Walkable paths between buildings (undirected)
PATHS = [
    ("Main Gate", "Admin Block"),
    ("Main Gate", "Medical Center"),
    ("Admin Block", "Library"),
    ("Admin Block", "Canteen"),
    ("Library", "Auditorium"),
    ("Library", "CS Department"),
    ("Canteen", "CS Department"),
    ("Canteen", "Hostel"),
    ("Medical Center", "Hostel"),
    ("Medical Center", "Canteen"),
    ("Hostel", "Sports Ground"),
    ("Canteen", "Sports Ground"),
    ("CS Department", "Sports Ground"),
]


def distance(a, b):
    (x1, y1), (x2, y2) = BUILDINGS[a], BUILDINGS[b]
    return math.hypot(x1 - x2, y1 - y2)


def build_graph():
    graph = {name: [] for name in BUILDINGS}
    for a, b in PATHS:
        d = distance(a, b)
        graph[a].append((b, d))
        graph[b].append((a, d))
    return graph


def a_star(graph, start, goal):
    """A* search. g = distance walked so far, h = straight-line distance to goal."""
    open_heap = [(distance(start, goal), 0.0, start)]
    came_from = {}
    g_score = {start: 0.0}
    explored = 0

    while open_heap:
        f, g, current = heapq.heappop(open_heap)
        if g > g_score.get(current, float("inf")):
            continue  # stale entry
        explored += 1

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1], g, explored

        for neighbour, cost in graph[current]:
            new_g = g + cost
            if new_g < g_score.get(neighbour, float("inf")):
                g_score[neighbour] = new_g
                came_from[neighbour] = current
                heapq.heappush(open_heap, (new_g + distance(neighbour, goal), new_g, neighbour))

    return None, float("inf"), explored


def draw_map(path=None):
    fig, ax = plt.subplots(figsize=(7, 6))
    for a, b in PATHS:
        (x1, y1), (x2, y2) = BUILDINGS[a], BUILDINGS[b]
        ax.plot([x1, x2], [y1, y2], color="lightgray", linewidth=2, zorder=1)

    if path:
        xs = [BUILDINGS[p][0] for p in path]
        ys = [BUILDINGS[p][1] for p in path]
        ax.plot(xs, ys, color="crimson", linewidth=4, zorder=2)

    for name, (x, y) in BUILDINGS.items():
        on_path = path and name in path
        ax.scatter(x, y, s=140, color="crimson" if on_path else "steelblue", zorder=3)
        ax.annotate(name, (x, y), textcoords="offset points", xytext=(0, 10),
                    ha="center", fontsize=8)

    ax.set_aspect("equal")
    ax.axis("off")
    return fig


# ---- UI ----
st.title("🎓 Smart Campus Route Finder")
st.caption("Finds the shortest walking route between two campus locations using the A* algorithm.")

graph = build_graph()
places = sorted(BUILDINGS)

col1, col2 = st.columns(2)
start = col1.selectbox("From", places, index=places.index("Main Gate"))
goal = col2.selectbox("To", places, index=places.index("CS Department"))

if st.button("Find shortest route", type="primary"):
    if start == goal:
        st.warning("Start and destination are the same.")
        st.pyplot(draw_map())
    else:
        path, total, explored = a_star(graph, start, goal)
        if path is None:
            st.error("No route found between these locations.")
            st.pyplot(draw_map())
        else:
            st.success(" → ".join(path))
            m1, m2, m3 = st.columns(3)
            m1.metric("Distance", f"{total:.0f} m")
            m2.metric("Walking time", f"{total / 80:.1f} min")  # ~80 m/min
            m3.metric("Nodes explored", explored)
            st.pyplot(draw_map(path))
else:
    st.pyplot(draw_map())

with st.expander("How A* works here"):
    st.write(
        "A* picks the next location with the lowest f = g + h, where g is the distance "
        "walked so far and h is the straight-line distance to the destination. "
        "Because h never overestimates, the route found is guaranteed to be the shortest."
    )
