% filenames1 = ["WG01_vol_50_avg.csv", "WG01_ani_50_avg.csv", "WG01_l1_50_avg.csv", "WG01_l3_50_avg.csv", "WG01_th1_50_avg.csv"];
% filenames2 = ["MONZ3_vol_50_avg.csv", "MONZ3_ani_50_avg.csv", "MONZ3_l1_50_avg.csv", "MONZ3_l3_50_avg.csv", "MONZ3_th1_50_avg.csv"];
% abbrv = ["$v$", "$A$", "$L_{min}$", "$L_{max}$", "$\theta_1$"];

filenames1 = ["WG01_th1_50_avg.csv", "WG01_dmin_50_avg.csv", "WG01_ani_50_avg.csv"];
filenames2 = ["MONZ3_th1_50_avg.csv", "MONZ3_dmin_50_avg.csv", "MONZ3_ani_50_avg.csv"];
abbrv = ["\boldmath$\theta_1$", "\boldmath$d_{min}$", "\boldmath$A$"];

filename3 = "WG01_delvtot.csv";
filename4 = "MONZ3_delvtot.csv";

fig = figure();
N_rows = length(filenames1);
nIDs = N_rows*2;
for i=1:N_rows
  filename1 = filenames1(i);
  filename2 = filenames2(i);

  [delvtot1, points1] = delvol_utils.load_plot_from_prep_delvtot(filename1, filename3);
  [delvtot2, points2] = delvol_utils.load_plot_from_prep_delvtot(filename2, filename4);

  [sigd1, mean1, std1] = delvol_utils.load_plot_from_prep_avg(filename1);
  [sigd2, mean2, std2] = delvol_utils.load_plot_from_prep_avg(filename2);

  ax = subplot(N_rows,2,2*i-1);
  plot(ax, sigd1, points1, 'b^', 'MarkerSize', 7, 'MarkerEdgeColor','blue','MarkerFaceColor','none', 'LineWidth', 2);
  set(ax, 'XDir','reverse');
  xlim([min(sigd1) max(sigd1)]);
  ylim_pre = ylim(ax);
  difference = ylim_pre(2) - ylim_pre(1);
  ylim([ylim_pre(1) ylim_pre(2)+difference*0.2]);
  if i==1
    title(ax, 'Granite 1, ⟨R²⟩=0.77', 'Interpreter', 'none', 'fontweight', 'bold');
  end

  alphabet = ('a':'z').';
  chars = num2cell(alphabet(1:nIDs));
  chars = chars.';
  charlbl = strcat('(',chars,')');
  text(ax, 0.025,0.92,charlbl{2*i-1},'Units', 'normalized', 'FontSize', 12, 'fontweight', 'bold')

  grid();
  set(ax, 'LineWidth', 2);
  set(ax, 'FontSize', 11);
  ylabel(ax, abbrv(i), 'Interpreter', 'latex', 'FontSize', 16, 'fontweight', 'bold');

  ax = subplot(N_rows,2,2*i);
  plot(ax, sigd2, points2, 'b^', 'MarkerSize', 7, 'MarkerEdgeColor','blue','MarkerFaceColor','none', 'LineWidth', 2);
  set(ax, 'XDir','reverse');
  xlim([min(sigd2) max(sigd2)]);
  ylim_pre = ylim(ax);
  difference = ylim_pre(2) - ylim_pre(1);
  ylim([ylim_pre(1) ylim_pre(2)+difference*0.2]);
  if i==1
    title(ax, 'Monzonite 3, ⟨R²⟩=0.54', 'Interpreter', 'none', 'fontweight', 'bold');
  end

  alphabet = ('a':'z').';
  chars = num2cell(alphabet(1:nIDs));
  chars = chars.';
  charlbl = strcat('(',chars,')');
  text(ax, 0.025,0.92,charlbl{2*i},'Units','normalized','FontSize',12, 'fontweight', 'bold')

  grid();
  set(ax, 'LineWidth', 2);
  set(ax, 'FontSize', 11);

end

han = axes(fig, 'visible', 'off');
han.Title.Visible='on';
han.XLabel.Visible='on';
han.YLabel.Visible='on';
xlabel(han, 'Normalized Time to Failure', 'Interpreter', 'none', 'fontweight', 'bold');
set(han, 'FontSize', 11);

set(gcf, 'Units', 'Centimeters', 'Position', [0, 0, 21.0, 29.7], 'PaperUnits', 'Centimeters', 'PaperSize', [21.0, 29.7]);
delvol_utils.save_plot(fig, save_name);
close all
