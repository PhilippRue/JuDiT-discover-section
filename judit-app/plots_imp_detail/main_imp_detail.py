from plots_imp_detail.imp_detail import create_impsite, preload_data
from bokeh.io import curdoc
from plots_imp_detail.tools import get_impname_label

# extract name of imp
try:
    name = curdoc().session_context.request.arguments.get('id')[0]
    if isinstance(name, bytes):
        impname = name.decode()
        impname = get_impname_label(impname)
except:
    impname = None
print(impname)

# set global variables
preload_data(load_data=True)

# create impsite
impsite = create_impsite(impname=impname, static_plot=True, return_pane=True, debug=True)

# make page available
impsite.servable()
