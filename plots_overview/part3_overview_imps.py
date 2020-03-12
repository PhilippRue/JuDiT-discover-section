#!/usr/bin/env python
# coding: utf-8


import panel as pn

pn.extension()


# load aiida
from aiida import load_profile
profile = load_profile()


from plots_overview.load_data import load_imp_properties

totimp_num_text = '#### Total number of impurities: {}'.format(len(list(load_imp_properties().keys())))
print(totimp_num_text)


"""
# add tap tool to scatter plot

from bokeh.models import TapTool
callback_tap = CustomJS()
tap = TapTool(callback=callback_tap)

scatterplot.add_tools(tap)
"""

from plots_overview.plot_periodic_table import periodic_table_with_buttons
from plots_overview.scatter_plot import make_scatterplot_with_hist


layout_periodic_table = periodic_table_with_buttons()
layout_with_hist = make_scatterplot_with_hist()

# combine plots
layout = pn.Column(pn.pane.Markdown("## Average values for different impurity configurations"), 
                   layout_periodic_table,
                   pn.pane.Markdown("## Scatter plot"),
                   layout_with_hist,
                   sizing_mode='stretch_both')

imps_overview = pn.Row(layout)


imps_overview


