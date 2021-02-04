classdef delvol_utils

  methods(Static)

    function [matrix_out] = load_csv(filename)
      % Reads the data from a .csv file and returns its values as
      % a matrix
      arguments
        filename string
      end
      storage = '~/Documents/MasterThesis/data/matlab/';
      file_path = strcat(storage, filename);
      matrix_out = readmatrix(file_path);
    end

    function [y_train, y_test, y_train_pred, y_test_pred, scores] = load_from_delvol(directory)
      % Reads the data from a set of .csv files and returns its values as
      % matrices
      arguments
        directory string
      end
      storage = '~/Documents/MasterThesis/results/delvol/';
      main_path = strcat(storage, directory);
      train_path = strcat(main_path, '/y_train.csv');
      test_path = strcat(main_path, '/y_test.csv');
      train_pred_path = strcat(main_path, '/y_train_pred.csv');
      test_pred_path = strcat(main_path, '/y_test_pred.csv');
      scores_path = strcat(main_path, '/scores.csv');

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
      storage = '~/Documents/MasterThesis/results/delvol/';
      main_path = strcat(storage, directory);
      scores_path = strcat(main_path, '/scores.csv');
      scores = readtable(scores_path, 'ReadRowNames', true);
      scores = sortrows(scores, 'RowNames');
    end

    function [headers, importances, folders] = load_importance(directory)
      % Reads the data from a set of .csv files and returns its values as
      % matrices
      arguments
        directory string
      end

      storage = '~/Documents/MasterThesis/results/delvol/';
      main_path = strcat(storage, directory);
      directory = dir(main_path);
      folders = {directory([directory.isdir]).name};
      folders = folders(~ismember(folders, {'.','..'}));
      % folders = sort(folders);
      importances = [];
      N_experiments = length(folders);

      for i = 1:N_experiments
        importance_path = strcat(main_path, '/');
        importance_path = strcat(importance_path, folders(i));
        importance_path = strcat(importance_path, '/cumulative_importance.csv');

        % opts = detectImportOptions(importance_path, 'NumHeaderLines', 1);
        importance = readtable(importance_path);
        headers = importance.Properties.VariableNames;
        importance = table2array(importance(1,:));
        importances = [importances ; importance];
      end
    end

    function [headers, importances, folders] = load_good_importance(directory)
      % Reads the data from a set of .csv files and returns its values as
      % matrices
      arguments
        directory string
      end

      storage = '~/Documents/MasterThesis/results/delvol/';
      main_path = strcat(storage, directory);
      directory = dir(main_path);
      folders = {directory([directory.isdir]).name};
      folders = folders(~ismember(folders, {'.','..'}));
      % folders = sort(folders);
      importances = [];
      N_experiments = length(folders);

      for i = 1:N_experiments
        importance_path = strcat(main_path, '/');
        importance_path = strcat(importance_path, folders(i));
        importance_path = strcat(importance_path, '/good_importances.csv');

        % opts = detectImportOptions(importance_path, 'NumHeaderLines', 1);
        importance = readtable(importance_path);
        headers = importance.Properties.VariableNames;
        importance = table2array(importance(1,:));
        importances = [importances ; importance];
      end
    end

    function [mean_filters, any_filters, weak_filters] = load_filter(directory)
      % Reads the data from a set of .dat files and returns its values

      arguments
        directory string
      end

      storage = '~/Documents/MasterThesis/results/delvol/';
      main_path = strcat(storage, directory);
      directory = dir(main_path);
      folders = {directory([directory.isdir]).name};
      folders = folders(~ismember(folders, {'.','..'}));
      mean_filters = [];
      any_filters = [];
      weak_filters = [];
      N_experiments = length(folders);

      for i = 1:N_experiments
        filter_path = strcat(main_path, '/');
        filter_path = strcat(filter_path, folders(i));
        filter_path = strcat(filter_path, '/filter.dat');

        data = readtable(filter_path);
        mean_filters = [mean_filters; data(1,1)];
        any_filters = [any_filters; data(2,1)];
        weak_filters = [weak_filters; data(3,1)];
      end
      mean_filters = table2array(mean_filters);
      any_filters = table2array(any_filters);
      weak_filters = table2array(weak_filters);
    end

    function [density_data] = load_from_density_data(filename)
      % Reads the data from a given .csv file and returns its values as
      % matrices
      arguments
        filename string
      end
      storage = '~/Documents/MasterThesis/data/density_data/';
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

      storage = '~/Documents/MasterThesis/results/delvol/';
      main_path = strcat(storage, directory);
      directory = dir(main_path);
      folders = {directory([directory.isdir]).name};
      folders = folders(~ismember(folders, {'.','..'}));
      folder = sort(folders);
      r2_train_scores = [];
      r2_test_scores = [];
      N_experiments = length(folders);

      for i = 1:N_experiments
        scores_path = strcat(main_path, '/');
        scores_path = strcat(scores_path, folders(i));
        scores_path = strcat(scores_path, '/scores.csv');

        opts = detectImportOptions(scores_path, 'NumHeaderLines', 0, 'ReadVariableNames', false);
        scores = readtable(scores_path, opts);
        r2_train = table2array(scores(:, R2_train_idx));
        r2_test = table2array(scores(:, R2_test_idx));
        r2_train_scores = [r2_train_scores r2_train];
        r2_test_scores = [r2_test_scores r2_test];
      end
    end

    function [y_train_list, y_test_list, y_train_pred_list, y_test_pred_list, r2_train, r2_test, scores, folders] = load_all_from_combined(directory)
      % Reads the data from a set of .csv files and returns its values as
      % matrices
      arguments
        directory string
      end
      R2_train_idx = 1;
      R2_test_idx = 2;

      storage = '~/Documents/MasterThesis/results/delvol/';
      main_path = strcat(storage, directory);
      directory = dir(main_path);
      folders = {directory([directory.isdir]).name};
      folders = folders(~ismember(folders, {'.','..'}));
      folder = sort(folders);

      N_experiments = length(folders);
      y_train_list = cell(N_experiments,0);
      y_test_list = cell(N_experiments,0);
      y_train_pred_list = cell(N_experiments,0);
      y_test_pred_list = cell(N_experiments,0);

      for i = 1:N_experiments
        scores_path = strcat(main_path, '/');
        scores_path = strcat(scores_path, folders(i));
        train_path = strcat(scores_path, '/y_train.csv');
        test_path = strcat(scores_path, '/y_test.csv');
        train_pred_path = strcat(scores_path, '/y_train_pred.csv');
        test_pred_path = strcat(scores_path, '/y_test_pred.csv');

        opts = detectImportOptions(train_path, 'NumHeaderLines', 0, 'ReadVariableNames', false);
        y_train = readtable(train_path, opts);
        opts = detectImportOptions(test_path, 'NumHeaderLines', 0, 'ReadVariableNames', false);
        y_test = readtable(test_path, opts);
        opts = detectImportOptions(train_pred_path, 'NumHeaderLines', 0, 'ReadVariableNames', false);
        y_train_pred = readtable(train_pred_path, opts);
        opts = detectImportOptions(test_pred_path, 'NumHeaderLines', 0, 'ReadVariableNames', false);
        y_test_pred = readtable(test_pred_path, opts);

        y_train_list{i} = y_train;
        y_test_list{i} = y_test;
        y_train_pred_list{i} = y_train_pred;
        y_test_pred_list{i} = y_test_pred;
      end

      scores_path = strcat(main_path, '/scores.csv');
      scores = readtable(scores_path, 'ReadRowNames', true);
      r2_train = table2array(scores(:, R2_train_idx));
      r2_test = table2array(scores(:, R2_test_idx));
    end

    function [y_train_list, y_test_list, y_train_pred_list, y_test_pred_list, r2_train, r2_test, scores, folders] = load_best_from_combined(directory)
      % Reads the data from a set of .csv files and returns its values as
      % matrices
      arguments
        directory string
      end
      R2_train_idx = 1;
      R2_test_idx = 2;

      storage = '~/Documents/MasterThesis/results/delvol/';
      main_path = strcat(storage, directory);
      directory = dir(main_path);
      folders = {directory([directory.isdir]).name};
      folders = folders(~ismember(folders, {'.','..'}));
      folder = sort(folders);

      N_experiments = length(folders);
      y_train_list = cell(N_experiments,0);
      y_test_list = cell(N_experiments,0);
      y_train_pred_list = cell(N_experiments,0);
      y_test_pred_list = cell(N_experiments,0);
      scores = cell(N_experiments,0);

      for i = 1:N_experiments
        scores_path = strcat(main_path, '/');
        scores_path = strcat(scores_path, folders(i));
        train_path = strcat(scores_path, '/y_train.csv');
        test_path = strcat(scores_path, '/y_test.csv');
        train_pred_path = strcat(scores_path, '/y_train_pred.csv');
        test_pred_path = strcat(scores_path, '/y_test_pred.csv');
        scores_path = strcat(scores_path, '/scores.csv');

        opts = detectImportOptions(train_path, 'NumHeaderLines', 0, 'ReadVariableNames', false);
        y_train = readtable(train_path, opts);
        opts = detectImportOptions(test_path, 'NumHeaderLines', 0, 'ReadVariableNames', false);
        y_test = readtable(test_path, opts);
        opts = detectImportOptions(train_pred_path, 'NumHeaderLines', 0, 'ReadVariableNames', false);
        y_train_pred = readtable(train_pred_path, opts);
        opts = detectImportOptions(test_pred_path, 'NumHeaderLines', 0, 'ReadVariableNames', false);
        y_test_pred = readtable(test_pred_path, opts);
        opts = detectImportOptions(scores_path, 'NumHeaderLines', 0, 'ReadVariableNames', false);
        score = readtable(scores_path, opts);

        y_train_list{i} = y_train;
        y_test_list{i} = y_test;
        y_train_pred_list{i} = y_train_pred;
        y_test_pred_list{i} = y_test_pred;
        scores{i} = score;
      end

      scores_path = strcat(main_path, '/scores.csv');
      scores_comp = readtable(scores_path, 'ReadRowNames', true);
      r2_train = table2array(scores_comp(:, R2_train_idx));
      r2_test = table2array(scores_comp(:, R2_test_idx));
    end

    function [] = save_plot(H, filename)
      arguments
        H
        filename string
      end
      storage = '~/Documents/MasterThesis/results/matlab/img/';
      file_path = strcat(storage, filename);
      saveas(H, file_path);
      msg = 'Saved MATLAB Plot to Path:';
      disp(msg);
      disp(file_path);
    end
  end
end
