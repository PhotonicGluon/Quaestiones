"""
plotting.py

Created on 2021-01-25
Updated on 2021-01-25

Copyright © Ryan Kan

Description: Plotting functions.
"""

# IMPORTS
import plotly.graph_objects as go

# CONSTANTS
THEME = {
    "autotypenumbers": "strict",
    "coloraxis": {
        "colorbar": {
            "outlinewidth": 0,
            "ticks": ""
        }
    },
    "xaxis": {
        "automargin": True,
        "gridcolor": "#283442",
        "linecolor": "#506784",
        "ticks": "",
        "title": {
            "standoff": 15
        },
        "zerolinecolor": "#283442",
        "zerolinewidth": 2
    },
    "yaxis": {
        "automargin": True,
        "gridcolor": "#283442",
        "linecolor": "#506784",
        "ticks": "",
        "title": {
            "standoff": 15
        },
        "zerolinecolor": "#283442",
        "zerolinewidth": 2
    }
}

# DEBUG CODE
if __name__ == "__main__":
    import plotly.io as pio

    data = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
    positions = list(range(1, len(data) + 1))

    layout = {
        "title": {
            "text": "Test Plot",
            "x": 0.5  # Makes the title centred
        }
    }

    fig = go.Figure(layout={**THEME, **layout})
    fig.add_trace(go.Scatter(x=positions, y=data))
    print(pio.to_json(fig))
