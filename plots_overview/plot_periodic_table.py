
import numpy as np
from plots_overview.load_data import load_all
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize, LogNorm, to_hex
from bokeh.models import (ColumnDataSource, LinearColorMapper, LogColorMapper, ColorBar, BasicTicker)
import bokeh.plotting as bkp
from bokeh.transform import dodge
from bokeh.models import CustomJS
from bokeh.models import RadioButtonGroup
from bokeh.models.widgets import Paragraph
from bokeh.layouts import column, row
from bokeh.models import HoverTool
from about import judit_footer, judit_header
import panel as pn
from plots_overview import (formatter_int, formatter_2f, formatter_1e, 
                            blank_color, initialize_periodic_table, 
                            bokeh_palette, cmap)



# some settings
width = 900         # plot width
alpha = 0.65         # alpha value of color scale
log_scale = 0        # use log scale for colors
cbar_height = 500    # height of color map
cbar_fontsize = 8   # size of cbar labels
cbar_standoff = 12   # distance of labels to cbar


def get_data_on_perdic_table():
    """Get ColumnDataSource """

    global color_mapper_all

    symbols, atomic_numbers, groups, periods, group_range, period_label = initialize_periodic_table()

    imp_properties_all, imp_properties_sorted, all_DOSingap, all_DOSingap_sorted, all_dc, all_dc_sorted = load_all()

    color_list_all_allEF = []
    data_values_allEF = []
    data_values_str_allEF = []
    data_allEF = []
    dstr_allEF = []
    data_elements_allEF = []
            
    # now extract data from dict to arrays
    for EFset in [0,-200,-400, 'all']:
        
        # collect imp properties 
        if EFset!='all':
            imp_properties = imp_properties_sorted[EFset]
        else:
            imp_properties = imp_properties_all.get_dict()
            
        # sort out 'wrong' data
        imp_properties0 = {}
        for k,v in imp_properties.items():
            if 'EF-' not in k:
                efshift = 0.2
            if 'EF-400' in k:
                efshift = -0.2
            else:
                efshift = 0.
            mmap = v['zimp']*1000000+1000*v['zhost']+v['ilayer']+efshift
            if 1: #mmap in mapping_data_ok:
                imp_properties0[k] = v
        imp_properties = imp_properties0
        

        num_impcalcs = {}
        rms_impcalcs = {}
        omom, smom = {}, {}
        nmag = {}
        # unpack imp_properties array
        for k, v in imp_properties.items():
            impname = k.split(':')[1].split('_')[0]
            if impname not in num_impcalcs.keys():
                rms_impcalcs[impname] = []
                num_impcalcs[impname] = 0
                omom[impname], smom[impname] = [], []
                nmag[impname] = 0
            num_impcalcs[impname] += 1
            rms_impcalcs[impname].append(v.get('rms'))
            smom[impname].append(abs(v.get('spin_moment_imp')[2]))
            omom[impname].append(abs(v.get('orbital_moment_imp')[2]))
            if abs(v.get('spin_moment_imp')[2])> 10**-4:
                nmag[impname] += 1
                
        # extract values for charge doping and DOS in Gap
        if EFset!='all':
            DOSinGap_values = all_DOSingap_sorted[EFset]
            dc_values = all_dc_sorted[EFset]
        else:
            DOSinGap_values = all_DOSingap
            dc_values = all_dc
        DOSinGap = {}
        for k,v in DOSinGap_values.items():
            impname = k.split(':')[1].split('_')[0]
            if impname not in DOSinGap.keys():
                DOSinGap[impname] = []
            DOSinGap[impname].append(v)
        charge_doping = {}
        for k,v in dc_values.items():
            impname = k.split(':')[1].split('_')[0]
            if impname not in charge_doping.keys():
                charge_doping[impname] = []
            charge_doping[impname].append(v)

        # now fill big data array
        data = []; data_elements = []; dstr = []
        for k, v in imp_properties.items():
            impname = k.split(':')[1].split('_')[0]
            if impname not in data_elements:
                data_elements.append(impname)
                data.append([num_impcalcs[impname],
                            np.mean(rms_impcalcs[impname]), np.std(rms_impcalcs[impname]),
                            np.mean(smom[impname]), np.std(smom[impname]),
                            np.mean(omom[impname]), np.std(omom[impname]),
                            nmag[impname], nmag[impname]/float(num_impcalcs[impname])*100.,
                            np.mean(charge_doping.get(impname,-2)), np.std(charge_doping.get(impname,-2)), 
                            np.mean(DOSinGap.get(impname,-0.3)), np.std(DOSinGap.get(impname,-0.3))
                            ])
                dstr.append(['%i', # num clacs
                            '%.3e', '%.3e', # rms (mean/std)
                            '%.3f', '%.3f', # smom (mean/std)
                            '%.3f', '%.3f', # omom (mean/std)
                            '%i', # number mag
                            '%.2f', # % mag
                            '%.2f', '%.2f', # % charge_doping (mean/std)
                            '%.2f', '%.2f' # % DOS in Gap (mean/std)
                            ])
        from numpy import array
        data = array(data)
        dstr = array(dstr)
        data_elements = array(data_elements)
        
        # store in big arrays
        data_allEF.append(data)
        dstr_allEF.append(dstr)
        data_elements_allEF.append(data_elements)
        
        # set up color scales
        color_scale = []
        color_mapper_all = []
        #print(EFset, len(data[0]))
        for color_component in range(len(data[0,:])):
            #Define color map called 'color_scale'
            if log_scale == 0:
                ColorMapper = LinearColorMapper
                norm = Normalize(vmin = min(data[:,color_component]), vmax = max(data[:,color_component]))
            elif log_scale == 1:
                for datum in data[:,color_component]:
                    if datum < 0:
                        raise ValueError('Entry for element '+datum+' is negative but'
                        ' log-scale is selected')
                ColorMapper = LogColorMapper
                norm = LogNorm(vmin = min(data[:,color_component]), vmax = max(data[:,color_component]))

            color_mapper_all.append(ColorMapper(palette = bokeh_palette, 
                                                low=min(data[:,color_component]), 
                                                high=max(data[:,color_component])))
            color_scale.append(ScalarMappable(norm=norm, cmap=cmap).to_rgba(data[:,color_component], alpha=None))
            
        #Define color for blank entries
        default_value = None
        color_list_all = []
        data_values = []
        data_values_str = []
        for i in range(len(symbols)):
            color_list_all.append([blank_color for ii in data[0,:]])
            data_values.append([None for ii in data[0,:]])
            data_values_str.append(['' for ii in data[0,:]])
            
        #Compare elements in dataset with elements in periodic table and set color etc. accordingly
        from numpy import arange 
        idx = arange(len(symbols))
        for i, data_element in enumerate(data_elements):
            element_entry = idx[symbols == data_element]
            if len(element_entry)>0:
                element_index =element_entry[0]
            else:
                print('WARNING: Invalid chemical symbol: '+data_element)
            if color_list_all[element_index][0] != blank_color:
                print('WARNING: Multiple entries for element '+data_element)

            for j in range(len(data[0,:])):
                color_list_all[element_index][j] = to_hex(color_scale[j][i])

            # add data values that are shown by hover tool
            data_values[element_index] = data[i,:]
            for j in range(len(data[i])):
                data_values_str[element_index][j] = dstr[i,j]%data[i,j]

        color_list_all = array(color_list_all)
        data_values = array(data_values)
        data_values_str = array(data_values_str)
        
        # store big arrays
        color_list_all_allEF.append(color_list_all)
        data_values_allEF.append(data_values)
        data_values_str_allEF.append(data_values_str)



    #Define figure properties for visualizing data
    source_allEF = []
    for iEF in [3,0,1,2,3]: # first entry is active values (i.e. without EF shift)
        source_allEF.append(
            ColumnDataSource(
                data=dict(
                    plot_component=[0 for x in groups],
                    group=[str(x) for x in groups],
                    period=[str(y) for y in periods],
                    sym=symbols,
                    atomic_number=atomic_numbers,
                    type_color=color_list_all_allEF[iEF][:,0],
                    type_color0=color_list_all_allEF[iEF][:,0],
                    type_color1=color_list_all_allEF[iEF][:,1],
                    type_color2=color_list_all_allEF[iEF][:,2],
                    type_color3=color_list_all_allEF[iEF][:,3],
                    type_color4=color_list_all_allEF[iEF][:,4],
                    type_color5=color_list_all_allEF[iEF][:,5],
                    type_color6=color_list_all_allEF[iEF][:,6],
                    type_color7=color_list_all_allEF[iEF][:,7],
                    type_color8=color_list_all_allEF[iEF][:,8],
                    type_color9=color_list_all_allEF[iEF][:,9],
                    type_color10=color_list_all_allEF[iEF][:,10],
                    type_color11=color_list_all_allEF[iEF][:,11],
                    type_color12=color_list_all_allEF[iEF][:,12],
                    num_impcalcs=data_values_allEF[iEF][:,0],
                    num_impcalcs_str=data_values_str_allEF[iEF][:,0],
                    rms_mean=data_values_allEF[iEF][:,1],
                    rms_mean_str=data_values_str_allEF[iEF][:,1],
                    rms_std=data_values_allEF[iEF][:,2],
                    rms_std_str=data_values_str_allEF[iEF][:,2],
                    smom_mean=data_values_allEF[iEF][:,3],
                    smom_mean_str=data_values_str_allEF[iEF][:,3],
                    smom_std=data_values_allEF[iEF][:,4],
                    smom_std_str=data_values_str_allEF[iEF][:,4],
                    omom_mean=data_values_allEF[iEF][:,5],
                    omom_mean_str=data_values_str_allEF[iEF][:,5],
                    omom_std=data_values_allEF[iEF][:,6],
                    omom_std_str=data_values_str_allEF[iEF][:,6],
                    nummag=data_values_allEF[iEF][:,7],
                    nummag_impcalcs_str=data_values_str_allEF[iEF][:,7],
                    percent_mag=data_values_allEF[iEF][:,8],
                    percent_mag_impcalcs_str=data_values_str_allEF[iEF][:,8],
                    # additional fields for charge doping and DOS in Gap
                    charge_doping_mean=data_values_allEF[iEF][:,9],
                    charge_doping_mean_str=data_values_str_allEF[iEF][:,9],
                    charge_doping_std=data_values_allEF[iEF][:,10],
                    charge_doping_std_str=data_values_str_allEF[iEF][:,10],
                    DOSinGap_mean=data_values_allEF[iEF][:,11],
                    DOSinGap_mean_str=data_values_str_allEF[iEF][:,11],
                    DOSinGap_std=data_values_allEF[iEF][:,12],
                    DOSinGap_std_str=data_values_str_allEF[iEF][:,12]
                )
            )
        )

    return source_allEF


