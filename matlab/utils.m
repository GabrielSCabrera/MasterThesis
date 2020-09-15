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

    function [] = save_plot(H, filename)
      arguments
        H
        filename string
      end
      storage = "~/Documents/MasterThesis/results/matlab/img/";
      file_path = strcat(storage, filename);
      saveas(H, file_path);
    end

  end
end
