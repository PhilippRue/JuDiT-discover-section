# Functions to plot host DOS

from .global_settings import *
import bokeh.plotting as bkp
from aiida.orm import load_node
from bokeh.models import ColumnDataSource
import numpy as np


def get_data_dos():

    # load DOS data
    Sb2Te3_6QL_DOS = load_node(UUID_HOST_DOS) # +/-5eV
    dos_data = Sb2Te3_6QL_DOS.outputs.dos_data_interpol

    xlbl, x, xunit = dos_data.get_x()
    xlbl += ' ('+xunit+')'
    # shift Fermi level
    x += EF0

    ylbl, y, yunit = dos_data.get_y()[0] # total dos
    ylbl += ' ('+yunit+')'

    # find values for gap region
    ymax = max(np.sum(y[1::2,:], axis=0) - np.sum(y[0::2,:], axis=0))
    
    # create dos source for plotting with bokeh
    #                                     E-EF    (        spin up     )   (     -spin down     )
    source = ColumnDataSource(data=dict(x=x[0], y=np.sum(y[1::2,:], axis=0) - np.sum(y[0::2,:], axis=0),
                                       )
                             )
    
    return source, ymax



def plot_dos():
    
    # prepare DOS data
    source_dos, ymax = get_data_dos()

    # open bokeh figure
    # for paper plot:
    #dos_plot = bkp.figure(plot_width=500, plot_height=300, y_range = [0, ymax*1.05], x_range=[-4, 3])
    dos_plot = bkp.figure(plot_width=400, plot_height=400, y_range = [0, ymax*1.05], x_range=[-4, 3],
                          tools='pan,box_zoom,wheel_zoom,reset,save',)

    # set title and axis labels for DOS plot
    dos_plot.title.text = "Sb2Te3 6QL DOS"
    dos_plot.xaxis.axis_label = 'E (eV)'
    dos_plot.yaxis.axis_label = 'DOS (states/eV)'
    
    gapwidth = gapend - gapstart
    
    # add vbar (blue) to right plot
    dos_plot.vbar(x=gapstart+gapwidth/2, width=gapwidth, bottom=-0.1*ymax, top=ymax*1.2, color='lightblue', 
            alpha=0.4, name='grey')

    # plot DOS data
    dos_plot.line('x', 'y', source=source_dos, line_width=3, line_alpha=0.6, color='black', legend_label='total DOS')
    
    # add lines
    dos_plot.line([0.2, 0.2], [-200, 200], line_width=1, line_alpha=0.8, color='green', legend_label='+200meV')
    dos_plot.line([-0.2, -0.2], [-200, 200], line_width=1, line_alpha=0.8, color='red', legend_label='-200meV')

    dos_plot.legend.location = "bottom_left"
    dos_plot.legend.click_policy="hide"
    
    dos_plot.grid.visible = False


    return dos_plot, ymax