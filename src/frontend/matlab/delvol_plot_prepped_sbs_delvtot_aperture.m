% GRANITE AND MONZONITE DELVTOT FOR APERTURE WG01 MONZ5

filenames = ["WG01_l1_50.csv", "WG02_l1_50", "MONZ5_l1_25.csv"];
abbrv = ["\boldmath$L_{min}$ 50\%", "\boldmath$L_{min}$ 50\%", "\boldmath$L_{min}$ 25\%"];

filenames2 = ["WG01_delvtot.csv", "WG02_delvtot.csv", "MONZ5_delvtot.csv"];

titles = ["Granite 1", "Granite 2", "Monzonite 5"];

fig = figure();
N_rows = length(filenames);
nIDs = N_rows;
for i=1:N_rows
  filename = filenames(i);
  filename2 = filenames2(i);
  title_text = titles(i);

  [delvtot, points] = delvol_utils.load_plot_from_prep_delvtot(filename, filename2);

  p = polyfit(delvtot, points, 1);
  slope = p(1);
  intercept = p(2);
  x2 = [min(delvtot), max(delvtot)];
  y2 = [x2(1)*slope + intercept, x2(2)*slope + intercept];

  ax = subplot(N_rows,1,i);
  plot(ax, delvtot, points, 'b^', 'MarkerSize', 7, 'MarkerEdgeColor','blue','MarkerFaceColor','none', 'LineWidth', 2);
  hold on
  plot(ax, x2, y2, 'k:', 'LineWidth', 2);
  hold off
  if i == 1
    legend(ax, "Experimental Data", "Line of Best Fit");
  end
  xlim([min(delvtot) max(delvtot)]);
  ylim_pre = ylim(ax);
  difference = ylim_pre(2) - ylim_pre(1);
  ylim([ylim_pre(1) ylim_pre(2)+difference*0.2]);
  title(ax, title_text, 'Interpreter', 'none', 'fontweight', 'bold');

  alphabet = ('a':'z').';
  chars = num2cell(alphabet(1:nIDs));
  chars = chars.';
  charlbl = strcat('(',chars,')');
  text(ax, 0.025,0.92,charlbl{i},'Units','normalized','FontSize',12, 'fontweight', 'bold')

  grid();
  set(ax, 'LineWidth', 2);
  set(ax, 'FontSize', 11);
  ylabel(ax, abbrv(i), 'Interpreter', 'latex','FontSize', 16, 'fontweight', 'bold');

end

han = axes(fig, 'visible', 'off');
han.Title.Visible='on';
han.XLabel.Visible='on';
han.YLabel.Visible='on';
xlabel(han,'Change in Total Volume', 'Interpreter', 'none', 'fontweight', 'bold');
set(han, 'FontSize', 11);

xh = get(han,'xlabel');
p = get(xh,'position');
p(2) = 1.25*p(2);
set(xh,'position',p);

set(gcf, 'Units', 'Centimeters', 'Position', [0, 0, 21.0, 29.7], 'PaperUnits', 'Centimeters', 'PaperSize', [21.0, 29.7]);
delvol_utils.save_plot(fig, save_name);
close all
