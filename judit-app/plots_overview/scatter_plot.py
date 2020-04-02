
from plots_overview.load_data import load_all
from matplotlib import cm
from plots_overview import formatter_int, formatter_2f, formatter_1e, blank_color, initialize_periodic_table
import numpy as np
from matplotlib.colors import Normalize, LogNorm, to_hex
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Select
from bokeh.layouts import column, row
import bokeh.plotting as bkp
from bokeh.models import HoverTool
from bokeh.models import CustomJS
import panel as pn

height_plot = 500
height_hist = 150
width_plot = 700
width_hist = 200 #150

left_padding = 80


name0x = 'Zimp'
name0y = 'spinmom'
name0c = 'None'


formatters = {'Zimp': formatter_int,
            'Zhost': formatter_int,
            'ilayer': formatter_int,
            'EFshift': formatter_2f,
            'orbmom': formatter_2f,
            'rms': formatter_1e,
            'spinmom': formatter_2f,
            'etot_Ry':formatter_1e,
            }


def get_scatter_column_data_source(load_data=False):

    if not load_data:
        imp_properties_all, _, all_DOSingap, _, all_dc, _ = load_all()
        symbols, atomic_numbers, _, _, _, _ = initialize_periodic_table()


        out_all = []
        for k, v in imp_properties_all.items():
            if 'EF' not in k:
                efval = 0.0
            elif 'EF-200' in k:
                efval = -0.2
            else:
                efval = -0.4
            tmp = [v['zimp'], v['zhost'], v['ilayer'], efval, v['orbital_moment_imp'], v['rms'], v['spin_moment_imp'], v['etot_Ry']]
            out_all.append(tmp)
        out_all = np.array(out_all)


        mapping_imp_props = {0:'Zimp' ,
                            1:'Zhost' ,
                            2:'ilayer' ,
                            3:'EFshift' ,
                            4:'orbmom' ,
                            5:'rms' ,
                            6:'spinmom' ,
                            7:'etot_Ry',
                            }


        dictdata = {}
        for idx, name in mapping_imp_props.items():
            dictdata[name] = out_all[:,idx]
            if name in ['orbmom', 'spinmom']:
                dictdata[name] = np.array([i[2] for i in out_all[:,idx]])
            elif name =='ecore':
                dictdata[name] = out_all[:,12]-out_all[:,13]
                
        # take uniform sign convention
        dictdata['orbmom'] = dictdata['orbmom']*np.sign(dictdata['spinmom'])
        dictdata['spinmom'] = dictdata['spinmom']*np.sign(dictdata['spinmom'])

        # add DOS in gap and charge-transfer values
        values_DOSinGap_sorted = np.array([-0.03 for i in range(len(dictdata['ilayer']))])
        mapping = dictdata['Zimp']*1000000+1000*dictdata['Zhost']+dictdata['ilayer']+dictdata['EFshift']
        allowed_keys = list(imp_properties_all.keys())
        for k in all_DOSingap.keys():
            impname, hostname, ilayer = k.split(':')[1].split('_')[0], k.split('[')[0].split('_')[-1], k.split('[')[1].split(']')[0]
            zimp, zhost, ilayer = int(atomic_numbers[symbols==impname][0]), int(atomic_numbers[symbols==hostname][0]), int(ilayer)
            efshift = 0
            if 'EF-400' in k:
                efshift = -0.4
            elif 'EF-200' in k:
                efshift = -0.2
            # set value
            if k in allowed_keys and (1000000*zimp+1000*zhost+ilayer+efshift) in mapping:
                values_DOSinGap_sorted[np.where(mapping==(1000000*zimp+1000*zhost+ilayer+efshift))[0][0]] = all_DOSingap[k]
                
        dictdata['DOS_in_gap'] = values_DOSinGap_sorted


        values_dc_sorted = np.array([-0.02 for i in range(len(dictdata['ilayer']))])
        for k in all_dc.keys():
            impname, hostname, ilayer = k.split(':')[1].split('_')[0], k.split('[')[0].split('_')[-1], k.split('[')[1].split(']')[0]
            zimp, zhost, ilayer = int(atomic_numbers[symbols==impname][0]), int(atomic_numbers[symbols==hostname][0]), int(ilayer)
            efshift = 0
            if 'EF-400' in k:
                efshift = -0.4
            elif 'EF-200' in k:
                efshift = -0.2
            # set value
            if k in allowed_keys and (1000000*zimp+1000*zhost+ilayer+efshift) in mapping:
                values_dc_sorted[np.where(mapping==(1000000*zimp+1000*zhost+ilayer+efshift))[0][0]] = all_dc[k]
                
        dictdata['charge_doping'] = values_dc_sorted


        # add color dict entries
        dictdata['color_None'] = np.array(['navy' for i in range(len(dictdata['spinmom']))]) # default value


        for name in list(mapping_imp_props.values())+['DOS_in_gap', 'charge_doping']:
            if name == 'EFshift':
                dictdata[name] = dictdata[name]+0.2
            val = dictdata[name]
            if name=='orbmom': val = abs(val)
            norm = Normalize(vmin = min([ival for ival in val if ival is not None]), vmax = max([ival for ival in val if ival is not None]))
            cmap_scatter = cm.plasma
            colors = []
            for ival in val:
                if ival is not None:
                    colors.append(to_hex(cm.ScalarMappable(norm=norm, cmap=cmap_scatter).to_rgba(ival, alpha=0.6)))
                else:
                    colors.append(blank_color)
            colors = np.array(colors)
            dictdata['color_'+name] = colors


        # remove 'missing' data from scatterplot
        cd = dictdata['charge_doping']
        gapfill = dictdata['DOS_in_gap']
        mcd = np.where(cd==-0.02)[0]
        mgf = np.where(gapfill==-0.03)[0]
        notm = np.array(list(set(list(mcd)+list(mgf))))
        m = [i for i in range(len(cd)) if i not in notm]
        for k,v in dictdata.items():
            dictdata[k] = v[m]


        # define default values:
        dictdata['x'] = dictdata[name0x]
        dictdata['y'] = dictdata[name0y]
        dictdata['color'] = dictdata['color_'+name0c]

        # save dictdata to file for later reuse
        np.save('judit-app/data/scatter_source.npy', dictdata) 

    else:
        # Load from file
        dictdata = np.load('judit-app/data/scatter_source.npy',allow_pickle='TRUE').item()

    # save as ColumnDataSource
    source_scatter = ColumnDataSource(data=dictdata)

    return source_scatter


