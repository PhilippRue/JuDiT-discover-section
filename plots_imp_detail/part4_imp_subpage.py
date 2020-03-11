#!/usr/bin/env python
# coding: utf-8


import panel as pn

pn.extension()


# global settings

EF0 = 0.2

gapmax = 0.095    #0.105
gapmin = -0.062  #-0.06



# start with progress bar
import ipywidgets as widgets
from IPython.display import display


def init_pbar_imp(Nmax):
    pbar_imp = widgets.IntProgress(
        value=0,
        min=0,
        max=Nmax,
        step=1,
        description='Loading:',
        bar_style='', # 'success', 'info', 'warning', 'danger' or ''
        orientation='horizontal'
    )
    display(pbar_imp)
    return pbar_imp

# show progress bar (updated during the course of this script via incrementing pbar.value)
pbar_imp = init_pbar_imp(7)



from time import time



# load aiida
from aiida import load_profile
profile = load_profile()


# load other modules
import ipywidgets as widgets
import markdown 
from aiida.orm import load_node
from aiida_kkr.tools import plot_kkr

from aiida_kkr.calculations import VoronoiCalculation
from aiida.orm import StructureData

from ase_notebook import AseView, ViewConfig

import numpy as np

from ipywidgets import HBox, VBox



pbar_imp.value += 1




Sb2Te3_6QL_bandstruc = load_node('d3a077c4-967e-41a1-9817-a687e8ab475d') # -0.5eV..+0.3eV, corrected K-path

show_empty_atoms= False

# shift reference energy
EF0 = 0.2

gapend = 0.095    #0.105
gapstart = -0.062  #-0.06

radius_impcls = 4.5 # Ang.



#imp_properties_all = load_node('f8fb868c-fe36-4593-ac32-dfd45b83ca24')
imp_properties_all = load_node('3e65d6eb-d25e-48c3-8727-c969da1aff42')



