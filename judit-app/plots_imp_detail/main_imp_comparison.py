from plots_imp_detail.imp_comparison import create_imp_comparison_page
from plots_imp_detail.imp_detail import preload_data
from bokeh.io import curdoc

# extract name of imps
try:
    name = curdoc().session_context.request.arguments.get('id')[0]
    if isinstance(name, bytes):
        list_show_imps_str = name.decode()
        list_show_imps = []
        for i in list_show_imps_str.split(' ')[1:]:
            tmp = tmp.replace('%', ' ')
            if tmp[0]==' ': tmp = tmp[1:]
            tmp = tmp.split('?bokeh-session-id')[0]
            list_show_imps.append(tmp)
except:
    list_show_imps = None
print(list_show_imps)


# set global variables
imp_properties_all, all_DOSingap, all_dc = preload_data(load_data=True)

# open comparison page
imp_cmp_page_full = create_imp_comparison_page(list_show_imps, imp_properties_all, all_DOSingap, all_dc, return_full_page=True)

imp_cmp_page_full.servable()

