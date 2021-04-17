[scores] = delvol_utils.load_from_combined(directory);
N_experiments = height(scores);
avg_idx = 2;
std_idx = 6;

xpoints = linspace(0, N_experiments, N_experiments);
folders = delvol_utils.rewrite_folders(scores.Properties.RowNames);

avg_arr = table2array(scores(:,avg_idx));
std_arr = table2array(scores(:,std_idx));
fig = errorbar(xpoints, avg_arr, std_arr, 'b-s', 'MarkerSize', 10, 'MarkerEdgeColor','red','MarkerFaceColor','white', 'LineStyle', 'none', 'Color', 'b', 'LineWidth', 2);
chunk = 0.1*(max(xpoints) - min(xpoints));
xlim([min(xpoints) - chunk max(xpoints) + chunk]);
set(gca(), 'xtick', xpoints, 'xticklabel', folders);
xlabel('Experiment', 'Interpreter', 'none', 'fontweight', 'bold');
ylabel('R² Mean Score and Standard Deviation', 'Interpreter', 'none', 'fontweight', 'bold');
grid();
xtickangle(15);
set(gca(), 'LineWidth', 2);
set(gca(), 'FontSize', 11);
delvol_utils.save_plot(fig, save_name);
close all
