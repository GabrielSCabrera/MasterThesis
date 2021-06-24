[delvtot1, points1] = delvol_utils.load_plot_from_prep_delvtot(filename1, filename2);

fig = figure();
ax = gca();
plot(ax, delvtot1, points1, 'b^', 'MarkerSize', 8, 'MarkerEdgeColor','blue','MarkerFaceColor','none', 'LineWidth', 2);
xlim([min(delvtot1) max(delvtot1)]);
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
