import bokeh.plotting as bkp
import numpy as np
from plots_imp_detail.tools import get_impname_label
from plots_imp_detail.imp_detail import plot_impdos
import panel as pn
from bokeh.palettes import Set1_8 as palette
from plots_imp_detail.imp_detail import get_impdata_by_name
from about import judit_footer, judit_header
from plots_imp_detail.imp_detail import preload_data
import traceback

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
    



def create_imp_comparison_page(list_show_imps, imp_properties_all, all_DOSingap, all_dc, return_full_page, debug=False): 
    if list_show_imps is not None:
        source = {'Zimp':[], 'impurity index':[], 'spin mom.':[], 
                'orb mom.':[], 'DOS in gap':[], 'charge doping':[],
                'color':[]
                }
        
        ii = 0
        error_messages = []
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
                

            try:
                impdata, _ = get_impdata_by_name(impname_select, imp_properties_all, 
                                                 all_DOSingap, all_dc, noref=True)
                source['Zimp'].append(impdata['zimp'])
                source['impurity index'].append(ii)
                source['spin mom.'].append(impdata['spin_moment_imp'][-1])
                source['orb mom.'].append(impdata['orbital_moment_imp'][-1])
                source['DOS in gap'].append(impdata['DOS_in_gap'])
                source['charge doping'].append(impdata['charge_doping'])
                source['color'].append(color)
            except:
                error_messages.append('Error loading  {}'.format(impname_select))
                if debug: traceback.print_exc()
 
            ii+=1
            
        source = bkp.ColumnDataSource(data=source)
        
        # create scatter plots
        scatterplot0 = get_scatterplot(source, 'impurity index', 'spin mom.', 'impurity index', 
                                    'spin moment (mu_B)', 'Spin moment', yrange_min=(-0.1,0.1))
        title = pn.Row(pn.Column(pn.pane.HTML('<br></br>'),
                                pn.pane.Markdown("### Physical properties of the impurity", width=500),
                                ),
                    #pn.pane.HTML("<img  align='right' src='https://www.fz-juelich.de/SiteGlobals/StyleBundles/Bilder/NeuesLayout/logo.jpg?__blob=normal' width='150'/>"),
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
        info_text = """
    ## Impurity comparison page


    Comparison plots for the selected impurities.
    Shown are 

    * impurity density of states
    * impurity properties vs. impurities
        * spin and orbital moment
        * DOS in gap
        * charge doping

    The colors used in the DOS plot are reused for the datapoints in the plots showing the physical properties (right column).
        """
        for error in error_messages:
            info_text += "\n\n"+error
        info_text = pn.pane.Markdown(info_text, width=600)

        output_imp_cmp_update =  pn.Row(pn.Column(info_text,
                                                    impdos_plot),
                                        scatterplots
                                        )
    else:
        output_imp_cmp_update = pn.pane.Markdown("No impurities selected")

    # build imp comparison page
    output_imp_cmp_full = pn.Column(judit_header,
                                    output_imp_cmp_update,
                                    judit_footer
                                    )

    if return_full_page:
        return output_imp_cmp_full
    else:
        return output_imp_cmp_update

    #output_imp_cmp.show(title="Impurity comparison page", verbose=True)


