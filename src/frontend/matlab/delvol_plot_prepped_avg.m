[sigd, mean, std] = delvol_utils.load_plot_from_prep_avg(filename);

fig = figure();
errorbar(sigd, mean, std, ':s', 'MarkerSize', 10, 'MarkerEdgeColor','red','MarkerFaceColor','white', 'LineStyle', 'none', 'LineWidth', 1)
xlabel('Differential Stress [MPa]', 'Interpreter', 'none');
ylabel(label, 'Interpreter', 'none');
grid();
delvol_utils.save_plot(fig, save_name);
