"""
make_SolventsList.py, Geoffrey Weal, 30/4/24

This method is designed to require that SolventsList is a list, even if their is only one value in the list.
"""
import numpy as np

def make_SolventsList(SolventsList):
	"""
	This method is designed to require that SolventsList is a list, even if their is only one value in the list.

	Parameters
	----------
	SolventsList : list of ints, np.int64
		This is the SolventsList to convert to a list.

	Returns
	-------
	SolventsList : list of ints
		This is the SolventsList as a list.
	"""
	if isinstance(SolventsList,np.int64):
		return [int(SolventsList)]
	return SolventsList