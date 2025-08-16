'''
Geoffrey Weal, ReJig_tidy_data.py, 30/4/24

This program is designed to tidy up your data folder and get rid of unnecessary files, particularly those very large files. 
'''
import os, shutil

from ReJig.ReJig_Programs.shared_general_methods.shared_gaussian_methods import found_a_gaussian_job_that_has_run
from ReJig.ReJig_Programs.shared_general_methods.shared_gaussian_methods import did_gaussian_job_complete
from ReJig.ReJig_Programs.shared_general_methods.shared_gaussian_methods import gaussian_temp_files_to_remove
from ReJig.ReJig_Programs.shared_general_methods.shared_gaussian_methods import remove_slurm_output_files

class CLICommand:
    """Will tidy up your data folder and get rid of unnecessary files, particularly those very large files.
    """

    @staticmethod
    def add_arguments(parser):
        pass

    @staticmethod
    def run(args):
        Run_method()

def Run_method():
    """
    This method will remove all unnecessary files for jobs that have completed.
    """

    # First, setup all the initial variables.
    current_path = os.getcwd()
    print('----------------------------------------------')
    print('Tidying Folders from the root path: '+str(current_path))
    print('----------------------------------------------')
    did_find_job = False
    did_not_tidy_jobs = []

    # Second, go through each subdirectory in the parent directory. 
    for root, dirs, files in os.walk(current_path):

        # 2.1: sort the directory just to make tidying happen in alphabetical order.
        dirs.sort()

        # 2.2: Determine if any Gaussian files exists in the current file under investigation. 
        if found_a_gaussian_job_that_has_run(root, files):

            # 2.3: indicate that at least one Gaussian job has been found. 
            did_find_job = True

            # 2.4: Determine if the gaussian job completed or not. 
            has_GS_GS_opt_completed = did_gaussian_job_complete(root+'/rejig_opt.log')

            # 2.5: Did this ground state optimisation calculation finish.
            if has_GS_GS_opt_completed:
                gaussian_temp_files_to_remove(root, files, remove_chk_file=True, remove_fort7_file=True, print_to_display=False)
                remove_slurm_output_files(root)
            else:
                did_not_tidy_jobs.append(root)

            # 2.6: Do not need to move further down the subdirectories anymore, remove all dirs and files lists.
            dirs[:]  = []
            files[:] = []
            
    # Third, print information about this tidying run.
    if not did_find_job:
        print('Finshed, but no temp files were found for tidying.')
    elif len(did_not_tidy_jobs) > 0:
        print('----------------------------------------------')
        print('The following jobs were not tidied. These are either still running or failed.')
        print()
        for root in did_not_tidy_jobs:
            print(root)
    else:
        print('Finished tidying ReJig jobs.')
    print('----------------------------------------------')

