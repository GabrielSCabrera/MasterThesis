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
    l1 = plot(number, r2_train_scores(j,i), 'rs');
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
    l2 = plot(number, r2_test_scores(j,i), 'b^');
  end
end

legend([l1, l2],{'Training Set', 'Testing Set'});
scaler = 0.1;
xl = xlim;
dx = xl(2) - xl(1);
xlim([xl(1)-dx*scaler xl(2)+dx*scaler]);
title('$R^2$ Scores for Prediction of Fracture Densities by No. of Experiments', 'Interpreter', 'latex')
xlabel('Number of Experiments', 'Interpreter', 'latex');
ylabel('$R^2$ Score', 'Interpreter', 'latex');
grid();
delvol_utils.save_plot(fig, save_name);
hold off
exit();
