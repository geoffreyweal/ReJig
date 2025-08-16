"""
Reconstruct.py, Geoffrey Weal, 30/4/24

This module is designed to reconstruct the crystal, where the geometrically relaxed molecules have replaced their non-relaxed counterparts in the crystal.
"""
import os, sys, shutil, traceback
from tqdm import tqdm
import numpy as np
from copy import deepcopy

from ase.io import read, write
from ase.visualize import view
from ase.constraints import FixAtoms

from SUMELF import read_crystal
from SUMELF import obtain_graph, process_crystal
from SUMELF import make_crystal
from SUMELF import remove_folder, make_folder
from SUMELF import add_graph_to_ASE_Atoms_object

from ReJig.Utilities.make_SolventsList      import make_SolventsList
from ReJig.Utilities.check_molecules        import check_molecules
from ReJig.Utilities.utilities              import get__added_or_modified__values
from ReJig.ReJig_Programs.Did_Complete_Main import Did_Complete_Main
from ReJig.Reconstruct.print_final_message  import print_final_message

class CLICommand:
	"""This module is designed to reconstruct the crystal, where the geometrically relaxed molecules have replaced their non-relaxed counterparts in the crystal.
	"""

	@staticmethod
	def add_arguments(parser):
		parser.add_argument('--ReJig_dirpath',        nargs=1, help='This is the folder containing the ReJig files.', default=['rejigged_crystals'])
		parser.add_argument('--process_all_crystals', nargs=1, help='This indicates if you want to process all crystal data, even for jobs that have not converged. Any jobs that have not begun will not be processed weither this tag is set to True or False.', default=['False'])

	@staticmethod
	def run(arguments):

		# First, obtain the folder containing the files of crystals that we have rejigged molecules in. 
		rejig_dirpath = arguments.ReJig_dirpath
		if len(rejig_dirpath) != 1:
			raise Exception('Error: ReJig_dirpath has more than one input')
		rejig_dirpath = rejig_dirpath[0]

		# Second, obtain the tag that indicates if you want to process any jobs that have not converged. 
		process_all_crystals = arguments.process_all_crystals
		if len(process_all_crystals) != 1:
			raise Exception('Error: ReJig_dirpath has more than one input')
		process_all_crystals = str(process_all_crystals[0]).lower()
		if   process_all_crystals in ['t', 'true']:
			process_all_crystals = True
		elif process_all_crystals in ['f', 'false']:
			process_all_crystals = False
		else:
			raise Exception('Error: The value for "--process_all_crystals" must be either "True" or "False".')

		# Third, run the reconstruct method
		Run_method(rejig_dirpath=rejig_dirpath, process_all_crystals=process_all_crystals)