"""
# EF+200:
kickout_list = ['imp:'+i[0]+'_layer_Sb['+i[1]+']' for i in [['Co','22'], ['Co','32'], ['Co','36'],
                                                     ['Fe','12'], ['Fe','22'], ['Fe','32'], ['Fe','36'],
                                                     ['Mn','22'], ['Mn','32'], ['Mn','36']
                                                    ]]
# EF:
kickout_list+= ['EF-200_imp:'+i[0]+'_layer_Sb['+i[1]+']' for i in [['V','22'], 
                                                            ['Fe','10'], ['Fe','22'], ['Fe','26'], ['Fe','32'], ['Fe','36'], 
                                                            ['Co','10'], ['Co','22'], ['Co','24'], ['Co','34'], ['Co','36'], 
                                                            ['Nb','22'], ['Nb','32'], ['Nb','36'], 
                                                            ['Tc','22'], ['Tc','32'], ['Tc','36'], 
                                                           ]]
# EF-200:
kickout_list+= ['EF-400_imp:'+i[0]+'_layer_Sb['+i[1]+']' for i in [['V','22'],
                                                                   ['Fe','22'], ['Fe','26'], ['Fe','28'], ['Fe','30'], ['Fe','32'], ['Fe','36'], 
                                                                   ['Co','10'], ['Co','22'], ['Co','32'], ['Co','36'], 
                                                                   ['Nb','22'], ['Nb','36'], ['Nb','32'], 
                                                                   ['Mo','22'], ['Mo','32'], ['Mo','36'], 
                                                                   ['Tc','32'], ['Tc','36']
                                                           ]]



kickout_list = [i.replace('Sb[10]','Te[10]').replace('Sb[34]','Te[34]').replace('Sb[24]','Te[24]').replace('Sb[28]','Te[28]').replace('Sb[30]','Te[30]') for i in kickout_list]


# from overview (wrong/ missing charge doping, gap filling or else)
kickout_list += ['EF-200_imp:Al_layer_Sb[22]', 'EF-200_imp:Sc_layer_Sb[22]', 'EF-200_imp:Cl_layer_Te[24]', 'imp:Sr_layer_Sb[12]', 'EF-200_imp:Os_layer_Sb[22]', 'EF-200_imp:Pb_layer_Sb[22]', 'EF-400_imp:Se_layer_Sb[16]', 'EF-400_imp:Rb_layer_Sb[16]', 'EF-400_imp:Sr_layer_Sb[16]', 'EF-400_imp:Y_layer_Sb[16]', 'EF-400_imp:Zr_layer_Sb[16]', 'EF-400_imp:Nb_layer_Sb[16]', 'EF-400_imp:Mo_layer_Sb[16]', 'EF-400_imp:Tc_layer_Sb[16]', 'EF-400_imp:Ru_layer_Sb[16]', 'EF-400_imp:Rh_layer_Sb[16]', 'EF-400_imp:Pd_layer_Sb[16]', 'EF-400_imp:Ag_layer_Sb[16]', 'EF-400_imp:Cd_layer_Sb[16]', 'EF-400_imp:In_layer_Sb[16]', 'EF-400_imp:Sb_layer_Sb[16]', 'EF-400_imp:Te_layer_Sb[16]', 'EF-400_imp:Cs_layer_Sb[16]', 'EF-400_imp:Ba_layer_Sb[16]', 'EF-400_imp:La_layer_Sb[16]', 'EF-400_imp:Hf_layer_Sb[16]', 'EF-400_imp:Ta_layer_Sb[16]', 'EF-400_imp:Re_layer_Sb[16]', 'EF-400_imp:Os_layer_Sb[16]', 'EF-400_imp:Ir_layer_Sb[16]', 'EF-400_imp:Pt_layer_Sb[16]', 'EF-400_imp:Au_layer_Sb[16]', 'EF-400_imp:Hg_layer_Sb[16]', 'EF-400_imp:Tl_layer_Sb[16]', 'EF-400_imp:Pb_layer_Sb[16]', 'EF-400_imp:H_layer_Te[18]', 'EF-400_imp:Li_layer_Te[18]', 'EF-400_imp:Be_layer_Te[18]', 'EF-400_imp:B_layer_Te[18]', 'EF-400_imp:C_layer_Te[18]', 'EF-400_imp:N_layer_Te[18]', 'EF-400_imp:O_layer_Te[18]', 'EF-400_imp:F_layer_Te[18]', 'EF-400_imp:Na_layer_Te[18]', 'EF-400_imp:Mg_layer_Te[18]', 'EF-400_imp:Al_layer_Te[18]', 'EF-400_imp:Si_layer_Te[18]', 'EF-400_imp:P_layer_Te[18]', 'EF-400_imp:S_layer_Te[18]', 'EF-400_imp:Cl_layer_Te[18]', 'EF-400_imp:K_layer_Te[18]', 'EF-400_imp:Ca_layer_Te[18]', 'EF-400_imp:Sc_layer_Te[18]', 'EF-400_imp:V_layer_Te[18]', 'EF-400_imp:Cr_layer_Te[18]', 'EF-400_imp:Mn_layer_Te[18]', 'EF-400_imp:Fe_layer_Te[18]', 'EF-200_imp:N_layer_Sb[26]', 'imp:Tl_layer_Sb[32]', 'imp:Ir_layer_Te[14]', 'imp:Pt_layer_Sb[16]', 'EF-200_imp:Sr_layer_Te[28]', 'imp:Os_layer_Sb[12]', 'EF-200_imp:C_layer_Te[24]', 'EF-200_imp:Na_layer_Sb[12]', 'EF-200_imp:Mg_layer_Sb[12]', 'EF-200_imp:Al_layer_Sb[12]', 'EF-200_imp:Si_layer_Sb[12]', 'EF-200_imp:P_layer_Sb[12]', 'EF-200_imp:S_layer_Sb[12]', 'EF-200_imp:Cl_layer_Sb[12]', 'EF-200_imp:K_layer_Sb[12]', 'EF-200_imp:Ca_layer_Sb[12]', 'EF-200_imp:Sc_layer_Sb[12]', 'EF-200_imp:V_layer_Sb[12]', 'EF-200_imp:Cr_layer_Sb[12]', 'EF-200_imp:Mn_layer_Sb[12]', 'EF-200_imp:Co_layer_Sb[12]', 'EF-200_imp:Ni_layer_Sb[12]', 'EF-200_imp:Cu_layer_Sb[12]', 'EF-200_imp:Zn_layer_Sb[12]', 'EF-200_imp:Ga_layer_Sb[12]', 'EF-200_imp:Ge_layer_Sb[12]', 'EF-200_imp:As_layer_Sb[12]', 'EF-200_imp:Se_layer_Sb[12]', 'EF-200_imp:Rb_layer_Sb[12]', 'EF-200_imp:Sr_layer_Sb[12]', 'EF-200_imp:Y_layer_Sb[12]', 'EF-200_imp:Zr_layer_Sb[12]', 'EF-200_imp:Nb_layer_Sb[12]', 'EF-200_imp:Mo_layer_Sb[12]', 'EF-200_imp:Tc_layer_Sb[12]', 'EF-200_imp:Ru_layer_Sb[12]', 'EF-200_imp:Rh_layer_Sb[12]', 'EF-200_imp:Ag_layer_Sb[12]', 'EF-200_imp:Cd_layer_Sb[12]', 'EF-200_imp:In_layer_Sb[12]', 'EF-200_imp:Sb_layer_Sb[12]', 'EF-200_imp:Te_layer_Sb[12]', 'EF-200_imp:Cs_layer_Sb[12]', 'EF-200_imp:Ba_layer_Sb[12]', 'EF-200_imp:La_layer_Sb[12]', 'EF-200_imp:Hf_layer_Sb[12]', 'EF-200_imp:Ta_layer_Sb[12]', 'EF-200_imp:Re_layer_Sb[12]', 'EF-200_imp:Os_layer_Sb[12]', 'EF-200_imp:Ir_layer_Sb[12]', 'EF-200_imp:Pt_layer_Sb[12]', 'EF-200_imp:Au_layer_Sb[12]', 'EF-200_imp:Hg_layer_Sb[12]', 'EF-200_imp:Tl_layer_Sb[12]', 'EF-200_imp:Pb_layer_Sb[12]', 'EF-200_imp:H_layer_Te[14]', 'EF-200_imp:Li_layer_Te[14]', 'EF-200_imp:Be_layer_Te[14]', 'EF-200_imp:B_layer_Te[14]', 'EF-200_imp:N_layer_Te[14]', 'EF-200_imp:O_layer_Te[14]', 'imp:Au_layer_Sb[22]', 'EF-200_imp:Hg_layer_Te[14]', 'EF-200_imp:Rb_layer_Te[24]', 'EF-200_imp:Y_layer_Sb[16]', 'EF-200_imp:Mo_layer_Sb[16]', 'EF-200_imp:Ag_layer_Sb[16]', 'EF-200_imp:Pt_layer_Sb[36]', 'EF-400_imp:Mg_layer_Te[30]', 'EF-200_imp:Mo_layer_Te[18]', 'imp:Hg_layer_Sb[26]', 'EF-200_imp:Te_layer_Te[18]', 'EF-200_imp:Ba_layer_Te[18]', 'EF-200_imp:Tl_layer_Te[18]', 'EF-200_imp:Be_layer_Te[20]', 'EF-200_imp:C_layer_Te[20]', 'EF-200_imp:Cr_layer_Te[20]', 'EF-200_imp:Zn_layer_Te[20]', 'EF-200_imp:In_layer_Te[20]']




Nko = 0; kol = []
imp_properties_all_curated = {}
for k,v in imp_properties_all.get_dict().items():
    #print(k)
    if k not in kickout_list:
        imp_properties_all_curated[k] = v
    else:
        print(k)
        kol+=[k]
        Nko += 1
len(list(imp_properties_all_curated.keys())), len(list(imp_properties_all.keys())), Nko, len(kickout_list)




from aiida.orm import Dict

#change imp_proerties_all collection
#imp_properties_all = Dict(dict=imp_properties_all_curated)

#imp_properties_all.store()
"""



