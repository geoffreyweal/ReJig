'''
Geoffrey Weal, Run_Adsorber_submitSL_slurm.py, 16/06/2021

This program is designed to submit all sl files called submit.sl to slurm.
'''
import os
from subprocess import Popen, PIPE, TimeoutExpired

from ReJig.ReJig_Programs.ReJig_submit_jobs_to_slurm_settings_methods.settings_methods                     import check_submit_settingsTXT, read_submit_settingsTXT_file
from ReJig.ReJig_Programs.ReJig_submit_jobs_to_slurm_methods.determine_quantum_computing_software_type     import determine_quantum_computing_software_type
from ReJig.ReJig_Programs.ReJig_submit_jobs_to_slurm_methods.ReJig_submit_gaussian_jobs_to_slurm           import general_gaussian_submission
#from ReJig.ReJig_Programs.ReJig_submit_jobs_to_slurm_methods.ReJig_submit_orca_jobs_to_slurm               import general_orca_submission
from ReJig.ReJig_Programs.ReJig_submit_jobs_to_slurm_methods.check_max_jobs_in_queue_after_next_submission import check_max_jobs_in_queue_after_next_submission
from ReJig.ReJig_Programs.ReJig_submit_jobs_to_slurm_methods.countdown                                     import countdown
from ReJig.ReJig_Programs.ReJig_submit_jobs_to_slurm_methods.wait_for_pending_slurm_job_queue_decrease     import wait_for_pending_slurm_job_queue_decrease

# Get the path to the settings script.
this_scripts_path = os.path.dirname(os.path.abspath(__file__))
submit_settings_name = 'ReJig_submit_jobs_to_slurm_settings_methods/submit_settings.txt'
path_to_settings_txt_file = this_scripts_path+'/'+submit_settings_name

class CLICommand:
    """Submit ReJig geometric optimisation jobs to slurm.
    """

    @staticmethod
    def add_arguments(parser):
        pass

    @staticmethod
    def run(args_submit):

        # First, use this method to create a settings.txt file if it doesn't already exist, and check that the current settings.txt file can be read without problems.
        check_submit_settingsTXT(path_to_settings_txt_file)

        # Second, run this program.
        Run_method()

# =========================================================================================================================================

