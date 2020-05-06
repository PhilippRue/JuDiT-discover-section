
import os
import panel as pn
import numpy as np
from plots_overview.load_data import load_imp_properties
from plots_imp_detail import spinner_text
from plots_imp_detail.imp_detail import preload_data
from bokeh.client import show_session
from pandas import DataFrame
from plots_imp_detail.imp_detail import get_impdata_by_name, preload_data
from plots_imp_detail.tools import get_impname_label
from global_settings import EF0

def prepare_imp_properties_lists(imp_properties_all):

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

    return zimps, ilayers, zhosts, iefs, impnames_all_sorted


class Select_Impurity():
    
    def __init__(self):

        imp_properties_all = load_imp_properties()
        zimps, ilayers, zhosts, iefs, impnames_all_sorted = prepare_imp_properties_lists(imp_properties_all)

        self.zimps = zimps
        self.ilayers = ilayers
        self.zhosts = zhosts
        self.iefs = iefs
        self.impnames_all_sorted = impnames_all_sorted

        EFvals = [ 'EF -200meV', 'EF+0meV', 'EF+200meV']
        self.EF_value = pn.widgets.Select(options=EFvals, value=EFvals[1])
        
        bounds = (int(zimps.min()),int(zimps.max()))
        self.Zimp = pn.widgets.IntRangeSlider(start=bounds[0], end=bounds[1])
        
        bounds = (int(ilayers.min()), int(ilayers.max()))
        self.layer_index = pn.widgets.IntRangeSlider(start=bounds[0], end=bounds[1])
        
        bounds = (int(zhosts.min()), int(zhosts.max()))
        self.Zhost = pn.widgets.IntRangeSlider(start=bounds[0], end=bounds[1])
        
        self.selection_widget = pn.widgets.MultiSelect(name='', options=[], size=8, max_width=200)
    
    
    def preselected_list(self):
        
        ef_select = self.EF_value.value
        zimp_select = self.Zimp.value
        layer_select = self.layer_index.value
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
        mask_find_ef = np.where(self.iefs==ief_select)
        zimps_selected, ilayers_selected = self.zimps[mask_find_ef], self.ilayers[mask_find_ef]
        zhosts_selected = self.zhosts[mask_find_ef]
        impnames_selected = self.impnames_all_sorted[mask_find_ef]
        
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
        #print(times[1:]-times[0])
        
        return list(impnames_selected)
    
    
    def update_selection_list(self):
        impname_selection = self.preselected_list()
        self.selection_widget.options = impname_selection
    
        
    def view_preselected_list(self):
        # initialize selection widget
        self.update_selection_list()
        
        return pn.Row(pn.Column(pn.Row(pn.pane.Markdown("EF value:", width=60), self.EF_value),
                                pn.Row(pn.pane.Markdown("Zimp:", width=60), self.Zimp),
                                pn.Row(pn.pane.Markdown("Layer index:", width=60), self.layer_index),
                                pn.Row(pn.pane.Markdown("Zhost:", width=60), self.Zhost)
                               ),
                      pn.Column(pn.pane.Markdown("Choose one or more impurities for detailed view or download", width=250),
                                self.selection_widget,
                                ),
                     )



def callback_selection_button(b):
    """Callback function that updates the output text."""

    global imp_select
    global output_pane
        
    # get list of selected impurities
    list_show_imps = imp_select.selection_widget.value
        
    # create a string that shows the current selection in output pane
    str_imp_list = 'no impurity selected'
    if len(list_show_imps)>0:
        str_imp_list = ''
        for iimp in list_show_imps:
            str_imp_list += '* {}\n'.format(iimp)
        str_imp_list = 'Selected impurities:\n\n{}'.format(str_imp_list)
    output_pane.object = '{}'.format(str_imp_list)
    

callback_selection_button_js="""
console.log('open link:'+url.value);
console.log(url.value.length);
if (url.value.length>0) {
    window.open(url.value);
}
"""


def reset_values(b):
    global imp_select
    imp_select.EF_value.value = imp_select.EF_value.values[1]
    imp_select.layer_index.value = (imp_select.layer_index.start, imp_select.layer_index.end)
    imp_select.Zimp.value = (imp_select.Zimp.start, imp_select.Zimp.end)
    imp_select.Zhost.value = (imp_select.Zhost.start, imp_select.Zhost.end)
    imp_select.update_selection_list()


def set_3d(b):
    global imp_select
    imp_select.Zimp.value =(21, 30)
    imp_select.update_selection_list()


def set_4d(b):
    global imp_select
    imp_select.Zimp.value =(39, 48)
    imp_select.update_selection_list()


def select_list(b):
    global imp_select
    imp_select.update_selection_list()


def link_text_field_to_multiselect(target, event):
    # get source (i.e. MultiSelect widget) from event
    source = event.new
    print('link_text_field:', source)

    # extract url
    url = ""

    # open imp detail page
    if len(source)==1:
        url = os.getenv("WEBADDRESS")
        if url is None:
            url = "http://localhost:5006/judit/"
        url += "main_imp_detail?id="+source[0]

    # open imp comparison page
    if len(source)>1:
        list_show_imps_str = ','.join(source)
        url = os.getenv("WEBADDRESS")
        if url is None:
            url = "http://localhost:5006/judit/"
        url += "main_imp_comparison?id="+list_show_imps_str

    print(url)

    # set target text with url
    print(target.value)
    target.value = url
    print(target.value)


