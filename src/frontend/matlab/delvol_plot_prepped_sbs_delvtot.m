[delvtot1, points1] = delvol_utils.load_plot_from_prep_delvtot(filename1, filename3);
[delvtot2, points2] = delvol_utils.load_plot_from_prep_delvtot(filename2, filename4);

fig = figure();
ax = subplot(1,2,1);
plot(ax, delvtot1, points1, 'b^', 'MarkerSize', 8, 'MarkerEdgeColor','blue','MarkerFaceColor','none', 'LineWidth', 2);
xlim([min(delvtot1) max(delvtot1)]);
title(ax, 'Granite 1', 'Interpreter', 'none', 'fontweight', 'bold');
grid();

ax = subplot(1,2,2);
plot(ax, delvtot2, points2, 'b^', 'MarkerSize', 8, 'MarkerEdgeColor','blue','MarkerFaceColor','none', 'LineWidth', 2);
xlim([min(delvtot2) max(delvtot2)]);
title(ax, 'Monzonite 3', 'Interpreter', 'none', 'fontweight', 'bold');
grid();

han = axes(fig, 'visible', 'off');
han.Title.Visible='on';
han.XLabel.Visible='on';
han.YLabel.Visible='on';
xlabel(han,'Change in Total Volume', 'Interpreter', 'none', 'fontweight', 'bold');
set(han, 'FontSize', 11);

xh = get(han,'xlabel');
p = get(xh,'position');
p(2) = 1.5*p(2);
set(xh,'position',p);

yh = get(han,'ylabel');
p = get(yh,'position');
p(1) = 1.25*p(1);
set(yh,'position',p);

delvol_utils.save_plot(fig, save_name);
close all