def make_scatterplot(source_scatter):

    scatterplot = bkp.figure(tools='pan,box_zoom,wheel_zoom,reset,lasso_select,box_select,undo,redo,save', #,save',
                             plot_width=width_plot, plot_height=height_plot,
                             min_width=width_plot, min_height=height_plot,
                             max_width=2*width_plot, max_height=2*height_plot,
                             min_border_left=left_padding, sizing_mode='scale_both'
                        )



    hover = HoverTool()
    hover.tooltips = [("Imp", " @Zimp[@Zhost] (@ilayer)"), # things displayed by hover tool, needs to be in 'source' dict
            ("EF shift", "@EFshift"), 
            ("spin", "@spinmom"), 
            ("orbmom", "@orbmom"), 
            ("charge doping", "@charge_doping"),
            ("DOS in gap", "@DOS_in_gap"),
            ]
    scatterplot.add_tools(hover)

    scatterplot.scatter('x', 'y', source=source_scatter, fill_alpha=0.1, # 0.1
                        color='color', size=10

    )
    scatterplot.xaxis.axis_label = name0x
    scatterplot.yaxis.axis_label = name0y

    return scatterplot


def get_scatterplot_and_buttons():

    source_scatter = get_scatter_column_data_source(load_data=True)
    scatterplot = make_scatterplot(source_scatter)

    callback_change_x = CustomJS(args=dict(source=source_scatter, plot=scatterplot, formatters=formatters
                                    ),
                        code="""/// get value of active button
                                var val = cb_obj.value
                                /// change x column
                                source.data['x'] = source.data[val]
                                source.change.emit()
                                /// update x axis label
                                plot.below[0].axis_label = val
                                plot.below[0].formatter = formatters[val]
                                plot.change.emit()
                                """
                        )

    callback_change_y = CustomJS(args=dict(source=source_scatter, plot=scatterplot, formatters=formatters
                                    ),
                        code="""/// get value of active button
                                var val = cb_obj.value
                                /// change y column
                                source.data['y'] = source.data[val]
                                source.change.emit()
                                /// update y axis label
                                plot.left[0].axis_label = val
                                plot.left[0].formatter = formatters[val]
                                plot.change.emit()
                                """
                        )

    callback_change_color = CustomJS(args=dict(source=source_scatter,),
                        code="""/// get value of active button
                                var val = cb_obj.value
                                /// change color column
                                source.data['color'] = source.data['color_'+val]
                                source.change.emit()
                                """
                        )


    options_select = ['Zimp', 'Zhost', 'ilayer', 'EFshift', 'rms', 'spinmom', 'orbmom', 
                    'etot_Ry', 'charge_doping', 'DOS_in_gap']

    select_x = Select(title='Choose X:', value=name0x, options=options_select, width=100, max_height=50)
    select_x.js_on_change('value', callback_change_x)
    select_y = Select(title='Choose Y:', value=name0y, options=options_select, width=100, max_height=50)
    select_y.js_on_change('value', callback_change_y)
    select_color = Select(title='Choose color:', value=name0c, options=['None']+options_select, width=100, max_height=50)
    select_color.js_on_change('value', callback_change_color)

    return scatterplot, source_scatter, select_x, select_y, select_color


