"""
2d_scatter_plot_example.py

This script demonstrates generating 2D scatter plots using Matplotlib and Plotly.
It creates random data points, labels them, and visualizes two sets of points with
different colors. The script includes:
- Matplotlib scatter plot with text labels and grid.
- Plotly scatter plots with hover-only labels and visible text labels.
- Performance timing for both libraries.
Ideal for learning and reference in creating 2D visualizations.

Author: Aston Li
Created: May 14, 2025
"""

import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px


def matplotlib_show(
    x_points: np.ndarray,
    y_points: np.ndarray,
    point_labels: list[str],
    save: bool = False,
) -> None:
    # Matplotlib
    start_time = time.time()
    try:
        plt.figure(figsize=(16, 9), dpi=100)  # optional

        plt.scatter(x_points, y_points, color="blue", s=20, marker="o")
        plt.scatter(x_points + 100, y_points + 100, color="red", s=30)

        for i, (xi, yi) in enumerate(zip(x_points, y_points, strict=True)):
            plt.text(
                xi,
                yi,
                str(point_labels[i]),
                fontsize=9,
                ha="left",
                va="bottom",
            )

        # custom range
        # plt.xlim(-5, max(x_points) * 1.2)
        # plt.ylim(-5, max(y_points) * 1.2)

        # Set the x/y-axis maximum to 1.2 times the data's maximum value, with
        # the minimum determined automatically
        plt.xlim(None, max(x_points) * 1.2)
        plt.ylim(None, max(y_points) * 1.2)

        plt.xlabel("X-Axis")
        plt.ylabel("Y-Axis")
        plt.title("Scatter Plot with Number Labels")
        plt.grid(True)

        # plt.tight_layout()
        if save:
            plt.savefig("matplotlib_scatter.png")
        plt.show()
        plt.close()
    except Exception as e:
        print("Matplotlib failed：", e)

    matplotlib_time = time.time() - start_time
    print(f"Matplotlib: {matplotlib_time:.4f} 秒")


def plotly_show(
    x_points: np.ndarray,
    y_points: np.ndarray,
    point_labels: list[str],
    hover_only: bool,
    save: bool = False,
) -> None:
    # Plotly
    start_time = time.time()
    try:
        df_a = pd.DataFrame(
            {
                "X-Axis": x_points,
                "Y-Axis": y_points,
                "label": point_labels,
                "Source": "A",
            }
        )
        df_b = pd.DataFrame(
            {
                "X-Axis": x_points + 100,
                "Y-Axis": y_points + 100,
                "label": point_labels,
                "Source": "B",
            }
        )
        df_all = pd.concat([df_a, df_b])

        if hover_only:
            fig = px.scatter(
                df_all,
                x="X-Axis",
                y="Y-Axis",
                color="Source",
                hover_data=["label"],
                color_discrete_map={"A": "blue", "B": "red"},
            )
        else:
            # fig = px.scatter(x=x_points, y=y_points, text=point_labels)
            fig = px.scatter(
                df_all,
                x="X-Axis",
                y="Y-Axis",
                color="Source",
                text="label",  # label show on point
                hover_data=["X-Axis", "Y-Axis", "label"],  # hover
                color_discrete_map={"A": "blue", "B": "red"},
            )
            fig.update_traces(textposition="top center")

            fig.update_traces(
                hovertemplate="%{text}<br>X: %{x}<br>Y: %{y}<extra></extra>"
            )

        # Set the x/y-axis range with the maximum at 1.2 times the data's
        # maximum value, leaving the minimum to be set automatically
        fig.update_xaxes(range=[None, max(x_points) * 1.2])
        fig.update_yaxes(range=[None, max(y_points) * 1.2])
        fig.update_layout(
            title="Scatter Plot with Number Labels",
            # xaxis={"range": [-5, max(x_points) * 1.2]},
            # yaxis={"range": [-5, max(y_points) * 1.2]},
            font={"size": 12},
        )

        if save:
            fig.write_image(
                "plotly_scatter.png",
                format="png",
                width=1600,
                height=900,
                scale=1,
            )
        fig.show()
    except Exception as e:
        print("Plotly failed：", e)

    plotly_time = time.time() - start_time
    print(f"Plotly: {plotly_time:.4f} 秒")


if __name__ == "__main__":
    np.random.seed(42)
    # x = np.random.rand(10000)
    # y = np.random.rand(10000)
    # x = np.random.uniform(low=0, high=100, size=50)
    # y = np.random.uniform(low=0, high=100, size=50)
    x: np.ndarray = np.round(
        np.random.uniform(low=0, high=2000, size=50), decimals=2
    )
    y: np.ndarray = np.round(
        np.random.uniform(low=0, high=2000, size=50), decimals=2
    )
    labels: list[str] = [f"ID.{i}" for i in range(len(x))]

    save_image: bool = True

    matplotlib_show(x, y, labels, save=save_image)

    plotly_show(x, y, labels, hover_only=False, save=save_image)
