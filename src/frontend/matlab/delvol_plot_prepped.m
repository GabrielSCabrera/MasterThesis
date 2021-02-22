[sigd, val] = delvol_utils.load_plot_from_prep(filename);

fig = plot(sigd, val, 'bo');
xlabel('Differential Stress [MPa]', 'Interpreter', 'none');
ylabel(label, 'Interpreter', 'none');
grid();
delvol_utils.save_plot(fig, save_name);
