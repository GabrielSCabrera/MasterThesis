# MasterThesis

### Support

Developed and tested for the `gnome` terminal, and is likely to work on most Unix/Linux systems.

### Requirements

Dataset files (`M8_1_bins.zip`,`M8_2_bins.zip`,`MONZ5_bins.zip`, and `WG04_bins.zip`) should be saved in the directory `/home/<user>/Documents/MasterThesis/bins/`.

### Functionality

Once the data files are in place, open *this* directory in your terminal and run a command.  These are listed below:

| Command        | Description                                                       | Requirements                           | Output                    |
|----------------|-------------------------------------------------------------------|----------------------------------------|---------------------------|
| make           | Runs `main.py`                                                    | N/A                                    | N/A                       |
| make clean     | Removes all `__pycache__` directories                             | N/A                                    | N/A                       |
| make reset     | Removes all *generated* directories and files                     | N/A                                    | N/A                       |
| make split     | Splits a selected dataset into training and testing sets          | Dataset in `/data/` directory          | Compressed `.npz` arrays  |
| make train_DNN | Creates a *DNN* model using `scikit-learn` and a selected dataset | Split data in `/split_data/` directory | Trained model `.dnn` file |
