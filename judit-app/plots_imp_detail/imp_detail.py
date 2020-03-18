import panel as pn
from aiida_kkr.calculations import VoronoiCalculation
from aiida.orm import StructureData, load_node
from plots_imp_detail import *
import numpy as np
from ase_notebook import ViewConfig, AseView
from plots_host_system.global_settings import *
import bokeh.plotting as bkp
from plots_overview.load_data import load_all 
from about import judit_footer, judit_header


def prepare_plotting_structure(return_struc=False):
    # find and plot structure
    Sb2Te3_6QL_bandstruc = load_node(UUID_HOST_BANDSTRUC)
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
        return structure0, structure

    # now construct ase object and use ase's viewer
    ase_atoms = structure.get_ase()
    
    return ase_atoms



def get_impinfo(impname):
    tmp = impname.split(':')[1].split('_')
    impsymbol = tmp[0]
    ilayer = int(tmp[-1].split('[')[1][:-1])
    return ilayer, impsymbol



def prepare_impcls_strucplot(impname, static_plot=False):
    global old_impname, structure0
    
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



def get_EFval_from_impname(impname):
    if 'EF-' not in impname:
        return 0
    else:
        return float(impname.split('EF-')[1].split('_')[0])/1000.
    
def get_impdata_by_name(impname, imp_properties_all, all_DOSingap, all_dc, noref=False):
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
        impdata['DOS_in_gap'] = all_DOSingap[impname]
    except KeyError:
        impdata['DOS_in_gap'] = None
    # add charge doping
    try:
        impdata['charge_doping'] = all_dc[impname]
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

        ['Impurity cluster', [
            'atoms_in_impurity_cluster',
            'ilayer',
            'zimp',
            'zhost',
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


def load_host_DOS():
    # load DOS data of host
    dos_host = load_node(UUID_HOST_DOS) # +/-5eV
    xhost = dos_host.outputs.dos_data_interpol.get_x()
    yhost = dos_host.outputs.dos_data_interpol.get_y()[0]

    #collect host DOS arrays
    yhost_spin1 = np.sum(yhost[1][0::2], axis=0) / (6*5)  # spin up of host per QL
    yhost_spin2 = np.sum(yhost[1][1::2], axis=0) / (6*5)  # spin dn of host per QL
    yhost = np.array(list(yhost_spin1)+list(yhost_spin2[::-1]))
    xhost = xhost[1][0] + EF0 # adapt Fermi level
    xhost = np.array(list(xhost[:])+list(xhost[::-1]))

    return xhost, yhost


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
    x, y, ys, yp, yd, _, _ = load_impdos_data(impname)
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



def create_impsite(impname=None, static_plot=False, return_pane=False, open_new_tab=False):
    
    global imp_properties_all, all_DOSingap, all_dc
    global output_impsite

    # add title text
    title = pn.pane.Markdown("## Impurity detail page", width=700)


    try:
        impdata, _ = get_impdata_by_name(impname, imp_properties_all, all_DOSingap, all_dc)

        strucview_imp = prepare_impcls_strucplot(impname, static_plot=static_plot)

        out_text_details = print_ordered_output_dir(impdata, return_text=True)
        out_text_details_md = ''
        for i in out_text_details:
            out_text_details_md += i+'\n'
        out_text_details = out_text_details_md

        impdos_plot = plot_impdos(impname)

        display_all = pn.Row(impdos_plot, strucview_imp)
        display_all = pn.Column(display_all, pn.pane.Markdown(out_text_details))
    except:
        if impname is not None:
            display_all = pn.pane.Markdown("Error loading impurity: {}".format(impname))
        else:
            display_all = pn.pane.Markdown("No impurity selected yet. Go back to main page to select one.")

    # combine different parts of the page
    display_all = pn.Column(judit_header, title, display_all, judit_footer)
        
    if open_new_tab:
        output_impsite = display_all
        output_impsite.show(title="Impurity detail page")
    else:
        output_impsite = display_all
    
    if return_pane:
        return output_impsite


def preload_data(load_data=False):
    global imp_properties_all, all_DOSingap, all_dc, structure0
 
    from time import time
    t0 = time()
    structure0, _ = prepare_plotting_structure(return_struc=True)
    t1 = time()
    if not load_data:
        imp_properties_all, _, all_DOSingap, _, all_dc, _ = load_all()
        np.save('judit-app/data/imp_properties.npy', imp_properties_all)
        np.save('judit-app/data/all_DOSingap.npy', all_DOSingap)
        np.save('judit-app/data/all_dc.npy', all_dc)
    else:
        imp_properties_all = np.load('judit-app/data/imp_properties.npy', allow_pickle=True).item()
        all_DOSingap = np.load('judit-app/data/all_DOSingap.npy', allow_pickle=True).item()
        all_dc = np.load('judit-app/data/all_dc.npy', allow_pickle=True).item()
    t2 = time()
    print('timings preload_data:', t1-t0, t2-t1)

    return imp_properties_all, all_DOSingap, all_dc


