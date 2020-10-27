[y_train, y_test, y_train_pred, y_test_pred, r2_train, r2_test, scores, folders] = utils.load_best_from_combined(directory);

N_plots = size(y_train);
N_plots = N_plots(2);
closest_square = ceil(sqrt(double(N_plots)));

fig = figure();
for i = 1:N_plots
  r2_train_str = r2_train(i);
  r2_test_str = r2_test(i);
  label = folders{i};
  format_spec = '%s; R^2 Train = %.2f, Test = %.2f';
  title_string = sprintf(format_spec, label, r2_train_str, r2_test_str);
  r2_tests = zeros(height(y_test{i}), 0);

  for j = 1:height(y_train{i})
    score = scores{i};
    r2_tests(j) = table2array(score(j,2));
  end

  [maximum, idx] = min(r2_tests);

  a0 = table2array(y_train{i}(idx,:));
  b0 = table2array(y_train_pred{i}(idx,:));
  c0 = table2array(y_test{i}(idx,:));
  d0 = table2array(y_test_pred{i}(idx,:));
  iters = size(a0);
  iters = iters(2);

  a = [];
  b = [];
  c = [];
  d = [];

  for j = 1:iters
    a_val = a0(j);
    b_val = b0(j);
    if isa(a_val, 'cell')
      a_val = str2double(a_val);
    end
    if isa(b_val, 'cell')
      b_val = str2double(b_val);
    end
    if not(isnan(a_val) || isnan(b_val))
      a = [a a_val];
      b = [b b_val];
    end
  end
  iters = size(c0);
  iters = iters(2);
  for j = 1:iters
    c_val = c0(j);
    d_val = d0(j);
    if isa(c_val, 'cell')
      c_val = str2double(c_val);
    end
    if isa(d_val, 'cell')
      d_val = str2double(d_val);
    end
    if not(isnan(c_val) || isnan(d_val))
      c = [c c_val];
      d = [d d_val];
    end
  end

  diag_ac = [min([min(a), min(c)]) max([max(a), max(c)])];
  diag_bd = [min([min(b), min(d)]) max([max(b), max(d)])];

  ax = subplot(closest_square, closest_square, i);
  axes(ax);
  line1 = plot(a, b, 'bx', 'MarkerSize', 4);
  if diag_ac(1) < diag_ac(2)
    xlim(diag_ac);
  end
  if diag_bd(1) < diag_bd(2)
    ylim(diag_bd);
  end
  title(title_string, 'Units', 'normalized', 'Position', [0.5, -0.2, 0]);
  ax.FontSize = 5;
  hold on
  line2 = plot(c, d, 'r.', 'MarkerSize', 8);
  line3 = plot([-1000 1000], [-1000, 1000], 'k:');
  hold off
end

han = axes(fig,'visible','off');
han.Title.Visible ='on';
han.XLabel.Visible ='on';
han.YLabel.Visible ='on';
ylabel(han,'Predicted Values');
xlabel(han,'Expected Values');
title_obj = title(han,'Worst Expected vs. Predicted Values of Fracture Densities');
titlePos = get(title_obj , 'position');
titlePos(1) = 0.45;
titlePos(2) = 1.02;
set(title_obj, 'position' , titlePos);
hL = legend([line1, line2, line3],{'Training Data','Testing Data','f(x) = x'}, 'Interpreter', 'latex');
newPosition = [0.82 0.94 0.05 0.05];
newUnits = 'normalized';
set(hL,'Position', newPosition,'Units', newUnits);

utils.save_plot(fig, save_name_1);
utils.save_plot(fig, save_name_2);

for i = 1:N_plots
  r2_train_str = r2_train(i);
  r2_test_str = r2_test(i);
  label = folders{i};
  format_spec = '%s; R^2 Train = %.2f, Test = %.2f';
  title_string = sprintf(format_spec, label, r2_train_str, r2_test_str);
  r2_tests = zeros(height(y_test{i}), 0);

  for j = 1:height(y_train{i})
    score = scores{i};
    r2_tests(j) = table2array(score(j,2));
  end

  [maximum, idx] = min(r2_tests);

  a0 = table2array(y_train{i}(idx,:));
  b0 = table2array(y_train_pred{i}(idx,:));
  c0 = table2array(y_test{i}(idx,:));
  d0 = table2array(y_test_pred{i}(idx,:));
  iters = size(a0);
  iters = iters(2);

  a = [];
  b = [];
  c = [];
  d = [];
  iters = size(a0);
  iters = iters(2);
  for j = 1:iters
    a_val = a0(j);
    b_val = b0(j);
    if isa(a_val, 'cell')
      a_val = str2double(a_val);
    end
    if isa(b_val, 'cell')
      b_val = str2double(b_val);
    end
    if not(isnan(a_val) || isnan(b_val))
      a = [a a_val];
      b = [b b_val];
    end
  end
  iters = size(c0);
  iters = iters(2);
  for j = 1:iters
    c_val = c0(j);
    d_val = d0(j);
    if isa(c_val, 'cell')
      c_val = str2double(c_val);
    end
    if isa(d_val, 'cell')
      d_val = str2double(d_val);
    end
    if not(isnan(c_val) || isnan(d_val))
      c = [c c_val];
      d = [d d_val];
    end
  end

  ax = subplot(closest_square, closest_square, i);
  axes(ax);

  % diag_x = [min([min(a(a > 0)), min(c(c > 0))]) max([max(a(a > 0)), max(c(c > 0))])];
  % diag_y = [min([min(b(b > 0)), min(d(d > 0))]) max([max(b(b > 0)), max(d(d > 0))])];
  diag_x = [min([min(a), min(c)]) max([max(a), max(c)])];
  diag_y = [min([min(b), min(d)]) max([max(b), max(d)])];
  diag_line = linspace(-100, 100, 5E3);

  line1 = loglog(a, b, 'bx', 'MarkerSize', 4);
  if diag_x(1) < diag_x(2)
    xlim([diag_x(1) diag_x(2)]);
  end
  if diag_y(1) < diag_y(2)
    ylim([diag_y(1) diag_y(2)]);
  end
  title(title_string, 'Units', 'normalized', 'Position', [0.5, -0.2, 0]);
  ax.FontSize = 5;
  hold on
  line2 = loglog(c, d, 'r.', 'MarkerSize', 8);
  line3 = loglog(diag_line, diag_line, 'k:');
  hold off

end

han = axes(fig,'visible','off');
han.Title.Visible ='on';
han.XLabel.Visible ='on';
han.YLabel.Visible ='on';
ylabel(han,'log( Predicted Values )');
xlabel(han,'log( Expected Values )');
title_obj = title(han,'Worst Expected vs. Predicted Values of Fracture Densities (Log)');
titlePos = get(title_obj , 'position');
titlePos(1) = 0.4;
titlePos(2) = 1.02;
set(title_obj, 'position' , titlePos);
hL = legend([line1, line2, line3],{'Training Data','Testing Data','f(x) = x'}, 'Interpreter', 'latex');
newPosition = [0.82 0.94 0.05 0.05];
newUnits = 'normalized';
set(hL,'Position', newPosition,'Units', newUnits);

utils.save_plot(fig, save_name_3);
utils.save_plot(fig, save_name_4);

exit
