# Functions to plot crystal structure:

# make all global settings available here
from .global_settings import *
from aiida.orm import load_node
from aiida_kkr.calculations import VoronoiCalculation
from aiida.orm import StructureData
import numpy as np


def prepare_plotting_structure(return_struc=False, show_empty_atoms=False):

    # find and plot structure, extract if from parent of bandstructure calc
    Sb2Te3_6QL_bandstruc = load_node(UUID_HOST_BANDSTRUC) # -0.5eV..+0.3eV, corrected K-path
    structure0, _ = VoronoiCalculation.find_parent_structure(Sb2Te3_6QL_bandstruc)

    if structure0.has_vacancies:
        cell = structure0.cell
        
        # correct cell ...
        cell[2] = [i*8 for i in cell[2]]

        stmp = StructureData(cell=cell)
        for site in structure0.sites:
            k = structure0.get_kind(site.kind_name)
            pos = np.array(site.position)
            pos[2] = -pos[2]
            if not k.has_vacancies:
                stmp.append_atom(position=pos, symbols=k.symbol)
            elif show_empty_atoms:
                stmp.append_atom(position=pos, symbols='X')
            #else:
            #    print("removing atom", site)
        stmp.set_pbc(structure0.pbc)
        structure = stmp
        
    if return_struc:
        return structure

    # now construct ase object and use ase's viewer
    ase_atoms = structure.get_ase()
    
    return ase_atoms




def create_structure_plot(ase_atoms, static_plot=False):

    from ase_notebook import AseView, ViewConfig

    # set up structure viewer from ase_notebook

    config_dict = {
        'atom_show_label': True, #True,
        'rotations': "-90x,-60y,0z",
        #'rotations': "-90x,-60y,180z",
        'show_uc_repeats': True,
        'show_bonds': False,
        'show_unit_cell': False,
#        'canvas_size': [120, 400],
        'canvas_size': [120, 400],
        'zoom': 1.0,
        'show_axes': True,
        'canvas_background_opacity': 0.05,
        'canvas_color_background': 'black',
        'axes_length': 30,
    }
    
    #ase_atoms.rotate(180, 'z', rotate_cell=True)
    ase_atoms.rotate('-z', 'z', rotate_cell=True)
    #ase_atoms.rotate(-90, 'x', rotate_cell=True)
    #ase_atoms.rotate(-60, 'y', rotate_cell=True)

    config = ViewConfig(**config_dict)
    ase_view = AseView(config)
    ase_view_imp = AseView(config)
    ase_view_imp.config.zoom = 0.7

    
    if not static_plot:
        strucview = ase_view.make_render(
                ase_atoms, center_in_uc=False,
                repeat_uc=(3,3,1), use_atom_arrays=True,
                create_gui=True, #True, 
            )
    else:
        ase_view.config.zoom = 1.2
        ase_view.config.atom_show_label = False
        ase_view.config.show_axes = False
        ase_view.config.canvas_background_opacity = 0.0
        strucview = ase_view.make_svg(ase_atoms, center_in_uc=False,
                repeat_uc=(3,3,1)
             )
        
    return strucview

