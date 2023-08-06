import pandas as pd
from scipy.stats import chi2_contingency, ttest_ind
from statsmodels.stats.multitest import multipletests
from math import log10, floor
import numpy as np
import statsmodels.api as sm

#### make cohort summary table
def summarise(data, f, med_iqr = [], mean_sd = []):
    #med_iqr factors will be calculated as median (IQR), 
    #mean_sd will be mean (sd)
    #others n (%)
    #age will automatically be 
    data_n = data[f].sum().astype(int)
    data_p = (data_n / data.shape[0]) * 100
    data_p = data_p.round(1)
    
    o_v = data_n.astype(str) + " (" + data_p.astype(str) + "%)"
    
    for x in mean_sd:
        ov_age_m = data[[x]].mean().round(2)[0].astype(str)
        ov_age_sd = data[[x]].std().round(2)[0].astype(str)
        o_v[x] = ov_age_m + " (" + ov_age_sd + ")"
    
    for x in med_iqr:
        Q1 = data[x].quantile(0.25)
        Q3 = data[x].quantile(0.75)
        IQR = Q3 - Q1
        ov_age_m = data[x].median() #.round(2).astype(str)
        #o_v[x] = ov_age_m + " (" + IQR + ")"
        o_v[x] = "{:0.2f} ({:0.2f})".format(ov_age_m, IQR)
        
    o_v['N'] = str(data.shape[0])
    
    #ov_name = "Overall (N=" + str(overall.shape[0]) + ")"
    #tbl = pd.DataFrame({ov_name: o_v})
    return o_v

def summarise_data(data, cols, rows, med_iqr = [], mean_sd = [], with_not = True, 
                   overall=True, overall_name = None, tests = None, correct=True):
    tbl = pd.DataFrame()
    if overall:
        if overall_name == None:
            overall_name = "Overall"
        tbl[overall_name] = summarise(data, rows, med_iqr, mean_sd)
    for d in cols:
        on = data[data[d]]
        not_on = data[~data[d]]
        s_on = summarise(on, rows, med_iqr, mean_sd)
        s_not_on = summarise(not_on, rows, med_iqr, mean_sd)
        tbl[d] = s_on
        if with_not:
            tbl['Not ' + d] = s_not_on
        #stats
        if tests != None:
            pvals = []
            raw_name = 'Raw p-value ' + d + ' vs. Not ' + d
            corr_name = 'Corrected p-value ' + d + ' vs. Not ' + d
            for index, row in tbl.iterrows():
                test_type = tests.get(index,'')
                p = None
                if test_type == 'ttest':
                    t, p = ttest_ind(on[index], not_on[index], nan_policy='omit')
                if test_type == 'chi2':
                    table = pd.crosstab(data[d], data[index])
                    chi2, p, dof, ex = chi2_contingency(table)
                pvals.append(p)
            tbl[raw_name] = pvals
            if correct:
                tbl[corr_name] = None
                w = ~tbl[raw_name].isna()
                r, corr, s, b = multipletests(tbl.loc[w,raw_name], method='bonferroni')
                tbl.loc[w,corr_name] = corr
    return tbl

def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)

def analyse(factors, data, significance_level = 0.05, add_constant = True):
    X = data[factors]
    y = data['Endpoint Status']

    if add_constant:
        X = sm.add_constant(X)
        
    X = X.astype(float)
    
    #model = sm.OLS(y, X).fit() #linear regression
    model = sm.Logit(y, X).fit()
    params = model.params
    conf = model.conf_int()
    conf['OR'] = params
    conf.columns = ['Lower 95%CI', 'Upper 95%CI', 'OR']
    or_ci = np.exp(conf)
    or_ci = or_ci.round(2)
    or_ci['raw P-value'] = model.pvalues
    or_ci['Significant'] = or_ci['raw P-value'] < significance_level
    print(model.summary())
    print()
    print(or_ci)
    return or_ci