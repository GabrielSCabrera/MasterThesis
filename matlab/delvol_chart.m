directory = "M8_1";
[y_train, y_test, y_train_pred, y_test_pred, scores] = delvol_utils.load_from_delvol(directory);
N_plots = height(y_train);

closest_square = ceil(sqrt(double(N_plots)));

fig = figure();
for i = 1:N_plots
  r2_train = table2array(scores(i,1));
  r2_test = table2array(scores(i,2));
  format_spec = '$R^2$ Train $ = %.2f$, $R^2$ Test $ = %.2f$';
  title_string = sprintf(format_spec, r2_train, r2_test);
  a = str2double(rmmissing(table2array(y_train(i,:))));
  b = str2double(rmmissing(table2array(y_train_pred(i,:))));
  c = str2double(rmmissing(table2array(y_test(i,:))));
  d = str2double(rmmissing(table2array(y_test_pred(i,:))));
  diag_ac = [min([min(a), min(c)]) max([max(a), max(c)])];
  diag_bd = [min([min(b), min(d)]) max([max(b), max(d)])];

  ax = subplot(closest_square, closest_square, i);
  axes(ax);
  line1 = plot(a, b, 'bx', 'MarkerSize', 4);
  xlim(diag_ac);
  ylim(diag_bd);
  title(title_string, 'Interpreter', 'latex', 'Units', 'normalized', 'Position', [0.5, -0.2, 0]);
  ax.FontSize = 5;
  hold on
  line2 = plot(c, d, 'r.', 'MarkerSize', 8);
  line3 = plot([-100 100], [-100, 100], 'k:');
  hold off
end

han = axes(fig,'visible','off');
han.Title.Visible ='on';
han.XLabel.Visible ='on';
han.YLabel.Visible ='on';
ylabel(han,'Predicted Values');
xlabel(han,'Expected Values');
title_obj = title(han,'Expected vs. Predicted Values of Fracture Densities');
titlePos = get(title_obj , 'position');
titlePos(1) = 0.45;
titlePos(2) = 1.02;
set(title_obj, 'position' , titlePos);
hL = legend([line1, line2, line3],{'Training Data','Testing Data','$f(x) = x$'}, 'Interpreter', 'latex');
newPosition = [0.82 0.94 0.05 0.05];
newUnits = 'normalized';
set(hL,'Position', newPosition,'Units', newUnits);

delvol_utils.save_plot(fig, "delvol_results.png");
delvol_utils.save_plot(fig, "delvol_results.pdf");

for i = 1:N_plots
  r2_train = table2array(scores(i,1));
  r2_test = table2array(scores(i,2));
  format_spec = '$R^2$ Train $ = %.2f$, $R^2$ Test $ = %.2f$';
  title_string = sprintf(format_spec, r2_train, r2_test);
  a = str2double(rmmissing(table2array(y_train(i,:))));
  b = str2double(rmmissing(table2array(y_train_pred(i,:))));
  c = str2double(rmmissing(table2array(y_test(i,:))));
  d = str2double(rmmissing(table2array(y_test_pred(i,:))));
  diag_x = [min([min(a(a > 0)), min(c(c > 0))]) max([max(a(a > 0)), max(c(c > 0))])];
  diag_y = [min([min(b(b > 0)), min(d(d > 0))]) max([max(b(b > 0)), max(d(d > 0))])];
  diag_line = linspace(-100, 100, 5E3);

  ax = subplot(closest_square, closest_square, i);
  axes(ax);

  line1 = loglog(a, b, 'bx', 'MarkerSize', 4);
  xlim([diag_x(1) diag_x(2)]);
  ylim([diag_y(1) diag_y(2)]);
  title(title_string, 'Interpreter', 'latex', 'Units', 'normalized', 'Position', [0.5, -0.2, 0]);
  ax.FontSize = 5;
  hold on
  line2 = loglog(c, d, 'r.', 'MarkerSize', 8);
  line3 = loglog(diag_x, diag_y, 'k:');
  line3 = loglog(diag_line, diag_line, 'k:');
  hold off
end
han = axes(fig,'visible','off');
han.Title.Visible ='on';
han.XLabel.Visible ='on';
han.YLabel.Visible ='on';
ylabel(han,'$\log($ Predicted Values $)$', 'Interpreter', 'latex');
xlabel(han,'$\log($ Expected Values $)$', 'Interpreter', 'latex');
title_obj = title(han,'Expected vs. Predicted Values of Fracture Densities (Log)');
titlePos = get(title_obj , 'position');
titlePos(1) = 0.4;
titlePos(2) = 1.02;
set(title_obj, 'position' , titlePos);
hL = legend([line1, line2, line3],{'Training Data','Testing Data','$f(x) = x$'}, 'Interpreter', 'latex');
newPosition = [0.82 0.94 0.05 0.05];
newUnits = 'normalized';
set(hL,'Position', newPosition,'Units', newUnits);

delvol_utils.save_plot(fig, "delvol_results_log.png");
delvol_utils.save_plot(fig, "delvol_results_log.pdf");

exit
