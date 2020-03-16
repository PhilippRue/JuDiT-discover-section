### Overview of impurity properties

import panel as pn
from plots_overview.load_data import load_imp_properties
from global_settings import website_width
from bokeh.sampledata.periodic_table import elements
import numpy as np
from matplotlib.cm import plasma, inferno, magma, viridis

from aiida import load_profile
load_profile()





# tick formatters
from bokeh.models import PrintfTickFormatter
formatter_int = PrintfTickFormatter(format='%i')
formatter_2f = PrintfTickFormatter(format='%.2f')
formatter_1e = PrintfTickFormatter(format='%.1e')

blank_color = '#c4c4c4'
cmap_choice = 3      # cmaps (0: plasma, 1: inferno, 2: magma, 3: viridis)
extended = True      # show Lanthanides and actinides


period_remove = []   # remove selected groups from plot
group_remove = []    # remove selected groups


#Assign color palette
if cmap_choice == 0:
    cmap = plasma
    bokeh_palette = 'Plasma256'
elif cmap_choice == 1:
    cmap = inferno
    bokeh_palette = 'Inferno256'
elif cmap_choice == 2:
    cmap = magma
    bokeh_palette = 'Magma256'
elif cmap_choice == 3:
    cmap = viridis
    bokeh_palette = 'Viridis256'


def initialize_periodic_table():

    g = elements['group'].values
    p = elements['period'].values
    a = elements['atomic number'].values
    s = elements['symbol'].values


    # add entry for vacancy
    symbols = np.array(list(s)+['X'])
    groups = np.array(list(g)+['2'])
    periods = np.array(list(p)+['La'])
    atomic_numbers = np.array(list(a)+['0'])
        
    #Define number of and groups
    period_label = ['1', '2', '3', '4', '5', '6', '7']
    group_range = [str(x) for x in range(1, 19)]

    #Remove any groups or periods
    if group_remove:
        for gr in group_remove:
            group_range.remove(gr)
    if period_remove:
        for pr in period_remove:
            period_label.remove(pr)
            
    # add auxiliary period labels for a blank line and La and Ac series
    period_label.append('blank')
    period_label.append('La')
    period_label.append('Ac')

    # plot La and Ac series? set element groups and periods accoddingly
    if extended:
        count = 0
        for i in range(56,70):
            periods[i] = 'La'
            groups[i] = str(count+4)
            count += 1

        count = 0
        for i in range(88,102):
            periods[i] = 'Ac'
            groups[i] = str(count+4)
            count += 1

    return symbols, atomic_numbers, groups, periods, group_range, period_label, 

def get_Nimps(load_data=False):

    if not load_data:
        Nimps = len(list(load_imp_properties().keys()))
        np.save('judit-app/data/n_imps.npy', Nimps)
    else:
        Nimps = np.load('judit-app/data/n_imps.npy')

    return Nimps

def make_overview_panels():

    from time import time
    import numpy as np

    times = [time()]

    Nimps = get_Nimps(load_data=True)

    totimp_num_text = '#### Total number of impurities: {}'.format(Nimps)
    print(totimp_num_text)
    times+= [time()]


    layout_periodic_table = pn.pane.PNG('judit-app/images/statuc_image_periodic_table.png', width=int(website_width*0.8), 
                                        link_url='main_periodic_table')
    #from plots_overview.plot_periodic_table import periodic_table_with_buttons
    #layout_periodic_table = periodic_table_with_buttons()


    layout_with_hist = pn.pane.PNG('judit-app/images/static_image_scatter_plot.png', width=int(website_width*0.8), 
                                link_url='main_scatterplot_site')
    #from plots_overview.scatter_plot import make_scatterplot_with_hist
    #layout_with_hist = make_scatterplot_with_hist()

    times+= [time()]

    # combine plots
    layout = pn.Column(pn.pane.Markdown("## Average values for different impurity configurations"), 
                    layout_periodic_table,
                    pn.pane.Markdown("## Scatter plot"),
                    layout_with_hist,
                    )

    imps_overview = pn.Row(layout)

    times+= [time()]
    times = np.array(times)
    print('timings make_overview_panels:', times[1:]-times[:-1])

    return totimp_num_text, imps_overview
