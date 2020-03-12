from aiida.orm import load_node


def load_imp_properties():
    imp_properties_all = load_node('3e65d6eb-d25e-48c3-8727-c969da1aff42')
    return imp_properties_all

def load_and_sort_imp_properties_by_EFval():

    imp_properties_all = load_imp_properties().get_dict()

    # sort data according to EF value
    imp_properties_sorted = {}
    for EFset in [0, -200, -400]:
        imp_properties_sorted[EFset] = {}
        for k, v in imp_properties_all.items():
            add_element = False
            if EFset==0 and 'EF-' not in k:
                add_element = True
            elif 'EF%i'%EFset in k:
                add_element = True
            #print(EFset, k, add_element, 'EF%i'%EFset)
            if add_element:
                imp_properties_sorted[EFset][k] = v

    return imp_properties_all, imp_properties_sorted


def load_and_sort_gapfill():
    # load DOS in gap and charge-transfer values
    all_DOSingap = load_node('afe3e960-c335-4eca-8477-4e83a0dfbb53').get_dict()

    # sort after EF value
    all_DOSingap_sorted = {0:{},-200:{},-400:{}}
    for k,v in all_DOSingap.items():
        if 'EF-200' in k:
            all_DOSingap_sorted[-200][k] = v
        if 'EF-400' in k:
            all_DOSingap_sorted[-400][k] = v
        else:
            all_DOSingap_sorted[0][k] = v
    return all_DOSingap, all_DOSingap_sorted


def load_and_sort_charge_doping():

    all_dc = load_node('04724d7f-4970-4a47-9447-64db5c6f11aa').get_dict()

    # sort after EF value
    all_dc_sorted = {0:{},-200:{},-400:{}}
    for k,v in all_dc.items():
        if 'EF-200' in k:
            all_dc_sorted[-200][k] = v
        if 'EF-400' in k:
            all_dc_sorted[-400][k] = v
        else:
            all_dc_sorted[0][k] = v
    return all_dc, all_dc_sorted


def load_all():

    imp_properties_all, imp_properties_sorted = load_and_sort_imp_properties_by_EFval()
    all_DOSingap, all_DOSingap_sorted = load_and_sort_gapfill()
    all_dc, all_dc_sorted = load_and_sort_charge_doping()

    return imp_properties_all, imp_properties_sorted, all_DOSingap, all_DOSingap_sorted, all_dc, all_dc_sorted 