def get_periodic_table_plot():
    """Plot the periodic table with colors (returns bokeh figure)"""

    global names
    
    symbols, atomic_numbers, groups, periods, group_range, period_label = initialize_periodic_table()

    # get ColumnDataSource for values on periodic table
    source_allEF = get_data_on_perdic_table()

    # EF=0 starting values
    source = source_allEF[0]
        
    # create figure
    plot = bkp.figure(x_range=group_range, 
            y_range=list(reversed(period_label)), 
            tools='pan,wheel_zoom,reset,save',
            title = 'Impurities in Sb2Te3 (6QL)'
            )

    # set up hover tool
    hover = HoverTool()
    hover.tooltips = [("Element", "@sym"), # things displayed by hover tool, needs to be in 'source' dict
            ("# impcalcs", "@num_impcalcs"), 
            ("% magnetic", "@percent_mag"), 
            ("<spin mom>", "@smom_mean (+/-@smom_std)"), 
            ("<orb mom>", "@omom_mean (+/-@omom_std)"), 
            ("<charge doping>", "@charge_doping_mean (+/-@charge_doping_std)"), 
            ("<DOS in gap>", "@DOSinGap_mean (+/-@DOSinGap_std)"), 
            ]

    # add hover tool to plot
    plot.tools.append(hover)

    plot.plot_width = width
    plot.min_width = width
    plot.max_width = width*2
    plot.sizing_mode = 'scale_both'
    plot.outline_line_color = None
    plot.toolbar_location='above'
    # coloured patches for the elements:
    rects = plot.rect('group', 'period', 0.9, 0.9, source=source, alpha=alpha, color='type_color')
    plot.axis.visible = False # show axis?
    text_props = {
        'source': source,
        'angle': 0,
        'color': 'black',
        'text_align': 'left',
        'text_baseline': 'middle'
    }
    # add text for all pairs of (x,y)=(group,period)
    x = dodge("group", -0.4, range=plot.x_range)
    y = dodge("period", 0.3, range=plot.y_range)
    y2 = dodge("period", -0.3, range=plot.y_range) # to displat 'c_value' entry as well
    # here add the texts inside atom boxes
    plot.text(x=x, y='period', text='sym', text_font_style='bold', text_font_size='16pt', **text_props)
    plot.text(x=x, y=y, text='atomic_number', text_font_size='11pt', **text_props)

    txt = {0: 'num_impcalcs', 1: 'rms_mean', 2: 'rms_std', 3: 'smom_mean', 4: 'smom_std', 5: 'omom_mean', 
        6: 'omom_std', 7: 'nummag', 8: 'percent_mag', 9: 'charge_doping_mean', 10: 'DOSinGap_mean'}[0]
    color_value = plot.text(x=x, y=y2, text=txt, text_font_size='8pt', name='color_value', **text_props) # uses y2



    # deactivate grid
    plot.grid.grid_line_color = None


    # title of color bar
    names = ['# imps', '<rms>', 'rms std', 
            '<spin mom>', 'spin std', 
            '<orb mom>', 'orbital mom std', 
            '# magnetic', '% magnetic',
            '<Charge doping>', 'charge dop std', '<DOS in gap>', 'dos in gap std'
            ]
    title_name = names[0]

    # for log scale use this as ticker
    from bokeh.models import LogTicker, BasicTicker

    ticker = BasicTicker(desired_num_ticks=10)

    # add color bar
    color_bar = ColorBar(color_mapper=color_mapper_all[0],
        ticker=ticker, border_line_color=None,
        label_standoff=cbar_standoff, location=(0,0), orientation='vertical',
        scale_alpha=alpha, major_label_text_font_size=str(cbar_fontsize)+'pt',
        title=title_name, formatter=formatter_int, padding=20
    )

    if cbar_height is not None:
        color_bar.height = cbar_height

    plot.add_layout(color_bar,'right')

    """
    color_bar_plot = bk.figure(title="My color bar title", title_location="right", 
                            plot_width=100, min_width=100, sizing_mode='stretch_both',
                            toolbar_location=None)

    color_bar_plot.add_layout(color_bar, 'right')
    color_bar_plot.title.align="center"
    color_bar_plot.title.text_font_size = '12pt'
    """

    return plot, source, source_allEF, color_bar


