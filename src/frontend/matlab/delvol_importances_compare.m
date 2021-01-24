[headers, importances, folders] = delvol_utils.load_importance(directory);
[rows, cols] = size(importances);

fig = figure();
ax = gca();
hold on

for j = 1:rows
  plot(1:cols, importances(j,:));
end

xtickangle(45);

legend(folders, 'Interpreter', 'none');
set(gca, 'xtick', 1:cols, 'xticklabel', headers);
set(gca,'TickLabelInterpreter','none');
xlabel('Features', 'Interpreter', 'none');
ylabel('Cumulative Importance', 'Interpreter', 'latex');
title('The Cumulative Importances of Individual Features Over All Rock Types');
grid();
set(gca, 'FontSize', 8);

delvol_utils.save_plot(fig, save_name);
hold off