def Run_method(rejig_dirpath='rejigged_crystals', process_all_crystals=False):
	"""
	This module is designed to reconstruct the crystal, where the geometrically relaxed molecules have replaced their non-relaxed counterparts in the crystal.

	Parameters
	----------
	rejig_folder : str.
		This is the folder that contains the crystals that have been rejigged using Gaussian/ORCA. 
	process_all_crystals : bool.
		This boolean indicates if you want to process all crystals, even if they have not converged yet. Any crystals that have not begun being processed by Gaussian/ORCA will not be processed if this tag is True or False. 
	"""

	# First, check that rejig_folder exists
	if not os.path.exists(rejig_dirpath):
		raise Exception(f'Error: Could not find {rejig_dirpath}')

	# Second, get the path to the folder to save reconstructed crystals to.
	save_reconstructed_crystals_dirpath = rejig_dirpath + '_reconstructed'

	# Third, get the path to the folder to save reconstructed crystals to.
	save_reconstructed_molecules_dirpath = rejig_dirpath + '_reconstructed_molecules'

	# Fourth, get the path to the folder containing all the trajectory files
	save_reconstructed_molecules_trajectory_dirpath = rejig_dirpath + '_reconstructed_molecules_trajectory'

	# Fifth, remove all previous runs of the ``ReJig reconstruct`` module.
	remove_folder(save_reconstructed_crystals_dirpath)
	remove_folder(save_reconstructed_molecules_dirpath)
	remove_folder(save_reconstructed_molecules_trajectory_dirpath)

	# Sixth, make the folder to save geoemtric optimisation trajcetory files to. 
	make_folder(save_reconstructed_molecules_trajectory_dirpath)

	# Seventh, initalise a list to store any crystals have have not been reconstructed yet
	#         * this is because molecules to be rejigged have not been geometrically optimised completely yet. 
	crystals_not_reconstructed_yet = []

	# Eighth, initialise a progress bar for reconstructing the crystals that have been rejigged. 
	pbar = tqdm(sorted(os.listdir(rejig_dirpath)), desc='Reconstructing Crystals', unit='crystal')

	# Ninth, for each crystal in the rejig_dirpath folder:
	for crystal_name in pbar:

		# Tenth, get the path into the crystal folder.
		dirpath = rejig_dirpath+'/'+crystal_name

		# Eleventh, check that that you are inspecting is a folder.
		if not os.path.isdir(dirpath):
			continue

		# Twelfth, get the filepath to the crystal to rejig.
		filepath = dirpath+'/'+crystal_name+'.xyz'

		# Thirteenth, get the name of the identifier for this crystal. 
		crystal_identifier = crystal_name.split()[0]

		# Fourteenth, write the crystal identifier to the progress bar. 
		pbar.set_description(str(crystal_identifier))

		# Fifteenth, load the ase.Atoms object of the crystal. 
		crystal = read_crystal(filepath)

		# Sixteenth, make sure that the periodic boundary condition setting for this crystal object is True. 
		crystal.set_pbc(True)

		# Seventeenth, get the graph of the crystal.
		crystal, crystal_graph = obtain_graph(crystal,name='crystal')

		# Eighteenth, get the molecules and the graphs associated with each molecule in the crystal.
		molecules, molecule_graphs, SolventsList, symmetry_operations, cell = process_crystal(crystal,crystal_graph=crystal_graph,take_shortest_distance=True,return_list=False,logger=None,print_progress=False)
		
		# Ninteenth, determine the solvents in the crystal
		solvent_components = list(make_SolventsList(crystal.info['SolventsList'])) if ('SolventsList' in crystal.info) else []

		# Twentieth, check to make sure the molecules are all good.
		molecules, molecule_graphs, solvent_components = check_molecules(molecules, molecule_graphs, solvent_components)

		# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

		# Twenty-first, get the paths to the molecules that have been rejigged, and get the lists of any molecules
		#               that have not geometrically relaxed or not begun. 
		opt_jobs_finished_successfully, opt_jobs_finished_unsuccessfully, opt_jobs_not_begun = Did_Complete_Main(dirpath+'/'+'rejig_molecules', print_progress=False)

		# Twenty-second, determine if there are any crystals that have molecules that have not begun optimisation. 
		if len(opt_jobs_not_begun) > 0:
			crystals_not_reconstructed_yet.append((crystal_identifier, opt_jobs_finished_unsuccessfully, opt_jobs_not_begun))
			continue

		# Twenty-third, determine if there are any incomplete geometric optimisations, and if so dont reconstruct this 
		#               crystal yet as there are more calculations that we are waiting to complete. 
		#               * If `process_all_crystals` is True, ignore this step.
		if (not process_all_crystals) and (len(opt_jobs_finished_unsuccessfully) > 0):
			crystals_not_reconstructed_yet.append((crystal_identifier, opt_jobs_finished_unsuccessfully, opt_jobs_not_begun))
			continue

		# Twenty-fourth, determine if this crystal needs rejigging.
		if len(opt_jobs_finished_successfully) == 0:

			# 24.1: No rejigging is need, so return False
			pbar.set_description(f'There are no atoms in crystal {crystal_identifier} that need to be rejigged')
			continue

		# Twenty-fifth, indicate that this molecule will have file created for rejigging.
		pbar.set_description(f'There are atoms in crystal {crystal_identifier} to be rejigged')
		pbar.set_description(f'Will reconstruct the crystal: {crystal_identifier}')

		# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

		# Twenty-sixth, initialise a list for containing the rejigged molecules.
		rejigged_molecules_list = []

		# Twenty-seventh, initialise a dictionary for holding information about the optimisation trajectory of the optimised molecules
		all_molecule_optimisation_trajectories = {}

		# Twenty-eighth, for each rejigged molecule in opt_jobs_finished_successfully.
		for path_to_rejigged_molecule in opt_jobs_finished_successfully:

			# 28.1: Get the name of the regigged molecule.
			molecule_name = int(path_to_rejigged_molecule.split('/')[-2].replace('S',''))

			# 28.2: Check that molecule_name is not already in rejigged_molecules_list. 
			#       * If so, there are two of the same molecule in opt_jobs_finished_successfully.
			#       * This should not a problem and should be reported. 
			if molecule_name is rejigged_molecules_list:
				raise Exception('molecule_name already is rejigged_molecules_list?')

			# 28.3: Obtain the functional and basis set that was being used to optimise the structure. 
			functional_and_basis_set = path_to_rejigged_molecule.split('/')[-1]

			# 28.4: Obtain the rejigged molecule from Gaussian/ORCA.
			rejigged_molecule = read(path_to_rejigged_molecule+'/rejig_opt.log', index=-1)

			# 28.5: Update the position of the atoms in molecule_name to the rejigged version.  
			molecules[molecule_name].set_positions(rejigged_molecule.get_positions())

			# 28.6: Obtain the optimisation trajectory for the molecule. 
			full_optimisation_trajectory = read(path_to_rejigged_molecule+'/rejig_opt.log', index=':')

			# 28.7: Add the optimisation trajectory for this molecule to the all_molecule_optimisation_trajectories dictionary. 
			all_molecule_optimisation_trajectories[molecule_name] = full_optimisation_trajectory

			# 28.8: Add name of rejigged molecule to rejigged_molecules_list.
			rejigged_molecules_list.append(molecule_name)

		# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

		# Twenty-ninth, make the folder for containing the reconstructed crystals. 
		make_folder(save_reconstructed_crystals_dirpath)

		# Thirtieth, create the updated crystal.
		crystal, crystal_graph = make_crystal(molecules, symmetry_operations, cell, wrap=False, solvent_components=SolventsList, remove_solvent=False, molecule_graphs=molecule_graphs, return_all_molecules=False)

		# Thirty-first, add the node and edge information from the molecules graph back to the molecule
		add_graph_to_ASE_Atoms_object(crystal, crystal_graph)

		# Thirty-second, have the updated crystal as a xyz file to the repaired_crystal_database folder. 
		write(save_reconstructed_crystals_dirpath+'/'+crystal_name+'.xyz', crystal)

		# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

		# Thirty-third, write the path to save the reconstructed (and original) molecules to for this crystal. 
		path_to_reconstructed_crystal_molecules = save_reconstructed_molecules_dirpath+'/'+crystal_name

		# Thirty-fourth, make the folder for containing the reconstructed crystals. 
		make_folder(path_to_reconstructed_crystal_molecules)

		# Thirty-fifth, create the original xyz file for the molecules in this crystal. 
		for molecule_name in sorted(molecules.keys()):

			# 35.1: Obtain the molecule.
			molecule = molecules[molecule_name].copy()

			# 35.2: Obtain the associated graph for the molecule. 
			molecule_graph = deepcopy(molecule_graphs[molecule_name])

			# 35.3: Add the node and edge information from the molecules graph back to the molecule
			add_graph_to_ASE_Atoms_object(molecule, deepcopy(molecule_graph))

			# 35.4: Obtain the solvent tag for this molecule (determining if it is a solvent or not). 
			solvent_tag = 'S' if molecule_name in solvent_components else ''

			# 35.5: Save molecule to disk.
			write(path_to_reconstructed_crystal_molecules+'/'+str(molecule_name)+str(solvent_tag)+'.xyz', molecule)

			# 35.6: If this molecule has been rejigged, write the trajectory of the geometric optimisation for this molecule to disk.
			if molecule_name in rejigged_molecules_list:

				# 35.6.1: Obtain the trajectory for the optimisation process for this molecule
				molecule_optimisation_trajectory = all_molecule_optimisation_trajectories[molecule_name]

				# 35.6.2: Save the optimisation trajectory for this molecule to disk.
				write(save_reconstructed_molecules_trajectory_dirpath+'/'+crystal_name+'_'+str(molecule_name)+str(solvent_tag)+'_traj.xyz', molecule_optimisation_trajectory)

		# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

	# Thirty-sixth, print all the crystals that were not reconstructed, and the reasons. 
	print_final_message(crystals_not_reconstructed_yet, rejig_dirpath)

# --------------------------------------------------------------------------------------------------------------

