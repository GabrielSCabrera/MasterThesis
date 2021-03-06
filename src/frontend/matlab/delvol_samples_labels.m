[r2_train_scores, r2_test_scores, folders] = delvol_utils.load_R2_from_combined(directory);
[y_train, y_test, y_train_pred, y_test_pred, r2_train, r2_test, scores, folders] = delvol_utils.load_all_from_combined(directory);

fig = figure();
ax = gca();
hold on

[foo, N_tabs] = size(y_train_pred);
for i = 1:N_tabs
  tab = y_train_pred{i};
  [N_rows, N_cols] = size(tab);
  for j = 1:N_rows
    row = tab(j,:);
    number = 0;
    for k = 1:width(row)
      if str2double(row(1,k)) ~= 0
        number = number + 1;
      end
    end
    l1 = plot(i, number, 'rs');
  end
end

[foo, N_tabs] = size(y_test_pred);
for i = 1:N_tabs
  tab = y_test_pred{i};
  [N_rows, N_cols] = size(tab);
  for j = 1:N_rows
    row = tab(j,:);
    number = 0;
    for k = 1:width(row)
      if str2double(row(1,k)) ~= 0
        number = number + 1;
      end
    end
    l2 = plot(i, number, 'b^');
  end
end

xpoints = linspace(1, N_tabs, N_tabs);
scaler = 0.1;
xlim([1-N_tabs*scaler N_tabs+N_tabs*scaler]);
set(gca, 'xtick', xpoints, 'xticklabel', scores.Properties.RowNames);
legend([l1, l2],{'Training Set', 'Testing Set'});
% title('No. of Experiments per-Run, per-Rock-Type', 'Interpreter', 'latex')
xlabel('Experiment (Rock Type Abbreviation)', 'Interpreter', 'latex');
ylabel('Number of Experiments', 'Interpreter', 'latex');
grid();
delvol_utils.save_plot(fig, save_name);
hold off