#all_dc_node = Dict(dict=all_dc)
#all_dc_node.store()
all_dc_node = load_node('04724d7f-4970-4a47-9447-64db5c6f11aa')
all_dc = all_dc_node.get_dict()




from aiida.orm import Dict
#all_DOSingap_node = Dict(dict=all_DOSingap)
#all_DOSingap_node.store()
all_DOSingap_node = load_node('afe3e960-c335-4eca-8477-4e83a0dfbb53')
all_DOSingap = all_DOSingap_node.get_dict()
#all_DOSingap_node



pbar_imp.value += 1



def prepare_plotting_structure(return_struc=False):
    # find and plot structure
    structure0, voro_calc = VoronoiCalculation.find_parent_structure(Sb2Te3_6QL_bandstruc)

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
        return structure0, structure

    # now construct ase object and use ase's viewer
    ase_atoms = structure.get_ase()
    
    return ase_atoms


structure0, structure = prepare_plotting_structure(return_struc=True)




pbar_imp.value += 1




T0 = time()



def get_impinfo(impname):
    tmp = impname.split(':')[1].split('_')
    impsymbol = tmp[0]
    ilayer = int(tmp[-1].split('[')[1][:-1])
    return ilayer, impsymbol

# initial value
old_impname = None

def prepare_impcls_strucplot(impname, static_plot=False):
    global old_impname
    
    # set up structure viewer from ase_notebook
    config_dict = {
        'atom_show_label': True,
        'rotations': "-90x,-61y,0z",
        'show_uc_repeats': True,
        'show_bonds': False,
        'show_unit_cell': False,
        'canvas_size': [150, 500],
        'zoom': 1.0,
        'show_axes': True,
        'canvas_background_opacity': 0.00,
        'canvas_color_background': 'black',
        'axes_length': 30,
        'atom_opacity': 0.95
    }

    config = ViewConfig(**config_dict)
    ase_view_imp = AseView(config)
    ase_view_imp.config.zoom = 0.7
    
    # extract layer index and symbol of impurity
    ilayer, impsymbol = get_impinfo(impname)

    # now construct auxiliary structure
    cell = np.array(structure0.cell)

    s_impcluster = StructureData(cell=cell, pbc=structure0.pbc)
    site0 = structure0.sites[ilayer]
    pos0 = np.array(site0.position)
    for site in structure0.sites:
        for ix in range(-8,8):
            for iy in range(-8,8):
                pos = np.array(site.position) + cell[0]*ix + cell[1]*iy
                # make sure position is inside box:
                if np.sqrt(np.sum((pos-pos0)[:2]**2))<radius_impcls*1.1:
                    if np.sqrt(np.sum((pos-pos0)**2))==0:
                        s_impcluster.append_atom(position=pos, symbols=impsymbol)
                    else:
                        k = structure0.get_kind(site.kind_name)
                        if not k.has_vacancies:
                            s_impcluster.append_atom(position=pos, symbols=k.symbol)
                        elif show_empty_atoms:
                            s_impcluster.append_atom(position=pos, symbols='X')

    # find ghost atoms
    ghost_map = []
    for site in s_impcluster.sites:
        pos = np.array(site.position)
        if np.sqrt(np.sum((pos-pos0)**2))<radius_impcls:
            ghost_map.append(False)
        else:
            ghost_map.append(True)
    ghost_map = np.array(ghost_map)

    # create ase atoms object from auxiliary structure with ghost atoms mapping
    ase_atoms_impcls = s_impcluster.get_ase()
    ase_atoms_impcls.set_array('ghost', ghost_map)

    # rotate to have impurities at top site
    ase_atoms_impcls.rotate('-z', 'z', rotate_cell=True)
    
    # create plot
    if not static_plot:
        ase_view_imp.config.zoom = 1.0
        strucview_imp = ase_view_imp.make_render(
                ase_atoms_impcls, center_in_uc=True,
                create_gui=True, 
            )
    else:
        ase_view_imp.config.zoom = 1.2
        strucview_imp = ase_view_imp.make_svg(ase_atoms_impcls, center_in_uc=False,
             )
        
    # save impname for later
    old_impname = impname
        
    return strucview_imp




T1 = time()
#T1-T0



pbar_imp.value += 1


# -----

# ### Impurity properties


def get_EFval_from_impname(impname):
    if 'EF-' not in impname:
        return 0
    else:
        return float(impname.split('EF-')[1].split('_')[0])/1000.
    
def get_impdata_by_name(impname, imp_properties_all, all_DOSingap_node, all_dc_node, noref=False):
    impdata = imp_properties_all[impname]
    EFval = get_EFval_from_impname(impname)
    impdata['Delta_EF'] = EFval
    if not noref:
        # get also host-in host reference
        end = impname.split('layer_')[1]
        hostname = 'imp:'+end[:2]+'_layer_'+end
        impdata_ref = imp_properties_all[hostname]
        impdata_ref['Delta_EF'] = 0
    else:
        impdata_ref = None
    # add DOS_in_gap
    try:
        impdata['DOS_in_gap'] = all_DOSingap_node.get_dict()[impname]
    except KeyError:
        impdata['DOS_in_gap'] = None
    # add charge doping
    try:
        impdata['charge_doping'] = all_dc_node.get_dict()[impname]
    except KeyError:
        impdata['charge_doping'] = None
    # now return data
    return impdata, impdata_ref



def get_charge_transfer(impdata, impdata_ref):
    ilayer = np.array(impdata['impcls_ilayer'])
    imp_pos = np.array(impdata['impcls_position'])
    zhost = np.array(impdata['impcls_zhost'])
    imp_charge = np.array(impdata['total_charge_per_atom'])

    imp_charge_ref = np.array(impdata_ref['total_charge_per_atom'])

    # sort arrays according to position in impurity cluster
    m = np.sqrt(np.sum(imp_pos**2, axis=1)).argsort()
    ilayer, imp_pos, zhost = ilayer[m], imp_pos[m], zhost[m]
    imp_charge_ref = imp_charge_ref[m]
    imp_charge = imp_charge[m]

    # compute change in charge (Delta n [imp-host])
    a, b = imp_charge[0]-impdata['zimp'], imp_charge_ref[0]-impdata['zhost']
    dc = np.zeros_like(imp_charge)
    dc[0] = a-b
    dc[1:] = (imp_charge-imp_charge_ref)[1:]

    # compute distances to impurity
    dist_pos = np.sqrt(np.sum(imp_pos**2, axis=1))
    eps = 10**-4 # small number
    dist_unique = [0]
    for dist in dist_pos:
        if np.min(dist-np.array(dist_unique))>eps:
            dist_unique.append(dist)
    dist_unique = np.sort(np.array(dist_unique))

    return dc[0]



