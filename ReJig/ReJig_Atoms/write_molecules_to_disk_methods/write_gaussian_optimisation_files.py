"""
write_gaussian_optimisation_files.py, Geoffrey Weal, 29/4/24

This script is designed to write the gaussian files and submit.sl files required for performing Gaussian jobs for relaxing added or modified atoms in a molecule in your crystal. 
"""
from copy                                                                              import deepcopy
from SUMELF                                                                            import make_folder
from SUMELF                                                                            import check_molecule_against_file
from SUMELF                                                                            import add_graph_to_ASE_Atoms_object
from ReJig.ReJig_Atoms.write_molecules_to_disk_methods.write_methods.gaussian_modified import write_gaussian_in
from ReJig.ReJig_Atoms.write_molecules_to_disk_methods.write_methods.shared_methods    import change_folder_name_components
from ReJig.ReJig_Atoms.write_molecules_to_disk_methods.write_methods.shared_methods    import slurmSL_header, load_gaussian_programs, make_gaussian_temp_folder, remove_gaussian_temp_files

def write_gaussian_optimisation_files(molecule, molecule_graph, molecule_name, gaussian_jobs_path, calc_parameters, submission_information):
	"""
	This method will write information the Gaussian files to disk.

	Parameters
	----------
	molecule : ase.Atoms.
		This is the molecule. 
	molecule_graph : networkx.Graph
		This is the graph for the associated molecule. 
	molecule_name : str.
		This is the name of the molecule. 
	gaussian_jobs_path : str.
		This is the path to save gaussian jobs to.
	calc_parameters : list
		This dictionary contain all the information required for the Gaussian input RE file.
	submission_information : list
		This dictionary contain all the information required for the submit.sl script. 
	"""

	# First, make a copy of the gaussian_parameters and submission_information dictionaries.
	gaussian_parameters    = deepcopy(calc_parameters)
	submission_information = deepcopy(submission_information)
	del gaussian_parameters['calc_software']

	# Second, determine if some critical tags that are needed are in the submission_information dictionary. 
	got_cpu = 'cpus_per_task' in submission_information
	got_mem = 'mem' in submission_information
	got_time = 'time' in submission_information
	if not (got_cpu and got_time):
		print('Error: You need to specify the following in your submission_information dictionary:')
		if not got_cpu:
			print('\t* cpus_per_task')
		if not got_mem:
			print('\t* mem')
		if not got_time:
			print('\t* time')
		print('See https://github.com/geoffreyweal/ReJig/ for more information about these tags.')
		print('submission_information = '+str(submission_information))
		exit('This program will finish without completing.')

	# Third, copy some tag information that is in the submission_information dictionary to the gaussian_parameters dictionary.
	gaussian_parameters['nprocshared'] = submission_information['cpus_per_task']

	# Fourth, give the name of the folder to place gaussian files to.
	functional = change_folder_name_components(gaussian_parameters['method'])
	basis_set = change_folder_name_components(gaussian_parameters['basis'])
	funct_and_basis_name = 'F_'+functional+'_B_'+basis_set
	gaussian_folder = str(gaussian_jobs_path)+'/'+str(molecule_name)+'/'+str(funct_and_basis_name)

	# Fifth, make the folder to save the gif and slurm submit files.
	make_folder(gaussian_folder)

	# =============================================================================
	# Sixth, for those temporary files that I have control over where they get saved to, 
	# indicate to the .gjf file where to save those files.

	# 6.1, provide the name and filepath for each of the scratch files.
	scratch_dir_given = ('temp_folder_path' in gaussian_parameters) # was gaussian_scratch_name
	if scratch_dir_given:
		temp_folder_path = gaussian_parameters['temp_folder_path']+'/'+gaussian_folder
		del gaussian_parameters['temp_folder_path']
		submission_information['temp_folder_path'] = temp_folder_path

	# 6.2: Make the checkpoint file.
	gaussian_parameters['chk'] = 'gaussian.chk'

	# 6.3: Make path folder and file details for the other gaussian checkpoint files.
	for suffix in ['rwf','int','d2e','skr']:
		if scratch_dir_given: # A scratch path is given.
			gaussian_parameters[suffix] = temp_folder_path+'/'+'gaussian.'+str(suffix)
		else: # A scratch path has not been given.
			# Default name given called gaussian.suffix, whether scratch_dir_given is True or False
			gaussian_parameters[suffix] = 'gaussian.'+str(suffix)

	# =============================================================================

	# Seventh, write the name of the gjf files to make
	ground_structure_GS_DFT_main_opt  = 'rejig_opt.gjf'

	# Eighth, get the full path to to the gif file.
	full_path_to_gjf_file = gaussian_folder +'/'+ground_structure_GS_DFT_main_opt

	# =============================================================================

	# Ninth, add the graph details of the molecule back from the graph to the molecule. 
	# Some of these are useful for the gjf file, including multiplicity.
	add_graph_to_ASE_Atoms_object(molecule, molecule_graph)

	# =============================================================================

	# Tenth, create the gaussian .gjf file for optimising the ground and excited structures.
	with open(full_path_to_gjf_file, 'w') as fd:	
		write_gaussian_in(fd, molecule.copy(), perform_opt=True, perform_CalcAll=False, perform_TD=False, perform_freq=False, perform_raman=False, perform_density=False, perform_pop=False, read_chk_file=False, molecule_name=molecule_name, **gaussian_parameters)

	# Eleventh, create the submit script for submitting jobs to slurm.
	make_gaussian_submitSL(ground_structure_GS_DFT_main_opt, gaussian_folder, functional, basis_set, gaussian_parameters, **submission_information)

