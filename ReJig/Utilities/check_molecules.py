"""
check_molecules.py, Geoffrey Weal, 30/4/24

This method is designed to check the molecules are all good.
"""

def check_molecules(molecules, molecule_graphs, solvent_components, original_molecules=None):
	"""
	This method is designed to check the molecules are all good.

	Parameters
	----------
	molecules : dict. of ase.Atoms
		This is the dict. of molecules in the crystal
	molecule_graphs : dict. of networkx.Graph 
		This is the dict that contains the graph of each molecule in the molecules dictionary. 
	solvent_components : list of int.
		This list contains the indices of all the solvents in the molecules list. 
	original_molecules : dict. of ase.Atoms or None
		These are the dict. of molecules that was obtained from the original molecules before removing aliphatic sidechains. If set to None, molecules are molecules from the unmodified crystal. Default: None.
	"""

	# First, record all the molecules that have problems with them.
	problematic_molecule_names = []

	# Second, for each molecule in the molecules dictionary.
	for mol_name, molecule in molecules.items():

		# Third, if their are no atoms in the molecule, record it as a problem.
		if len(molecule) == 0:
			problematic_molecule_names.append(mol_name)

	# Fourth, sort the problematic_molecule_names list
	problematic_molecule_names.sort()

	# Fifth, report the issue to the user if there are problematic molecules, and ask the user if they want to continue otherwise. 
	if len(problematic_molecule_names) > 0:

		# 5.1: Print error message.
		traceback_stack = traceback.extract_stack()
		print('Error: These is an issue at:')
		for trace in traceback_stack:
			print(f'  {trace.filename}, line {trace.lineno} in {trace.name}')#: {trace.line}')
		print('Molecules '+str([prob_mol_name for prob_mol_name in problematic_molecule_names])+' in the crystal have no atoms in it?')
		print("Look at the GUI's to see the problem")
		print('One or more GUIs show all the problematic molecules before and after the RSGC has been applied to it')
		print('The other GUI shows all the OK molecules')

		# 5.2: For each problematic molecule
		for problematic_molecule_name in problematic_molecule_names:

			# 5.2.1: Create a list that contains the problematic molecule.
			problem_molecule = [molecules[problematic_molecule_name]]

			# 5.2.2: If original_molecules is not none, add the original molecule to the list to compare molecule with.
			if original_molecules is not None:
				problem_molecule.append(original_molecules[problematic_molecule_name])

			# 5.2.3: Open the GUI to allow the user to see the problematic molecule (and its original version if given).
			view(problem_molecule)

		# 5.3: Show all the ok molecules
		view([molecules[prob_mol_name] for prob_mol_name in molecules.keys() if (prob_mol_name not in problematic_molecule_names)])

		# 5.4: Check with the user if they want to continue anyway.
		while True:
			to_continue = input('Would you like to continue without these problematic molecules in the crystal? (y/N): ')
			to_continue = to_continue.lower()
			if to_continue in ['y', 'yes']:
				break
			elif to_continue in ['n', 'no']:
				exit('Program will exit without completing.')
			print('Please type either yes (y) or no (n).')

		# 5.5: Mark the problematic molecules as None objects. 
		for prob_mol_name in problematic_molecule_names:
			molecules[prob_mol_name] = None
			molecule_graphs[prob_mol_name] = None

		# 5.6: Update molecules, molecule_graphs, and solvent_components to remove molecules with no atoms
		molecules, molecule_graphs, solvent_components = remove_None_placeholders(molecules, molecule_graphs, solvent_components)

	# Sixth, return the molecules and molecule_graphs objects
	return molecules, molecule_graphs, solvent_components

def remove_None_placeholders(molecules, molecule_graphs, solvent_components):
	"""
	This method is designed to remove any None objects from the molecules, molecule_graphs, and solvent_components dictionaries and lists.

	Parameters
	----------
	molecules : dict. of ase.Atoms
		This is the dict. of molecules in the crystal
	molecule_graphs : dict. of networkx.Graph 
		This is the dict that contains the graph of each molecule in the molecules dictionary. 
	solvent_components : list of int.
		This list contains the indices of all the solvents in the molecules list. 

	Returns
	-------
	molecules : dict. of ase.Atoms
		This is the dict. of molecules in the crystal
	molecule_graphs : dict. of networkx.Graph 
		This is the dict that contains the graph of each molecule in the molecules dictionary. 
	solvent_components : list of int.
		This list contains the indices of all the solvents in the molecules list. 
	"""

	# First, check if there are any None objects in the molecules list.
	None_object_names = []
	for mol_name in sorted(molecules.keys(), reverse=False):
		if molecules[mol_name] is None:
			None_object_names.append(mol_name)

	# Second, if there are values in None_object_names, there are None objects to remove, so do that
	if len(None_object_names) > 0:

		# 2.1: Remove all None objects from molecules and molecule_graphs, and their respective indices from solvent_components
		for None_object_name in None_object_names:
			del molecules[None_object_name]
			del molecule_graphs[None_object_name]
			if None_object_name in solvent_components:
				solvent_components.remove(None_object_name)

		# 2.2: Place all remaining molecules and molecule_graphs objects together, as well as a boolean to indicate if it is a solvent.
		all_data = []
		for mol_name in sorted(molecules.keys(), reverse=False):
			molecule       = molecules[mol_name]
			molecule_graph = molecule_graphs[mol_name]
			is_solvent = mol_name in solvent_components
			all_data.append([mol_name, molecule, molecule_graph, is_solvent])

		# 2.3: Sort all_data by the mol_name.
		all_data.sort(key=lambda x:x[0], reverse=False)

		# 2.4: Decrement molecules by the approproriate amount
		for index, (old_mol_name, molecule, molecule_graph, is_solvent) in enumerate(all_data):

			# 2.4.1: Write the new name for this molecule.
			new_mol_name = index + 1

			# 2.4.2: Change the old_mol_name to new_mol_name for this datum set. 
			all_data[index][0] = new_mol_name

		# 2.4: Check that none of the molecules in all_data have the same name.
		if not len(all_data) == len(set([mol_name for mol_name, _, _, _ in all_data])):
			raise Exception('Error: Some molecules have the same indices after None objects have been removed from the all_data list. This is a programming error.')

		# 2.5: Construct new molecules and molecule_graphs dictionaries, as well as a new solvent_components list.
		molecules = {}; molecule_graphs = {}; solvent_components = []
		for mol_name, molecule, molecule_graph, is_solvent in all_data:
			molecules[mol_name]       = molecule
			molecule_graphs[mol_name] = molecule_graph
			if is_solvent:
				solvent_components.append(mol_name)

	# Third, return molecules, molecule_graphs, and solvent_components.
	return molecules, molecule_graphs, solvent_components

# -----------------------------------------------------------------------------------------------------------------------------
