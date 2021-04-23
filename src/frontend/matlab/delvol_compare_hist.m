[scores] = delvol_utils.load_from_combined(directory);
[r2_train_scores, r2_test_scores, folders] = delvol_utils.load_R2_from_combined(directory);
[rows, cols] = size(r2_train_scores);

R2_train_idx = 1;
R2_test_idx = 2;

N_experiments = height(scores);
avg_idx = 2;
std_idx = 6;

xpoints = linspace(1, N_experiments, N_experiments);
folders = delvol_utils.rewrite_folders(scores.Properties.RowNames);

avg_arr = table2array(scores(:,avg_idx));
std_arr = table2array(scores(:,std_idx));
fig = figure();
ax = gca();
errorbar(xpoints, avg_arr, std_arr, 'b:s', 'MarkerSize', 10, 'MarkerEdgeColor','red','MarkerFaceColor','white', 'LineStyle', 'None', 'Color', 'b', 'LineWidth', 1);
chunk = 0.1*(max(xpoints) - min(xpoints));

hold on
box on
step = 1.0/rows;
color_dist = 0:step:1;
for i = 1:cols
  for j = 1:rows
    plot(i, r2_test_scores(j,i), 'Marker', '^', 'MarkerFaceColor', 'white', 'MarkerEdgeColor', 'b', 'MarkerSize', 4, 'LineStyle', 'none', 'LineWidth', 1);
    % plot(i, r2_test_scores(j,i), 'Marker', 'o', 'MarkerFaceColor', 'none', 'MarkerEdgeColor', [1-color_dist(j) 0 color_dist(j)], 'MarkerSize', 10, 'LineStyle', 'none', 'LineWidth', 2);
  end
end

xlim([min(xpoints) - chunk max(xpoints) + chunk]);
set(ax, 'xtick', xpoints, 'xticklabel', folders);
xlabel('Experiment', 'Interpreter', 'none', 'fontweight', 'bold');
ylabel('R² Mean Score and Standard Deviation', 'Interpreter', 'none', 'fontweight', 'bold');
grid();
xtickangle(15);
set(ax, 'LineWidth', 2);
set(ax, 'FontSize', 11);

delvol_utils.save_plot(fig, save_name);
hold off
