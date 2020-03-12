#!/usr/bin/env python

import numpy as np
from time import time
times = [time()]

# get number of impurities
from plots_overview import get_Nimps
get_Nimps(load_data=False)

times+= [time()]

get_Nimps(load_data=False)

times+= [time()]

# accelerate loading of imp properties
from plots_imp_detail.imp_detail import preload_data
preload_data(load_data=False)

times+= [time()]

preload_data(load_data=True)

times+= [time()]


# collect data for scatter plot (reload for faster access)
print('Prepare scatter plot data')

from plots_overview.scatter_plot import get_scatter_column_data_source
get_scatter_column_data_source(load_data=False)

times+= [time()]

get_scatter_column_data_source(load_data=True)

times+= [time()]


# collect data for periodic table plot (reload for faster access)
print('Prepare periodic table plot data')
from plots_overview.plot_periodic_table import get_data_on_perdic_table
get_data_on_perdic_table(load_data=False)

times+= [time()]

get_data_on_perdic_table(load_data=True)

times+= [time()]

# print timing info
times = np.array(times)
print('timings', times[1:]-times[:-1])