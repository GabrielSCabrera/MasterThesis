[headers, importances, folders] = delvol_utils.load_good_importance(directory);
[N_good] = delvol_utils.load_N_good(directory);
[mean_filters, any_filters, weak_filters] = delvol_utils.load_filter(directory);
[rows, cols] = size(importances);

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

plot(1:cols, totals(1,:));

xtickangle(45);

set(gca, 'xtick', 1:cols, 'xticklabel', headers);
set(gca,'TickLabelInterpreter','none');
xlabel('Features', 'Interpreter', 'none');
ylabel('Total Cumulative Importance Over All Experiments (Normed Prior to Summation)', 'Interpreter', 'latex');
title('The Cumulative Importances of Individual Features Over All Rock Types');
grid();
set(gca, 'FontSize', 8);

delvol_utils.save_plot(fig, save_name);
hold off
