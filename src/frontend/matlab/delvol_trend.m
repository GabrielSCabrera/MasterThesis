[density_data] = delvol_utils.load_from_density_data(directory);
N_experiments = height(density_data);
delvol_idx = 1;
sigd_idx = 3;

delvol = table2array(density_data(:,delvol_idx));
sigd = table2array(density_data(:,sigd_idx));
fig = plot(sigd, delvol);
hold on
plot(sigd, delvol, 'rx');
xlabel('$\sigma_d$', 'Interpreter', 'latex');
ylabel('$\nabla \rho$', 'Interpreter', 'latex');
title('Del-Density as a Function of Stress over Time', 'Interpreter', 'latex');
grid();
xlim([min(sigd) max(sigd)]);
grid();
delvol_utils.save_plot(fig, save_name);
hold off
