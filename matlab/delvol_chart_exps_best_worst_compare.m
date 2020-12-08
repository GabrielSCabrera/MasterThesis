[y_train, y_test, y_train_pred, y_test_pred, r2_train, r2_test, scores, folders] = delvol_utils.load_best_from_combined(directory);

N_plots = size(y_train);
N_plots = N_plots(2);
closest_square = ceil(sqrt(double(N_plots)));

fig = figure();
for i = 1:N_plots
  label = folders{i};
  format_spec = '%s; Best R^2 = %.2f, Worst R^2 = %.2f';
  r2_tests = zeros(height(y_test{i}), 0);

  for j = 1:height(y_train{i})
    score = scores{i};
    r2_tests(j) = table2array(score(j,2));
  end

  [maximum, idx] = max(r2_tests);

  a0 = table2array(y_train{i}(idx,:));
  b0 = table2array(y_train_pred{i}(idx,:));
  iters = size(a0);
  iters = iters(2);

  a = [];
  b = [];

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

  [minimum, idx] = min(r2_tests);
  title_string = sprintf(format_spec, label, maximum, minimum);

  c0 = table2array(y_test{i}(idx,:));
  d0 = table2array(y_test_pred{i}(idx,:));

  c = [];
  d = [];

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
  line1 = plot(a, b, 'bx', 'MarkerSize', 4);
  title(title_string, 'Units', 'normalized', 'Position', [0.5, -0.2, 0]);
  ax.FontSize = 5;
  hold on
  line2 = plot(c, d, 'r.', 'MarkerSize', 8);
  xl = xlim;
  line3 = plot([-1E8 1E8], [-1E8, 1E8], 'k:');
  xlim(xl);
  hold off
end

han = axes(fig,'visible','off');
han.Title.Visible ='on';
han.XLabel.Visible ='on';
han.YLabel.Visible ='on';
ylabel(han,'Predicted Values');
xlabel(han,'Expected Values');
title_obj = title(han,'Best & Worst Expected vs. Predicted Values of Fracture Densities');
titlePos = get(title_obj , 'position');
titlePos(1) = 0.45;
titlePos(2) = 1.02;
set(title_obj, 'position' , titlePos);
hL = legend([line1, line2],{'Best Results','Worst Results'}, 'Interpreter', 'latex');
newPosition = [0.82 0.94 0.05 0.05];
newUnits = 'normalized';
set(hL,'Position', newPosition,'Units', newUnits);
grid();

delvol_utils.save_plot(fig, save_name_1);
delvol_utils.save_plot(fig, save_name_2);

exit
