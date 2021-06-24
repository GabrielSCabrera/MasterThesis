filenames1 = ["WG02_l1_min_avg.csv", "M8_1_l1_75_avg.csv", "M8_2_l1_min_avg.csv"];
filenames2 = ["WG02_delvtot.csv", "M8_1_delvtot.csv", "M8_2_delvtot.csv"];

abbrv = ["\boldmath$L_{min}$ min.", "\boldmath$L_{min}$ 75 \%", "\boldmath$L_{min}$ min."];
titles = ["Granite 2", "Marble 1", "Marble 2"];

fig = figure();
N_rows = length(filenames1);
nIDs = N_rows;
for i=1:N_rows
  filename1 = filenames1(i);
  filename2 = filenames2(i);
  title_text = titles(i);

  [time, points] = delvol_utils.load_plot_from_prep_delvtot(filename1, filename2);

  [sigds, means, stds] = delvol_utils.load_plot_from_prep_avg(filename1);

  p = polyfit(sigds, points, 1);
  slope = p(1);
  intercept = p(2);
  x2 = [min(sigds), max(sigds)];
  y2 = [x2(1)*slope + intercept, x2(2)*slope + intercept];

  ax = subplot(N_rows,1,i);
  plot(ax, sigds, points, 'b^', 'MarkerSize', 7, 'MarkerEdgeColor','blue','MarkerFaceColor','none', 'LineWidth', 2);
  hold on
  plot(ax, x2, y2, 'k:', 'LineWidth', 2);
  hold off
  if i == 1
    legend(ax, "Experimental Data", "Line of Best Fit");
  end
  set(ax, 'XDir','reverse');
  xlim([min(sigds) max(sigds)]);
  ylim_pre = ylim(ax);
  difference = ylim_pre(2) - ylim_pre(1);
  ylim([ylim_pre(1) ylim_pre(2)+difference*0.2]);
  title(ax, title_text, 'Interpreter', 'none', 'fontweight', 'bold');

  alphabet = ('a':'z').';
  chars = num2cell(alphabet(1:nIDs));
  chars = chars.';
  charlbl = strcat('(',chars,')');
  text(ax, 0.025,0.92,charlbl{i},'Units', 'normalized', 'FontSize', 12, 'fontweight', 'bold')

  grid();
  set(ax, 'LineWidth', 2);
  set(ax, 'FontSize', 11);
  ylabel(ax, abbrv(i), 'Interpreter', 'latex', 'FontSize', 16, 'fontweight', 'bold');

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