pbar_imp.value += 1




def take0(inlist):
    return inlist[0]

def do_trafo(inlist, trafo):
    if trafo is None:
        return inlist
    elif trafo=='take0':
        return take0(inlist)
    else:
        raise ValueError('trafo invalid')

def print_ordered_output_dir(resdict, return_text=False):
    # first define list for ourdered output of dict
    order_output_keys = [
        ['Version info', [
            'calculation_label',
            'uuid',
            'kkrimp_parser_version',
            'JuKKR_code_version',
            'kkrimp_calculation_plugin_version'
        ]],

        ['General settings KKR', [
            'lmax', 
            'XC', 
            'Nepts',
            'kmesh_GFwriteout',
            'nspin',
            'with_soc',
            'Delta_EF'
        ]],

        ['Impurity cluster', [
            'atoms_in_impurity_cluster',
            'ilayer',
            'zimp',
            'zhost',
            #'impcls_ilayer',
            #'impcls_position',
            #'impcls_zhost'
        ]],

        ['Convergence / results', [
            'rms',
            'etot_Ry',
            'etot_conv_Ry',
            'total_energy_eV',
            'total_charge_per_atom',
            'spin_moment_imp',
            'orbital_moment_imp',
            'DOS_in_gap',
            'charge_doping'
        ]]
    ]
    
    # maybe change some formatting
    special_formatting = {'code_version': {'key':'JuKKR_code_version'},
                          'total_charge_per_atom': {'key':'imp_charge', 'trafo': 'take0'}
                         }
    
    # now print output
    text_output = ['Calculation details:\n====================\n']
    
    for key in order_output_keys:
        text_output.append('{}'.format(key[0]))
        text_output.append('-'*len(key[0]))
        for subkey in key[1]:
            val = resdict.get(subkey)
            if subkey in special_formatting.keys():
                special_format = special_formatting[subkey]
                subkey = special_format['key']
                trafo = special_format.get('trafo', None)
                val = do_trafo(val, trafo)
            text_output.append('* {}: {}'.format(subkey, val))
        text_output.append('')
        #text_output.append('\n====================================\n')
    
    if return_text:
        return text_output
    else:
        print(text_output)



pbar_imp.value += 1



def plot_charge_transfer(impdata):
    imp_pos = np.array(impdata['impcls_position'])
    import matplotlib.pyplot as mpl

    mpl.figure(figsize=(9,5))
    mpl.subplot(1,2,1)
    mpl.axhline(0, ls=':', color='grey', lw=1)
    mpl.plot(np.sqrt(np.sum(imp_pos**2, axis=1))[:], (dc)[:], 'o-')
    mpl.ylabel(r'$\Delta n$ (e)')
    mpl.xlabel('distance to imp. ($\AA$)')
    mpl.subplot(1,2,2)
    mpl.axhline(0, ls=':', color='grey', lw=1)
    mpl.plot(np.sqrt(np.sum(imp_pos**2, axis=1))[1:], 
        [np.sum(dc[:i]) for i in range(1,len(dc))],
        'x-', color='r'
        )
    mpl.ylabel(r'$\sum \Delta n$ (e)')
    mpl.xlabel('distance to imp. ($\AA$)')

    mpl.tight_layout()
    mpl.suptitle('Charge neutrality vs. distance from impurity', fontsize=14)

    mpl.subplots_adjust(top=0.92)
    mpl.show()



pbar_imp.value += 1


# -----


from aiida.orm import load_node

def load_host_DOS():
    # load DOS data of host
    dos_host = load_node('edb8f4ec-38a0-46c9-9334-4448915aebb1') # DOS host system
    xhost = dos_host.outputs.dos_data_interpol.get_x()
    yhost = dos_host.outputs.dos_data_interpol.get_y()[0]

    #collect host DOS arrays
    yhost_spin1 = np.sum(yhost[1][0::2], axis=0) / (6*5)  # spin up of host per QL
    yhost_spin2 = np.sum(yhost[1][1::2], axis=0) / (6*5)  # spin dn of host per QL
    yhost = np.array(list(yhost_spin1)+list(yhost_spin2[::-1]))
    xhost = xhost[1][0] + EF0 # adapt Fermi level
    xhost = np.array(list(xhost[:])+list(xhost[::-1]))

    return xhost, yhost


xhost, yhost = load_host_DOS()


