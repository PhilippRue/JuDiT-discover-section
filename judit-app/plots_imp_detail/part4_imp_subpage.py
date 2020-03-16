#!/usr/bin/env python
# coding: utf-8

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

