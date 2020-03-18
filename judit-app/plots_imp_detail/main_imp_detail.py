from plots_imp_detail.imp_detail import create_impsite, preload_data
from bokeh.io import curdoc

# extract name of imp
try:
    name = curdoc().session_context.request.arguments.get('id')[0]
    if isinstance(name, bytes):
        impname = name.decode()
        impname = impname.split('?bokeh-session-id')[0]
except:
    impname = None
print(impname)

# set global variables
preload_data(load_data=True)

# create impsite
impsite = create_impsite(impname=impname, static_plot=True, return_pane=True)

# make page available
impsite.servable()