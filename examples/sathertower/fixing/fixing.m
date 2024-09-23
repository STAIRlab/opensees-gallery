clear;
% Define the filenames for your CSV files
sectionFile = 'Section_df.csv';
elemDefFile = 'ModifiedElemDef_cladding.csv';

% Read the data from both CSV files
sectionData = readtable(sectionFile);
elemDefData = readtable(elemDefFile);

% Initialize an empty array to store the corresponding indices
indices = NaN(height(elemDefData), 1);

% Loop through each row in 'ModifiedElemDef_cladding' and match 'sect_id' with 'id'
for i = 1:height(elemDefData)
    sect_id = elemDefData.sect_id{i}; % Get the sect_id from 'ModifiedElemDef_cladding'
    % Find the corresponding index in 'Section_df'
    for j = 1:height(sectionData)
        a = strcmp(sectionData.id{j}, sect_id);
        if a == 1
            break;
        end
    end
    elemDefData.Index{i} = j;
end


% Write the updated 'ModifiedElemDef_cladding' back to a CSV file
writetable(elemDefData, 'ModifiedElemDef_cladding_updated.csv');
