"""GROUPS OF FEATURES FOR CLASS DelDensity"""

delden_groups = {}
delvol_groups = {}

delden_groups['all'] = [
    "glob_den", "sigd", "ep", "del_f", "del_sig", "del_ep", "den_p10",
    "den_p20", "den_p30", "den_p40", "den_p50", "den_mean", "den_p60",
    "den_p70", "den_p80", "den_p90", "den_max", "den_sum", "den_std",
    "den_numloc", "den_volloc", "dist_p10", "dist_p20", "dist_p30",
    "dist_p40", "dist_p50", "dist_mean", "dist_p60", "dist_p70", "dist_p80",
    "dist_p90", "dist_max", "dist_sum", "dist_std", "c_10", "c_20", "c_30",
    "c_40", "c_50", "c_60", "c_70", "c_80", "c_90", "c_len",
]

delden_groups['noglobden'] = [
    "sigd", "ep", "del_f", "del_sig", "del_ep", "den_p10", "den_p20",
    "den_p30", "den_p40", "den_p50", "den_mean", "den_p60", "den_p70",
    "den_p80", "den_p90", "den_max", "den_sum", "den_std", "den_numloc",
    "den_volloc", "dist_p10", "dist_p20", "dist_p30", "dist_p40",
    "dist_p50", "dist_mean", "dist_p60", "dist_p70", "dist_p80",
    "dist_p90", "dist_max", "dist_sum", "dist_std", "c_10", "c_20",
    "c_30", "c_40", "c_50", "c_60", "c_70", "c_80", "c_90", "c_len",
]

delden_groups['micro'] = [
    "den_p10", "den_p20", "den_p30", "den_p40", "den_p50", "den_mean",
    "den_p60", "den_p70", "den_p80", "den_p90", "den_max", "den_sum",
    "den_std", "den_numloc", "den_volloc", "dist_p10", "dist_p20",
    "dist_p30", "dist_p40", "dist_p50", "dist_mean", "dist_p60",
    "dist_p70", "dist_p80", "dist_p90", "dist_max", "dist_sum",
    "dist_std", "c_10", "c_20", "c_30", "c_40", "c_50", "c_60", "c_70",
    "c_80", "c_90", "c_len",
]

delden_groups['curr'] = [
    "glob_den", "sigd", "ep", "den_p10", "den_p20", "den_p30",
    "den_p40", "den_p50", "den_mean", "den_p60", "den_p70", "den_p80",
    "den_p90", "den_max", "den_sum", "den_std", "den_numloc",
    "den_volloc", "dist_p10", "dist_p20", "dist_p30", "dist_p40",
    "dist_p50", "dist_mean", "dist_p60", "dist_p70", "dist_p80",
    "dist_p90", "dist_max", "dist_sum", "dist_std", "c_10", "c_20",
    "c_30", "c_40", "c_50", "c_60", "c_70", "c_80", "c_90", "c_len",
]

"""GROUPS OF FEATURES FOR CLASS DelVolDensity"""

delvol_groups['all'] = [
    'dmin_min', 'dmin_25', 'dmin_50', 'dmin_75', 'dmin_max', 'th1_min',
    'th1_25', 'th1_50', 'th1_75', 'th1_max', 'th3_min', 'th3_25', 'th3_50',
    'th3_75', 'th3_max', 'l1_min', 'l1_25', 'l1_50', 'l1_75', 'l1_max',
    'l3_min', 'l3_25', 'l3_50', 'l3_75', 'l3_max', 'ani_min', 'ani_25',
    'ani_50', 'ani_75', 'ani_max', 'vol_min', 'vol_25', 'vol_50', 'vol_75',
    'vol_max', 'dc_25', 'dc_50', 'dc_75', 'dc_max', 'tot_vol', 'rand'
]

"""GROUPS OF EXPERIMENTS FOR CLASS DelDensity"""

delden_exps = {}

delden_exps['all'] = [
    "M8_1", "M8_2", "MONZ3", "MONZ4", "MONZ5", "WG01", "WG02", "WG04"
]
delden_exps['M8'] = [
    "M8_1", "M8_2"
]
delden_exps['MONZ'] = [
    "MONZ3", "MONZ4", "MONZ5"
]
delden_exps['WG'] = [
    "WG01", "WG02", "WG04"
]
delden_exps['MONZ-WG'] = [
    "MONZ3", "MONZ4", "MONZ5", "WG01", "WG02", "WG04"
]

"""GROUPS OF EXPERIMENTS FOR CLASS DelDensity"""

delvol_exps = {}

delvol_exps['all'] = [
    "M8_1", "M8_2", "MONZ3", "MONZ4", "MONZ5", "WG01", "WG02", "WG04"
]
delvol_exps['M8'] = [
    "M8_1", "M8_2"
]
delvol_exps['MONZ'] = [
    "MONZ3", "MONZ4", "MONZ5"
]
delvol_exps['WG'] = [
    "WG01", "WG02", "WG04"
]
delvol_exps['MONZ-WG'] = [
    "MONZ3", "MONZ4", "MONZ5", "WG01", "WG02", "WG04"
]
