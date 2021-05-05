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

    function [headers] = rewrite_headers()
      % Replaces headers with percentiles
      headers = ["min", "25%", "50%", "75%", "max", "min", "25%", "50%", "75%", "max", "min", "25%", "50%", "75%", "max", "min", "25%", "50%", "75%", "max", "min", "25%", "50%", "75%", "max", "min", "25%", "50%", "75%", "max", "min", "25%", "50%", "75%", "max", "25%", "50%", "75%", "max", "tot_vol", "rand"];
    end

    function [out] = rewrite_folders(folders)
      % Replaces headers with percentiles
      orig = ["M8_1" "M8_2" "MONZ3" "MONZ4" "MONZ5" "WG01" "WG02" "WG04"];
      new = ["Marble 1" "Marble 2" "Monzonite 3" "Monzonite 4" "Monzonite 5" "Granite 1" "Granite 2" "Granite 4"];
      out = [];

      for i=1:length(folders)
        for j=1:length(orig)
          if orig(j) == folders(i)
            out = [out new(j)];
            break
          end
        end
      end
    end

    function [ax] = add_vlines(ax)
      % Adds vertical lines to separate features by category
      idx = [5. 10. 15. 20. 25. 30. 35. 39.];
      % names = ["dmin", "th1", "th3", "l1", "l3", "ani", "vol", "dc"];
      names = ["$d_{min}$", "$\theta_1$", "$\theta_3$", "$L_{min}$", "$L_{max}$", "$A$", "$v$", "$d_c$"];
      diff = 0.5;
      ypos_ratio = 1.04;
      ypos = ylim(ax);
      ypos = ypos_ratio*(ypos(2)-ypos(1));
      for i = 1:length(idx)
        xline(ax, idx(i) + diff, 'k', 'LineWidth', 2);
        if i == 1
          xpos = idx(i)/2;
        else
          xpos = (idx(i)-idx(i-1))/2 + idx(i-1);
        end
        text(ax, xpos, ypos, names(:,i), 'FontSize', 18, 'FontWeight','bold', 'HorizontalAlignment', 'center', 'Interpreter', 'latex');
      end
      ax.LineWidth = 2;
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

    function [x_points] = load_logspace(directory)
      % Reads the data from a set of .dat files and returns its values

      arguments
        directory string
      end

      storage = '~/Documents/MasterThesis/results/delvol/';
      main_path = strcat(storage, directory);
      directory = dir(main_path);
      points_path = strcat(main_path, '/logspace_x_points.dat');
      x_points = readtable(points_path,'ReadVariableNames',false);
      x_points = table2array(x_points);
      x_points = str2double(x_points);
    end

    function [x_points] = load_linspace(directory)
      % Reads the data from a set of .dat files and returns its values

      arguments
        directory string
      end

      storage = '~/Documents/MasterThesis/results/delvol/';
      main_path = strcat(storage, directory);
      directory = dir(main_path);
      points_path = strcat(main_path, '/linspace_x_points.dat');
      x_points = readtable(points_path,'ReadVariableNames',false);
      x_points = table2array(x_points);
      x_points = str2double(x_points);
    end

    function [sigd, strain] = load_stress_strain(filename)
      % Reads the data from a .csv file and returns its values

      arguments
        filename string
      end

      storage = '~/Documents/MasterThesis/data/stress_strain_exps/';
      path = strcat(storage, filename);
      load(path)

      sigd = times_real(:,3);
      strain = times_real(:,2);
    end

    function [sigd, val] = load_plot_from_prep_no_outliers(filename)
      % Reads the data from a set of .csv files and returns its values

      arguments
        filename string
      end

      storage = '~/Documents/MasterThesis/data/formatted_data/';
      path = strcat(storage, filename);
      data = readtable(path);
      data = table2array(data);
      data = rmoutliers(data);
      sigd = data(:,1);
      val = data(:,2);
    end

    function [sigd, val] = load_plot_from_prep(filename)
      % Reads the data from a set of .csv files and returns its values

      arguments
        filename string
      end

      storage = '~/Documents/MasterThesis/data/formatted_data/';
      path = strcat(storage, filename);
      data = readtable(path);
      data = table2array(data);
      sigd = data(:,1);
      val = data(:,2);
    end

    function [sigd, mean, std] = load_plot_from_prep_no_outliers_avg(filename)
      % Reads the data from a set of .csv files and returns its values

      arguments
        filename string
      end

      storage = '~/Documents/MasterThesis/data/formatted_data/';
      path = strcat(storage, filename);
      data = readtable(path);
      data = table2array(data);
      data = rmoutliers(data);
      sigd = data(:,1);
      mean = data(:,2);
      std = data(:,3);
    end

    function [sigd, mean, std] = load_plot_from_prep_avg(filename)
      % Reads the data from a set of .csv files and returns its values

      arguments
        filename string
      end

      storage = '~/Documents/MasterThesis/data/formatted_data/';
      path = strcat(storage, filename);
      data = readtable(path);
      data = table2array(data);
      sigd = data(:,1);
      mean = data(:,2);
      std = data(:,3);
    end

    function [delvtot, points] = load_plot_from_prep_delvtot(filename1, filename2)
      % Reads the data from a set of .csv files and returns its values

      arguments
        filename1 string
        filename2 string
      end

      storage = '~/Documents/MasterThesis/data/formatted_data/';
      path = strcat(storage, filename1);
      data = readtable(path);
      data = table2array(data);
      points = data(:,2);

      storage2 = '~/Documents/MasterThesis/data/formatted_data/';
      path2 = strcat(storage2, filename2);
      data2 = readtable(path2);
      data2 = table2array(data2);
      delvtot = data2(:,2);

    end

    function [sigd, points] = load_plot_from_prep_sigd(filename1, filename2)
      % Reads the data from a set of .csv files and returns its values

      arguments
        filename1 string
        filename2 string
      end

      storage = '~/Documents/MasterThesis/data/formatted_data/';
      path = strcat(storage, filename1);
      data = readtable(path);
      data = table2array(data);
      points = data(:,2);

      storage2 = '~/Documents/MasterThesis/data/formatted_data/';
      path2 = strcat(storage2, filename2);
      data2 = readtable(path2);
      data2 = table2array(data2);
      sigd = data2(:,2);

    end


    function [N_good] = load_N_good(directory)
      % Reads the data from a set of .dat files and returns its values

      arguments
        directory string
      end

      storage = '~/Documents/MasterThesis/results/delvol/';
      main_path = strcat(storage, directory);
      directory = dir(main_path);
      folders = {directory([directory.isdir]).name};
      folders = folders(~ismember(folders, {'.','..'}));
      N_good = [];
      N_experiments = length(folders);

      for i = 1:N_experiments
        filter_path = strcat(main_path, '/');
        filter_path = strcat(filter_path, folders(i));
        filter_path = strcat(filter_path, '/N_good.dat');

        data = readtable(filter_path);
        N_good = [N_good; data(1,1)];
      end
      N_good = table2array(N_good);
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
      folders = sort(folders);
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

    function [y_train_list, y_test_list, y_train_pred_list, y_test_pred_list, r2_train, r2_test, scores, folders] = load_all_from_combined_final(directory)
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

      scores_path = strcat(main_path, '/MONZ3/scores.csv');
      scores = readtable(scores_path, 'ReadRowNames', false);
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
