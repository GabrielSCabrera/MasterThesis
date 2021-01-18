[r2_train_scores_1, r2_test_scores_1, folders] = delden_utils.load_R2_from_combined(directory_1);
[r2_train_scores_2, r2_test_scores_2, folders] = delden_utils.load_R2_from_combined(directory_2);
[rows_1, cols_1] = size(r2_train_scores_1);
[rows_2, cols_2] = size(r2_train_scores_2);
R2_train_idx = 1;
R2_test_idx = 2;

fig = figure();
ax = gca();
hold on
step_1 = 1.0/rows_1;
step_2 = 1.0/rows_2;
color_dist_1 = 0:step_1:1;
color_dist_2 = 0:step_2:1;
for i = 1:cols_1
  for j = 1:rows_1
    L1 = plot(i, r2_test_scores_1(j,i), 'Marker', 'o', 'MarkerFaceColor', [1-color_dist_1(j) 0 color_dist_1(j)], 'MarkerEdgeColor', [1-color_dist_1(j) 0 color_dist_1(j)]);
  end
end
for i = 1:cols_2
  for j = 1:rows_2
    L2 = plot(i, r2_test_scores_2(j,i), 'Marker', '^', 'MarkerFaceColor', [1-color_dist_2(j) 0 color_dist_2(j)], 'MarkerEdgeColor', [1-color_dist_2(j) 0 color_dist_2(j)]);
  end
end
set(gca, 'xtick', 1:cols_1, 'xticklabel', folders);
scaler = 0.1;
xlim([1-cols_1*scaler cols_1+cols_1*scaler]);
ylim([0 1])
legend([L1, L2],{'Linear', 'Logarithmic'});
ylabel('R^2 Score')
xlabel('Experiment')
delden_utils.save_plot(fig, save_name);
hold off
exit();
