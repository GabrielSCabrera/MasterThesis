import utils;

filename_1 = "test_file_1.dat";
filename_2 = "test_file_2.dat";
x = linspace(0, 10, 10);
y1 = utils.load_csv(filename_1);
y2 = utils.load_csv(filename_2);
disp(y1);
disp(y2);

fig = figure;
plot(x,y1);
hold on
plot(x,y2);
hold off
title("Sample Plot Title");
xlabel("Sample X-Axis Label");
ylabel("Sample Y-Axis Label");
legend({'Curve 1', 'Curve 2'});
utils.save_plot(fig, "test_plot.pdf");
