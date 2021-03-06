[sigd, val] = delvol_utils.load_plot_from_prep_no_outliers(filename);

fig = figure();
ax = axes
plot(sigd, val, 'bo');
set(ax, 'XDir','reverse')
xlabel('Normalized Time to Failure', 'Interpreter', 'none');
ylabel(label, 'Interpreter', 'none');
grid();
delvol_utils.save_plot(fig, save_name);
