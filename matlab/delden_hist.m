[r2_train_scores, r2_test_scores, folders] = delden_utils.load_R2_from_combined(directory);
[rows, cols] = size(r2_train_scores);
R2_train_idx = 1;
R2_test_idx = 2;

fig = figure();
ax = gca();
hold on
step = 1.0/rows;
color_dist = 0:step:1;
for i = 1:cols
  for j = 1:rows
    % plot(i, r2_train_scores(j,i), 'Marker', 'x', 'MarkerFaceColor', [1-color_dist(j) 0 color_dist(j)], 'MarkerEdgeColor', [1-color_dist(j) 0 color_dist(j)]);
    plot(i, r2_test_scores(j,i), 'Marker', 'o', 'MarkerFaceColor', [1-color_dist(j) 0 color_dist(j)], 'MarkerEdgeColor', [1-color_dist(j) 0 color_dist(j)]);
  end
end
set(gca, 'xtick', 1:cols, 'xticklabel', folders);
scaler = 0.1;
xlim([1-cols*scaler cols+cols*scaler]);
delden_utils.save_plot(fig, save_name);
hold off
exit();
