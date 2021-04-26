""" Utilities for Google Cloud"""

import subprocess

# GSUTIL TO BUCKET STORAGE ---------------------------------------------------------------

def gsutil_cp(source_file, dest_file):
    assert source_file, 'No SOURCE file specified'
    assert dest_file,   'No DESTINATION file specified'
    print(subprocess.check_output(['gsutil', 'cp', source_file, dest_file]))

def gsutil_ls(bucket_name):
    assert bucket_name, 'No Bucket Name specified'
    sims_csv_string = subprocess.check_output(['gsutil', 'ls', 'gs://' + bucket_name])
    sims_csv_list   = str(sims_csv_string).split('\n')
    return filter(None, sims_csv_list)


