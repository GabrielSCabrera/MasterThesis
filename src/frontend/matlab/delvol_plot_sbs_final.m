[time, points] = delvol_utils.load_plot_from_prep_scatter(filename1);
[sigd, means, stds] = delvol_utils.load_plot_from_prep_avg(filename2);

fig = figure();

ax = subplot(2,1,1);

[X, Y, Z] = delvol_utils.get_heatmap_matrices(time, points);
xlim_1 = [min(time) max(time)];
ylim_1 = [min(min(points), 0) max(1, max(points))];

set(ax,'Color','k')
s = pcolor(ax, X,Y,Z);
colorbar(ax);
s.EdgeColor = 'none';
colormap(ax, hot);
grid();
ax.GridColor = [1,1,1];
set(ax,'layer','top')
xlim(ax, xlim_1);
ylim(ax, ylim_1);
set(ax, 'XDir','reverse');

ax = subplot(2,1,2);
errorbar(ax, sigd, means, stds, ':s', 'MarkerSize', 8, 'MarkerEdgeColor','red','MarkerFaceColor','white', 'Color', 'b', 'LineStyle', 'none', 'LineWidth', 2);
xlim(ax, xlim_1);
ylim(ax, ylim_1);
set(ax, 'XDir','reverse');

grid();

han = axes(fig, 'visible', 'off');
han.Title.Visible='on';
han.XLabel.Visible='on';
han.YLabel.Visible='on';
ylabel(han, label, 'Interpreter', 'none', 'fontweight', 'bold');
xlabel(han,'Time to Failure', 'Interpreter', 'none', 'fontweight', 'bold');
set(han, 'FontSize', 11);

xh = get(han,'xlabel');
p = get(xh,'position');
p(2) = 1.5*p(2);
set(xh,'position',p);

yh = get(han,'ylabel');
p = get(yh,'position');
p(1) = 1.25*p(1);
set(yh,'position',p);

fig.Position = [10 10 500 1000];

delvol_utils.save_plot(fig, save_name);
close all
