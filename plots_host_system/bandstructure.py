# Functions to plot bandstructure

# make all global settings available here
from .global_settings import *
import bokeh.plotting as bkp
from aiida.orm import load_node
from bokeh.models import Label

def load_bandstruc_data():

    Sb2Te3_6QL_bandstruc = load_node(UUID_HOST_BANDSTRUC) # -0.5eV..+0.3eV, corrected K-path

    if 'saved_data_dispersion.npy' in Sb2Te3_6QL_bandstruc.outputs.retrieved.list_object_names():
        # load data
        import numpy as np
        with Sb2Te3_6QL_bandstruc.outputs.retrieved.open('saved_data_dispersion.npy') as f:
            fn = f.name
        data_bandstruc = np.load(fn)
    else:
        raise ValueError('Could not load bandstructure data')

    with Sb2Te3_6QL_bandstruc.outputs.retrieved.open('output.0.txt') as f:
        ef = [float(i.split('=')[2].split()[0]) for i in f.readlines() if 'Fermi' in i][0]

    ne = len(set(data_bandstruc[:,0]))
    nk = int(len(data_bandstruc)/ne)
    data_bandstruc = data_bandstruc.reshape(ne,nk,-1)


    y = (data_bandstruc[:,0,0] - ef)*13.6 + EF0
    x = data_bandstruc[0,:,2] - data_bandstruc[0,:,3]
    dtot = data_bandstruc[:,:,5]
    
    return x, y, dtot


def plot_bandstruc():
    x, y, dtot = load_bandstruc_data()

    x_range=[-0.6,0.4] #x.min(),x.max()]
    y_range=[y.min(),y.max()]

    dw = x_range[1]-x_range[0]
    dh = y_range[1]-y_range[0]

    # for paper plot:
    #p = bkp.figure(plot_width=500, plot_height=350,
    p = bkp.figure(plot_width=350, plot_height=400, 
                   tools='pan,box_zoom,wheel_zoom,reset,save',
               #tooltips=[("x", "$x"), ("y", "$y")],
               x_range=x_range, y_range=y_range)

    # must give a vector of image data for image parameter
    p.image(image=[-dtot], x=x_range[0], y=y_range[0], dw=dw, dh=dh, palette="Greys256")


    p.title.text = "Sb2Te3 6QL bandstructure"
    p.yaxis.axis_label = 'E-EF (eV)'

    p.xaxis.ticker = [-0.6, 0, 0.4]
    p.xaxis.major_label_overrides = {-0.6: 'M', 0: 'Gamma', 0.4: 'K'}

    #bkp.show(p)
    return p


def add_ef_lines_bandstruc(bandstruc_plot, ymax):


    gapwidth = gapend - gapstart

    # add hbar (blue) to left plot
    bandstruc_plot.hbar(y=gapstart+gapwidth/2, height=gapwidth, left=-0.1*ymax, right=ymax*1.2, color='lightblue', 
           alpha=0.4, name='grey')

    # add lines for other EF positions
    bandstruc_plot.line([-2, 2], [0.2, 0.2], line_width=1, line_alpha=0.8, color='green', legend_label='+200meV')
    bandstruc_plot.line([-2, 2], [-0.2,-0.2], line_width=1, line_alpha=0.8, color='red', legend_label='-200meV')

    # make legend and allow lines to disappear on click
    bandstruc_plot.legend.location = "top_left"
    bandstruc_plot.legend.click_policy="hide"

    # add text to label bulk band gap region
    band_gap_text = Label(x=-0.55, y=-0.01, x_units='data', y_units='data',
                          text='bulk band gap', render_mode='css',
                         )
    bandstruc_plot.add_layout(band_gap_text)
