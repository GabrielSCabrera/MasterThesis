[scores] = delvol_utils.load_from_combined(directory);
[x_points] = delvol_utils.load_linspace(directory);
N_experiments = height(scores);
avg_idx = 2;
std_idx = 6;

chunk = 0.1*(max(x_points) - min(x_points));

avg_arr = table2array(scores(:,avg_idx));
std_arr = table2array(scores(:,std_idx));
fig = plot(x_points, avg_arr, 'b-^');

xlim([min(x_points) - chunk max(x_points) + chunk]);
xlabel('Number of Models', 'Interpreter', 'none', 'fontweight', 'bold');
ylabel('R² Average Score', 'Interpreter', 'none', 'fontweight', 'bold');
% title('Comparing Mean $R^2$ Scores by Number of Models', 'Interpreter', 'latex');
grid();
set(gca(), 'LineWidth', 2);
set(gca(), 'FontSize', 11);
delvol_utils.save_plot(fig, save_name_1);

fig = plot(x_points, std_arr, 'b-^')
xlim([min(x_points) - chunk max(x_points) + chunk]);
xlabel('Number of Models', 'Interpreter', 'none', 'fontweight', 'bold');
ylabel('R² Standard Deviation', 'Interpreter', 'none', 'fontweight', 'bold');
% title('Comparing Std. of $R^2$ Scores by Number of Models', 'Interpreter', 'latex');
grid();
set(gca(), 'LineWidth', 2);
set(gca(), 'FontSize', 11);
delvol_utils.save_plot(fig, save_name_2);
