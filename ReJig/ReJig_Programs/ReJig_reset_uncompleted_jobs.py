'''
Geoffrey Weal, ReJig_reset_uncompleted_jobs.py, 30/4/24

This program is designed to reset jobs that did not complete.
'''
import os, shutil
from tqdm import tqdm
from ase.io import read, write

from ReJig.ReJig_Programs.shared_general_methods.shared_gaussian_methods import did_gaussian_job_complete, did_gaussian_opt_job_complete
from ReJig.ReJig_Programs.shared_general_methods.shared_gaussian_methods import gaussian_temp_files_to_remove
from ReJig.ReJig_Programs.shared_general_methods.shared_gaussian_methods import remove_slurm_output_files
from ReJig.ReJig_Programs.shared_general_methods.shared_gaussian_methods import found_a_gaussian_job_that_has_run

class CLICommand:
    """Will reset jobs that did not complete. Only run this program if you know all your other jobs have finished, as this program will break and also reset any jobs that are still running.
    """

    @staticmethod
    def add_arguments(parser):
        pass

    @staticmethod
    def run(args):
        Run_method()

def Run_method():
    """
    This method will reset jobs that did not complete. 

    Only run this program if you know all your other jobs have finished, as this program will break and also reset any jobs that are still running.
    """

    # First, ask the user if any jobs are running, as this program will not know if jobs are running still or ended without completing. 
    print('----------------------------------------------')
    print('This program will reset all ReJig jobs that did not complete')
    print()
    print('IMPORTANT: This program can not recognise if a Gaussian/ORCA job is still running')
    print('ONLY USE THIS PROGRAM IF YOU ARE NOT CURRENTLY RUNNING ANY REJIG GAUSSIAN/ORCA JOBS')
    print()
    while True:
        value = input("Are you happy to continue (y/[n]): ")
        if (value is None) or (value == ''):
            value = 'no'
        if   (value.lower() == 'n') or (value.lower() == 'no'):
            exit('Will exit this program without resetting.'+'\n'+'----------------------------------------------')
        elif (value.lower() == 'y') or (value.lower() == 'yes'):
            print('Will proceed to resetting uncomplete ReJig Gaussian/ORCA jobs.')
            break
        else:
            print('Input must be either:')
            print('\tN/n/NO/No/no: Do not perform resetting.')
            print('\tY/y/YES/Yes/yes: Do not perform resetting.')
            print('Try again.')
            print()
    print('----------------------------------------------')

    # Second, setup all the initial variables.
    current_path = os.getcwd()
    print('----------------------------------------------')
    print('Resetting uncompleted jobs from the root path: '+str(current_path))
    print('----------------------------------------------')

    # Third, go through each subdirectory in the parent directory. 
    original_path = os.getcwd()
    pbar = tqdm(os.walk(current_path), bar_format='')
    jobs_that_have_been_reset = []
    for root, dirs, files in pbar:

        # 3.1: Write description to progress bar.
        pbar.set_description('Reset: '+str(len(jobs_that_have_been_reset))+'; Currently in: '+str(root.replace(original_path+'/','')))

        # 3.2: Sort the directory just to make tidying happen in alphabetical order.
        dirs.sort()

        # 3.3: Determine if any Gaussian files exists in the current file under investigation. 
        if found_a_gaussian_job_that_has_run(root, files):

            # 3.3.1: Determine if the Gaussian log file exists.
            if os.path.exists(root+'/rejig_opt.log'):

                # 3.3.2: If the output.log file shows that the program finished successfully, remove all temp files. 
                if not did_gaussian_opt_job_complete(root+'/rejig_opt.log')[0]:
                    
                    # 3.3.3: Update the gjf file with the last complete image in rejig_opt.log
                    gjf_was_updated = update_gif_file_from_previous_outputLOG(root, 'rejig_opt.log', 'rejig_opt.gjf')
                    rename_gaussian_output_file(root, output_name='rejig_opt.log', gjf_was_updated=gjf_was_updated)
                    #remove_gaussian_file(root, output_name='rejig_opt.log')

                    # 3.3.4: Remove temp files as well as any results files like slurm files. 
                    remove_slurm_output_files(root)
                    jobs_that_have_been_reset.append((root, 'rejig_opt'))

                # 3.3.5: Clean up the temp files while we are at it for any ReJig calcs, completed or uncompleted.
                gaussian_temp_files_to_remove(root, files, remove_chk_file=True, remove_fort7_file=True, print_to_display=False)

            # 3.3.6: Do not need to move further down the subdirectories anymore, remove all dirs and files lists.
            dirs[:]  = []
            files[:] = []

        # 3.4: Updated the progress bar.
        pbar.set_description('Reset: '+str(len(jobs_that_have_been_reset))+'; Currently in: '+str(root.replace(original_path+'/','')))

    # Fourth, print out which jobs have finished. 
    print('----------------------------------------------')
    if len(jobs_that_have_been_reset) == 0:
        print('No Jobs were reset')
    else:
        print('The following jobs were reset:')
        print()
        for job, log_name in jobs_that_have_been_reset:
            print(str(job)+': '+str(log_name))
    print('----------------------------------------------')

# --------------------------------------------------------------------------------------------------

