'''
Did_Complete.py, Geoffrey Weal, 11/04/2022

This program will determine which of your dimers have been successfully calculated in Gaussian.
'''
import os

from ReJig.ReJig_Programs.Did_Complete_Main import Did_Complete_Main

class CLICommand:
    """Will determine which geometric optimisation jobs have completed and which ones have not.
    """

    @staticmethod
    def add_arguments(parser):
        pass

    @staticmethod
    def run(args):
        Run_method()

def Run_method():
    """
    This method will determine which of your dimers have been successfully calculated in Gaussian.
    """
    print('########################################################################')
    print('########################################################################')
    print('Checking if OPV_Dimer_Pairer job have completed in Gaussian')
    print('-----------------------------------------------------------')

    # First, obtain the current directory path.
    general_path = os.getcwd()

    # Second, determine which ECCP Gaussian jobs have completed or not.
    opt_jobs_finished_successfully, opt_jobs_finished_unsuccessfully, opt_jobs_not_begun = Did_Complete_Main(general_path)

    # Third, print the results from the optimisation that completed. 
    if not (len(opt_jobs_finished_successfully) == 0):
        print('########################################################################')
        print('########################################################################')
        print('-------------------')
        print('Jobs that completed'.upper())
        print('-------------------')
        with open('ReJig_completed_OPT_jobs.txt','w') as completed_OPT_jobsTXT:
            for dirpath in opt_jobs_finished_successfully:
                print(dirpath)
                completed_OPT_jobsTXT.write(dirpath+'\n')

    # Fourth, print the results from the optimisation that did not complete.
    if not (len(opt_jobs_finished_unsuccessfully) == 0):
        print('########################################################################')
        print('########################################################################')
        print('--------------------------')
        print('Jobs that did not complete'.upper())
        print('--------------------------')
        with open('ReJig_incompleted_OPT_jobs.txt','w') as incompleted_OPT_jobsTXT:
            for dirpath in opt_jobs_finished_unsuccessfully:
                print(dirpath)
                incompleted_OPT_jobsTXT.write(dirpath+'\n')

    # Fifth, print the results from the optimisation that have not begun.
    if not (len(opt_jobs_not_begun) == 0):
        print('########################################################################')
        print('########################################################################')
        print('--------------------------')
        print('Jobs that have not begun yet'.upper())
        with open('ECCP_pending_OPT_jobs.txt','w') as pending_OPT_jobsTXT:
            for dirpath in opt_jobs_not_begun:
                print(dirpath)
                pending_OPT_jobsTXT.write(dirpath+'\n')

    print('########################################################################')
    print('########################################################################')

# ========================================================================================================

def get_re_details_string(dirpath, re_details):
    """
    This method is designed to tostring the detrails about the reorganisation energy calculation.

    Parameters
    ----------
    dirpath : str.
        This is the path to the ECCP reorgnisation energy job set.
    re_details : list
        This is all the information about the ECCP job.
    """

    # First, get the calculation type for this reorganisation energy detail
    calculation_type = re_details[0]

    # Second, obtain the data from the re_details list.
    calculation_type, did_main_preopt_finish, has_main_preopt_fully_converged, main_preopt_converged_image_index, total_no_of_images_made_during_main_preopt, did_main_opt_finish, has_main_opt_fully_converged, main_opt_converged_image_index, total_no_of_images_made_during_main_opt, did_freq_finish, is_freq_force_convergence_good, no_of_negative_frequencies, did_sp_finish = re_details

    # Third, determine which reorganisation jobs have completed.
    did_main_preopt_complete                                                      = get_string_result(did_main_preopt_finish)
    main_preopt_converged_image_index, total_no_of_images_made_during_main_preopt = get_opt_converged_string_result(main_preopt_converged_image_index, total_no_of_images_made_during_main_preopt)
    did_main_opt_complete                                                         = get_string_result(did_main_opt_finish)
    main_opt_converged_image_index, total_no_of_images_made_during_main_opt       = get_opt_converged_string_result(main_opt_converged_image_index, total_no_of_images_made_during_main_opt)
    did_freq_complete                                                             = get_freq_string_result(did_freq_finish, is_freq_force_convergence_good)
    no_of_negative_frequencies                                                    = str(no_of_negative_frequencies) if (no_of_negative_frequencies is not None) else 'X'
    did_sp_calc_complete                                                          = get_string_result(did_sp_finish)

    # Fourth, write the toString
    tostring = ''
    tostring += 'P'+str(did_main_preopt_complete)+'('
    if has_main_preopt_fully_converged:
        tostring += 'Full Conv'
    else:
        tostring += str(main_preopt_converged_image_index)+'/'+str(total_no_of_images_made_during_main_preopt)
    tostring += ')|'
    tostring += 'M'+str(did_main_opt_complete)+'('
    if has_main_opt_fully_converged:
        tostring += 'Full Conv'
    else:
        tostring += str(main_opt_converged_image_index)+'/'+str(total_no_of_images_made_during_main_opt)
    tostring += ')|F'+str(did_freq_complete)+'('+str(no_of_negative_frequencies)+')|S'+str(did_sp_calc_complete)

    # Fifth, return the toString
    return tostring