def load_impdos_data(impname, return_all=True):
    from aiida.orm import QueryBuilder, WorkChainNode

    # find name of DOS calculation
    dosname = 'Sb2Te3_slab_'+impname+'_DOS'

    # search for DOS calculation
    qb = QueryBuilder()
    qb.append(WorkChainNode, tag='imp_scf_nodes', 
              filters={
                  'and':[{'attributes.process_label':{'==':'kkr_imp_dos_wc'}},
                         {'label':{'==':dosname}}
                        ]})
    res = qb.all()
    has_DOS_data = False
    if len(res)==1:
        dos_wf = res[0][0]
        
        try:
            # extract arrays
            x = dos_wf.outputs.dos_data_interpol.get_x()
            y = dos_wf.outputs.dos_data_interpol.get_y()[0] # tot only
            ys = dos_wf.outputs.dos_data_interpol.get_y()[1] # s only
            yp = dos_wf.outputs.dos_data_interpol.get_y()[2] # p only
            yd = dos_wf.outputs.dos_data_interpol.get_y()[3] # d only
            has_DOS_data = True
        except:
            print('No DOS data found:', dos_wf)
        
    if has_DOS_data:
        # collect label etc.
        xlbl, x = x[0]+' ('+x[2]+')', x[1]
        ylbl, y = y[0]+' ('+y[2]+')', y[1]
        ys =ys[1]
        yp =yp[1]
        yd =yd[1]

        # find number of atoms in imp cluster
        nat = len(dos_wf.outputs.last_calc_output_parameters['charge_core_states_per_atom'])

        # adapt Fermi level
        for ii in range(len(x)):
            x[ii,:]+=EF0


        #concatenate spin up and down to single array
        yall = []
        for yy in [y, ys, yp, yd]:
            ytmp = []
            for iat in range(nat):
                xtmp2, ytmp2 = [], []
                for ispin in range(2):
                    if ispin==0:
                        ytmp2 += list(yy[iat*2+ispin, :])
                    else:
                        ytmp2 += list((-1)*yy[iat*2+ispin, ::-1])
                ytmp.append(ytmp2)
            yall.append(np.array(ytmp))
        y, ys, yp, yd = yall[0], yall[1], yall[2], yall[3]

        # do the same for x-array
        x = np.array(list(x[0,:])+list(x[0,::-1]))
    else:
        x, y, ys, yp, yd, xlbl, ylbl =  None, None, None, None, None, None, None
    
    if return_all:
        return x, y, ys, yp, yd, xlbl, ylbl
    else:
        return x,y


def get_ingap_DOS(x, y, gapmin, gapmax):
    # compute in-gap DOS
    xint = x[:]
    m1 = xint>=gapmin
    m2 = xint<=gapmax
    mint = m1==m2
    # make sure - sign for down spin is removed
    signcorr = np.ones_like(x)
    signcorr[int(len(x)/2):] = -1
    # energy step width (needed for integration)
    de = xint[1]-xint[0]
    # integrate DOS in gap region
    DOS_in_gap = sum((signcorr*y[0,:])[mint])*de

    return DOS_in_gap




import bokeh.plotting as bkp
    
def plot_impdos(impname, show_host_dos=True, show_l_channels=True, reuse_fig=None, 
                line_color=None, scalefac_host=None, add_bulk_gap_region=True, linewidth=None,
                lw_host=4, overwrite_label=None):

    # output to static HTML file
    #output inside notobook
    bkp.output_notebook(hide_banner=True)

    # create a new plot with a title and axis labels
    if reuse_fig is None:
        impdos_plot = bkp.figure(title="impurity DOS", plot_width=700, plot_height=550,
                                 tools='pan,box_zoom,wheel_zoom,reset,save')
    else:
        impdos_plot = reuse_fig
    
    # load data
    x, y, ys, yp, yd, xlbl, ylbl = load_impdos_data(impname)
    if show_host_dos:
        xhost, yhost = load_host_DOS()
        hostname = 'Sb2Te3 host'
        if scalefac_host is not None:
            yhost *= scalefac_host
            hostname += ' x '+str(scalefac_host)
        impdos_plot.line(xhost, yhost, legend_label=hostname, line_width=lw_host, color='black', 
                         alpha=0.6, muted_alpha=0.2, muted_color="black" )
        
    
    if add_bulk_gap_region:
        # add vbar (blue) to right plot
        gapwidth = gapend-gapstart
        impdos_plot.vbar(x=gapstart+gapwidth/2, width=gapwidth, bottom=-20, top=20, color='lightblue', 
                alpha=0.4, name='grey')


    ymin, ymax = 0,0
    plot_components = [0,1,2,3] # tot, s, p, d
    if not show_l_channels:
        plot_components = [0] # tot only

    for iat in range(1): #nat):
        name0 = impname.replace('imp:','') #dos_wf.label.replace('Sb2Te3_slab_imp:','').replace('_DOS','')
        name0 = name0.replace('_layer','').split('[')[0]
        for component in plot_components: 
            lw=2
            # set colors etc for different components
            if component==0:
                yy = y
                if line_color is None:
                    clr = 'black'
                else:
                    clr = line_color
                name=name0 + ', total'
                lw=3
            elif component==1:
                yy = ys
                clr = 'navy'
                name=name0 + ', s'
            elif component==2:
                yy = yp
                clr = 'red'
                name=name0 + ', p'
            elif component==3:
                yy = yd
                clr = 'green'
                name=name0 + ', d'
                
            # eventually overwrite line width with input
            if linewidth is not None:
                lw = linewidth
                
            # change name according to EF value convention
            if 'EF-' not in name:
                name = 'EF+200_'+name
            elif 'EF-200' in name:
                name = name.replace('EF-200_','')
            elif 'EF-400' in name:
                name = name.replace('EF-400_','EF-200_')
                
            # overwrite label from input
            if overwrite_label is not None:
                name = overwrite_label
            
            # plot DOS line 
            if yy is not None:
                ytmp = yy[iat,:]
            else:
                # if DOS data is not found:
                x = np.array([0])
                ytmp = np.zeros_like(x)
            impdos_plot.line(x, ytmp, legend_label=name, line_width=lw, color=clr, 
                             muted_alpha=0.2, muted_color=clr )
            # collect min/max values on y axis 
            ymin = min(ymin,ytmp.min())
            ymax = max(ymax,ytmp.max())

    # set x and y range
    if reuse_fig is None:
        ymin =ymin*1.1
        ymax = ymax*1.1
    else:
        #if ymin*1.1<reuse_fig.y_range.start:
        #    ymin = ymin*1.1
        #else:
        #    ymin = reuse_fig.y_range.start
        if ymax*1.1>reuse_fig.y_range.end:
            ymax = ymax*1.1
        else:
            ymax = reuse_fig.y_range.end
    impdos_plot.y_range.start = ymin
    impdos_plot.y_range.end = ymax
    impdos_plot.x_range.start = -4.7
    impdos_plot.x_range.end = 5

    # add axis labels
    impdos_plot.xaxis.axis_label = 'E (eV)'
    impdos_plot.yaxis.axis_label = 'DOS (states/eV)'

    # make lines clickable
    #impdos_plot.legend.click_policy="hide"
    impdos_plot.legend.click_policy="mute"

    return impdos_plot


