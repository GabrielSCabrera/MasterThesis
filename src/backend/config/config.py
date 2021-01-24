from pathlib import Path
import numpy as np
import os

seed = 1337

np.random.seed(seed)

n_jobs = -2
term_width = 80

# MAIN DIRECTORIES
documents_path = Path.home() / "Documents"
storage_path = documents_path / "MasterThesis"
hidden_path = Path.home() / ".MasterThesis"
credentials_path = hidden_path / "credentials"
package_root_path = Path(__file__).parent.parent.parent

data_url_root = Path(
    r"storage.googleapis.com/gsc_thesis"
)
data_url = data_url_root / "data"
bins_url = data_url / "bins"
density_data_url = data_url / "density_data"
denvolden_data_url = data_url / "delvol_data"

data_path = storage_path / "data"
results_path = storage_path / "results"

# SUBDIRECTORIES
bins_relpath = data_path / "bins"
input_txts_relpath = data_path / "input_txts"
split_bins_relpath = data_path / "split_bins"
DNN_models_relpath = data_path / "DNN_models"
clusters_relpath = data_path / "clusters"
density_data_relpath = data_path / "density_data"
delvol_data_relpath = data_path / "delvol_data"

plot_2D_relpath = results_path / "img_2D"
plot_3D_relpath = results_path / "img_3D"
delden_relpath = results_path / "delden"
delvol_relpath = results_path / "delvol"

matlab_data_relpath = data_path / "matlab"
matlab_results_relpath = results_path / "matlab"
matlab_img_relpath = matlab_results_relpath / "img"

# FILES
matlab_files_abspath = package_root_path / "frontend" / "matlab"

delden_pred_str = "del_den"
delden_savename = "delden_results"
delden_datafile = "damage_{}_s25_d9.txt"
delden_xgb_obj = "reg:squarederror"
delden_cv_folds = 10
delden_train_data = "y_train.csv"
delden_test_data = "y_test.csv"
delden_train_pred_data = "y_train_pred.csv"
delden_test_pred_data = "y_test_pred.csv"
delden_scores_data = "scores.csv"

delvol_pred_str = "delv50"
delvol_savename = "delden_results"
delvol_datafile = "{}_3D_delvol_a3000_subv300.txt"
delvol_xgb_obj = "reg:squarederror"
delvol_cv_folds = 10
delvol_train_data = "y_train.csv"
delvol_test_data = "y_test.csv"
delvol_train_pred_data = "y_train_pred.csv"
delvol_test_pred_data = "y_test_pred.csv"
delvol_scores_data = "scores.csv"
delvol_importance_data = "cumulative_importance.csv"
delvol_shap_data = "shap.csv"
delvol_models_dir = "models"
delvol_model_names = "model_{:03d}"
delvol_R2_threshold = 0.7
delvol_filter_data = "filter.dat"

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

documents_path.mkdir(exist_ok = True)
storage_path.mkdir(exist_ok = True)
hidden_path.mkdir(exist_ok = True)
data_path.mkdir(exist_ok = True)
bins_relpath.mkdir(exist_ok = True)
results_path.mkdir(exist_ok = True)
split_bins_relpath.mkdir(exist_ok = True)
DNN_models_relpath.mkdir(exist_ok = True)
clusters_relpath.mkdir(exist_ok = True)
density_data_relpath.mkdir(exist_ok = True)
delvol_data_relpath.mkdir(exist_ok = True)
plot_2D_relpath.mkdir(exist_ok = True)
plot_3D_relpath.mkdir(exist_ok = True)
delden_relpath.mkdir(exist_ok = True)
delvol_relpath.mkdir(exist_ok = True)
matlab_data_relpath.mkdir(exist_ok = True)
matlab_results_relpath.mkdir(exist_ok = True)
matlab_img_relpath.mkdir(exist_ok = True)
credentials_path.mkdir(exist_ok = True)
input_txts_relpath.mkdir(exist_ok = True)

labels = ["M8_1", "M8_2", "MONZ5", "WG04"]  # Names of datasets