def get_data_for_histograms(source_scatter):

    dict_vhist_all, dict_vhist = {}, {}
    dict_hhist_all, dict_hhist = {}, {}
    for name, data in source_scatter.data.items():
        if 'color' not in name:
            vhist, vedges = np.histogram(data, bins=50)
            dict_vhist_all[name] = {'left': 0, 'right':vhist, 'top':vedges[:-1], 'bottom':vedges[1:]}
            # copy values to hhist specs
            dict_hhist_all[name] = {}
            dict_hhist_all[name]['left'] = dict_vhist_all[name]['bottom']
            dict_hhist_all[name]['right'] = dict_vhist_all[name]['top']
            dict_hhist_all[name]['top'] = dict_vhist_all[name]['right']
    
    dict_vhist['bottom'] = dict_vhist_all[name0y]['bottom']
    dict_vhist['top'] = dict_vhist_all[name0y]['top']
    dict_vhist['right'] = dict_vhist_all[name0y]['right']

    dict_hhist['left'] = dict_hhist_all[name0x]['left']
    dict_hhist['top'] = dict_hhist_all[name0x]['top']
    dict_hhist['right'] = dict_hhist_all[name0x]['right']

    return dict_vhist, dict_hhist, dict_vhist_all, dict_hhist_all


def get_histograms(source_scatter, scatterplot):

    # create the vertical histograms
    
    dict_vhist, dict_hhist, dict_vhist_all, dict_hhist_all = get_data_for_histograms(source_scatter)

    src_hist_y = ColumnDataSource(data=dict_vhist)
    src_hist_x = ColumnDataSource(data=dict_hhist)

    # link y_range by passing scatterplot.y_range:
    yhist = bkp.figure(tools=['hover', 'box_zoom', 'reset'], toolbar_location='right', 
                       plot_width=width_hist, plot_height=height_plot,
                       x_axis_location="below", y_axis_location="right", y_range=scatterplot.y_range)
    xhist = bkp.figure(tools=['hover', 'box_zoom', 'reset'], toolbar_location='right',
                       plot_width=width_plot, plot_height=height_hist,
                       x_axis_location="above", y_axis_location="left",
                       min_border_left=left_padding, x_range=scatterplot.x_range)

    yhist.quad(source=src_hist_y, left=0, bottom='bottom', top='top', right='right', 
            fill_alpha=0.6, color='navy')
    xhist.quad(source=src_hist_x, bottom=0, left='left', right='right', top='top', 
            fill_alpha=0.6, color='navy')


    xhist.xaxis.axis_label = name0x
    xhist.yaxis.axis_label = 'counts'
    yhist.xaxis.axis_label = 'counts'
    yhist.yaxis.axis_label = name0y

    xhist.y_range.start = 0
    yhist.x_range.start = 0

    return xhist, yhist, src_hist_x, src_hist_y, dict_vhist_all, dict_hhist_all


