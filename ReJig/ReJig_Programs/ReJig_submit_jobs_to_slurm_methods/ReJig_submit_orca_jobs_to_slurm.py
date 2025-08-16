'''
Geoffrey Weal, ReJig_submit_orca_jobs_to_slurm.py, 15/6/2023

This program contains methods for submitting ORCA jobs to slurm if appropriate to do so.
'''
from ReJig.ReJig_Programs.shared_general_methods.shared_orca_methods import did_orca_opt_job_complete
#from ReJig.ReJig_Programs.shared_general_methods.shared_orca_methods import did_orca_job_complete

def general_orca_submission(filenames):
    """
    This method is design to determine if you can submit ORCA ATC or EET calculations.

    Parameters
    ----------
    filenames : list of str.
        These are all the filenames of files in the directory you want to look at.

    Returns
    -------
    submission_filenames : all the filenames for submission scripts to submit to slurm.
    """

    # First, create the submission_filenames list
    submission_filenames = []

    # Second, if rejig_opt.log is already in the directory, this job has already run so dont submit it. 
    #         --> Only submit this job if rejig_opt.log does not already exist.
    if ('rejig_opt.log' not in filenames): 
        submission_filenames.append('submit.sl')

    # Fourth, return submission_filenames
    return submission_filenames

# ==============================================================================================================
