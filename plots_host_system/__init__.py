### Electronic structure of Sb$_2$Te$_3$ host crystal

import panel as pn
from plots_host_system.host_crystal_structure import create_structure_plot, prepare_plotting_structure
from plots_host_system.bandstructure import plot_bandstruc, add_ef_lines_bandstruc
from plots_host_system.host_dos import plot_dos

def create_host_plots():

    pn.extension('mathjax')

    # load aiida if necessary
    from aiida import load_profile
    profile = load_profile()

    ase_atoms = prepare_plotting_structure()
    strucview = create_structure_plot(ase_atoms, static_plot=True)

    # create bandstructure plot
    bandstruc_plot = plot_bandstruc()

    # make DOS plot
    dos_plot , ymax = plot_dos()
    # add ef lines to bandstructure plot (needs to be done here since some values are otherwise not defined)
    add_ef_lines_bandstruc(bandstruc_plot, ymax)

    # put bandstructure and DOS plots together
    layout = pn.Row(bandstruc_plot,dos_plot)

    #struc_title = pn.pane.LaTeX("Thin film (6QL) of Sb$_2$Te$_3$")
    #host_plots = pn.Row(pn.Column(struc_title, strucview), layout)
    host_plots = pn.Row(strucview, layout)

    return host_plots



host_plots = create_host_plots()
host_plots.servable()
