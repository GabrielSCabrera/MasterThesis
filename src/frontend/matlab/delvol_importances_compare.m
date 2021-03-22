[headers, importances, folders] = delvol_utils.load_importance(directory);
[rows, cols] = size(importances);

headers = delvol_utils.rewrite_headers();
fig = figure();
ax = gca();
hold on

for j = 1:rows
  plot(1:cols, importances(j,:));
end
[ax] = delvol_utils.add_vlines(ax);

xtickangle(45);

legend(folders, 'Interpreter', 'none');
set(ax, 'xtick', 1:cols, 'xticklabel', headers);
set(ax,'TickLabelInterpreter','none');
xlabel('Features', 'Interpreter', 'none');
ylabel('Cumulative Importance', 'Interpreter', 'latex');
% title('The Cumulative Importances of Individual Features Over All Rock Types');
set(ax, 'FontSize', 8);

delvol_utils.save_plot(fig, save_name);
hold off
