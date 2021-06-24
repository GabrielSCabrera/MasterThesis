[delvtot, points] = delvol_utils.load_plot_from_prep_delvtot(filename1, filename2);
[delvtot_sorted, idx_sorted] = sort(delvtot);
points_sorted = points(idx_sorted);

N_bins = 50;
x_points = [];
mean_points = [];
std_points = [];
mean_array = [points_sorted(1)];
distance = 0;
tol = (delvtot_sorted(end) - delvtot_sorted(1))/N_bins;
for i=2:length(delvtot_sorted)
  distance = distance + delvtot_sorted(i) - delvtot_sorted(i-1);
  if distance > tol
    distance = 0;
    x_points = [x_points delvtot_sorted(i-1)];
    mean_points = [mean_points mean(mean_array)];
    std_points = [std_points std(mean_array)];
    mean_array = [points_sorted(i)];
  else
    mean_array = [mean_array points_sorted(i)];
  end
end

x_points = [x_points delvtot_sorted(end)];
mean_points = [mean_points mean(mean_array)];
std_points = [std_points std(mean_array)];

fig = figure();
ax = subplot(2,1,1);
xlim_1 = [min(delvtot) max(delvtot)];
ylim_1 = [min(min(points),0) max(1, max(points))];

[X, Y, Z] = delvol_utils.get_heatmap_matrices(delvtot, points);

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

ax = subplot(2,1,2);
errorbar(ax, x_points, mean_points, std_points, ':s', 'MarkerSize', 8, 'MarkerEdgeColor','red','MarkerFaceColor','white', 'Color', 'b', 'LineStyle', 'none', 'LineWidth', 2);
xlim(ax, xlim_1);
ylim(ax, ylim_1);
grid();

han = axes(fig, 'visible', 'off');
han.Title.Visible='on';
han.XLabel.Visible='on';
han.YLabel.Visible='on';
ylabel(han, label, 'Interpreter', 'none', 'fontweight', 'bold');
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

fig.Position = [10 10 500 1000];

delvol_utils.save_plot(fig, save_name);
close all
