# Performing Geometric Optimisations

Once you have run the ``ReJig`` program, you will see a new folder has been created called ``rejigged_crystals``. This folder contains all the crystals you gave in the [Run_ReJig.py](https://github.com/geoffreyweal/ReJig/blob/main/Documentation/docs/Files/Using_The_ReJig_Program/Run_ReJig.py) file that you want the added/modified atoms to be geometrically optimised. 

* You will notice that not all the crystals from ``crystal_database_dirname`` variable in the [Run_ReJig.py](https://github.com/geoffreyweal/ReJig/blob/main/Documentation/docs/Files/Using_The_ReJig_Program/Run_ReJig.py) file have been added to ``rejigged_crystals``. Only the crystals that contains atoms that have been added/modified will have been added to this folder. 
* If a crystal does not have any added/modified atoms, we don't need to perform any geometric optimisations, so we don't need to include this crystal in this folder. 

Here is an example of what this may look like:

<figure markdown="span">
	<img alt="rejigged_crystals_folder.png" src="Images/Performing_Geometric_Optimisations/rejigged_crystals_folder.png?raw=true" width="900" />
  <figcaption>This is an example of the `rejigged_crystals` folder that contains all the crystals to be rejigged.</figcaption>
</figure>

Once you have run the ``Run_ReJig.py`` file, we will want to

1. Submit the Gaussian/ORCA geometric optimisation jobs to slurm. 
2. Check that the Gaussian/ORCA calculations have completed
3. Reconstruct the crystal with the geometrically optimised molecule. 

Here is an overview of all the modules available in the ``ReJig`` program:

```bash
username@computer-name Desktop % ReJig -h
usage: ReJig [-h] [--version] [-T] {help,submit,submit_settings,did_complete,reset,tidy,reconstruct} ...

ReJig command line tool.

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -T, --traceback

Sub-commands:
  {help,submit,submit_settings,did_complete,reset,tidy,reconstruct}
    help                Help for sub-command.
    submit              Submit ReJig geometric optimisation jobs to slurm.
    submit_settings     Change the settings for how slurm jobs are submitted using the `ReJig submit` module.
    did_complete        Will determine which geometric optimisation jobs have completed and which ones have not.
    reset               Will reset jobs that did not complete. Only run this program if you know all your other jobs have finished, as this program will break and also reset any jobs that are still running.
    tidy                Will tidy up your data folder and get rid of unnecessary files, particularly those very large files.
    reconstruct         This module is designed to reconstruct the crystal, where the geometrically relaxed molecules have replaced their non-relaxed counterparts in the crystal.
```

Here is a description of each of the available modules:

## The ``submit`` module

This module allows the user to submit all the geometric optimisation jobs created by the ``ReJig`` program to slurm. 

To use this module, change into the directory containing your ``ReJig`` files (i.e. the newly created ``rejigged_crystals`` folder), and run this module:

```bash
# Change directory into the `rejigged_crystals` folder.
cd rejigged_crystals

# Submit all your jobs in the rejigged_crystals` folder to slurm. 
ReJig submit
```

!!! note

    This will run until all your jobs have been submitted to slurm. This may take a while, so it is best to keep this in a live terminal or to write a submit.sl script to that will run this module thought slurm. 

## The ``submit_settings`` module




## The ``did_complete`` module

This method is designed to allow the user to check which geometric optimisation jobs have completed or not, as well as which jobs have not begun running. 

To use this module, change into the directory containing your ``ReJig`` files (i.e. the newly created ``rejigged_crystals`` folder), and run this module:

```bash
# Change directory into the `rejigged_crystals` folder.
cd rejigged_crystals

# Run the `did_complete` module.
ReJig did_complete
```

## The ``reset`` module

This method is designed to reset any jobs that did not complete successfully. 

* If Gaussian/ORCA had performed any geometric steps, the ``reset`` module will update the Gaussian/ORCA input file with the last geometric step from the uncompleted optimisation. 

To use this module, change into the directory containing your ``ReJig`` files (i.e. the newly created ``rejigged_crystals`` folder), and run this module:

```bash
# Change directory into the `rejigged_crystals` folder.
cd rejigged_crystals

# Run the `did_complete` module.
ReJig reset
```

!!! warning

    It is **highly recommended** that you do not run this if you currently have jobs running in slurm. This is because this program will read these jobs as having not completed and reset them while they are running. 

## The ``tidy`` module

This method is designed to remove any temporary Gaussian/ORCA files. These files include:

* ``Gaussian.chk``

To use this module, change into the directory containing your ``ReJig`` files (i.e. the newly created ``rejigged_crystals`` folder), and run this module:

```bash
# Change directory into the `rejigged_crystals` folder.
cd rejigged_crystals

# Run the `did_complete` module.
ReJig tidy
```
