"""
get_neighbouring_hydrogens_to_modify.py, Geoffrey Weal, 31/5/24

This method is designed to obtain any neighbouring hydrogens that are bound to atoms that are also bound to 
atom with the "added_or_modified" tag equal to True. 
"""

def get_neighbouring_hydrogens_to_modify(molecule, molecule_graph, added_or_modified_values):
	"""
	This method is designed to obtain any neighbouring hydrogens that are bound to atoms that are also bound to 
	atom with the "added_or_modified" tag equal to True. 

	Parameters
	----------
	molecule : ase.Atoms
		This is the molecule to analyse
	molecule_graph : networkx.Graph
		This is the associated graph for this molecule. This indicates how atoms are bonded to each other.
	added_or_modified_values : list of bool.
		This list indicates which atoms have been added or modified. These are the atoms we want to rejig. 

	Returns
	-------
	neighbours_of_neighbouring_atom_indices : set
		This set contains all the hydrogen atoms that are 2nd neighbours to atoms we want to rejig. 
	"""

	# First, check that each of the inputs have the same length (they should as they are from the same molecule).
	if not (len(molecule) == len(molecule_graph) == len(added_or_modified_values)):
		raise Exception('Error')

	# Second, initialise a set to record all the neighbouring atoms the user also wants to be rejigged during
	#         DFT calculations.
	neighbours_of_neighbouring_atom_indices = set()

	# Third, for each of the atoms added_or_modified tags in added_or_modified_values.
	for index, added_or_modified_value in enumerate(added_or_modified_values):

		# Fourth, if added_or_modified_value is False, move on to the next atom in the molecule. 
		if added_or_modified_value == False:
			continue

		# Fifth, for each neighbouring atom to atom index.
		for neighbouring_index in molecule_graph[index]:

			# Sixth, for each atom neighbouring atom neighbouring_index.
			for neigh_of_neigh_index in molecule_graph[neighbouring_index]:

				# Seventh, we dont want to get into a infinite loop when neigh_of_neigh_index.
				#          is atom index.
				if neigh_of_neigh_index == index:
					continue

				# Eighth, if atom neigh_of_neigh_index is not a hydrogen atom, move on.
				if molecule[neigh_of_neigh_index].symbol not in ['H', 'D', 'T']:
					continue

				# Ninth, record neigh_of_neigh_index in neighbours_of_neighbouring_atom_indices
				neighbours_of_neighbouring_atom_indices.add(neigh_of_neigh_index)

	# Tenth, return neighbours_of_neighbouring_atom_indices
	return neighbours_of_neighbouring_atom_indices

