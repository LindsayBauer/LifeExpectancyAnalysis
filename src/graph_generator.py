import os
from get_data import SRC_DIR

from annual_avg_LE import plot_annual_average_LE
from decreasing_LE_trends import plot_trends
from hc_spending_vs_LE import plot_expenditure_versus_LE
from heatmap import plot_heatmap
from LE_by_status import plot_LE_by_status
from LE_change import plot_LE_changes
from LE_histogram import plot_LE_distribution
from LE_timelines import plot_longest_LE_timeline, plot_shortest_LE_timeline
from status_pie_chart import plot_status_pie_chart
from world_maps import plot_worldmap_LE, plot_worldmap_spending
from worldclouds_longest_LE import plot_LE_wordclouds

if __name__ == '__main__':
    os.mkdir(SRC_DIR / "graphs")
    plot_status_pie_chart()
    plot_LE_changes()
    plot_LE_wordclouds()
    plot_longest_LE_timeline()
    plot_shortest_LE_timeline()
    plot_annual_average_LE()
    plot_LE_distribution()
    plot_worldmap_LE()
    plot_LE_by_status()
    plot_trends()
    plot_expenditure_versus_LE()
    plot_worldmap_spending()
    plot_heatmap()