old_suffix = 'old'
def update_gif_file_from_previous_outputLOG(root, output_name, previous_gjf_name):
    """
    This method will update the gif file will the previous self-consistancy field completed geometric step.

    Parameters
    ----------
    root : str
        This is the path to the gaussian output file.
    output_name : str.
        This is the name of the output file.
    previous_gjf_name str.
        This is the name of the gjf file that produced the output file given by output_name.

    Returns
    -------
    Return True if this method updated the gjf file, False if not.
    """
    
    # First, obtain the structure of the previously completed gemoetry step.
    try:
        previously_completed_geometric_step = read(root+'/'+output_name,index=-1)
    except:
        print('Log file does not contain a starting configuration.')
        print('This is likely because Gaussian had only just begun for a few secnods before being cancelled.')
        print('The gjf file will not need to be updated.')
        return False

    # Second, obtain the initial lines of the gif file or the previous gaussian job.
    gjf_input_lines_start = []
    gjf_input_lines_end   = []
    old_checkpoint_filename = None
    checkpoint_filename = None
    with open(root+'/'+previous_gjf_name,'r') as previousGJF:
        atomic_positions_number_of_blank_lines = 2
        no_of_blank_lines = 0
        found_second_blank_line_first_line = True
        for line in previousGJF:
            line = line.rstrip()
            # Read if there is already a line to read input from the checkpoint.
            if ('# Geom=Check Guess=Read' in line) or ('# Geom=Check Guess=TCheck' in line): 
                line = '# Geom=Check Guess=TCheck ! Will read in the geometry and electronic details from the checkpoint file'
            # Record lines from gjf about how to run the gaussian job (link0).
            if   no_of_blank_lines < atomic_positions_number_of_blank_lines:
                gjf_input_lines_start.append(line)
            elif no_of_blank_lines > atomic_positions_number_of_blank_lines:
                gjf_input_lines_end.append(line)
            elif found_second_blank_line_first_line:
                gjf_input_lines_start.append(line)
                found_second_blank_line_first_line = False
            # Determine where the breaks between the link0, title, and atom positions lines are.
            if (line == "") or line.isspace():
                no_of_blank_lines += 1

    # Third, rename the previous gjf file as a old file.
    # 3.1: Get all the names of the previous gjf files.
    previous_gjf_names = []
    for file in os.listdir(root):
        if os.path.isfile(root+'/'+file) and file.startswith(previous_gjf_name) and (not file == previous_gjf_name):
            if 'original' in file:
                continue
            previous_gjf_names.append(file)

    # 3.2: Check that there is a consecutive order of numbering in previous_gjf_names
    previous_gjf_old_numbers = sorted([int(x.replace(previous_gjf_name+'.'+old_suffix,'')) for x in previous_gjf_names])
    if not (previous_gjf_old_numbers == list(range(1,len(previous_gjf_old_numbers)+1))):
        raise Exception('huh?')

    # 3.3: Rename gif file to next old file
    os.rename(root+'/'+previous_gjf_name, root+'/'+previous_gjf_name+'.'+old_suffix+str(len(previous_gjf_old_numbers)+1))

    # Fourth, create the new gjf file with updated geometric structure.
    with open(root+'/'+previous_gjf_name,'w') as currentGJF: 
        currentGJF.write('\n'.join(gjf_input_lines_start)+'\n')
        for atom in previously_completed_geometric_step:
            currentGJF.write(str(atom.symbol)+'\t'+str(atom.x)+'\t'+str(atom.y)+'\t'+str(atom.z)+'\n')
        currentGJF.write('\n'+'\n'.join(gjf_input_lines_end)+'\n\n')

    # Fifth, return True, as this method has updated the gjf file
    return True

# --------------------------------------------------------------------------------------------------

def rename_gaussian_output_file(root, output_name='output.log', gjf_was_updated=True):
    """
    This method will remove all files that were created during the Gaussian calculation run by the slurm job.

    Parameters
    ----------
    root : str
        This is the path to the gaussian output file.
    output_name : str.
        This is the name of the output file 
    """

    if not gjf_was_updated:
        os.remove(root+'/'+output_name)
        return 
        '''
        if '.' in output_name:
            output_name = output_name.split('.')
            output_name.insert(-1,'nogeometryupdate')
            output_name = '.'.join(output_name)
        else:
            output_name+'.'+'nogeometryupdate'
        '''

    if output_name in os.listdir(root):

        # 3.1: Get all the names of the previous log files.
        previous_log_names = []
        for file in os.listdir(root):
            if os.path.isfile(root+'/'+file) and file.startswith(output_name) and (not file == output_name):
                previous_log_names.append(file)

        # 3.2: Check that there is a consecutive order of numbering in previous_log_names
        previous_log_old_numbers = sorted([int(x.replace(output_name+'.'+old_suffix,'')) for x in previous_log_names])
        if not (previous_log_old_numbers == list(range(1,len(previous_log_old_numbers)+1))):
            raise Exception('huh?')

        # 3.3: Rename log file to next old file
        os.rename(root+'/'+output_name, root+'/'+output_name+'.'+old_suffix+str(len(previous_log_old_numbers)+1))

def remove_gaussian_file(root, output_name='output.log'):
    """
    This method will remove all files that were created during the Gaussian calculation run by the slurm job.

    Parameters
    ----------
    root : str
        This is the path to the gaussian output file.
    output_name : str.
        This is the name of the output file 
    """
    if output_name in os.listdir(root):
        os.remove(root+'/'+output_name)

# --------------------------------------------------------------------------------------------------



