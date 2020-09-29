[density_data] = utils.load_from_density_data(directory);
N_experiments = height(density_data);
delden_idx = 1;
sigd_idx = 3;

delden = table2array(density_data(:,delden_idx));
sigd = table2array(density_data(:,sigd_idx));
fig = plot(sigd, delden);
hold on
plot(sigd, delden, 'rx');
xlabel('\sigma_d');
ylabel('\nabla \rho');
title('Del-Density as a Function of Stress over Time');
grid();
xlim([min(sigd) max(sigd)]);
utils.save_plot(fig, save_name);
hold off
exit();
