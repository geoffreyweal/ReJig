"""
Run_ReJig.py, Geoffrey Weal, 1/5/24

This script will allow you to run the ReJig Crystals (ReJig) program upon the crystals of interest. 

The ReJig program will allow the user to use Gaussian or ORCA to geometrically optimise those atoms in the crystals 
of interest that have either been added to the crystal or the position of the atom has been modified in the crystal. 

"""
import os, shutil
from ReJig import ReJig_Atoms

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PART I: Get the names of the folders holding the crystals you want to remove sidegroups from

# First, give the name of the folder that contains the crystal database you want to remove sidegroups from here. 
crystal_database_dirname = 'crystals_with_sidechains_removed'

# Second, this dictionary will add tags to your Gaussian .gjf file for performing a ground state geometric optimisation jobs.
calc_parameters = {'calc_software': 'Gaussian'}
calc_parameters['mem']                          = '64GB'
calc_parameters['method']                       = 'wB97XD'
calc_parameters['basis']                        = '6-31+G(d,p)'
calc_parameters['temp_folder_path']             = '/tmp/wealge'
calc_parameters['extra']                        = '# maxdisk=2TB scf=(xqc,maxcycle=512)'

# Third, this tag indicates if you want to obtain Gaussian input files of molecules for performing geometric optimisation jobs. 
submission_information = {}
submission_information['cpus_per_task'] = 16
submission_information['mem']           = '68GB'
submission_information['time']          = '03-00:00'
submission_information['partition']     = 'parallel'
submission_information['constraint']    = 'AVX'
submission_information['email']         = 'geoffreywealslurmnotifications@gmail.com'

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Part II: Check that the folders of the databases exist.

# Fourth, check that the crystal database you gave exists. 
if not os.path.exists(crystal_database_dirname):
	raise Exception(f'Error: {crystal_database_dirname} does not exist in {os.getcwd()}')

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Part III: Get the paths to the crystals you want to rejig. 

# Fifth, get the names of the files contained in the crystal database folder.
crystal_database_filenames = sorted(os.listdir(crystal_database_dirname))

# Sixth, initalise the list to hold all the paths to the crystals to remove sidegroups from.
filepath_names = []

# Seventh, obtain all the paths to the crystals you want to rejig. 
for crystal_database_filename in crystal_database_filenames:

	# 7.1: Make sure that the file ends with ".xyz".
	if not crystal_database_filename.endswith('.xyz'):
		continue

	# 7.2: Add the path to the crystal file to the filepath_names list.
	filepath_names.append(crystal_database_dirname+'/'+crystal_database_filename)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PART IV: Reset ReJig files from previous ReJig runs.

# Eighth, remove the folder that we will place crystals in that we will remove sidegroups from.
crystal_database_with_removed_sidegroups_folder_name = f'rejigged_{crystal_database_dirname}'
if os.path.exists(crystal_database_with_removed_sidegroups_folder_name):
	shutil.rmtree(crystal_database_with_removed_sidegroups_folder_name)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PART V: Run the ReJig program on the crystals you want to rejig.

# Ninth, obtain the total number of crystal you want to process with the RSGC program. 
total_no_of_crystals = str(len(filepath_names))

# Tenth, initialise a counter to record the number of crystals that you want to rejig. 
rejig_counter = 0

# Eleventh: For each crystal in the filepath_names list. 
for counter, filepath in enumerate(filepath_names, start=0):

	# 11.1: Print to screen how many crystals have been processed by the RSGC program. 
	print('Running crystal: '+str(counter)+' out of '+total_no_of_crystals)

	# 11.2: Run the ReJig program. 
	did_make_rejig_files = ReJig_Atoms(filepath, calc_parameters=calc_parameters, submission_information=submission_information)

	# 11.3: Count if the crystal (given by filepath) has been rejigged. 
	if did_make_rejig_files:
		rejig_counter += 1

# Twelfth, print the num 
print(f'Number of crystals to rejig: {rejig_counter}')

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -