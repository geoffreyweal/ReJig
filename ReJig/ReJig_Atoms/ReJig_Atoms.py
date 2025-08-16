"""
ReJig_Atoms.py, Geoffrey Weal, 28/4/24

This method is designed to create Gaussian or ORCA files to allow added or modified atoms in molecules to geometrically relax. 

"""
import os, shutil
import traceback
import numpy as np
from copy import deepcopy

#from tqdm import tqdm

#from ase import Atoms
from ase.io import write #, read
from ase.visualize import view
from ase.constraints import FixAtoms

#from SUMELF import get_distance
from SUMELF import read_crystal
from SUMELF import obtain_graph, process_crystal
from SUMELF import make_crystal
from SUMELF import make_folder #, remove_folder
from SUMELF import add_graph_to_ASE_Atoms_object

from ReJig.Utilities.make_SolventsList                                                   import make_SolventsList
from ReJig.Utilities.check_molecules                                                     import check_molecules
from ReJig.Utilities.utilities                                                           import get__added_or_modified__values
from ReJig.ReJig_Atoms.get_neighbouring_hydrogens_to_modify                              import get_neighbouring_hydrogens_to_modify
from ReJig.ReJig_Atoms.write_molecules_to_disk_methods.write_gaussian_optimisation_files import write_gaussian_optimisation_files
#from ReJig.ReJig_Atoms.write_molecules_to_disk_methods.write_orca_optimisation_files     import write_orca_optimisation_files

