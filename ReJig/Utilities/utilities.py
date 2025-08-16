"""
utilities.py, Geoffrey Weal, 29/4/24

This script contains a number of methods that are used by the ReJig program. 
"""
import numpy as np

def get__added_or_modified__values(molecule_graph):
	"""
	This method is designed to obtain the added_or_modified values from the graph of the molecule

	Parameters
	----------
	molecule_graph : networkx.Graph
		This is the graph of a molecule
	"""

	# First, initialise a list to hold the added_or_modified values
	added_or_modified_values = []

	# Second, for each atom in the molecule
	for atom_index, atom_information in molecule_graph.nodes.items():

		# 2.1: Check if the 'added_or_modified' tag exists in this molecule.
		if 'added_or_modified' not in atom_information:
			added_or_modified_values.append(None)
			continue

		# 2.2: Obtain the "added_or_modified" value.
		added_or_modified_value = atom_information['added_or_modified']

		# 2.3: Perform several checks about the added_or_modified value.
		is_a_valid_string = isinstance(added_or_modified_value, str) and (added_or_modified_value.lower() in ['t', 'true', 'f', 'false'])
		is_a_bool         = isinstance(added_or_modified_value, bool)
		is_a_numpy_bool   = isinstance(added_or_modified_value, np.bool_)

		# 2.4: Determine if the input from "added_or_modified" is value.
		if is_a_valid_string or is_a_bool or is_a_numpy_bool:
			added_or_modified_value = bool(added_or_modified_value)
		else:
			raise Exception(f'Error: added_or_modified_value is not a boolean. added_or_modified_value = {added_or_modified_value}')

		# 2.5: If added_or_modified_value is a boolean, record it.
		added_or_modified_values.append(added_or_modified_value)

	# Third, return added_or_modified_values
	return added_or_modified_values