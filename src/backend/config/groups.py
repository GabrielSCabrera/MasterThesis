"""GROUPS OF FEATURES FOR CLASS DelDensity"""

delden_groups = {}

delden_groups['full'] = [
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

"""GROUPS OF EXPERIMENTS FOR CLASS DelDensity"""

delden_exps = {}

delden_exps['full'] = [
    "M8_1", "M8_2", "MONZ3", "MONZ4", "MONZ5", "WG01", "WG02", "WG04"
]
delden_exps['exp1s'] = [
    "M8_1", "M8_2"
]
delden_exps['exp2s'] = [
    "MONZ3", "MONZ4", "MONZ5"
]
delden_exps['exp3s'] = [
    "WG01", "WG02", "WG04"
]
delden_exps['exp4s'] = [
    "MONZ3", "MONZ4", "MONZ5", "WG01", "WG02", "WG04"
]
