from pathlib import Path

delden_xgb_gridsearch_defaults = {
    "colsample_bytree": [0.8, 0.9],
    "alpha":            [0, 3],
    "learning_rate":    [0.1, 0.2],
    "n_estimators":     [200, 300],
    "max_depth":        [4, 5, 6]
}

data_bucket_files = [
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
