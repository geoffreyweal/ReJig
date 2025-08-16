'''
analyse_RE_output.py, Geoffrey Weal, 29/12/22

This method is designed to check if a RE Gaussian job has completed or not.
'''
import os
from ReJig.ReJig_Programs.shared_general_methods.shared_gaussian_methods import did_gaussian_opt_job_complete
from ReJig.ReJig_Programs.shared_general_methods.shared_orca_methods     import did_orca_opt_job_complete

def analyse_optimised_output(software_type, path):
    """
    This method is designed to check if an ATC Gaussian job has completed or not.

    Parameters
    ----------
    software_type : str.
        This is the software you want to use for locally optimising molecules. This can be either Gaussian or ORCA. 
    path : str.
        This is the path to the RE job files.

    Returns
    -------
    The results of the job: str.
        * 'NBY': Not begun yet.
        * 'NC' : Not complete.
        * 'C'  : Complete.
    """

    if software_type == 'Gaussian':
        return analyse_output_Gaussian(path)
    elif software_type == "ORCA":
        return analyse_output_ORCA(path)
    raise Exception('Error, you need to use with Gaussian or ORCA software. software_type = '+str(software_type))

# ----------------------------------------------------------------------------------------

def analyse_output_Gaussian(path):
    """
    This method is designed to check if an ATC Gaussian job has completed or not.

    Parameters
    ----------
    path : str.
        This is the path to the RE job files.

    Returns
    -------
    The results of the job: str.
        * 'NBY': Not begun yet.
        * 'NC' : Not complete.
        * 'C'  : Complete.
    """

    # ========================================================================
    # First, if the output.log file does not exist, return this.

    # 1.1.1: This is the ground structure log files to check.
    main_opt_name = 'rejig_opt.log'

    # 1.1.2: Get paths to files.
    path_to_opt = path+'/'+main_opt_name

    # 1.1.3: Check if these files exist.
    opt_begun = os.path.exists(path_to_opt)

    # 1.1.4: If none of the log files exist, this job has not begun.
    if not opt_begun:
        return 'NBY', None # Not begun yet.

    # ========================================================================

    # Second, check if the optimisation finished successfully or not. 
    did_main_opt_finish, has_main_opt_fully_converged, main_opt_converged_image_index, total_no_of_images_made_during_main_opt = did_gaussian_opt_job_complete(path_to_opt, get_most_converged_image=True, get_total_no_of_images=True)

    # Third, determine if the optimisation has completed based on did_main_opt_finish
    has_completed = 'C' if did_main_opt_finish else 'NC'

    # Fourth, return results of calculations. 
    optimisation_details = (did_main_opt_finish, has_main_opt_fully_converged, main_opt_converged_image_index, total_no_of_images_made_during_main_opt) if not did_main_opt_finish else None

    # Fifth, return if the ReJig program completed and reorganisation energy information. 
    return has_completed, optimisation_details

# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------