def get_string_result(did_finish):
    if did_finish is None:
        return '-'
    elif did_finish:
        return 'Y'
    else:
        return 'N'

def get_opt_converged_string_result(main_opt_converged_image_index, total_no_of_images_made_during_main_opt):
    max_string_bit_no = 4
    # Get max no of images string
    if total_no_of_images_made_during_main_opt is None:
        total_no_of_images_made_during_main_opt_string = ' '*(max_string_bit_no-len('X'))+'X'
    else:
        extra_string = ' '*(max_string_bit_no-len(str(total_no_of_images_made_during_main_opt)))
        total_no_of_images_made_during_main_opt_string = extra_string+str(total_no_of_images_made_during_main_opt)

    # get converged string
    if total_no_of_images_made_during_main_opt is None:
        main_opt_converged_image_index_string = ' '*(max_string_bit_no-len('X'))+'X'
    elif main_opt_converged_image_index is None:
        main_opt_converged_image_index_string = ' '*(max_string_bit_no-len('X'))+'X'
    else:
        main_opt_converged_image_index_string = total_no_of_images_made_during_main_opt + main_opt_converged_image_index + 1
        extra_string = ' '*(max_string_bit_no-len(str(main_opt_converged_image_index_string)))
        main_opt_converged_image_index_string = extra_string+str(main_opt_converged_image_index_string)

    # return strings
    return main_opt_converged_image_index_string, total_no_of_images_made_during_main_opt_string

def get_freq_string_result(did_freq_finish, is_freq_force_convergence_good):
    if did_freq_finish is None:
        return '-'
    elif did_freq_finish and is_freq_force_convergence_good:
        return 'Y'
    elif did_freq_finish and not is_freq_force_convergence_good:
        return 'C'
    elif not did_freq_finish and is_freq_force_convergence_good:
        raise Exception('huh?')
    else:
        return 'N'

def separate_list_based_on_neg_freqs(re_jobs_finished_unsuccessfully):
    """
    This method will separate lists based on if negative frequencies were obtained or not.

    Parameters
    ----------
    re_jobs_finished_unsuccessfully 
    """

    # First, create the list for jobs that had and had no negative frequencies.
    re_jobs_finished_unsuccessfully_no_neg_freq = []
    re_jobs_finished_unsuccessfully_neg_freq    = []

    # Second, go through each entry in re_jobs_finished_unsuccessfully and separate into jobs that had and had no negative frequencies.
    for dirpath, re_details in re_jobs_finished_unsuccessfully:

        # 2.1: Obtain the data from the re_details list.
        calculation_type, did_main_preopt_finish, has_main_preopt_fully_converged, main_preopt_converged_image_index, total_no_of_images_made_during_main_preopt, did_main_opt_finish, has_main_opt_fully_converged, main_opt_converged_image_index, total_no_of_images_made_during_main_opt, did_freq_finish, is_freq_force_convergence_good, no_of_negative_frequencies, did_sp_finish = re_details

        # 2.2: Move job into those that had and had no negative frequencies.
        if   (no_of_negative_frequencies is None) or (no_of_negative_frequencies == 0):
            re_jobs_finished_unsuccessfully_no_neg_freq.append((dirpath, re_details))
        elif no_of_negative_frequencies > 0:
            re_jobs_finished_unsuccessfully_neg_freq.append((dirpath, re_details))
        else:
            raise Exception('huh?')

    # Third, return the split lists.
    return re_jobs_finished_unsuccessfully_no_neg_freq, re_jobs_finished_unsuccessfully_neg_freq

# ========================================================================================================