def link_download_data_to_multiselect(target, event):
    target._clicks += 1


def get_download_button(url):
    """
    construct download buttons taking data form selection widget
    """

    @pn.depends(url)
    def get_df_from_selection(url):
        """
        get pandas dataframe from selection widget
        """
        # get list of imp names from selection widget via selection url
        impnames_all = url 
        
        print('impnames_all0', impnames_all)

        if impnames_all is not None:
            impnames_all = impnames_all.split('id=')[1]
            if ',' not in impnames_all:
                impnames_all = [impnames_all]
            else:
                impnames_all = impnames_all.split(',')
            print('impnames_all', impnames_all)
        else:
            impnames_all = []

        # fill data dict with dicts of calculations
        data_dict = {}
        first = True

        imp_properties_all, all_DOSingap, all_dc = preload_data(load_data=True, load_structure=False)

        # collect data for all imps
        for impname in impnames_all:
            impdata, _ = get_impdata_by_name(get_impname_label(impname), imp_properties_all, all_DOSingap, all_dc)
            # append to lists of data
            for key, val in impdata.items():
                if key=='Delta_EF':
                    val = EF0 - val # correct for Fermi level shift
                if first:
                    data_dict[key] = [val]
                else:
                    data_dict[key].append(val)
            first = False
        
        # convert to dataframe
        df = DataFrame(data_dict)

        return df

    @pn.depends(url)
    def get_data_to_download(url):
        """
        extract data for download and return as csv
        """
        # get pandas dataframe
        print('get_df_from_selection:', url)
        df = get_df_from_selection(url)
        print('get_df_from_selection:', df)
        from io import StringIO
        sio = StringIO()
        df.to_csv(sio)
        sio.seek(0)
        # return csv data
        return sio

    # construct download button with callback to update data
    download_button = pn.widgets.FileDownload(callback=get_data_to_download, filename='judit_data.csv', auto=False, embed=False)

    # initialize download button (mimicks the first click that transfers initial data)
    download_button.param.set_param('_clicks', download_button._clicks+1)

    return download_button


def get_buttons_with_callbacks():

    global imp_select

    # add button and output pane to show selection
    button = pn.widgets.Button(name="Show impurity details in new tab", button_type="primary")
    button.on_click(callback_selection_button)
    # make URL in auxiliary text field, this is automatically updated with each change in the MultiSelect
    url = pn.widgets.TextInput(name="Selection URL", value=None, disabled=True)#, placeholder="")
    imp_select_widget = imp_select.selection_widget
    imp_select_widget.link(url, callbacks={'value': link_text_field_to_multiselect})

    # now use url to adapt opening of new tab
    button.js_on_click(args={'url': url},
                       code=callback_selection_button_js)
    button = pn.Column(button, url) # need to show url here as well otherwise linking does not work

    button_reset_selection = pn.widgets.Button(name="Reset selection", button_type="primary", width_policy='min')
    button_reset_selection.on_click(reset_values)

    button_3d_selection = pn.widgets.Button(name="Select 3d imps.", button_type="primary", width_policy='min')
    button_3d_selection.on_click(set_3d)

    button_4d_selection = pn.widgets.Button(name="Select 4d imps.", button_type="primary", width_policy='min')
    button_4d_selection.on_click(set_4d)

    button_select_list= pn.widgets.Button(name="Apply filter", button_type="success", width_policy='min')
    button_select_list.on_click(select_list)

    download_button = get_download_button(url)
    # need to update the _clicks property of download_button manually, otherwise only the first click takes new data
    imp_select_widget.link(download_button, callbacks={'value': link_download_data_to_multiselect})

    return button, button_reset_selection, button_3d_selection, button_4d_selection, button_select_list, download_button


def construct_spinner():
    spinner = pn.pane.HTML("", width=50, height=50).servable()
    return spinner


def make_imp_selector():


    from time import time
    import numpy as np

    times = [time()]

    global spinner, output_pane, imp_select
    global imp_properties_all, all_DOSingap, all_dc

    output_pane = pn.pane.Markdown('no impurity selected', width=200)
    spinner = construct_spinner()
    imp_select = Select_Impurity()

    times+= [time()]

    button, button_reset_selection, button_3d_selection, button_4d_selection, button_select_list, download_widget = get_buttons_with_callbacks()

    times+= [time()]

    # prepare some stuff
    imp_properties_all, all_DOSingap, all_dc = preload_data(load_data=True)

    times+= [time()]

    # combine everything to a panel
    imp_select_panel = pn.Row(pn.Column(pn.pane.Markdown('####Select impurity for detail page'),
                                        imp_select.view_preselected_list(),
                                        pn.Column(
                                            pn.Row(button_select_list,
                                                button_3d_selection,
                                                button_4d_selection,
                                                button_reset_selection,
                                                ),
                                            download_widget,
                                            )
                                        ),
                              pn.Column(pn.pane.HTML('<br></br><br></br>'),
                                        button,
                                        pn.Row(output_pane, spinner),
                                       )
                            )

    times+= [time()]
    times = np.array(times)
    print('timings imp_selector:', times[1:]-times[:-1])

    return imp_select_panel
