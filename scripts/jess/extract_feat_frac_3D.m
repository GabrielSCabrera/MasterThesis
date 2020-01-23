close all
clearvars

% read in bin file
% from make_2D.m

ei=1;
sn = 1200;

% noise threshold of fractures 3000 2000, 1000, 500
as = [3000];

while ei<=4
    bfilo = '/Users/mcbeck/Dropbox/HADES/tracking/matlab/mats/EXP/bins/EXP_XMPa.bin';
    if ei==1
        exp = 'M8_1'
        rn = 1000;
        cn = 1000;
     
        axial_stress= [26:4:78 80:2:118 122:2:130];
        Pc  = 20;
        Poring  = 10;
        diff_stress = axial_stress - Pc - Poring;
        fail_stress = 130.7 - 20 - Poring;
    elseif ei==2
        exp = 'M8_2'
        rn = 900;
        cn = 900;

        axial_stress = [152:185 187:196];        
        Pc = 25;
        Poring = 15;
        diff_stress = axial_stress - Pc - Poring;
        fail_stress = 196.82 - 25 - Poring;        
    elseif ei==3
        exp = 'MONZ5'
        rn = 800;
        cn = 800;
        %sigs = [2 5 30 35 40 40:5:90 92:2:130 131:149 150.5:0.5:161.5];
        
        axial_stress = [30:5:40 40:5:85 90:2:128 130:1:149 150.5:0.5:161.5];
        Pc = 25;
        Poring = 21.875-0.2344;
        diff_stress = axial_stress*(25/16) - Pc - Poring;
        fail_stress = (161.36*25/16) - 25 - Poring;
    else
        exp = 'WG04'
        bfilo = strrep(bfilo, 'EXP_', 'EXP_SCAN_');
        rn = 800;
        cn = 800;
        
        % removed scans 46, 47, stresses = 142, 143
        scans = [1 2 4:10 12:22 25:36 39:44 48:55 59 60 60 60:63];
        axial_stress = [15 15:5:95 95:5:110 112:2:140 141 144:1:148 148.5 149 149.5 149.5 150 150.5 151 151.5 152 152.5];
        
        Pc = 10;
        Poring = 13.43;
        diff_stress = axial_stress.*(25/16) - Pc - Poring;           % Differential stress of all the volumes \sigma
        fail_stress = 152.544*25/16 - 10 - Poring;   % Differential stress at failure \sigma_c
    end

    sigs = axial_stress;
    sig_dists = (fail_stress-diff_stress)/fail_stress;
    
%     figure(1)
%     hold on
%     plot(diff_stress, sig_dists, 'ro')
%     
%     return
    
    bfil = strrep(bfilo, 'EXP', exp);
    
    for ai=1:length(as)
        a_noise = as(ai);
        
        prop_str = "%.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f ";
        format = strcat("%.1f %.3f %.2f %.2f %.2f ", prop_str, "\n");
        filestr = "sig sig_d cx cy cz area theta lmin lmax aniso dcmin dc5 dc10 dc25 dc50 dc75\n";
        prop_num = length(split(filestr, ' '));

        txtfile = ['/Users/mcbeck/Dropbox/HADES/tracking/learning/txts/inputs/' exp '_3D_frac_full_a' num2str(a_noise) '.txt'];

        di=1;
        datalines = nan(1e5, prop_num);
        for si=1:length(sigs)

            %si = length(sigs)-1; % for testing

            sig = sigs(si)
            sig_d = sig_dists(si);
            bin = strrep(bfil, 'X', num2str(sig));

            if ei==4
               scan = scans(si); 
               bin = strrep(bin, 'SCAN', num2str(scan)); 
            end

            disp(bin);
            if exist(bin, 'file')==0
               disp('File not found')
               disp(bin)
               return 
            end
            
            fid = fopen(bin);
            A = fread(fid);
            data = reshape(A, [rn cn sn]);
           
            sub = data;

            CC = bwconncomp(sub); % 26, most conservation connection
            s = regionprops(CC,'Centroid');
            f = regionprops(CC,'PixelList');
            cents = cat(1,s.Centroid);
            pixs = CC.PixelIdxList;

            areas = nan(length(pixs), 1);
            for pi=1:length(pixs)
               num = length(pixs{pi}) ;
               areas(pi) = num;
            end

            % remove segmented volumes that are < threshold value
            i_noise = find(areas<a_noise);

            if length(pixs)>1
                for pi=1:length(pixs)

                    % if this fracture is not in the noise
                    if sum(pi==i_noise)==0
                        pix = pixs{pi};

                        xyz=cat(1,f(pi).PixelList);

                        cent = cents(pi, :);
                        cent_else = cents([1:pi-1 pi+1:length(pixs)], :);

                        [centc, area, theta, l_min, l_max, aniso] = get_geo_sing_2D(xyz(:,1), xyz(:,2), xyz(:,3));

                        dists_c = sqrt((cent(1)-cent_else(:,1)).^2 + (cent(2)-cent_else(:,2)).^2 + (cent(3)-cent_else(:,3)).^2);

                        datalines(di, :) = [sig sig_d centc(1) centc(2) centc(3) area theta l_min l_max aniso min(dists_c) prctile(dists_c, 5) prctile(dists_c, 10) prctile(dists_c, 25) prctile(dists_c, 50) prctile(dists_c, 75)];
                        di=di+1;

                    end            
                end
            end    
         end

        datalines = datalines(~isnan(datalines(:, 1)), :);

        datastr = sprintf(format, datalines');
        filestr = strcat(filestr, datastr);

        % write data to new file
        fid = fopen(txtfile, 'w');
        fprintf(fid, filestr);
        fclose(fid);
        disp(txtfile)
        
    end
    
    ei=ei+1;
end