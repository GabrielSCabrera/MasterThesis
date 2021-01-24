[headers, importances, folders] = delvol_utils.load_importance(directory);
[mean_filters, any_filters] = delvol_utils.load_filter(directory);
[rows, cols] = size(importances);

fig = figure();
ax = gca();
hold on

new_folders = [];
for j = 1:rows
  if any_filters(j,1) == 1
    plot(1:cols, importances(j,:));
    new_folders = [new_folders folders(j)];
  end
end

xtickangle(45);

legend(new_folders, 'Interpreter', 'none');
set(gca, 'xtick', 1:cols, 'xticklabel', headers);
set(gca,'TickLabelInterpreter','none');
xlabel('Features', 'Interpreter', 'none');
ylabel('Cumulative Importance', 'Interpreter', 'latex');
title('The Cumulative Importances of Individual Features Over All Rock Types');
grid();
set(gca, 'FontSize', 8);

delvol_utils.save_plot(fig, save_name);
hold off
