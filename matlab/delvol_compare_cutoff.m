[scores] = delvol_utils.load_from_combined(directory);
N_experiments = height(scores);
avg_idx = 2;
std_idx = 6;

xpoints = linspace(0, N_experiments, N_experiments);

avg_arr = table2array(scores(:,avg_idx));
std_arr = table2array(scores(:,std_idx));
errorbar(xpoints, avg_arr, std_arr, ':s', 'MarkerSize', 10, 'MarkerEdgeColor','red','MarkerFaceColor','white', 'LineStyle', 'none', 'LineWidth', 1, 'DisplayName', 'Mean and Std of R^2');
chunk = 0.1*(max(xpoints) - min(xpoints));
hold on
plot([min(xpoints) - chunk max(xpoints) + chunk], [0.5, 0.5], 'r:', 'DisplayName', 'Acceptable Score Cutoff');
xlim([min(xpoints) - chunk max(xpoints) + chunk]);
legend();
set(gca, 'xtick', xpoints, 'xticklabel', scores.Properties.RowNames);
xlabel('Experiment (Rock Type Abbreviation)', 'Interpreter', 'latex');
ylabel('$R^2$ Average Score and Standard Deviation', 'Interpreter', 'latex');
title('Comparing Mean and Std. of $R^2$ Scores for Each Experiment', 'Interpreter', 'latex');
grid();
fig = gcf();
delvol_utils.save_plot(fig, save_name);
hold off
exit();