def add_buttons_to_periodic_table(plot, source, source_allEF, color_bar):

    formatters = [formatter_int, formatter_1e, formatter_1e, 
                formatter_2f, formatter_2f, formatter_2f,
                formatter_2f, formatter_int, formatter_2f,
                formatter_2f, formatter_2f, formatter_2f, formatter_2f,
                ]



    # using radiobuttons
    names_rb, cmap_update_rb, formatter_rb, cname_rb, newtitle_rb = [], [], [], [], []
    for index in [0,3,5,8,9,11]: # num imps, smom, omom, percent mag, charge_doping, DOSinGap 
        names_rb.append(names[index])
        cmap_update_rb.append(color_mapper_all[index])
        formatter_rb.append(formatters[index])
        newtitle_rb.append(names[index])
        cname_rb.append('type_color'+str(index))

    callback_rb = CustomJS(args=dict(source=source, cbar=color_bar, cmap_update=cmap_update_rb, 
                                    formatter=formatter_rb, newtitle=newtitle_rb, 
                                    cname=cname_rb),
                        code="""
                                /// get index of active button
                                idx = cb_obj.active
                                
                                /// set color according to color name
                                source.data['type_color'] = source.data[cname[idx]]
                                /// update value of plot_component index
                                source.data['plot_component'][0] = idx
                                
                                /// update color mapper
                                cbar.color_mapper = cmap_update[idx]
                                /// update title of color bar
                                cbar.title = newtitle[idx]
                                /// update color bar formatter
                                cbar.formatter = formatter[idx]
                                
                                ///submit changes
                                source.change.emit();
                                cbar.change.emit();    
                                """
                        )
                        
    toggles = RadioButtonGroup(labels=names_rb, active=0, callback=callback_rb)
                        

    # using radiobuttons
    allsources = [source_allEF[{-200:1, 0:2, 200:3, 'all':4}[index]] for index in [-200,0,200,'all']] 
    callback_EF = CustomJS(args=dict(source=source, allsources=allsources, colorbuttons=toggles,
                                    cbar=color_bar, cmap_update=cmap_update_rb, 
                                    formatter=formatter_rb, newtitle=newtitle_rb, 
                                    cname=cname_rb),
                        code="""
                                /// get value of active button
                                idx = cb_obj.active
                                
                                /// save value of colorbuttons active value (store in plot_component)
                                ///colorbuttons.active = source.data['plot_component'][0]
                                
                                /// now overwrite data of source with new source
                                newsource = allsources[idx]
                                source.data = newsource.data
                                
                                /// restore value of colorbuttons active button etc.
                                idx = colorbuttons.active
                                
                                
                                /// set color according to color name
                                source.data['type_color'] = source.data[cname[idx]]
                                /// update value of plot_component index
                                source.data['plot_component'][0] = idx
                                
                                /// update color mapper
                                cbar.color_mapper = cmap_update[idx]
                                /// update title of color bar
                                cbar.title = newtitle[idx]
                                /// update color bar formatter
                                cbar.formatter = formatter[idx]
                                
                                
                                
                                /// finally submit changes
                                source.change.emit();
                                colorbuttons.change.emit()
                                cbar.change.emit(); 
                                """
                        )
    names_EF = ['EF= '+str(EFvalue)+'meV' for EFvalue in [-200,0,200]]+['all']
    EFbuttons = RadioButtonGroup(labels=names_EF, active=3, callback=callback_EF)
    

    EFtext = Paragraph(text="""Select Fermi level:""", width=110, align='start')
    Colortext = Paragraph(text="""Select color scale:""", width=110, align='start')


    buttonrow = row([Colortext]+[toggles])
    layout_periodic_table = column(row([EFtext]+[EFbuttons]), buttonrow , plot, sizing_mode='scale_both')

    return layout_periodic_table


def periodic_table_with_buttons():

    ptable_plot, source, all_sources, color_bar = get_periodic_table_plot()
    complete_periodic_table_plot = add_buttons_to_periodic_table(ptable_plot, source, all_sources, color_bar)

    return complete_periodic_table_plot

# standalone version
layout_periodic_table = pn.Column(judit_header, periodic_table_with_buttons(), judit_footer)


layout_periodic_table.servable()