% https://se.mathworks.com/matlabcentral/answers/175881-save-folder-one-above-current-directory
directory  = pwd;
storage = "/Documents/MasterThesis/data/matlab/input_data/";
idcs   = strfind(directory'/');
home_directory = directory(1:idcs(end)-1);
filename = "test_file.dat";

opts = detectImportOptions(path);
A = readmatrix(filename, opts);
