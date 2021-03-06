[sigd, mean, std] = delvol_utils.load_plot_from_prep_no_outliers_avg(filename);

fig = figure();
ax = axes
errorbar(sigd, mean, std, ':s', 'MarkerSize', 10, 'MarkerEdgeColor','red','MarkerFaceColor','white', 'LineStyle', 'none', 'LineWidth', 1)
set(ax, 'XDir','reverse')
xlabel('Normalized Time to Failure', 'Interpreter', 'none');
ylabel(label, 'Interpreter', 'none');
xlim([0,1]);
grid();
delvol_utils.save_plot(fig, save_name);
