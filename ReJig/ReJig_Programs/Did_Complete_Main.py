'''
Did_Complete_Main.py, Geoffrey Weal, 08/03/2019

This program will determine which of your dimers have been successfully calculated in Gaussian.
'''
import os, sys
from tqdm import tqdm

from ReJig.ReJig_Programs.Did_Complete_Main_methods.analyse_optimised_output import analyse_optimised_output

# -------------------------------------------------------------------------------

def Did_Complete_Main(general_path, print_progress=True):
    """
    This method will go through folders in search of output.log files, and will determine from those output.log files if they had finished successfully or not.

    Parameters
    ----------
    general_path : str.
        This is the overall directory to search through for output.log files.
    print_progress : bool.
        This boolean indicates if you want to print the details of the how many jobs this script has processed. 

    Returns
    -------
    atc_jobs_results : str.
        These are the results of ATC jobs.
    re_jobs_results : str.
        These are the results of RE jobs.
    fc_jobs_results : str.
        These are the results of FC jobs.
    eet_jobs_results : str.
        These are the results of EET jobs.
    ict_jobs_results : str.
        These are the results of ICT jobs.
    unalligned_jobs : str.
        These are all the unalligned jobs 
    """

    # First, initialise lists to record results to.
    opt_jobs_finished_successfully = []
    opt_jobs_finished_unsuccessfully = []
    opt_jobs_not_begun = []

    # Second, obtain the current working directory. 
    original_path = os.getcwd()

    # Third, obtain the os.walk object.
    pbar = os.walk(general_path)

    # Fourth, if you want to print the progress of this script to a progress bar, do it here.
    if print_progress:
        pbar = tqdm(pbar, unit='Jobs')

    # Fifth, determine all the Gaussian jobs to check. 
    for root, dirs, files in pbar:

        # 5.1: Sort dirs and files so that things come out in alphabetical order.
        dirs.sort()
        files.sort()

        # 5.2: Determine if a .gjf or inp. file is found. If so, we have found a Gaussian/ORCA job.
        if 'rejig_opt.gjf' in files:
            software_type = 'Gaussian'
            #input_file_name      = 'rejig_opt.gjf'
            #output_file_name     = 'rejig_opt.log'
        elif 'rejig_opt.inp' in files:
            software_type = 'ORCA'
            #input_file_name      = 'rejig_opt.inp'
            #output_file_name     = 'rejig_opt.out'
        else:
            continue

        # 5.3: Print details of where the program is up to:
        if print_progress:
            pbar.set_description(root.replace(original_path+'/',''))

        # 5.4: Go through the output.log file to see if the job finished successfully or not.
        completion_stage, re_details = analyse_optimised_output(software_type, root)

        # 5.5: Record if this job is complete, not complete, or has not yet begun.
        if completion_stage == 'C':
            opt_jobs_finished_successfully.append(root)
        elif completion_stage == 'NC':
            opt_jobs_finished_unsuccessfully.append(root)
        elif completion_stage == 'NBY':
            opt_jobs_not_begun.append(root)

        # 5.6: This will prevent the program looking further down the directories.
        dirs[:] = []
        files[:] = []

    # Sixth, sort each list alphabetically and combine together for easy management of data.
    opt_jobs_results = (sorted(opt_jobs_finished_successfully), sorted(opt_jobs_finished_unsuccessfully), sorted(opt_jobs_not_begun))

    # Seventh, return results of ECCP Gaussian jobs. 
    return opt_jobs_results

def add_to_list(root_and_stuff, completion_stage, jobs_finished_successfully, jobs_finished_unsuccessfully, jobs_not_begun):
    if completion_stage == 'NBY':
        jobs_not_begun.append(root_and_stuff)
    elif completion_stage == 'NC':
        jobs_finished_unsuccessfully.append(root_and_stuff)
    elif completion_stage == 'NCh':
        jobs_finished_unsuccessfully.append(root_and_stuff)
    elif completion_stage == 'C' or (completion_stage == 'NF'):
        jobs_finished_successfully.append(root_and_stuff)
    else:
        raise Exception('Error: completion_stage must be either "NBY", "NC", "NCh" or "C". completion_stage = '+str(completion_stage))



