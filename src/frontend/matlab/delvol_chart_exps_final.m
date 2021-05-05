[y_train, y_test, y_train_pred, y_test_pred, r2_train, r2_test, scores, folders] = delvol_utils.load_all_from_combined_final(directory);

idx = 4; % For MONZ3 set idx = 4

y_train = y_train(:,idx);
y_test = y_test(:,idx);
y_train_pred = y_train_pred(:,idx);
y_test_pred = y_test_pred(:,idx);

y_train = table2array(y_train{1});
y_test = table2array(y_test{1});
y_train_pred = table2array(y_train_pred{1});
y_test_pred = table2array(y_test_pred{1});

r2_train = table2array(scores(:,1));
r2_test = table2array(scores(:,2));

[scores_sorted, scores_idx] = sort(r2_test);
idx_best = scores_idx(end);
idx_second_best = scores_idx(end-1);
idx_worst = scores_idx(1);
idx_second_worst = scores_idx(2);

best = r2_test(idx_best);
second_best = r2_test(idx_second_best);
worst = r2_test(idx_worst);
second_worst = r2_test(idx_second_worst);

fig = figure();

ax1 = subplot(2, 2, 1);
plot(y_test(idx_best, :), y_test_pred(idx_best, :), 'ro', 'MarkerSize', 7, 'MarkerEdgeColor','red','MarkerFaceColor','none', 'LineWidth', 2);
grid();

hold on
plot(y_train(idx_best, :), y_train_pred(idx_best, :), 'b^', 'MarkerSize', 7, 'MarkerEdgeColor','blue','MarkerFaceColor','none', 'LineWidth', 2);

xlim0 = xlim();
ylim0 = ylim();
diag = [xlim0(1), xlim0(2)];
plot(diag, diag, 'k:')
xlim(xlim0);
ylim(ylim0);

label = strcat('(a) R²=', num2str(best, '%.2f'));
text(0.025,0.92,label,'Units','normalized','FontSize', 12, 'fontweight', 'bold')

hold off

ax2 = subplot(2, 2, 2);
plot(y_test(idx_second_best, :), y_test_pred(idx_second_best, :), 'ro', 'MarkerSize', 7, 'MarkerEdgeColor','red','MarkerFaceColor','none', 'LineWidth', 2);
grid();

hold on
plot(y_train(idx_second_best, :), y_train_pred(idx_second_best, :), 'b^', 'MarkerSize', 7, 'MarkerEdgeColor','blue','MarkerFaceColor','none', 'LineWidth', 2);

xlim0 = xlim();
ylim0 = ylim();
diag = [xlim0(1), xlim0(2)];
plot(diag, diag, 'k:')
xlim(xlim0);
ylim(ylim0);

label = strcat('(b) R²=', num2str(second_best, '%.2f'));
text(0.025,0.92,label,'Units','normalized','FontSize', 12, 'fontweight', 'bold')
hold off

ax3 = subplot(2, 2, 3);
plot(y_test(idx_second_worst, :), y_test_pred(idx_second_worst, :), 'ro', 'MarkerSize', 7, 'MarkerEdgeColor','red','MarkerFaceColor','none', 'LineWidth', 2);
grid();

hold on
plot(y_train(idx_second_worst, :), y_train_pred(idx_second_worst, :), 'b^', 'MarkerSize', 7, 'MarkerEdgeColor','blue','MarkerFaceColor','none', 'LineWidth', 2);

xlim0 = xlim();
ylim0 = ylim();
diag = [xlim0(1), xlim0(2)];
plot(diag, diag, 'k:')
xlim(xlim0);
ylim(ylim0);

label = strcat('(c) R²=', num2str(second_worst, '%.2f'));
text(0.025,0.92,label,'Units','normalized','FontSize', 12, 'fontweight', 'bold')
hold off

ax4 = subplot(2, 2, 4);
plot(y_test(idx_worst, :), y_test_pred(idx_worst, :), 'ro', 'MarkerSize', 7, 'MarkerEdgeColor','red','MarkerFaceColor','none', 'LineWidth', 2);
grid();

hold on
plot(y_train(idx_worst, :), y_train_pred(idx_worst, :), 'b^', 'MarkerSize', 7, 'MarkerEdgeColor','blue','MarkerFaceColor','none', 'LineWidth', 2);

xlim0 = xlim();
ylim0 = ylim();
diag = [xlim0(1), xlim0(2)];
plot(diag, diag, 'k:')
xlim(xlim0);
ylim(ylim0);

label = strcat('(d) R²=', num2str(worst, '%.2f'));
text(0.025,0.92,label,'Units','normalized','FontSize', 12, 'fontweight', 'bold')
hold off

han = axes(fig, 'visible', 'off');
han.Title.Visible='on';
han.XLabel.Visible='on';
han.YLabel.Visible='on';
xlabel(han, 'Expected', 'Interpreter', 'none', 'fontweight', 'bold');
ylabel(han,' Predicted', 'Interpreter', 'none', 'fontweight', 'bold');
set(han, 'FontSize', 11);

set(ax1, 'LineWidth', 2);
set(ax1, 'FontSize', 11);

set(ax2, 'LineWidth', 2);
set(ax2, 'FontSize', 11);

set(ax3, 'LineWidth', 2);
set(ax3, 'FontSize', 11);

set(ax4, 'LineWidth', 2);
set(ax4, 'FontSize', 11);

xh = get(han,'xlabel');
p = get(xh,'position');
p(2) = 1.25*p(2);
set(xh,'position',p);

delvol_utils.save_plot(fig, save_name);
close all
