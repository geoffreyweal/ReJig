# Reconstructing The Crystal

Once the Gaussian/ORCA geometric optimisation calculations have finished, we would like to reconstruct the crystals where the positions of atoms in the rejigged molecules have been updated with the geometric optimisation calculations. 

To use this module, change into the directory containing your ``rejigged_crystals`` folder, and run this module:

```bash
# Change directory into the directory that contains the `rejigged_crystals` folder.
cd directory_containing_the_rejigged_crystals_folder

# Submit all your jobs in the rejigged_crystals` folder to slurm. 
ReJig reconstruct
```

Once you have run the ``ReJig reconstruct`` module, you will see that a two new folder will have appeared in your ``directory_containing_the_rejigged_crystals_folder`` directory. These are:

* ``rejigged_crystals_reconstructed``: This folder contains all the crystals where any added/modified atoms have been geometrically relaxed using the ReJig program. Take the crystals from the ``rejigged_crystals_reconstructed`` forwards for the rest of your research. 
* ``rejigged_crystals_reconstructed_molecules``: This folder contains all the molecules in the crystals that have been processed by the ReJig program. These are the molecules that make up the crystals in the ``rejigged_crystals_reconstructed`` folder. 

!!! note

	Only those crystals where all the molecules have geometrically optimised will be processed by ``ReJig reconstruct``. If you want also want to process any crystals that have unconverged molecules, do the following in the terminal: 

	``ReJig reconstruct --process_all_crystals True``

!!! note

	The molecules in the ``rejigged_crystals_reconstructed_molecules`` are only to use to check the molecules in your crystals easily. 