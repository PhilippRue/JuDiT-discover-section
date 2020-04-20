


import panel as pn
from plots_host_system.host_crystal_structure import create_structure_plot, prepare_plotting_structure
from plots_host_system.bandstructure import plot_bandstruc, add_ef_lines_bandstruc
from plots_host_system.host_dos import plot_dos
from plots_host_system import host_system_header, legend
from about import judit_footer, judit_header

from aiida.manage.configuration import load_config, load_profile
from aiida.manage.configuration.profile import Profile
import os

config = load_config(create=True)

profile_name = os.getenv("AIIDA_PROFILE")

profile = Profile(
    profile_name, {
        "database_hostname":
        os.getenv("AIIDADB_HOST"),
        "database_port":
        os.getenv("AIIDADB_PORT"),
        "database_engine":
        os.getenv("AIIDADB_ENGINE"),
        "database_name":
        os.getenv("AIIDADB_NAME"),
        "database_username":
        os.getenv("AIIDADB_USER"),
        "database_password":
        os.getenv("AIIDADB_PASS"),
        "database_backend":
        os.getenv("AIIDADB_BACKEND"),
        "default_user":
        os.getenv("default_user_email"),
        "repository_uri":
        "file://{}/.aiida/repository/{}".format(os.getenv("AIIDA_PATH"),
                                                profile_name),
    })
config.add_profile(profile)
config.set_default_profile(profile_name)
config.store()



def create_host_plots_clean():

    pn.extension('mathjax')

    # load aiida if necessary
    profile = load_profile(profile_name)

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


host_plots = create_host_plots_clean()
host_plots = pn.Column(judit_header, host_system_header, host_plots, legend, judit_footer)
host_plots.servable()
