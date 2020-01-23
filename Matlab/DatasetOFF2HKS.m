DATASET_PATH = 'ModelNet10';
DATASET_PATH_OUT = 'HKS_ModelNet10';

meshClasses = dir('ModelNet10');
meshClasses = meshClasses(~ismember({meshClasses(:).name},{'.','..'}));

mesh_errors = []

n = 200;

for class = meshClasses'
    class_dir = fullfile(class.folder, class.name);
    meshes_dir = dir(strcat(class_dir, '/*.off'));
    
    if ~exist(fullfile(DATASET_PATH_OUT, class.name), 'dir')
       mkdir(fullfile(DATASET_PATH_OUT, class.name));
    end
    for mesh_dir = meshes_dir'
       m_dir = fullfile(mesh_dir.folder, mesh_dir.name);
       
       csv_name = fullfile(DATASET_PATH_OUT, class.name, strcat(extractBefore(mesh_dir.name, '.off'), '.csv'));
       disp(csv_name);
       if isfile(csv_name) 
           disp(strcat('already exists ', csv_name));
       else
            disp(mesh_dir.name)
            matrix = OFF2HKS(m_dir, n);
            NrNaN = sum(isnan(matrix(:)));
            if NrNaN == 0            
                csvwrite(csv_name, matrix);      
                disp(mesh_dir.name);
            else
                mesh_errors = [mesh_errors mesh_dir.name];
            end
       end
           
    end
end