# now read-in of all data finished, rest is impurity specific
pbar_imp.close()




# add footer to detail pages
footer = pn.pane.Markdown("""
Database version: XXXXX

[© Quantum Theory of Materials (PGI-1 / IAS-1)](https://www.fz-juelich.de/pgi/pgi-1/EN/Home/home_node.html)
""")



def create_impsite(impname, static_plot=False, return_pane=False, change_old_pane=None, open_new_tab=False):
    pbar_imp = init_pbar_imp(4)
    
    try:
    
        impdata, impdata_ref = get_impdata_by_name(impname, imp_properties_all, all_DOSingap_node, all_dc_node)

        pbar_imp.value += 1

        strucview_imp = prepare_impcls_strucplot(impname, static_plot=static_plot)

        pbar_imp.value += 1

        out_text_details = print_ordered_output_dir(impdata, return_text=True)
        out_text_details_md = ''
        for i in out_text_details:
            out_text_details_md += i+'\n'
        out_text_details = out_text_details_md

        # load DOS data
        x, y, ys, yp, yd, xlbl, ylbl = load_impdos_data(impname)

        # calculate ingap DOS
        DOS_in_gap = get_ingap_DOS(x, y, gapmin, gapmax)

        pbar_imp.value += 1

        impdos_plot = plot_impdos(impname)

        pbar_imp.value += 1


        # add title text
        title = pn.Row(pn.Column(#pn.pane.HTML('<br></br>'),
                                 pn.pane.Markdown("# Impurity detail page", width=700),
                                ),
                       pn.pane.HTML("<img  align='right' src='https://www.fz-juelich.de/SiteGlobals/StyleBundles/Bilder/NeuesLayout/logo.jpg?__blob=normal' width='150'/>"),
                      )

        display_all = pn.Row(impdos_plot, strucview_imp)

        # add output of calculation details
        display_all = pn.Column(title, display_all, pn.pane.Markdown(out_text_details), footer)

        pbar_imp.value += 1

        pbar_imp.close()
        
    except:
        display_all = pn.pane.Markdown("Error loading impurity: {}".format(impname))
        
        
    if open_new_tab:
        output_impsite = display_all
        output_impsite.show(title="Impurity detail page")
    else:
        if change_old_pane is not None:
            change_old_pane.objects[0] = impname
        else:
            output_impsite = display_all
    
    if return_pane:
        return output_impsite


# ## prepare imp names lists

# In[ ]:


import numpy as np

impnames_all, zimps, ilayers, iefs, zhosts = [], [], [], [], []
for k,v in imp_properties_all.get_dict().items():
    efval ,impsymb = k.split('imp:')
    if 'EF-400' in efval:
        efval = 'EF-200 meV'
        ief = 1
    elif 'EF-200' in efval:
        efval = 'EF'
        ief = 0
    else:
        efval = 'EF+200 meV'
        ief = 2
    impsymb, layer = impsymb.split('_')[0], impsymb.split('layer_')[1]
    impnames_all.append('{:>2}_{} {}'.format(impsymb, layer, efval))
    zimps.append(v['zimp'])
    ilayers.append(v['ilayer'])
    iefs.append(ief)
    zhosts.append(v['zhost'])

# order imp names after Fermi level, Zimp and then layer index
impnames_all, zimps, ilayers, iefs = np.array(impnames_all), np.array(zimps), np.array(ilayers), np.array(iefs)
zhosts = np.array(zhosts)

reorder_names = (iefs*1000000+zimps*1000+ilayers).argsort()
impnames_all_sorted = impnames_all[reorder_names]
zimps, ilayers, iefs = zimps[reorder_names], ilayers[reorder_names], iefs[reorder_names]
zhosts = zhosts[reorder_names]


# ## construct impurit selector with button


imp_select = Select_Impurity(name=markdown.markdown('### Select Impurity'))


