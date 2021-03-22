[headers, importances, folders] = delvol_utils.load_good_importance(directory);
[N_good] = delvol_utils.load_N_good(directory);
[mean_filters, any_filters, weak_filters] = delvol_utils.load_filter(directory);
[rows, cols] = size(importances);

headers = delvol_utils.rewrite_headers();
fig = figure();
ax = gca();
hold on

totals = zeros(cols);

for j = 1:rows
  step_N = N_good(j,1);
  if step_N >= 1
    disp(j);
    totals = totals + importances(j,:)/step_N;
  end
end

% plot(1:cols, totals(1,:), 'LineWidth', 2, 'MarkerSize', 8);

groups = [0 5 10 15 20 25 30 35 39 40 41];

for i=1:length(groups)-1
  idx1 = groups(i)+1;
  idx2 = groups(i+1);
  plot(idx1:idx2, totals(1,idx1:idx2), 'b-^', 'LineWidth', 2, 'MarkerSize', 8);
end

[ax] = delvol_utils.add_vlines(ax);

xtickangle(45);

set(ax, 'xtick', 1:cols, 'xticklabel', headers);
set(ax,'TickLabelInterpreter','none');
xlabel('Features', 'Interpreter', 'none');
ylabel('Total Cumulative Importance Over All Experiments (Normed Prior to Summation)', 'Interpreter', 'latex');
% title('The Cumulative Importances of Individual Features Over All Rock Types');
set(ax, 'FontSize', 8);

delvol_utils.save_plot(fig, save_name);
hold off
