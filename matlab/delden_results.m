directory = "delden_results_09_20_2020_11_20_07_153648";
[y_train, y_test, y_train_pred, y_test_pred] = utils.load_from_delden(directory);
N_plots = height(y_train);

closest_square = ceil(sqrt(N_plots));
fig = figure();
for i = 1:N_plots
  ax = subplot(closest_square, closest_square, i);
  axes(ax)
  a = str2double(rmmissing(table2array(y_train(i,:))));
  b = str2double(rmmissing(table2array(y_train_pred(i,:))));
  c = rmmissing(table2array(y_test(i,:)));
  d = rmmissing(table2array(y_test_pred(i,:)));
  line1 = plot(a, b, 'b.');
  hold on
  line2 = plot(c, d, 'r.');
  diag_ac = [min([min(a), min(c)]), max([max(a), max(c)])];
  diag_bd= [min([min(b), min(d)]), max([max(b), max(d)])];
  plot(diag_ac, diag_bd, 'k:');
  hold off
end

han = axes(fig,'visible','off');
han.Title.Visible ='on';
han.XLabel.Visible ='on';
han.YLabel.Visible ='on';
ylabel(han,'Predicted Values');
xlabel(han,'Expected Values');
title(han,'Distribution of Expected vs. Predicted Values of Fracture Densities');

hL = legend([line1, line2],{'Training Data','Testing Data'});
newPosition = [0.2 0.01 0.05 0.05];
newUnits = 'normalized';
set(hL,'Position', newPosition,'Units', newUnits);

utils.save_plot(fig, "delden_results.png");

for i = 1:N_plots
  ax = subplot(closest_square, closest_square, i);
  axes(ax)
  a = str2double(rmmissing(table2array(y_train(i,:))));
  b = str2double(rmmissing(table2array(y_train_pred(i,:))));
  c = rmmissing(table2array(y_test(i,:)));
  d = rmmissing(table2array(y_test_pred(i,:)));
  line1 = loglog(a, b, 'b.');
  hold on
  line2 = loglog(c, d, 'r.');
  diag_x = linspace(min([min(a(a > 0)), min(c(c > 0))]), max([max(a(a > 0)), max(c(c > 0))]), 1E3);
  diag_y = linspace(min([min(b(b > 0)), min(d(d > 0))]), max([max(b(b > 0)), max(d(d > 0))]), 1E3);
  loglog(diag_x, diag_y, 'k:');
  hold off
end
han = axes(fig,'visible','off');
han.Title.Visible ='on';
han.XLabel.Visible ='on';
han.YLabel.Visible ='on';
ylabel(han,'Predicted Values');
xlabel(han,'Expected Values');
title(han,'Distribution of Expected vs. Predicted Values of Fracture Densities (Logarithmic)');

hL = legend([line1, line2],{'Training Data','Testing Data'});
newPosition = [0.2 0.01 0.05 0.05];
newUnits = 'normalized';
set(hL,'Position', newPosition,'Units', newUnits);

utils.save_plot(fig, "delden_results_log.png");