def Run_method():
    '''
    This program is designed to submit all sl files called submit.sl to slurm.
    '''

    print('##################################################')
    print('Will submit your ReJig submit.sl scripts to slurm.')
    print('##################################################')

    # Second, read the settings from the settings file. 
    Max_jobs_in_queue_at_any_one_time, Max_jobs_pending_in_queue_from_ReJig_mass_submit, Max_jobs_running_in_queue_from_ReJig_mass_submit, time_to_wait_before_next_submission, time_to_wait_max_queue, time_to_wait_before_next_submission_due_to_temp_submission_issue, number_of_consecutive_error_before_exitting, time_to_wait_before_next_submission_due_to_not_waiting_between_submissions = read_submit_settingsTXT_file(path_to_settings_txt_file)
    wait_between_submissions = False

    # Third, indicate if there will be a small wait between jobs.
    if wait_between_submissions == True:
        print('This program will wait one minute between submitting jobs.')
    else:
        print('This program will not wait between submitting jobs.')
    print('Will begin to search for submit.sl and other .sl files.')
    print('***************************************************************************')

    # Fourth, time to submit all the GA scripts! Lets get this stuff going!
    if not wait_between_submissions:
        max_consec_counter = 250
        consec_counter = 0
    errors_list = []
    error_counter = 0
    path = os.getcwd()
    for (dirpath, dirnames, filenames) in os.walk(path):
        dirnames.sort()
        filenames.sort()

        # 4.1: Determine if the following submit scripts are in this folder
        is_submitSL_in_filenames = 'submit.sl' in filenames

        # 4.2: If there is a submit file to submit, submit it.        
        if any([is_submitSL_in_filenames]):
            
            # 4.2.1, determine what calculations we are looking at.
            software_type = determine_quantum_computing_software_type(dirpath, filenames)

            # 4.2.2: Figure out which submit files in the folder should be submitted to slurm.
            submission_filenames = []
            if is_submitSL_in_filenames:
                # Submitting either ATC or EET calculation.
                if software_type == 'Gaussian':
                    submission_filenames += general_gaussian_submission(filenames)
                elif software_type == 'ORCA':
                    submission_filenames += general_orca_submission(filenames)
                else:
                    raise Exception('ERROR: Could not determine what software will be used in this submission file.')

            # 4.2.3: If we do not have jobs to submit to slurm, move on. 
            if len(submission_filenames) == 0:
                dirnames[:] = []
                filenames[:] = []
                continue

            # ====================================================================================================
            # 4.4: Submit the jobs to slurm
            for submission_filename in submission_filenames:

                # ----------------------------------------------------------------
                # 4.4.1: Determine if it is the right time to submit jobs
                print('*****************************************************************************')
                while True:
                    reached_max_jobs, number_in_queue = check_max_jobs_in_queue_after_next_submission(dirpath, Max_jobs_in_queue_at_any_one_time)
                    if reached_max_jobs:
                        print('-----------------------------------------------------------------------------')
                        print('You can not have any more jobs in the queue before submitting the mass_sub. Will wait a bit of time for some of them to complete')
                        print('Number of Jobs in the queue = '+str(number_in_queue))
                        countdown(time_to_wait_before_next_submission)
                        print('-----------------------------------------------------------------------------')
                    else:
                        print('The number of jobs in the queue currently is: '+str(number_in_queue))
                        break
                
                # 4.4.2: Submit the jobs
                os.chdir(dirpath)
                name = dirpath.replace(path, '').split('/', -1)[1:]
                name = "_".join(str(x) for x in name)
                print("Submitting " + str(name) + " to slurm.")
                print('Submission .sl file found in: '+str(os.getcwd()))
                print('Submission filename: '+str(submission_filename))
                error_counter = 0
                while True:
                    if error_counter == number_of_consecutive_error_before_exitting:
                        break
                    else:
                        submitting_command = ['sbatch', str(submission_filename)]
                        proc = Popen(submitting_command, stdout=PIPE, stderr=PIPE) # shell=True, 
                        try:
                            if not (proc.wait(timeout=(2*60)) == 0): # 120 seconds
                                # A problem occurred during the submission. Report this and wait a bit before trying again.
                                error_counter += 1
                                if error_counter == number_of_consecutive_error_before_exitting:
                                    print('----------------------------------------------')
                                    print('Error in submitting submit script to slurm.')
                                    print('I got '+str(number_of_consecutive_error_before_exitting)+" consecutive errors. Something must not be working right somewhere. I'm going to stop here just in case something is not working.")
                                    print('')
                                    print('The following submit.sl scripts WERE NOT SUBMITTED TO SLURM')
                                    print('')
                                else:
                                    stdout, stderr = proc.communicate()
                                    print('----------------------------------------------')
                                    print('Error in submitting submit script to slurm. This error was:')
                                    print(stderr)
                                    print('Number of consecutive errors: '+str(error_counter))
                                    print('Run_submitSL_slurm.py will retry submitting this job to slurm after '+str(time_to_wait_before_next_submission_due_to_temp_submission_issue)+' seconds of wait time')
                                    print('----------------------------------------------')
                                    countdown(time_to_wait_before_next_submission_due_to_temp_submission_issue)
                            else:
                                # Submission successful, report this and move on.
                                stdout, stderr = proc.communicate()
                                job_number = int(stdout.decode("utf-8").replace('Submitted batch job',''))
                                print("Submitted " + str(name) + " to slurm: "+str(job_number))
                                # Wait until the running and pending queue for this program is available to move on.
                                wait_for_pending_slurm_job_queue_decrease(job_number, Max_jobs_pending_in_queue_from_ReJig_mass_submit, Max_jobs_running_in_queue_from_ReJig_mass_submit)
                                break
                        except TimeoutExpired:
                            # A problem occurred during the submission, sbatch timedout. Report this and wait a bit before trying again.
                            proc.kill()
                            error_counter += 1
                            if error_counter == number_of_consecutive_error_before_exitting:
                                print('----------------------------------------------')
                                print('Error in submitting submit script to slurm. Job timed-out after 2 minutes.')
                                print('I got '+str(number_of_consecutive_error_before_exitting)+" consecutive errors. Something must not be working right somewhere. I'm going to stop here just in case something is not working.")
                                print('')
                                print('The following submit.sl scripts WERE NOT SUBMITTED TO SLURM')
                                print('')
                            else:
                                print('----------------------------------------------')
                                print('Error in submitting submit script to slurm. Job timed-out after 2 minutes.')
                                print('Number of consecutive errors: '+str(error_counter))
                                print('Run_submitSL_slurm.py will retry submitting this job to slurm after '+str(time_to_wait_before_next_submission_due_to_temp_submission_issue)+' seconds of wait time')
                                print('----------------------------------------------')
                                countdown(time_to_wait_before_next_submission_due_to_temp_submission_issue)

                # 4.4.3: Check that there were any errors, and wait until it is possible to submit another job without going over the maximum limit for this user.
                if error_counter == number_of_consecutive_error_before_exitting:
                    print(dirpath)
                    errors_list.append(dirpath)
                else:
                    if wait_between_submissions:
                        reached_max_jobs, number_in_queue = check_max_jobs_in_queue_after_next_submission(dirpath)
                        print('The number of jobs in the queue after submitting job is currently is: '+str(number_in_queue))
                        #print('Will wait for '+str(time_to_wait_max_queue)+' to give time between consecutive submissions')
                        countdown(time_to_wait_max_queue)
                        print('*****************************************************************************')

                # 4.4.4: If you are waiting between 
                dirnames[:] = []
                filenames[:] = []
                if not wait_between_submissions:
                    if consec_counter >= max_consec_counter:
                        print('----------------------------------------------')
                        print('As you are not waiting between consecutive submissions, it is good practise to wait for a minute at some stage')
                        print(str(max_consec_counter) +' have been submitted consecutively. Will not wait for '+str(time_to_wait_before_next_submission_due_to_not_waiting_between_submissions)+' s before continuing')
                        print('----------------------------------------------')
                        countdown(time_to_wait_before_next_submission_due_to_not_waiting_between_submissions)
                        consec_counter = 0
                    else:
                        consec_counter += 1

            # ====================================================================================================
    # ============================================================================================================

    # Fifth, check out if there were any issues that meant that this program has to finish prematurally. 
    if len(errors_list) > 0:
        print('----------------------------------------------')
        print()
        print('"Run_submitSL_slurm.py" will finish WITHOUT HAVING SUBMITTED ALL JOBS.')
        print()
        print('*****************************************************************************')
        print('The following submit.sl SCRIPTS WERE NOT SUBMITTED SUCCESSFULLY.')
        print()
        for error_dirpath in errors_list:
            print(error_dirpath)
        print('*****************************************************************************') 
    else:
        print('*****************************************************************************')
        print('*****************************************************************************')
        print('*****************************************************************************')
        print('All submit.sl scripts have been submitted to slurm successfully.')
        print('*****************************************************************************')
        print('*****************************************************************************')
        print('*****************************************************************************')

# ------------------------------------------------------------------------------------------------
