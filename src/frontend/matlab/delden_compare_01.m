[scores] = delden_utils.load_from_combined(directory);
N_experiments = height(scores);
avg_idx = 2;
std_idx = 6;

xpoints = linspace(0, N_experiments, N_experiments);

avg_arr = table2array(scores(:,avg_idx));
std_arr = table2array(scores(:,std_idx));
fig = errorbar(xpoints, avg_arr, std_arr, ':s', 'MarkerSize', 10, 'MarkerEdgeColor','red','MarkerFaceColor','white', 'LineStyle', 'none', 'LineWidth', 1);
chunk = 0.1*(max(xpoints) - min(xpoints));
xlim([min(xpoints) - chunk max(xpoints) + chunk]);
ylim([0 1]);
set(gca, 'xtick', xpoints, 'xticklabel', scores.Properties.RowNames);
xlabel('Experiment (Rock Type Abbreviation)');
ylabel('R^2 Average Score and Standard Deviation');
grid();
delden_utils.save_plot(fig, save_name);
();
