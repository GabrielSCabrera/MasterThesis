[y_train, y_test, y_train_pred, y_test_pred, r2_train, r2_test, scores, folders] = delvol_utils.load_best_from_combined(directory);

N = size(y_train);
N = N(2);

fig = figure();
for i = 1:N
  label = folders{i};

  b0 = table2array(y_train_pred{i}(i,:));
  d0 = table2array(y_test_pred{i}(i,:));
  iters = size(b0);
  iters = iters(2);

  a = [];
  b = [];
  c = [];
  d = [];

  for j = 1:iters
    b_val = b0(j);
    if isa(b_val, 'cell')
      b_val = str2double(b_val);
    end
    if not(isnan(b_val))
      a = [a i];
      b = [b b_val];
    end
  end
  iters = size(d0);
  iters = iters(2);
  for j = 1:iters
    d_val = d0(j);
    if isa(d_val, 'cell')
      d_val = str2double(d_val);
    end
    if not(isnan(d_val))
      c = [c i];
      d = [d d_val];
    end
  end

  l1 = plot(a, b, 'r^');
  l2 = plot(c, d, 'bs');
  hold on
end
hL = legend([l1, l2],{'Training Set', 'Testing Set'});

han = axes(fig,'visible','off');
han.Title.Visible ='on';
han.XLabel.Visible ='on';
han.YLabel.Visible ='on';
ylabel(han,'Predicted Values', 'Interpreter', 'latex');
xlabel(han,'Experiment No.', 'Interpreter', 'latex');
title('Comparing Mean and Std. of $R^2$ Scores for Each Experiment', 'Interpreter', 'latex');
title_obj = title(han,'Experiment No. vs. Predicted Values of Fracture Densities', 'Interpreter', 'latex');
titlePos = get(title_obj , 'position');
titlePos(1) = 0.45;
titlePos(2) = 1.02;
set(title_obj, 'position' , titlePos);
newPosition = [0.82 0.94 0.05 0.05];
newUnits = 'normalized';
set(hL,'Position', newPosition,'Units', newUnits);
grid();

delvol_utils.save_plot(fig, save_name_1);
delvol_utils.save_plot(fig, save_name_2);
