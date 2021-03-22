[sigd, mean, std] = delvol_utils.load_plot_from_prep_avg(filename);

fig = figure();
ax = gca();
plot(sigd, mean, '-o', 'LineWidth', 2, 'MarkerSize', 8);
set(ax, 'XDir','reverse');
xlim([min(sigd) max(sigd)]);
xlabel('Normalized Time to Failure', 'Interpreter', 'none', 'fontweight', 'bold');
ylabel(label, 'Interpreter', 'none', 'fontweight', 'bold');
grid();
set(ax, 'FontSize', 11);
set(ax, 'LineWidth', 2);
delvol_utils.save_plot(fig, save_name);
