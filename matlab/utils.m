classdef utils

  methods(Static)

    function [matrix_out] = load_csv(filename)
      % Reads the data from a .csv file and returns its values as
      % a matrix
      arguments
        filename string
      end
      storage = "~/Documents/MasterThesis/data/matlab/";
      file_path = strcat(storage, filename);
      matrix_out = readmatrix(file_path);
    end

    function [y_train, y_test, y_train_pred, y_test_pred, scores] = load_from_delden(directory)
      % Reads the data from a set of .csv files and returns its values as
      % matrices
      arguments
        directory string
      end
      storage = "~/Documents/MasterThesis/results/delden/";
      main_path = strcat(storage, directory);
      train_path = strcat(main_path, "/y_train.csv");
      test_path = strcat(main_path, "/y_test.csv");
      train_pred_path = strcat(main_path, "/y_train_pred.csv");
      test_pred_path = strcat(main_path, "/y_test_pred.csv");
      scores_path = strcat(main_path, "/scores.csv");

      opts = detectImportOptions(train_path, 'NumHeaderLines', 0, 'ReadVariableNames', false);
      y_train = readtable(train_path, opts);
      opts = detectImportOptions(test_path, 'NumHeaderLines', 0, 'ReadVariableNames', false);
      y_test = readtable(test_path, opts);
      opts = detectImportOptions(train_pred_path, 'NumHeaderLines', 0, 'ReadVariableNames', false);
      y_train_pred = readtable(train_pred_path, opts);
      opts = detectImportOptions(test_pred_path, 'NumHeaderLines', 0, 'ReadVariableNames', false);
      y_test_pred = readtable(test_pred_path, opts);
      opts = detectImportOptions(scores_path, 'NumHeaderLines', 0, 'ReadVariableNames', false);
      scores = readtable(scores_path, opts);
    end

    function [scores] = load_from_combined(directory)
      % Reads the data from a set of .csv files and returns its values as
      % matrices
      arguments
        directory string
      end
      storage = "~/Documents/MasterThesis/results/delden/";
      main_path = strcat(storage, directory);
      scores_path = strcat(main_path, "/scores.csv");
      scores = readtable(scores_path, 'ReadRowNames', true);
      scores = sortrows(scores, 'RowNames');
    end

    function [density_data] = load_from_density_data(filename)
      % Reads the data from a given .csv file and returns its values as
      % matrices
      arguments
        filename string
      end
      storage = "~/Documents/MasterThesis/data/density_data/";
      path = strcat(storage, filename);
      density_data = readtable(path, 'ReadVariableNames', true);
    end

    function [r2_train_scores, r2_test_scores, folders] = load_R2_from_combined(directory)
      % Reads the data from a set of .csv files and returns its values as
      % matrices
      arguments
        directory string
      end
      R2_train_idx = 1;
      R2_test_idx = 2;

      storage = "~/Documents/MasterThesis/results/delden/";
      main_path = strcat(storage, directory);
      directory = dir(main_path);
      folders = {directory([directory.isdir]).name};
      folders = folders(~ismember(folders, {'.','..'}));
      folder = sort(folders);
      r2_train_scores = [];
      r2_test_scores = [];
      N_experiments = length(folders);

      for i = 1:N_experiments
        scores_path = strcat(main_path, "/");
        scores_path = strcat(scores_path, folders(i));
        scores_path = strcat(scores_path, "/scores.csv");

        opts = detectImportOptions(scores_path, 'NumHeaderLines', 0, 'ReadVariableNames', false);
        scores = readtable(scores_path, opts);
        r2_train = table2array(scores(:, R2_train_idx));
        r2_test = table2array(scores(:, R2_test_idx));
        r2_train_scores = [r2_train_scores r2_train];
        r2_test_scores = [r2_test_scores r2_test];
      end
    end

    function [] = save_plot(H, filename)
      arguments
        H
        filename string
      end
      storage = "~/Documents/MasterThesis/results/matlab/img/";
      file_path = strcat(storage, filename);
      saveas(H, file_path);
      msg = 'Saved MATLAB Plot to Path:';
      disp(msg);
      disp(file_path);
    end
  end
end
