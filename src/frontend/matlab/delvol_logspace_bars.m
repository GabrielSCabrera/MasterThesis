[scores] = delvol_utils.load_from_combined(directory);
[x_points] = delvol_utils.load_logspace(directory);
N_experiments = height(scores);
avg_idx = 2;
std_idx = 6;

avg_arr = table2array(scores(:,avg_idx));
std_arr = table2array(scores(:,std_idx));
fig = errorbar(x_points, avg_arr, std_arr, ':s', 'MarkerSize', 10, 'MarkerEdgeColor','red','MarkerFaceColor','white', 'LineStyle', 'none', 'LineWidth', 1);
chunk = 0.1*(max(x_points) - min(x_points));
xlim([min(x_points) - chunk max(x_points) + chunk]);
xlabel('Number of Models', 'Interpreter', 'latex');
ylabel('$R^2$ Average Score and Standard Deviation', 'Interpreter', 'latex');
% title('Comparing Mean and Std. of $R^2$ Scores by Number of Models', 'Interpreter', 'latex');
grid();
delvol_utils.save_plot(fig, save_name);
