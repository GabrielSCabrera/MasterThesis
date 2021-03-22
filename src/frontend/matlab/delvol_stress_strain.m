[sigd, strain] = delvol_utils.load_stress_strain(filename);

fig = figure();
plot(strain, sigd, 'b-o', 'LineWidth', 2, 'MarkerSize', 8);
ylabel('Differential Stress [MPa]', 'Interpreter', 'none', 'fontweight', 'bold');
xlabel('Axial Strain [Dimensionless]', 'Interpreter', 'none', 'fontweight', 'bold');
ylim([0 inf]);
grid();
set(gca(), 'LineWidth', 2);
set(gca(), 'FontSize', 11);
delvol_utils.save_plot(fig, save_name);
