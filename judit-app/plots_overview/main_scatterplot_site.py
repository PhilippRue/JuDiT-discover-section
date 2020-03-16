# standalone version
import panel as pn
from about import judit_footer, judit_header
from plots_overview.scatter_plot import make_scatterplot_with_hist

layout_with_hist = pn.Column(judit_header, make_scatterplot_with_hist(), judit_footer)

layout_with_hist.servable()