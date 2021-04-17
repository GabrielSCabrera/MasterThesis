[headers, importances, folders] = delvol_utils.load_good_importance(directory);
[N_good] = delvol_utils.load_N_good(directory);
[mean_filters, any_filters, weak_filters] = delvol_utils.load_filter(directory);
[rows, cols] = size(importances);

headers = delvol_utils.rewrite_headers();
fig = figure();
ax = gca();
box on;
hold on

totals1 = zeros(cols);
for j = 1:2
  step_N = N_good(j,1);
  if step_N >= 1
    totals1 = totals1 + importances(j,:)/step_N;
  end
end

totals2 = zeros(cols);
for j = 3:5
  step_N = N_good(j,1);
  if step_N >= 1
    totals2 = totals2 + importances(j,:)/step_N;
  end
end

totals3 = zeros(cols);
for j = 6:8
  step_N = N_good(j,1);
  if step_N >= 1
    totals3 = totals3 + importances(j,:)/step_N;
  end
end

% plot(1:cols, totals1(1,:), '-^', 'LineWidth', 2, 'MarkerSize', 8);
% plot(1:cols, totals2(1,:), '-s', 'LineWidth', 2, 'MarkerSize', 8);
% plot(1:cols, totals3(1,:), '-o', 'LineWidth', 2, 'MarkerSize', 8);

groups = [0 5 10 15 20 25 30 35 39 40 41];

for i=1:length(groups)-1
  idx1 = groups(i)+1;
  idx2 = groups(i+1);
  plot(idx1:idx2, totals1(1,idx1:idx2), 'b-^', 'LineWidth', 2, 'MarkerSize', 8);
  plot(idx1:idx2, totals2(1,idx1:idx2), 'r-s', 'LineWidth', 2, 'MarkerSize', 8);
  plot(idx1:idx2, totals3(1,idx1:idx2), 'g-o', 'LineWidth', 2, 'MarkerSize', 8);
end

[ax] = delvol_utils.add_vlines(ax);
legend('Marble', 'Monzonite', 'Granite');

xtickangle(90);

set(ax, 'xtick', 1:cols, 'xticklabel', headers);
set(ax,'TickLabelInterpreter','none');
xlabel('Feature Percentile', 'Interpreter', 'none', 'fontweight', 'bold');
ylabel('Normalized Cumulative Importance', 'Interpreter', 'none', 'fontweight', 'bold');
% title('The Cumulative Importances of Individual Features Over All Rock Types');
set(ax, 'FontSize', 11);
set(ax, 'LineWidth', 2);
ax.XAxis.TickLength = [0 0];
ax.YAxis.TickLength = [0 0];
xlim([0.5 cols+0.5]);

delvol_utils.save_plot(fig, save_name);
hold off
close all
