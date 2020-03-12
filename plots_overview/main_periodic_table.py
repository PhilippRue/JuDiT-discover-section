from about import judit_footer, judit_header
import panel as pn
from plots_overview.plot_periodic_table import periodic_table_with_buttons

# standalone version
layout_periodic_table = pn.Column(judit_header, periodic_table_with_buttons(), judit_footer)

layout_periodic_table.servable()