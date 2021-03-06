[sigd, strain] = delvol_utils.load_stress_strain(filename);

fig = figure();
plot(strain, sigd, 'bo');
ylabel('Differential Stres [MPa]', 'Interpreter', 'none');
xlabel('Axial Strain [Dimensionless]', 'Interpreter', 'none');
grid();
delvol_utils.save_plot(fig, save_name);