def ReJig_Atoms(filepath, calc_parameters, submission_information, rejig_neighbouring_hydrogens=False, place_files_in='rejigged_crystals'):
	"""
	This method is designed to create Gaussian or ORCA files to allow added or modified atoms in molecules to geometrically relax. 

	Parameters
	----------
	filepath : str.
		This is the path to the crystal file that you want to process. 
	calc_parameters : dict.
		This dictionary describes the parameters needs to perform the geometry optimisation job in Gaussian/ORCA.
	submission_information : dict.
		This dictionary describes all the parameters you want to add to the submit.sl script for submitting this Gaussian/ORCA job to slurm. 
	rejig_neighbouring_hydrogens : bool.
		This boolean indicates if you want any hydrogens that are attached to atoms that have the added_or_modified tag set to True to also allow to be rejigged.
	place_files_in : str.
		This is the folder you want to save ReJig files to.
	"""

	Rejig_rejigging_2nd_neighbour_filepath = 'Rejig_rejigging_2nd_neighbour.txt'
	if os.path.exists(Rejig_rejigging_2nd_neighbour_filepath):
		os.remove(Rejig_rejigging_2nd_neighbour_filepath)

	# First, check that the crystla file exists.
	if not os.path.exists(filepath):
		raise Exception(f'Error: Could not find {filepath}')

	# Second, obtain the filename of the crystal we want to Rejig.
	crystal_database_filename = os.path.basename(filepath)

	# Third, get the name of the identifier for this crystal. 
	crystal_identifier = crystal_database_filename.replace('.xyz','')

	# Fourth, preamble before beginning program
	no_of_char_in_divides = 70
	divide_string = '.'+'#'*no_of_char_in_divides+'.'
	print(divide_string)
	print(divide_string)
	print(divide_string)
	print('Looking at: '+str(filepath))
	print(divide_string)
	filepath_without_ext = '.'.join(filepath.split('.')[:-1])
	filename = os.path.basename(filepath)

	# Fifth, load the ase.Atoms object of the crystal. 
	crystal = read_crystal(filepath)
	'''
	if filepath.endswith('.cif'):
		crystal = read(filepath) #,disorder_groups='remove_disorder')
	else:
		crystal = read(filepath)
	'''

	# Sixth, make sure that the periodic boundary condition setting for this crystal object is True. 
	crystal.set_pbc(True)

	# Seventh, get the graph of the crystal.
	crystal, crystal_graph = obtain_graph(crystal,name='crystal')

	# Eighth, get the molecules and the graphs associated with each molecule in the crystal.
	molecules, molecule_graphs, SolventsList, symmetry_operations, cell = process_crystal(crystal,crystal_graph=crystal_graph,take_shortest_distance=True,return_list=False,logger=None)

	# Ninth, determine the solvents in the crystal
	solvent_components = list(make_SolventsList(crystal.info['SolventsList'])) if ('SolventsList' in crystal.info) else []

	# Tenth, check to make sure the molecules are all good.
	molecules, molecule_graphs, solvent_components = check_molecules(molecules, molecule_graphs, solvent_components)

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

	# Eleventh, initalise this dictionary to hold which molecules you would like to rejig.
	molecules_to_rejig = {}

	# Twelfth, remove the aliphatic sidegroup from molecules that are not solvents. Also get the list of molecules that are solvents. 
	for molecule_name in sorted(molecules.keys()):

		# 12.1: Obtain the molecule and its associated graph.
		molecule       = molecules[molecule_name].copy()
		molecule_graph = deepcopy(molecule_graphs[molecule_name])

		# 12.2: Obtain the "added_or_modified" tags from molecule_graph
		added_or_modified_values = get__added_or_modified__values(molecule_graph)

		# 12.3: If any of the values in "added_or_modified_values" are None objects, this means they are missing, so not this.
		if any([(value is None) for value in added_or_modified_values]):
			raise Exception('Error: There is a missing "added_or_modified" value in the crystal.')

		# 12.4: If there are no added or modified atoms in this molecule, pass here. 
		if not any(added_or_modified_values):
			continue

		# 12.5: If the user has set rejig_neighbouring_hydrogens to True, then we would like any hydrogens that are
		#       attached to the same atoms as those with the "added_or_modified" tag set to True to also be allowed
		#       to be rejigged using DFT with our quantum chemistry program.
		if rejig_neighbouring_hydrogens:

			# 12.5.1: Obtain all the 2nd neighbours we also want to rejig
			neighbours_of_neighbouring_atom_indices = get_neighbouring_hydrogens_to_modify(molecule, molecule_graph, added_or_modified_values)

			# 12.5.2: Obtain any 2nd neighbours that will be changed from False to True after running the previous step. 
			n_of_n_atom_indices_to_rejig = [index for index in neighbours_of_neighbouring_atom_indices_to_rejig if not added_or_modified_values[index]]

			# 12.5.3: Update all the 2nd neighbour we want to rejig, so that the "add_or_modified"
			#         values of these atoms is set to True. 
			if len(n_of_n_atom_indices_to_rejig) > 0:

				# 12.5.3.1: Print if any second neighbour hydrogens will have their added_or_modified_values tags changed.
				with open(Rejig_rejigging_2nd_neighbour_filepath, 'a+') as Rejig_rejigging_2nd_neighbourTXT:
					Rejig_rejigging_2nd_neighbourTXT.write(f'{crystal_identifier}\n')
					Rejig_rejigging_2nd_neighbourTXT.write(f'{n_of_n_atom_indices_to_rejig}\n')
					Rejig_rejigging_2nd_neighbourTXT.write('============================================================\n')

				# 12.5.3.2: Update added_or_modified_values. 
				for index in n_of_n_atom_indices_to_rejig:
					added_or_modified_values[index] = True

		# 12.6: Fix the atoms that you want to remain, only allowing the added or modified atoms to relax.
		molecule.set_constraint(FixAtoms(indices=[index for index in range(len(molecule)) if not added_or_modified_values[index]]))

		# 12.7: Record which molecules you are allowing to rejig. 
		molecules_to_rejig[molecule_name] = molecule

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

	# Thirteenth, determine if this crystal needs rejigging.
	if len(molecules_to_rejig) == 0:

		# 13.1: No rejigging is need, so return False
		print(f'There are no atoms in crystal {crystal_identifier} that need to be rejigged.')
		return False

	# Fourteenth, indicate that this molecule will have file created for rejigging.
	print(f'There are atoms in crystal {crystal_identifier} to be rejigged.'.upper())

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

	# Fifteenth, make the folder to place the editted crystal in if it doesnt currently exist.
	make_folder(place_files_in)

	# Sixteenth, get the directory for holding the crystal files. 
	crystal_foldername = place_files_in+'/'+crystal_identifier

	# Seventeenth, create the folder for storing the crystals we want to rejig.
	make_folder(crystal_foldername)

	# Eighteenth, create the directory for saving molecules to rejig into.
	rejig_molecules_directory = place_files_in+'/'+crystal_identifier+'/rejig_molecules'

	# Ninteenth, create the folder to store molecule files to be rejigged by Gaussian/ORCA. 
	make_folder(rejig_molecules_directory)

	# Twentieth, create the directory for saving the original molecule files into.
	original_molecules_directory = place_files_in+'/'+crystal_identifier+'/original_molecules'

	# Twenty-first, create the folder to store molecule xyz data to.
	make_folder(original_molecules_directory)

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
	
	# Twenty-second, obtain the software you want to use to relax the added or modified atoms in the molecules in the crystal. 
	calculation_software =  calc_parameters['calc_software']

	# Twenty-third, save the molecules you want to rejig to file.
	for molecule_name, molecule in sorted(molecules_to_rejig.items()):

		# 23.1: Obtain the graph for this molecule.
		molecule_graph = deepcopy(molecule_graphs[molecule_name])

		# 23.2: Determine if this molecule is a solvent, and if so record it in the molecule name.
		molecule_name_for_file = str(molecule_name) + str('S' if (molecule_name in solvent_components) else '')

		# 23.3: Create the files for running the program in Gaussian or ORCA. 
		if   calculation_software.lower() == 'gaussian':
			write_gaussian_optimisation_files(molecule, molecule_graph, molecule_name_for_file, rejig_molecules_directory, calc_parameters, submission_information)
		elif calculation_software.lower() == 'orca':
			write_orca_optimisation_files    (molecule, molecule_graph, molecule_name_for_file, rejig_molecules_directory, calc_parameters, submission_information)
		else:
			raise Exception("Error: calc_parameters['calc_software'] needs to be either Gaussian or ORCA. calc_parameters['calc_software'] = "+str(calc_parameters['calc_software']))

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

	# Twenty-fourth, create the original xyz file for the molecules in this crystal. 
	for molecule_name in sorted(molecules.keys()):

		# 24.1: Obtain the molecule and its associated graph.
		molecule       = molecules[molecule_name].copy()
		molecule_graph = deepcopy(molecule_graphs[molecule_name])

		# 24.2: Add the node and edge information from the molecules graph back to the molecule
		add_graph_to_ASE_Atoms_object(molecule, deepcopy(molecule_graph))

		# 24.3: Save molecule to disk
		solvent_tag = 'S' if molecule_name in solvent_components else ''
		write(original_molecules_directory+'/'+str(molecule_name)+str(solvent_tag)+'.xyz', molecule)

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

	# Twenty-fifth, copy the original crystal file for this molecule
	#shutil.copyfile(filepath, place_files_in+'/'+crystal_identifier+'/'+crystal_identifier+'.xyz')

	# Twenty-fifth, create the updated crystal.
	crystal, crystal_graph = make_crystal(molecules, symmetry_operations, cell, wrap=False, solvent_components=SolventsList, remove_solvent=False, molecule_graphs=molecule_graphs, return_all_molecules=False)

	# Twenty-sixth, add the node and edge information from the molecules graph back to the molecule
	add_graph_to_ASE_Atoms_object(crystal, crystal_graph)

	# Twenty-seventh, have the updated crystal as a xyz file to the repaired_crystal_database folder. 
	write(place_files_in+'/'+crystal_identifier+'/'+crystal_identifier+'.xyz', crystal)

	# Twenty-eighth, return True as we have made the file for this crystal to be rejigged.
	return True

# -----------------------------------------------------------------------------------------------------------------------------