def analyse_RE_output_ORCA(path):
    """
    This method is designed to check if an ATC ORCA job has completed or not.

    Parameters
    ----------
    path : str.
        This is the path to the RE job files.

    Returns
    -------
    The results of the job: str.
        * 'NBY': Not begun yet.
        * 'NC' : Not complete.
        * 'C'  : Complete.
    """

    raise Exception('Need to write')

    # First, if the output.log file does not exist, return this.
    if   calculation_type == 'ground_structure':
        # 1.1.1: This is the ground structure log files to check.
        main_opt_name      = 'eGS_gGS_main_opt.out'

        # 1.1.2: Get paths to files
        path_to_main_opt   = path+'/'+main_opt_name

        # 1.1.3: If none of the log files exist, this job has not begun.
        if not os.path.exists(path_to_main_opt):
            return 'NBY', None # Not begun yet.

    elif calculation_type == 'excited_structure':
        # 1.2.1: This is the excited structure log files to check.
        main_opt_name       = 'eES_gES_main_opt.out'

        # 1.2.2: Get paths to files
        path_to_main_opt    = path+'/'+main_opt_name

        # 1.2.3: If none of the log files exist, this job has not begun.
        if not os.path.exists(path_to_main_opt):
            return 'NBY', None # Not begun yet.
            
    else:
        raise Exception('Error, output file name must be either "GS_GS.out" or "ES_ES.out". Path to where issue is = '+str(path)+'. Check this out.')

    # ========================================================================
    # Second, get the names of all the output files that are made for a RE job.
    
    # 2.1: convert GS --> ES and ES --> GS
    if   calculation_type == 'ground_structure':
        GS_or_ES_type = 'GS'
    elif calculation_type == 'excited_structure':
        GS_or_ES_type = 'ES'
    else:
        raise Exception('huh?')

    # 2.2: Get the path to the frequency file
    freq_file         = 'e'+GS_or_ES_type                   +'_g'+GS_or_ES_type+'_freq.out'
    single_point_file = 'e'+convert_GS_and_ES(GS_or_ES_type)+'_g'+GS_or_ES_type+'.out'

    # 2.3: Get the path to the single point file
    freq_output_filepath = path+'/'+freq_file
    sp_output_filepath   = path+'/'+single_point_file
    # ========================================================================

    # Third, check if the main optimisation finished on the GS_GS.out or ES_ES.out files.
    did_main_opt_finish, has_main_opt_fully_converged, main_opt_converged_image_index, total_no_of_images_made_during_main_opt = did_orca_opt_job_complete(path_to_main_opt, get_most_converged_image=True, get_total_no_of_images=True) if os.path.exists(path_to_main_opt) else (None, None, None, None)

    # Fourth, check if the freq calc finished on the GS_GS_freq.out or ES_ES_freq.out files.
    did_freq_finish, is_freq_force_convergence_good, no_of_negative_frequencies = did_freq_orca_job_complete(freq_output_filepath) if os.path.exists(freq_output_filepath) else (None, None, None)

    # Fifth, check if the single point calc finished for the GS_ES.out or ES_GS.out files.
    did_sp_finish = did_orca_job_complete(sp_output_filepath) if os.path.exists(sp_output_filepath) else None

    # Sixth, determine if calculations have completed or not.
    if   calculation_type == 'ground_structure': 
        re_results_for_determining_completion = (did_main_opt_finish, did_freq_finish, did_sp_finish)
    elif calculation_type == 'excited_structure':
        re_results_for_determining_completion = (did_main_opt_finish, did_freq_finish, did_sp_finish)
    if all([(re_result_for_determining_completion == True) for re_result_for_determining_completion in re_results_for_determining_completion]):
        if no_of_negative_frequencies == 0:
            has_completed = 'C' 
        else:
            has_completed = 'NC'
    else:
        has_completed = 'NC'

    # Seventh, return results of calculations. 
    if (has_completed == 'NBY') or (has_completed == 'C'):
        re_details = None
    elif has_completed == 'NC':
        if   calculation_type == 'ground_structure':
            re_details = ('ground_structure',  did_main_opt_finish, has_main_opt_fully_converged, main_opt_converged_image_index, total_no_of_images_made_during_main_opt, did_freq_finish, is_freq_force_convergence_good, no_of_negative_frequencies, did_sp_finish)
        elif calculation_type == 'excited_structure':
            re_details = ('excited_structure', did_main_opt_finish, has_main_opt_fully_converged, main_opt_converged_image_index, total_no_of_images_made_during_main_opt, did_freq_finish, is_freq_force_convergence_good, no_of_negative_frequencies, did_sp_finish)
        else:
            raise Exception('Error, log name must be either "eGS_gGS.log" or "eES_gES.log". logfile_name = '+str(logfile_name)+'. Check this out.')
    else:
        return Exception('Huh?')

    # Eighth, return if the ReJig program completed and reorganisation energy information. 
    return has_completed, re_details

# ----------------------------------------------------------------------------------------

