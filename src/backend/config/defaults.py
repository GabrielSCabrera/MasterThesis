from pathlib import Path

delden_xgb_gridsearch_defaults = {
    "colsample_bytree": [0.8, 0.9],
    "alpha":            [0, 3],
    "learning_rate":    [0.1, 0.2],
    "n_estimators":     [200, 300],
    "max_depth":        [4, 5, 6]
}

delvol_xgb_gridsearch_defaults = {
    "colsample_bytree": [0.8, 0.9],
    "alpha":            [0, 3],
    "learning_rate":    [0.1, 0.2],
    "n_estimators":     [200, 300],
    "max_depth":        [4, 5, 6]
}

data_bucket_files = [
    Path('stress_strain_exps_npy') / 'times_M8_1.npy',
    Path('stress_strain_exps_npy') / 'times_M8_2.npy',
    Path('stress_strain_exps_npy') / 'times_MONZ3.npy',
    Path('stress_strain_exps_npy') / 'times_MONZ4.npy',
    Path('stress_strain_exps_npy') / 'times_MONZ5.npy',
    Path('stress_strain_exps_npy') / 'times_WG01.npy',
    Path('stress_strain_exps_npy') / 'times_WG02.npy',
    Path('stress_strain_exps_npy') / 'times_WG04.npy',
    Path('stress_strain_exps') / 'times_M8_1.mat',
    Path('stress_strain_exps') / 'times_M8_2.mat',
    Path('stress_strain_exps') / 'times_MONZ3.mat',
    Path('stress_strain_exps') / 'times_MONZ4.mat',
    Path('stress_strain_exps') / 'times_MONZ5.mat',
    Path('stress_strain_exps') / 'times_WG01.mat',
    Path('stress_strain_exps') / 'times_WG02.mat',
    Path('stress_strain_exps') / 'times_WG04.mat',
    Path('delvol_data') / 'M8_1_3D_delvol_a3000_subv300.txt',
    Path('delvol_data') / 'M8_2_3D_delvol_a3000_subv300.txt',
    Path('delvol_data') / 'MONZ3_3D_delvol_a3000_subv300.txt',
    Path('delvol_data') / 'MONZ4_3D_delvol_a3000_subv300.txt',
    Path('delvol_data') / 'MONZ5_3D_delvol_a3000_subv300.txt',
    Path('delvol_data') / 'WG01_3D_delvol_a3000_subv300.txt',
    Path('delvol_data') / 'WG02_3D_delvol_a3000_subv300.txt',
    Path('delvol_data') / 'WG04_3D_delvol_a3000_subv300.txt',
    Path('density_data') / 'damage_WG02_s25_d9.txt',
    Path('density_data') / 'damage_WG04_s25_d9.txt',
    Path('density_data') / 'damage_MONZ4_s25_d9.txt',
    Path('density_data') / 'damage_M8_2_s25_d9.txt',
    Path('density_data') / 'damage_M8_1_s25_d9.txt',
    Path('density_data') / 'damage_MONZ5_s25_d9.txt',
    Path('density_data') / 'damage_MONZ3_s25_d9.txt',
    Path('density_data') / 'damage_WG01_s25_d9.txt',
    Path('density_data') / 'damage_WG02_s25.txt',
    Path('density_data') / 'damage_WG04_s25.txt',
    Path('density_data') / 'damage_MONZ4_s25.txt',
    Path('density_data') / 'damage_M8_2_s25.txt',
    Path('density_data') / 'damage_M8_1_s25.txt',
    Path('density_data') / 'damage_MONZ5_s25.txt',
    Path('density_data') / 'damage_MONZ3_s25.txt',
    Path('density_data') / 'damage_WG01_s25.txt',
    Path('bins') / 'WG04_bins.zip',
    Path('bins') / 'MONZ5_bins.zip',
    Path('bins') / 'M8_2_bins.zip',
    Path('bins') / 'M8_1_bins.zip',
    Path('input_txts') / 'WG04_3D_frac_full_a3000.txt',
    Path('input_txts') / 'MONZ5_3D_frac_full_a500.txt',
    Path('input_txts') / 'WG04_3D_frac_full_a500.txt',
    Path('input_txts') / 'MONZ5_3D_frac_full_a1000.txt',
    Path('input_txts') / 'M8_2_3D_frac_full_a500.txt',
    Path('input_txts') / 'M8_1_3D_frac_full_a1000.txt',
    Path('input_txts') / 'MONZ5_3D_frac_full_a2000.txt',
    Path('input_txts') / 'M8_2_3D_frac_full_a3000.txt',
    Path('input_txts') / 'M8_2_3D_frac_full_a1000.txt',
    Path('input_txts') / 'M8_1_3D_frac_full_a3000.txt',
    Path('input_txts') / 'MONZ5_3D_frac_full_a3000.txt',
    Path('input_txts') / 'WG04_3D_frac_full_a2000.txt',
    Path('input_txts') / 'M8_1_3D_frac_full_a2000.txt',
    Path('input_txts') / 'WG04_3D_frac_full_a1000.txt',
    Path('input_txts') / 'M8_1_3D_frac_full_a500.txt',
    Path('input_txts') / 'M8_2_3D_frac_full_a2000.txt',
]