class Select_Impurity_no_param():
    
    EFvals = [ 'EF -200meV', 'EF+0meV', 'EF+200meV']
    EF_value = pn.widgets.Select(options=EFvals, value=EFvals[1])
    
    bounds = (int(zimps.min()),int(zimps.max()))
    Zimp = pn.widgets.IntRangeSlider(start=bounds[0], end=bounds[1])
    
    bounds = (int(ilayers.min()), int(ilayers.max()))
    layer_index = pn.widgets.IntRangeSlider(start=bounds[0], end=bounds[1])
    
    bounds = (int(zhosts.min()), int(zhosts.max()))
    Zhost = pn.widgets.IntRangeSlider(start=bounds[0], end=bounds[1])
    
    selection_widget = pn.widgets.MultiSelect(name='test', options=[], size=8)
    
    
    def preselected_list(self):
        
        ef_select, zimp_select, layer_select = self.EF_value.value, self.Zimp.value, self.layer_index.value
        zhost_select = self.Zhost.value
        
        # get ief value
        if '-200' in ef_select:
            ief_select = 1
        elif '+200' in ef_select:
            ief_select = 2
        else:
            ief_select = 0
            
        from time import time
        
        times = [time()]

        # select only chosen EF value
        mask_find_ef = np.where(iefs==ief_select)
        zimps_selected, ilayers_selected = zimps[mask_find_ef], ilayers[mask_find_ef]
        zhosts_selected = zhosts[mask_find_ef]
        impnames_selected = impnames_all_sorted[mask_find_ef]
        
        times.append(time())

        
        # implement lower bound of Zimp selection
        mask_find_zimp = np.where(zimps_selected>zimp_select[0]-0.2)
        zimps_selected, ilayers_selected = zimps_selected[mask_find_zimp], ilayers_selected[mask_find_zimp]
        zhosts_selected = zhosts_selected[mask_find_zimp]
        impnames_selected = impnames_selected[mask_find_zimp]
        
        times.append(time())

        # implement upper bound of Zimp selection
        mask_find_zimp = np.where(zimps_selected<zimp_select[1]+0.2)
        zimps_selected, ilayers_selected = zimps_selected[mask_find_zimp], ilayers_selected[mask_find_zimp]
        zhosts_selected = zhosts_selected[mask_find_zimp]
        impnames_selected = impnames_selected[mask_find_zimp]
        
        times.append(time())

        
        # implement lower bound of Zhost selection
        mask_find_zhost = np.where(zhosts_selected>zhost_select[0]-0.2)
        zimps_selected, ilayers_selected = zimps_selected[mask_find_zhost], ilayers_selected[mask_find_zhost]
        zhosts_selected = zhosts_selected[mask_find_zhost]
        impnames_selected = impnames_selected[mask_find_zhost]
        
        times.append(time())

        # implement upper bound of Zhost selection
        mask_find_zhost = np.where(zhosts_selected<zhost_select[1]+0.2)
        zimps_selected, ilayers_selected = zimps_selected[mask_find_zhost], ilayers_selected[mask_find_zhost]
        zhosts_selected = zhosts_selected[mask_find_zhost]
        impnames_selected = impnames_selected[mask_find_zhost]
        
        times.append(time())


        # implement lower bound of ilayer selection
        mask_find_layer = np.where(ilayers_selected>layer_select[0]-0.2)
        zimps_selected, ilayers_selected = zimps_selected[mask_find_layer], ilayers_selected[mask_find_layer]
        zhosts_selected = zhosts_selected[mask_find_layer]
        impnames_selected = impnames_selected[mask_find_layer]
        
        times.append(time())

        # implement upper bound of ilayer selection
        mask_find_layer = np.where(ilayers_selected<layer_select[1]+0.2)
        zimps_selected, ilayers_selected = zimps_selected[mask_find_layer], ilayers_selected[mask_find_layer]
        zhosts_selected = zhosts_selected[mask_find_layer]
        impnames_selected = impnames_selected[mask_find_layer]
        
        times.append(time())
        
        times = np.array(times)
        print(times[1:]-times[0])
        
        return list(impnames_selected)
    
    
    def update_selection_list(self):
        impname_selection = self.preselected_list()
        self.selection_widget.options = impname_selection
    
        
    def view_preselected_list(self):
        # update selection widget
        impname_selection = self.preselected_list()
        self.selection_widget = pn.widgets.MultiSelect(name='Chose one or more impurities for detailed view', 
                                                       options=impname_selection, size=8)
        
        return pn.Row(pn.Column(pn.Row(pn.pane.Markdown("EF value:", width=60), self.EF_value),
                                pn.Row(pn.pane.Markdown("Zimp:", width=60), self.Zimp),
                                pn.Row(pn.pane.Markdown("Layer index:", width=60), self.layer_index),
                                pn.Row(pn.pane.Markdown("Zhost:", width=60), self.Zhost)
                               ),
                      pn.Column(self.selection_widget))


# ## build impurity selector


def get_scatterplot(source, xcolname, ycolname, xlabel, ylabel, title, fill_alpha=0.8,
                    size=10, plot_width=600, plot_height=200, oldfig=None, yrange_min=None):
    """
    Create scatter plot in new figure, source should be ColumnDataSource 
    where xcolname, ycolname are the names of the x/y columns which are plotted.
    
    Source should have a color column from where the color of the points is taken
    
    If oldfig is given link the x_ranges of the two plots (should use the same source).
    """
    tools = 'pan,box_zoom,wheel_zoom,reset,save'
    if oldfig is None:
        scatterplot = bkp.figure(tools=tools, title=title, plot_width=plot_width, plot_height=plot_height)
    else:
        scatterplot = bkp.figure(tools=tools, title=title, plot_width=plot_width, plot_height=plot_height,
                                 x_range=oldfig.x_range)
    scatterplot.scatter(xcolname, ycolname, color='color', source=source, 
                        fill_alpha=fill_alpha, size=size)
    scatterplot.xaxis.axis_label = xlabel
    scatterplot.yaxis.axis_label = ylabel
    if yrange_min is not None:
        if yrange_min[0]<np.min(source.data.get(ycolname)):
            scatterplot.y_range.start = yrange_min[0]
        if yrange_min[1]>np.max(source.data.get(ycolname)):
            scatterplot.y_range.end = yrange_min[1]
    return scatterplot
    



def create_imp_comparison_page(list_show_imps):
    from bokeh.palettes import Set1_8 as palette
    
    
    source = {'Zimp':[], 'impurity index':[], 'spin mom.':[], 
              'orb mom.':[], 'DOS in gap':[], 'charge doping':[],
              'color':[]
             }
    
    
    ii = 0
    for iimp in list_show_imps:
        impname_select = get_impname_label(iimp)

        color = palette[ii%len(palette)]

        if ii==0:
            impdos_plot = plot_impdos(impname_select, show_host_dos=True, show_l_channels=False, 
                                      overwrite_label=iimp.split()[0], line_color=color)
        else:
            impdos_plot = plot_impdos(impname_select, show_host_dos=False, show_l_channels=False, 
                                      reuse_fig=impdos_plot, add_bulk_gap_region=False, 
                                      overwrite_label=iimp.split()[0], line_color=color)
            

        impdata, impdata_ref = get_impdata_by_name(impname_select, imp_properties_all, 
                                                   all_DOSingap_node, all_dc_node, noref=True)

        source['Zimp'].append(impdata['zimp'])
        source['impurity index'].append(ii)
        source['spin mom.'].append(impdata['spin_moment_imp'][-1])
        source['orb mom.'].append(impdata['orbital_moment_imp'][-1])
        source['DOS in gap'].append(impdata['DOS_in_gap'])
        source['charge doping'].append(impdata['charge_doping'])
        source['color'].append(color)
        
        ii+=1
        
    source = bkp.ColumnDataSource(data=source)
    
    # create scatter plots
    scatterplot0 = get_scatterplot(source, 'impurity index', 'spin mom.', 'impurity index', 
                                   'spin moment (mu_B)', 'Spin moment', yrange_min=(-0.1,0.1))
    title = pn.Row(pn.Column(pn.pane.HTML('<br></br>'),
                             pn.pane.Markdown("### Physical properties of the impurity", width=500),
                            ),
                   pn.pane.HTML("<img  align='right' src='https://www.fz-juelich.de/SiteGlobals/StyleBundles/Bilder/NeuesLayout/logo.jpg?__blob=normal' width='150'/>"),
                  )
    scatterplots = pn.Column(title, scatterplot0)
    scatterplots = pn.Column(scatterplots, get_scatterplot(source, 'impurity index', 'orb mom.',
                                                           'impurity index', 'orbital moment (mu_B)',
                                                           'Orbital moment', oldfig=scatterplot0,
                                                           yrange_min=(-0.1,0.1)
                                                           ))
    scatterplots = pn.Column(scatterplots, get_scatterplot(source, 'impurity index', 'DOS in gap',
                                                           'impurity index', 'DOS in gap (e/impurity)',
                                                           'DOS in gap', oldfig=scatterplot0
                                                           ))
    scatterplots = pn.Column(scatterplots, get_scatterplot(source, 'impurity index', 'charge doping',
                                                           'impurity index', 'charge doping (e/impurity)',
                                                           'Charge doping', oldfig=scatterplot0
                                                           ))
    
    # create info text
    info_text = pn.pane.Markdown("""
# JuDiT Impurity comparison page


Comparison plots for the selected impurities.
Shown are 

* impurity density of states
* impurity properties vs. impurities
    * spin and orbital moment
    * DOS in gap
    * charge doping

The colors used in the DOS plot are reused for the datapoints in the plots showing the physical properties (right column).
    """, width=600)


    output_imp_cmp = pn.Column(pn.Row(pn.Column(info_text,
                                                impdos_plot),
                                      scatterplots
                                     ),
                               footer
                              )
    
    output_imp_cmp.show(title="Impurity comparison page")




