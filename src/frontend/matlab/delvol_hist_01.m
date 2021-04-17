[r2_train_scores, r2_test_scores, folders] = delvol_utils.load_R2_from_combined(directory);
folders = delvol_utils.rewrite_folders(folders);
[rows, cols] = size(r2_train_scores);
R2_train_idx = 1;
R2_test_idx = 2;

fig = figure();
ax = gca();
hold on
box on
step = 1.0/rows;
color_dist = 0:step:1;
for i = 1:cols
  for j = 1:rows
    plot(i, r2_test_scores(j,i), 'Marker', '^', 'MarkerFaceColor', 'none', 'MarkerEdgeColor', 'b', 'MarkerSize', 10, 'LineStyle', 'none', 'LineWidth', 2);
    % plot(i, r2_test_scores(j,i), 'Marker', 'o', 'MarkerFaceColor', 'none', 'MarkerEdgeColor', [1-color_dist(j) 0 color_dist(j)], 'MarkerSize', 10, 'LineStyle', 'none', 'LineWidth', 2);
  end
end

set(gca, 'xtick', 1:cols, 'xticklabel', folders);
xlabel('Experiment', 'Interpreter', 'none');
ylabel('R² Score', 'Interpreter', 'none');
% title('Run- and Experiment-Wise $R^2$ Scores', 'Interpreter', 'latex');
scaler = 0.1;
xlim([1-cols*scaler cols+cols*scaler]);
ylim([0 1]);
grid();
xtickangle(15);
set(gca(), 'LineWidth', 2);
set(gca(), 'FontSize', 11);
delvol_utils.save_plot(fig, save_name);
hold off
