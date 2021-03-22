[headers, importances, folders] = delvol_utils.load_importance(directory);
[rows, cols] = size(importances);

for j = 1:rows
  fig = figure();
  ax = gca();
  box on;
  hold on
  step = 1.0/rows;
  color_dist = 0:step:1;

  temp_importances = importances(j,:);

  [out, idx] = sort(temp_importances, 'descend');
  new_headers = [];

  for i = 1:cols
    plot(i, temp_importances(idx(i)), 'Marker', 'o', 'MarkerFaceColor', [1-color_dist(j) 0 color_dist(j)], 'MarkerEdgeColor', [1-color_dist(j) 0 color_dist(j)], 'LineWidth', 2);
    new_headers = [new_headers headers(idx(i))];
  end

  xtickangle(90);

  set(ax, 'xtick', 1:cols, 'xticklabel', new_headers);
  set(ax,'TickLabelInterpreter','none');
  xlabel('Features', 'Interpreter', 'none', 'fontweight', 'bold');
  ylabel('Cumulative Importance', 'Interpreter', 'none', 'fontweight', 'bold');
  title_text = 'The Cumulative Importance of Individual Features for Rock Type';
  title_text = strcat(title_text, {' '}, string(folders(j)));
  % title(title_text, 'Interpreter', 'none');
  set(gca(), 'LineWidth', 2);
  set(gca(), 'FontSize', 11);
  grid();
  xlim([0 cols + 1]);
  save_text = strcat(save_name, string(folders(j)));
  save_text = strcat(save_text, '.png');
  delvol_utils.save_plot(fig, save_text);
  hold off
end
