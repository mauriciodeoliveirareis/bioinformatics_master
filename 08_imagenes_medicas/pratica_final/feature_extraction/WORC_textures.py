from radiomics import featureextractor
import os
from pathlib import Path
import pandas as pd
import logging

class TexturesError(Exception):
    """Base error related to Texture analysis method"""

def params_file_path(modality):
    main_path = Path('params_files')

    if modality == 'CT':
        params_path = main_path / 'params_CT.yaml'
    elif modality == 'MR':
        params_path = main_path / 'params_MR.yaml'
    else:
        raise TexturesError("Unsupported image modality!")
    
    return str(params_path)


# PARAMETERS #
###################################################
DISEASE = 'GIST' 
MODALITY = 'CT'

mask_file_name = 'mask.nii.gz'
serie_file_name = 'image.nii.gz'
###################################################


# List Patients
path_cases = Path(__file__).parent.parent / 'WORC_Images' / DISEASE
patients = os.listdir(path_cases)
patients.sort()

if '.DS_Store' in patients:
    patients.remove('.DS_Store')

if '_output.log' in patients:
    patients.remove('_output.log')

if 'texture_results.csv' in patients:
    patients.remove('texture_results.csv')

for patient in patients:
    if not Path(path_cases / patient).is_dir():
        patients.remove(patient)

# Logger
path_log = path_cases / '_output.log'
logging.basicConfig(filename=path_log, level=logging.INFO, filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')


df_radiomics = pd.DataFrame()

for p, patient in enumerate(patients):
    print(patient)
    logging.info(f'Analysing patient: {patient}')
    path_patient = Path(path_cases) / patient

    try:
        timepoints = os.listdir(path_patient)
        timepoints.sort()
    except NotADirectoryError:
        logging.error(f'Error in Directory {patient}')
        continue

    if '.DS_Store' in timepoints:
        timepoints.remove('.DS_Store')
    

    # Analyze Timepoints
    for t, timepoint in enumerate(timepoints):
        logging.info(f'Analysing timepoint: {timepoint} ')
        path_timepoint = path_patient / timepoint / 'NIFTI' 
        try: 
            path_mask = os.path.join(path_timepoint, mask_file_name)
            path_serie = os.path.join(path_timepoint, serie_file_name)

            if not os.path.exists(path_mask):
                logging.warning(f'Mask not detected for patient: {patient}, timepoint: {timepoint}')
                continue

            # TEXTURE ANALYSIS
            # ======================================
            params_path = params_file_path(MODALITY)
            extractor = featureextractor.RadiomicsFeatureExtractor(params_path)
            result = extractor.execute(path_serie, path_mask)

            # Store Results
            result = pd.DataFrame(result.items()).set_index(0).transpose()
            result.insert(0, 'PatientID', patient)
            df_radiomics = pd.concat([df_radiomics, result], axis=0)

        except Exception as e:
            logging.error(f'{patient} | {e}')
            continue

# Save Radiomics
logging.info('Saving Results')
path_results = path_cases / 'texture_results.csv'
df_radiomics.to_csv(path_results, index=False)