# ------------------------------------------------------------------------------------------------------------------------------

def make_gaussian_submitSL(optimisation_filename_DFT_main_opt, local_path, functional, basis_set, gaussian_parameters, cpus_per_task, mem, time, partition='parallel', constraint=None, nodelist=None, exclude=None, email='', gaussian_version='gaussian/g16', temp_folder_path=None):
	"""
	This method will write the submit.sl file in parallel

	Parameters
	----------
	optimisation_filename_DFT_main_opt : str. 
		This is the name of the optimisation file for performing the main optimisation process with DFT
	local_path : str. 
		This is the location to save this submit.sl file to
	perform_excited_state_calc : bool.
		This boolean indicates if you are performing a excited state optimisation.
	functional : str. 
		This is the functional you are going to use in your Gaussian calculation.
	basis_set : str. 
		This is the basis set you are going to use in your Gaussian calculation.
	gaussian_parameters : dict.
		This dictionary contains all the input parameters required for creating the gaussian input (.gjf) file.
	cpus_per_task : int
		This is the number of cpus you want to use for Gaussian jobs.
	mem : str.
		This is the amount of memory you want to use for Gaussian jobs.
	time : str.
		This is the amount of time you want to use for Gaussian jobs.
	partition : str.
		This is the partition to run this job on. Default: 'parallel'
	constraint : str.
		This is the slurm constraint. If you dont give this, this wont be set. Default: None
	nodelist : str.
		This is the slurm nodelist. If you dont give this, this wont be set. Default: None
	exclude : str.
		This is the slurm exclude nodes list. If you dont give this, this wont be set. Default: None
	email : str.
		This is the email to email about how this job is going. If you dont give this, this wont be set. Default: ''
	gaussian_version : str.
		This is the version of Gaussian you want to load/use in slurm. Default: 'gaussian/g16'
	temp_folder_path : str. or None
		This is the path to the scratch directory to save Gaussian temp files to. If you dont give this, Gaussian temp files will be saves to the default scratch directory. Default: None
	"""

	# Get version of Gaussian to use
	gaussian_version_suffix = str(gaussian_version.split('/')[-1])

	# Make changes to gaussian_parameters to change gaussian filenames to include "main_opt" in their name.
	gaussian_parameters_main_opt = deepcopy(gaussian_parameters)
	for gaussian_file in ['chk', 'd2e', 'int', 'rwf', 'skr']:
		if gaussian_file in gaussian_parameters_main_opt:
			gaussian_filename = gaussian_parameters_main_opt[gaussian_file]
			gaussian_filename = gaussian_filename.split('.')
			gaussian_filename = gaussian_filename[0]+'.'+gaussian_filename[1]
			gaussian_parameters_main_opt[gaussian_file] = gaussian_filename

	# Create names for job.
	optimisation_name_DFT_main_opt   = optimisation_filename_DFT_main_opt.replace('.gjf','')
	name = 'ReJig' + '-' + '-'.join(local_path.split('/')[-4:-1])

	# Writing the submit.sl script
	with open(local_path+'/submit.sl', "w") as submitSL:
		slurmSL_header(submitSL, name, mem, partition, constraint, nodelist, time, email, cpus_per_task=cpus_per_task, exclude=exclude)
		make_gaussian_temp_folder(submitSL, temp_folder_path)
		load_gaussian_programs(submitSL, gaussian_version)

		submitSL.write('# ================================\n')
		submitSL.write('# Prevent the optimisation job from running if it is already running or has already run.\n')
		submitSL.write('\n')
		submitSL.write('if ! [[ -f '+str(optimisation_name_DFT_main_opt)+'.log'+' ]]\n')
		submitSL.write('then\n')

		# Perform the proper DFT optimisation

		submitSL.write('\t# ============================\n')
		submitSL.write('\t# Perform the main geometry optimisation calculation with the desired functional and basis set.\n')
		submitSL.write('\t\n')
		submitSL.write('\techo "Performing main optimisation calculation"\n')
		submitSL.write('\tsrun '+gaussian_version_suffix+' < '+str(optimisation_filename_DFT_main_opt)+' > '+str(optimisation_name_DFT_main_opt)+'.log\n')
		submitSL.write('\techo "Finished main optimisation calculation"\n')
		submitSL.write('\t\n')
		submitSL.write('\t# ============================\n')

		# Perform final tasks and submit for frequency and single point analysis

		remove_gaussian_temp_files(submitSL, gaussian_parameters_main_opt, temp_folder_path, remove_chk_file=True, remove_temp_folder=True, prefix='\t')
		submitSL.write('\t# ----------------------------\n')
		submitSL.write('\techo "End of job"\n')
		submitSL.write('\t# ----------------------------\n')

		submitSL.write('fi\n')
		submitSL.write('# ================================\n')

# ------------------------------------------------------------------------------------------------------------------------------
