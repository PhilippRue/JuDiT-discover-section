### Electronic structure of Sb$_2$Te$_3$ host crystal

from global_settings import website_width
import panel as pn


host_system_header = pn.pane.Markdown("""
---
## Host system
                          """, width=website_width)#, sizing_mode='stretch_both')
host_system_header = pn.Column(host_system_header, pn.pane.Markdown("""
The impurities are embedded into a prototypical topological insulator.
We consider a thin film of 6 quituple layers (6QL) thickness which allows 
to embed inpurities at different depths from the surface.
For the impurities we considered substitutional positions at the Te and Sb positions of the first three QLs.

In order to simulate intrinsic doping in the host material we also shifted the Fermi level for the 
impurity embedding step from its intrinsic value in the middle of the bulk band gap into the valence 
and conduction bands (denoted by red and green lines, respectively). The blue shaded region corresponds
to the position of the bulk band gap in which only the topological surface states lives.
    """, width=website_width, sizing_mode='stretch_both'))#, sizing_mode='stretch_both')

legend = pn.pane.Markdown("#### Legend\n"
                          "* Red line: Fermi level shift into conduction band\n"
                          "* Green line: Fermi level shift into valence band\n"
                          "* blue region: region of bulk band gap\n", width=website_width)#, sizing_mode='stretch_both')



def get_static_host_plots():
    host_plots_static = pn.pane.PNG('./images/static_image_host_plots.png', width=int(0.8*website_width), 
                                    link_url='standalone') # link to standalone page
    host_plots_static = pn.Column(host_system_header, host_plots_static, legend, )
    return host_plots_static
