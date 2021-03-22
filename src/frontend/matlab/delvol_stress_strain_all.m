files_list = ["times_M8_1.mat", "times_M8_2.mat", "times_MONZ3.mat", "times_MONZ4.mat", "times_MONZ5.mat", "times_WG01.mat", "times_WG02.mat", "times_WG04.mat"];
labels = ["M8_1", "M8_2", "MONZ3", "MONZ4", "MONZ5", "WG01", "WG02", "WG04"];

fig = figure();

for i=1:length(files_list)
  [sigd, strain] = delvol_utils.load_stress_strain(files_list(i));
  ax = subplot(3,3,i);
  plot(ax, strain, sigd, '-o');
  % ylabel('Differential Stress [MPa]', 'Interpreter', 'none', 'fontweight', 'bold');
  % xlabel('Axial Strain [Dimensionless]', 'Interpreter', 'none', 'fontweight', 'bold');
  ylim([0 inf]);
  xlabel(gca, labels(i), 'Interpreter', 'none', 'fontweight', 'bold');
  grid();
  set(gca(), 'LineWidth', 2);
end
han = axes(fig, 'visible', 'off');
han.Title.Visible='on';
han.XLabel.Visible='on';
han.YLabel.Visible='on';
ylabel(han,'Differential Stress [MPa]', 'Interpreter', 'none', 'fontweight', 'bold');
xlabel(han,{'Axial Strain [Dimensionless]', ''}, 'Interpreter', 'none', 'fontweight', 'bold');
set(han, 'FontSize', 11);
delvol_utils.save_plot(fig, save_name);
close all
