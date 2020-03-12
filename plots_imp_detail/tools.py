

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