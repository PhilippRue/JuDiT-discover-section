#!/bin/bash -e

# This script is executed whenever the docker container is (re)started.

#===============================================================================
# debuging
set -x

#===============================================================================

# prepare data for faster access, this extracts data from the database 
# which would slow the buildup time of the website down
# results are saved in judit-app/data/*npy files
./prepare_data.py

# now serve the app (uses bokeh server in the background)
panel serve judit-app/judit_website_main.ipynb \
            judit-app/plots_host_system/standalone.py \
            judit-app/plots_overview/main_periodic_table.py \
            judit-app/plots_overview/main_scatterplot_site.py \
            judit-app/plots_imp_detail/main_imp_detail.py \
            judit-app/plots_imp_detail/main_imp_comparison.py \
    --port 5006                 \
    --log-level debug           \
    --allow-websocket-origin "*" \
    --prefix "$BOKEH_PREFIX" \
    --use-xheaders           \
    --address 0.0.0.0

#===============================================================================

#EOF
