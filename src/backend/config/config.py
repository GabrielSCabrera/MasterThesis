from .binfo import Binfo
from pathlib import Path
import numpy as np
import os

seed = 1337

np.random.seed(seed)

n_jobs = 8
term_width = 79

storage_path = Path.home() / "Documents" / "MasterThesis"

data_path = storage_path / "data"
results_path = storage_path / "results"

bins_relpath = data_path / "bins"
split_bins_relpath = data_path / "split_bins"
DNN_models_relpath = data_path / "DNN_models"
clusters_relpath = data_path / "clusters"
density_data_relpath = data_path / "density_data"

plot_2D_relpath = results_path / "img_2D"
plot_3D_relpath = results_path / "img_3D"
delden_relpath = results_path / "delden"

matlab_data_relpath = data_path / "matlab"
matlab_results_relpath = results_path / "matlab"
matlab_img_relpath = matlab_results_relpath / "img"

delden_pred_str = "del_den"
delden_savename = "delden_results"
delden_datafile = "damage_{}_s25.txt"
delden_xgb_obj = "reg:squarederror"
delden_cv_folds = 10
delden_train_data = "y_train.dat"
delden_test_data = "y_test.dat"
delden_train_pred_data = "y_train_pred.dat"
delden_test_pred_data = "y_test_pred.dat"

DNN_model_extension = ".dnn"
cluster_dir_labels = "CL{:05d}"
cluster_data = "CL_data.csv"
cluster_metadata = "CL_metadata.dat"

cluster_metadata_labels = {
    "T_macroscopic_failure": {"key": "T_mf", "type": "float"},
    "Center_position": {"key": "R_c", "type": "array_3"},
    "Mean_position": {"key": "R_m", "type": "array_3"},
}

cluster_uint_type = np.uint16

if not os.path.isdir(bins_relpath):
    msg = (
        "Missing required directory: '/Documents/MasterThesis/data/bins/'"
        f".  Dataset required in this location."
    )
    raise IOError(msg)

results_path.mkdir(exist_ok=True)
split_bins_relpath.mkdir(exist_ok=True)
DNN_models_relpath.mkdir(exist_ok=True)
clusters_relpath.mkdir(exist_ok=True)
density_data_relpath.mkdir(exist_ok=True)
plot_2D_relpath.mkdir(exist_ok=True)
plot_3D_relpath.mkdir(exist_ok=True)
delden_relpath.mkdir(exist_ok=True)
matlab_data_relpath.mkdir(exist_ok=True)
matlab_results_relpath.mkdir(exist_ok=True)
matlab_img_relpath.mkdir(exist_ok=True)

labels = ["M8_1", "M8_2", "MONZ5", "WG04"]  # Names of datasets

bin_dirs = {
    "M8_1": bins_relpath / "M8_1_bins",
    "M8_2": bins_relpath / "M8_2_bins",
    "MONZ5": bins_relpath / "MONZ5_bins",
    "WG04": bins_relpath / "WG04_bins",
}

bin_dims = {
    "M8_1": (1000, 1000, 1200),
    "M8_2": (900, 900, 1200),
    "MONZ5": (800, 800, 1200),
    "WG04": (800, 800, 1200),
}

bin_stresses = {}
bin_stresses["M8_1"] = np.concatenate(
    [np.arange(26, 82, 4), np.arange(80, 120, 2), np.arange(122, 132, 2)]
)

bin_stresses["M8_2"] = np.concatenate(
    [np.arange(152, 186), np.arange(187, 197)]
)

bin_stresses["MONZ5"] = np.concatenate(
    [
        [2, 5],
        np.arange(30, 45, 5),
        np.arange(40, 90, 5),
        np.arange(92, 132, 2),
        np.arange(131, 150),
        np.arange(150.5, 162, 0.5),
    ]
)

bin_stresses["WG04"] = np.concatenate(
    [
        [15],
        np.arange(15, 100, 5),
        np.arange(95, 115, 5),
        np.arange(112, 142, 2),
        [141],
        np.arange(144, 149),
        [
            148.5,
            149,
            142,
            143,
            149.5,
            149.5,
            150,
            150.5,
            151,
            151.5,
            152,
            152.5,
        ],
    ]
)

bins = {}
for l in labels:
    bins[l] = Binfo(l, bin_dirs[l], bin_dims[l], bin_stresses[l])
