%run NORDIC
clear all; close all;

dirdata = '<-PATH->';
cd(dirdata);
noiseVol = 0; %1 = noise volume for denoising; 0 = no noise volume

files = dir(fullfile(dirdata, '*.nii'));        % Create a struct of all files ending in .nii
ind = 1;
for ii = 1:numel(files)
    index = strfind(files(ii).name, 'ph');      % Find all nifti files containing ph (phase information)
    if ~isempty(index)
        filelist{ind} = files(ii).name;         % Create a list of all nifiti files containing ph
        ind = ind + 1;
    end
end


for irun = 1:numel(filelist)
    
    fn_magn_temp = filelist{irun};              % fn_magn_temp is the i'th file of the list (meaning actually the name of the file containing the phase)
    no_ph = fn_magn_temp(end-8:end-7);          % Series number indicating the list of files containing the phase.
    if strcmp(no_ph(1),'_')                     % Checks whether this series number is not _
        no_ph = str2num(no_ph(2));
        cut_ph = 8;
    else
        no_ph = str2num(no_ph);                 % If not _ then convert the series number of phase file to numbers.
        cut_ph = 9;
    end
    fn_magn_temp = [fn_magn_temp(1:end-cut_ph),num2str(no_ph-1),'.nii'];    % Set fn_magn_temp to the phase series number -1
    
    fn_magn_in=fn_magn_temp;                    % 
    fn_phase_in=filelist{irun};                 % Select phase file
    fn_out=['NORDIC_patch17_3D_' fn_magn_in(1:end-4)];     % Name 
    
    
    if noiseVol %NORDIC with noise volume for denoising
        ARG.noise_volume_last=1;
        ARG.NORDIC=1;
        ARG.save_add_info =1; % SAVES a matlab file with information on threshold and energy removed. Has not been curated well yet.
        ARG.temporal_phase = 1;
        ARG.phase_filter_width = 10;
        %ARG.magnitude_only = 1;
        ARG.kernel_size_PCA = [17 17 17];
        
        NIFTI_NORDIC_Github(fn_magn_in,fn_phase_in,fn_out,ARG)
    else
        %ARG.magnitude_only = 1;
        ARG.NORDIC = 1;
        ARG.save_add_info =1;
        ARG.temporal_phase = 1;
        ARG.phase_filter_width = 10;
        %NIFTI_NORDIC_Github(fn_magn_in,fn_phase_in,fn_out)
        NIFTI_NORDIC_Github(fn_magn_in,fn_phase_in,fn_out,ARG)
    end    
    
% %NORDIC for magnitude ONLY without noise volume for denoising
% fn_magn_in='name.nii.gz';
% fn_phase_in= fn_magn_in ;
% fn_out=['NORDIC_' fn_magn_in];
% ARG.magnitude_only=1;  
% ARG.NORDIC=1; 
% NIFTI_NORDIC_COMPLEX(fn_magn_in,fn_phase_in,fn_out,ARG)
% 
% %NORDIC_MP (g-factor corrected with MP estimation) for magnitude ONLY without noise volume for denoising
% fn_magn_in='name.nii.gz';
% fn_phase_in= fn_magn_in;
% fn_out=['NORDIC_' fn_magn_in];
% ARG.magnitude_only=1;
% ARG.MP=1;
% NIFTI_NORDIC_COMPLEX(fn_magn_in,fn_phase_in,fn_out,ARG)

% Below are other options that you can run.
        %ARG.make_complex_nii=1;  %  Saves both magnitude and phase nii files
        %ARG.NORDIC=0;  ARG.MP=2;
        %ARG.magnitude_only = 1;
        %ARG.kernel_size_PCA = [];
    
end