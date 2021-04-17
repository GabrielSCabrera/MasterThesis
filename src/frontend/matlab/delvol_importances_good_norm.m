[headers, importances, folders] = delvol_utils.load_good_importance(directory);
[N_good] = delvol_utils.load_N_good(directory);
[mean_filters, any_filters, weak_filters] = delvol_utils.load_filter(directory);
[rows, cols] = size(importances);

headers = delvol_utils.rewrite_headers();
folders = delvol_utils.rewrite_folders(folders);
fig = figure();
box on;
ax = gca();
hold on

groups = [0 5 10 15 20 25 30 35 39 40 41];

styles = ["b-^" "r-s" "g-o"];
new_folders = [];
for j = 1:rows
  if N_good(j,1) >= 1
    new_folders = [new_folders folders(j)];
    for i=1:length(groups)-1
      idx1 = groups(i)+1;
      idx2 = groups(i+1);
      h = plot(ax, idx1:idx2, importances(j,idx1:idx2)/N_good(j,1), styles(j), 'LineWidth', 2, 'MarkerSize', 8);
      if i > 1
        h.Annotation.LegendInformation.IconDisplayStyle = 'off';
      end
    end

  end
end
[ax] = delvol_utils.add_vlines(ax);

xtickangle(90);

legend(new_folders, 'Interpreter', 'none');
set(ax, 'xtick', 1:cols, 'xticklabel', headers);
set(ax,'TickLabelInterpreter','none');
xlabel('Feature Percentile', 'Interpreter', 'none', 'fontweight', 'bold');
ylabel('Normalized Cumulative Importance', 'Interpreter', 'none', 'fontweight', 'bold');
set(ax, 'FontSize', 11);
ax.XAxis.TickLength = [0 0];
ax.YAxis.TickLength = [0 0];
xlim([0.5 cols+0.5]);

delvol_utils.save_plot(fig, save_name);
hold off
close all
