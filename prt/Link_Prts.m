clear all
close all

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                  config variables                 %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

dirdata = '/path/tofunctional/';

subj = 'S06';

prt_mode = 'split';                                  % options: ['standard', 'split']

dirsubj = [dirdata, subj, '/'];                     %dirsubj2 = [dirdata,subj,'_PP_nordic','/'];

cond = {'WhatOn','WhatOff'};

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                   start of code                   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


xff(0,'transiosize','vtc',120000)
XTCList = {};
count=1;
for i=1:length(cond)

    list = dir([dirsubj,'*',cond{i},'*.vtc']);
    
    for j=1:length(list)
        currfile = list(j).name;
        indxr = strfind(currfile,'run');
        runNr = str2double(currfile(indxr+3));
      
        vtc = xff([dirsubj,currfile]);
   
       
        filesList = dir(dirsubj);

        if strcmp(prt_mode, 'standard')
            prtFilename = regexpi({filesList.name},['(?=', cond{i}, ')(.*)', 'run', num2str(runNr), '(.*)_[0-9][0-9]\.prt'],'match');
        elseif strcmp(prt_mode, 'split')
            prtFilename = regexpi({filesList.name},['(?=', cond{i}, ')(.*)', 'run', num2str(runNr), '(.*)_split\.prt'],'match');
        end
        
        vtc.NameOfLinkedPRT = [dirsubj, char([prtFilename{:}])];
        vtc.NrOfLinkedPRTs = 1;
        vtc.NrOfCurrentPRT = 1;

        vtc.SaveAs([dirsubj,currfile]);
        
       
        vtc.ClearObject;
        clear vtc;
        
    end
end

