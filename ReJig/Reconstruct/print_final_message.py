"""
print_final_message.py, Geoffrey Weal, 30/4/24

This method is designed to print if all the crystals that have been reconstructed, or if not ehich crystals have not been reconstructed and for what reason.
"""

def print_final_message(crystals_not_reconstructed_yet, rejig_dirpath):
	"""
	This method is designed to print if all the crystals that have been reconstructed, or if not ehich crystals have not been reconstructed and for what reason.

	Parameters
	----------
	crystals_not_reconstructed_yet : list
		This list contains all the crystals that have not bee reconstructed yet, along with the reasons.
	"""

	# First, if there are no non-reconstructed crystal to report, we dont need to run this method.
	if not len(crystals_not_reconstructed_yet) > 0:
		print(f'All crystals in database were processed. Path to database: {rejig_dirpath}')
		return

	# Second, intialise a list for recording which jobs did not run successfully, or are still running.
	all_opt_jobs_finished_unsuccessfully = []

	# Third, initalise a list for recording which jobs have not begun.
	all_opt_jobs_not_begun = []

	# Fourth, for each crystal that was not reconstructed. 
	for crystal_name, opt_jobs_finished_unsuccessfully, opt_jobs_not_begun in sorted(crystals_not_reconstructed_yet):

		# 4.1: Collect the jobs that did not complete or are still running. 
		if len(opt_jobs_finished_unsuccessfully) > 0:

			# 4.1.1: Obtain the names of the molecules only from the path in opt_jobs_finished_unsuccessfully.
			ojfu = [path.split('/')[-2] for path in opt_jobs_finished_unsuccessfully]

			# 4.1.2: Add this crystal information to the all_opt_jobs_finished_unsuccessfully list.
			all_opt_jobs_finished_unsuccessfully.append((crystal_name, ojfu))

		# 4.2: Collect the jobs that have not begun.
		if len(opt_jobs_not_begun) > 0:

			# 4.2.1: Obtain the names of the molecules that have not begun.
			ojnb = [path.split('/')[-2] for path in opt_jobs_not_begun]

			# 4.2.2: Add this crystal information to the all_opt_jobs_not_begun list.
			all_opt_jobs_not_begun.append((crystal_name, ojnb))

	# Fifth, print all the crystals that did not complete or are still running.
	if len(all_opt_jobs_finished_unsuccessfully) > 0:
		print('----------------------------------------------------------------------')
		print('The following molecules did not finish relaxing, or are still relaxing')
		for crystal_name, ojfu in sorted(all_opt_jobs_finished_unsuccessfully):
			print(str(crystal_name)+': '+str(', '.join(sorted(ojfu, key=lambda x: int(x.replace('S',''))))))
		print('----------------------------------------------------------------------')

	# Sixth, print all the crystals that have not begun.
	if len(all_opt_jobs_not_begun) > 0:
		print('----------------------------------------------------------------------')
		print('The following molecules have not begun being geometrically optimised')
		for crystal_name, ojnb in sorted(all_opt_jobs_not_begun):
			print(str(crystal_name)+': '+str(', '.join(sorted(ojnb, key=lambda x: int(x.replace('S',''))))))
		print('----------------------------------------------------------------------')

# --------------------------------------------------------------------------------------------------------------