def add_callbacks_histograms(xhist, yhist, src_hist_x, src_hist_y, dict_vhist_all, dict_hhist_all, select_x, select_y, select_color):

    callback_change_y_hist = CustomJS(args=dict(source=src_hist_y, dict_hist_all=dict_vhist_all, 
                                                select=select_y, plot=yhist, formatters=formatters
                                            ),
                                    code="""
                                        /// get value of active button
                                        var val = select.value
                                        /// change y histogram
                                        source.data['bottom'] = dict_hist_all[val]['bottom']
                                        source.data['top'] = dict_hist_all[val]['top']
                                        source.data['right'] = dict_hist_all[val]['right']
                                        source.change.emit()
                                        /// update y axis label
                                        plot.right[0].axis_label = val
                                        plot.right[0].formatter = formatters[val]
                                        plot.change.emit()
                                        """
                                    )

    callback_change_x_hist = CustomJS(args=dict(source=src_hist_x, dict_hist_all=dict_hhist_all, 
                                                select=select_x, plot=xhist, formatters=formatters
                                            ),
                                    code="""
                                        /// get value of active button
                                        var val = select.value
                                        /// change x histogram
                                        source.data['left'] = dict_hist_all[val]['left']
                                        source.data['right'] = dict_hist_all[val]['right']
                                        source.data['top'] = dict_hist_all[val]['top']
                                        source.change.emit()
                                        /// update x axis label
                                        plot.above[0].axis_label = val
                                        plot.above[0].formatter = formatters[val]
                                        plot.change.emit()
                                        """
                                    )

    # add callbacks for histograms to x/y selection buttons
    select_x.js_on_change('value', callback_change_x_hist)
    select_x.js_on_change('value', callback_change_y_hist)
    select_y.js_on_change('value', callback_change_x_hist)
    select_y.js_on_change('value', callback_change_y_hist)

    return select_x, select_y


def combine_scatterplot_with_hists(select_x, select_y, select_color, xhist, yhist, scatterplot):

    select_buttons = column(select_x, select_y, select_color, sizing_mode='scale_width')

    gspec = pn.GridSpec(sizing_mode='stretch_both', max_width=2000, max_height=1500)
    gspec[0,0:3] = xhist
    gspec[0, 3 ] = select_buttons
    gspec[1:3,0:3] = scatterplot
    gspec[1:3, 3] = yhist

    return gspec


def make_scatterplot_with_hist():
    from time import time
    times = [time()]
    scatterplot, source_scatter, select_x, select_y, select_color = get_scatterplot_and_buttons()
    times+= [time()]
    xhist, yhist, src_hist_x, src_hist_y, dict_vhist_all, dict_hhist_all = get_histograms(source_scatter, scatterplot)
    times+= [time()]
    select_x, select_y = add_callbacks_histograms(xhist, yhist, src_hist_x, src_hist_y, dict_vhist_all, dict_hhist_all, select_x, select_y, select_color)
    times+= [time()]
    layout = combine_scatterplot_with_hists(select_x, select_y, select_color, xhist, yhist, scatterplot)
    times+= [time()]
    times = np.array(times)
    print('timings scatterplot', times[1:]-times[0])

    return layout