spinner_text = """
<!-- https://www.w3schools.com/howto/howto_css_loader.asp -->
<div class="loader">
<style scoped>
.loader {
    border: 16px solid #f3f3f3; /* Light grey */
    border-top: 16px solid #3498db; /* Blue */
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 2s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
} 
</style>
</div>
"""
spinner = pn.pane.HTML("", width=50, height=50).servable()



import markdown
#imp_select = Select_Impurity(name=markdown.markdown('### Select Impurity'))
imp_select = Select_Impurity_no_param()

# add button and output pane to show selection
button = pn.widgets.Button(name="Show impurity details in new tab", button_type="primary")
output_pane = pn.pane.Markdown('no impurity selected', width=200)

def get_impname_label(impname_select):
    if 'EF-200' in impname_select:
        efval = 'EF-400_'
    elif 'EF+200' in impname_select:
        efval = ''
    else:
        efval = 'EF-200_'
    impsym, layer = impname_select.split('_')
    layer = layer.split()[0]
    impname_select = efval +'imp:'+ impsym +'_layer_'+ layer
    impname_select = impname_select.replace(' ', '')
    return impname_select


def callback_selection_button(b):
    """Callback function that happens if button in clicked."""
    
    # show spinner to visualize busy state
    spinner.object = spinner_text
    
    # get list of selected impurities
    list_show_imps = imp_select.selection_widget.value
    
    # extract impname and open imp detail page / or comp
    list_show_imps = imp_select.selection_widget.value
    if len(list_show_imps)==1:
        # open impurity detail page (single impurity)
        create_impsite(get_impname_label(list_show_imps[0]), static_plot=True, open_new_tab=True)
    elif len(list_show_imps)>1:
        # create page that compares the impurity properties, open new tab
        create_imp_comparison_page(list_show_imps)
    else:
        print('no impurity selected')
        
    # create a string that shows the current selection in output pane
    str_imp_list = 'no impurity selected'
    if len(list_show_imps)>0:
        str_imp_list = ''
        for iimp in list_show_imps:
            str_imp_list += '* {}\n'.format(iimp)
        str_imp_list = 'Selected impurities:\n\n{}'.format(str_imp_list)
    output_pane.object = '{}'.format(str_imp_list)
    
    # close spinner
    spinner.object = ""
    

button.on_click(callback_selection_button)


button_reset_selection = pn.widgets.Button(name="Reset selection", button_type="primary", width_policy='min')
def reset_values(b):
    imp_select.EF_value.value = imp_select.EF_value.values[1]
    imp_select.layer_index.value = (imp_select.layer_index.start, imp_select.layer_index.end)
    imp_select.Zimp.value = (imp_select.Zimp.start, imp_select.Zimp.end)
    imp_select.Zhost.value = (imp_select.Zhost.start, imp_select.Zhost.end)
    imp_select.update_selection_list()
button_reset_selection.on_click(reset_values)


button_3d_selection = pn.widgets.Button(name="Select 3d imps.", button_type="primary", width_policy='min')
def set_3d(b):
    imp_select.Zimp.value =(21, 30)
    imp_select.update_selection_list()
button_3d_selection.on_click(set_3d)


button_4d_selection = pn.widgets.Button(name="Select 4d imps.", button_type="primary", width_policy='min')
def set_4d(b):
    imp_select.Zimp.value =(39, 48)
    imp_select.update_selection_list()
button_4d_selection.on_click(set_4d)


button_select_list= pn.widgets.Button(name="Apply filter", button_type="success", width_policy='min')
def select_list(b):
    imp_select.update_selection_list()
button_select_list.on_click(select_list)

imp_select.EF_value


imp_select_panel = pn.Row(pn.Column(pn.pane.Markdown('####Select impurity for detail page'),
                                    imp_select.view_preselected_list(),
                                    pn.Row(button_select_list,
                                           button_3d_selection,
                                           button_4d_selection,
                                           button_reset_selection
                                          ),
                                   ),
                          pn.Column(pn.pane.HTML('<br></br><br></br>'),
                                    button,
                                    pn.Row(output_pane, spinner)
                                   )
                         )



# for debugging:

show_manual_plot = False

if show_manual_plot:
    list_show_imps = imp_select.selection_widget.value
    if len(list_show_imps)==1:
        # open impurity detail page (single impurity)
        create_impsite(get_impname_label(list_show_imps[0]), static_plot=True, open_new_tab=True)
    elif len(list_show_imps)>1:
        # create page that compares the impurity properties, open new tab
        create_imp_comparison_page(list_show_imps)

