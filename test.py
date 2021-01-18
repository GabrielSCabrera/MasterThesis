def B(string:str) -> str:
    '''
        Bold String Formatter
    '''
    return f'\033[1m{string}\033[m'

def I(string:str) -> str:
    '''
        Italic String Formatter
    '''
    return f'\033[3m{string}\033[m'

delden_groups = {}

delden_groups['full'] = (
    "glob_den", "sigd", "ep", "del_f", "del_sig", "del_ep", "den_p10",
    "den_p20", "den_p30", "den_p40", "den_p50", "den_mean", "den_p60",
    "den_p70", "den_p80", "den_p90", "den_max", "den_sum", "den_std",
    "den_numloc", "den_volloc", "dist_p10", "dist_p20", "dist_p30",
    "dist_p40", "dist_p50", "dist_mean", "dist_p60", "dist_p70", "dist_p80",
    "dist_p90", "dist_max", "dist_sum", "dist_std", "c_10", "c_20", "c_30",
    "c_40", "c_50", "c_60", "c_70", "c_80", "c_90", "c_len",
)

"""In files damage_EXP_s25.txt"""

delden_labels = {}

delden_labels["del_den"] = "Change in fracture density from this scan to the next."
delden_labels["glob_den"] = "Current global fracture density."
delden_labels["sigd"] = "Current macroscopic differential stress."
delden_labels["ep"] = "Current macroscopic axial strain."
delden_labels["del_f"] = "Current distance to failure."

delden_labels["del_sig"] = "Change in applied axial stress from this scan to the next."
delden_labels["del_ep"] = "Change in macroscopic axial strain from this scan to the next."

delden_labels["v_p10"] = "10ᵗʰ Percentile of Volume of Fractures."
delden_labels["v_p20"] = "20ᵗʰ Percentile of Volume of Fractures."
delden_labels["v_p30"] = "30ᵗʰ Percentile of Volume of Fractures."
delden_labels["v_p40"] = "40ᵗʰ Percentile of Volume of Fractures."
delden_labels["v_p50"] = "50ᵗʰ Percentile of Volume of Fractures."
delden_labels["v_p60"] = "60ᵗʰ Percentile of Volume of Fractures."
delden_labels["v_p70"] = "70ᵗʰ Percentile of Volume of Fractures."
delden_labels["v_p80"] = "80ᵗʰ Percentile of Volume of Fractures."
delden_labels["v_p90"] = "90ᵗʰ Percentile of Volume of Fractures."
delden_labels["v_max"] = "Maximum Volume of Fractures."
delden_labels["v_sum"] = "Sum of Volume of Fractures."
delden_labels["v_std"] = "Standard Deviation of Volume of Fractures."

delden_labels["den_p10"] = "10ᵗʰ Percentile of Density of Fractures."
delden_labels["den_p20"] = "20ᵗʰ Percentile of Density of Fractures."
delden_labels["den_p30"] = "30ᵗʰ Percentile of Density of Fractures."
delden_labels["den_p40"] = "40ᵗʰ Percentile of Density of Fractures."
delden_labels["den_p50"] = "50ᵗʰ Percentile of Density of Fractures."
delden_labels["den_p60"] = "60ᵗʰ Percentile of Density of Fractures."
delden_labels["den_p70"] = "70ᵗʰ Percentile of Density of Fractures."
delden_labels["den_p80"] = "80ᵗʰ Percentile of Density of Fractures."
delden_labels["den_p90"] = "90ᵗʰ Percentile of Density of Fractures."
delden_labels["den_max"] = "Maximum Density of Fractures."
delden_labels["den_mean"] = "Mean Density of Fractures."
delden_labels["den_sum"] = "Sum of Density of Fractures."
delden_labels["den_std"] = "Standard Deviation of Density of Fractures."

delden_labels["den_numloc"] = (
    "Number of sampling volumes with local fracture densities greater than the "
    "global fracture density."
)

delden_labels["den_volloc"] = (
    "Total fracture volume of all volumes with local greater than global "
    "fracture density."
)

delden_labels["dist_p10"] = "10ᵗʰ Percentile of Distance Between Fracture Centroids."
delden_labels["dist_p20"] = "20ᵗʰ Percentile of Distance Between Fracture Centroids."
delden_labels["dist_p30"] = "30ᵗʰ Percentile of Distance Between Fracture Centroids."
delden_labels["dist_p40"] = "40ᵗʰ Percentile of Distance Between Fracture Centroids."
delden_labels["dist_p50"] = "50ᵗʰ Percentile of Distance Between Fracture Centroids."
delden_labels["dist_p60"] = "60ᵗʰ Percentile of Distance Between Fracture Centroids."
delden_labels["dist_p70"] = "70ᵗʰ Percentile of Distance Between Fracture Centroids."
delden_labels["dist_p80"] = "80ᵗʰ Percentile of Distance Between Fracture Centroids."
delden_labels["dist_p90"] = "90ᵗʰ Percentile of Distance Between Fracture Centroids."
delden_labels["dist_mean"] = "Mean Distance Between Fracture Centroids."
delden_labels["dist_max"] = "Maximum Distance Between Fracture Centroids."
delden_labels["dist_sum"] = "Sum of Distance Between Fracture Centroids."
delden_labels["dist_std"] = "Standard Deviation of Distance Between Fracture Centroids."

delden_labels["c_10"] = "10ᵗʰ Percentile of (Pearson) Correlation Length of Densities."
delden_labels["c_20"] = "20ᵗʰ Percentile of (Pearson) Correlation Length of Densities."
delden_labels["c_30"] = "30ᵗʰ Percentile of (Pearson) Correlation Length of Densities."
delden_labels["c_40"] = "40ᵗʰ Percentile of (Pearson) Correlation Length of Densities."
delden_labels["c_50"] = "50ᵗʰ Percentile of (Pearson) Correlation Length of Densities."
delden_labels["c_60"] = "60ᵗʰ Percentile of (Pearson) Correlation Length of Densities."
delden_labels["c_70"] = "70ᵗʰ Percentile of (Pearson) Correlation Length of Densities."
delden_labels["c_80"] = "80ᵗʰ Percentile of (Pearson) Correlation Length of Densities."
delden_labels["c_90"] = "90ᵗʰ Percentile of (Pearson) Correlation Length of Densities."
delden_labels["c_len"] = "(Pearson) Correlation Length of Densities."

from textwrap import wrap

def _str_features(feats, width:int = 80) -> str:
    '''
        Returns information about the features being used in the model.
    '''
    sorted_feats = sorted(feats)
    string = map(delden_labels.get, sorted_feats)
    len_max = max(max(map(len, sorted_feats)), 9)
    string = (wrap(i, width - (len_max + 2)) for i in string)
    join_str = '\n' + ' '*(len_max+1)
    string = (join_str.join(i) for i in string)
    sorted_feats = (B(i) for i in sorted_feats)
    string = zip(sorted_feats, string)
    string = (f'{i[0]:{len_max+7}s} {I(i[1])}' for i in string)
    string = '\n'.join(string)
    title = f'{"FEATURES":{len_max}s} DEFINITIONS'
    title = B(title)
    string = f"{title}\n\n{string}"
    return string

print(_str_features(delden_groups['full']))
