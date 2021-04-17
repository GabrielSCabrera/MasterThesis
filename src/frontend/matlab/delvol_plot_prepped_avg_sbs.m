[sigd1, mean1, std1] = delvol_utils.load_plot_from_prep_avg(filename1);
[sigd2, mean2, std2] = delvol_utils.load_plot_from_prep_avg(filename2);

fig = figure();
ax = subplot(1,2,1);
errorbar(ax, sigd1, mean1, std1, ':s', 'MarkerSize', 8, 'MarkerEdgeColor','red','MarkerFaceColor','white', 'Color', 'b', 'LineStyle', 'none', 'LineWidth', 2);
set(ax, 'XDir','reverse');
xlim([min(sigd1) max(sigd1)]);
title(ax, 'Granite 1', 'Interpreter', 'none', 'fontweight', 'bold');
grid();

ax = subplot(1,2,2);
errorbar(ax, sigd2, mean2, std2, ':s', 'MarkerSize', 8, 'MarkerEdgeColor','red','MarkerFaceColor','white', 'Color', 'b', 'LineStyle', 'none', 'LineWidth', 2);
set(ax, 'XDir','reverse');
xlim([min(sigd2) max(sigd2)]);
title(ax, 'Monzonite 3', 'Interpreter', 'none', 'fontweight', 'bold');
grid();

han = axes(fig, 'visible', 'off');
han.Title.Visible='on';
han.XLabel.Visible='on';
han.YLabel.Visible='on';
xlabel(han, 'Normalized Time to Failure', 'Interpreter', 'none', 'fontweight', 'bold');
ylabel(han, label, 'Interpreter', 'none', 'fontweight', 'bold');
set(han, 'FontSize', 11);

yh = get(han,'ylabel');
p = get(yh,'position');
p(1) = 1.25*p(1);
set(yh,'position',p);

delvol_utils.save_plot(fig, save_name);
close all
