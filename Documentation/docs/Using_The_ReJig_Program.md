# How To Use The ReJig Program

The ReJig program is designed to allow any atoms that have been added or modified in the crystal structure to geometrically relax using Gaussian or ORCA (ORCA to be written). 

In this webpage, we will describe the steps for using the ReJig program to allow any added or modified atoms from the crystal structure to geometrically optimise. 

!!! example

	You can find examples for running the ReJig program in [the ``Examples`` folder here](https://github.com/geoffreyweal/ReJig/tree/main/Examples).

## Prelude: Which atoms will the ReJig Program allow to geometrically optimise?

Lets consider the atoms in the ``xyz`` file for molecule 1 of the ``ARUJOP`` crystal below (This file was obtained from running the ``ACSD``, ``ReCrystal``, and ``RSGC`` programs):

```title="Exert from the xyz file for molecule 1 of the ARUJOP crystal."
100
Lattice="24.86 0.0 0.0 -4.316272014399794 26.033006942297487 0.0 -8.38961840880601 -6.180026782058241 26.026363229765053" Properties=species:S:1:pos:R:3:initial_charges:R:1:involved_in_no_of_rings:I:1:added_or_modified:L:1:is_H_acceptor:S:1:is_spiro_atom:L:1:is_H_donor:S:1:hybridisation:S:1:NeighboursList:S:1
S        7.50786342      -1.27378265      14.75018110    0.00000000     1  F True  F False sp3 12,26
S        5.99231447       6.51914640      14.69448468    0.00000000     1  F True  F False sp3 13,16
O        9.39220907       2.84256088      15.51431512    0.00000000     0  F True  F False sp3 6,58
O        4.08908503       2.40280099      14.03341505    0.00000000     0  F True  F False sp3 14,65
F       10.06947275      13.20378108      15.98539230    0.00000000     0  F False  F False -  49
F        3.65074450      -7.90363172      12.84921553    0.00000000     0  F False  F False -  54
C        8.08744988       2.75368668      15.17597240    0.00000000     1  F False  F False sp2 2,22,37
F        5.50496721      -9.73672023      13.38796125    0.00000000     0  F False  F False -  38
O        7.36654778       8.69923159      15.14474076    0.00000000     0  F True  F True sp2 34
O        6.16432116      -3.47172146      14.22601014    0.00000000     0  F True  F True sp2 39
F        8.26723591      14.99995262      15.30610422    0.00000000     0  F False  F False -  57
C        5.08075977      11.33587538      14.43422105    0.00000000     1  F False  F False sp2 24,27,32
C        8.31995493       0.23719144      15.04063531    0.00000000     1  F False  F False sp3 0,37,59
C        5.14179674       5.00768371      14.52010805    0.00000000     1  F False  F False sp3 1,30,44
C        5.39395797       2.52825269      14.38216832    0.00000000     1  F False  F False sp2 3,30,50
C        6.27678505      -5.86352085      14.06985196    0.00000000     2  F False  F False sp2 18,20,39
C        4.50283778       7.43837882      14.45764477    0.00000000     1  F False  F False sp3 1,29,61
C        8.50378953      -6.08417031      14.79078222    0.00000000     1  F False  F False sp2 20,25,48
C        5.07998975      -6.12269836      13.59356951    0.00000000     1  F False  F False sp2 15,19,54
H        4.45296433      -5.45972132      13.42179552    0.00000000     0  F False  F False -  18
C        7.34007717      -6.78118904      14.32751296    0.00000000     2  F False  F False sp2 15,17,35
N        9.98011517      -9.29549365      15.19158822    0.00000000     0  F True  F True sp 33
C        7.30970595       3.87907782      15.03022477    0.00000000     1  F False  F False sp2 6,23,30
H        7.67745468       4.72240001      15.17336976    0.00000000     0  F False  F False -  22
C        5.36134099       9.87400200      14.52791595    0.00000000     1  F False  F False sp2 11,34,61
C        8.18926021      -4.66374155      14.81680859    0.00000000     1  F False  F False sp2 17,39,41
C        9.00276192      -2.16927028      15.01200631    0.00000000     1  F False  F False sp3 0,28,41
C        6.28804089      12.03246180      14.81160331    0.00000000     2  F False  F False sp2 11,31,46
C       10.04560924      -1.37763618      15.33993849    0.00000000     1  F False  F False sp2 26,40,59
C        3.43327173       6.60552423      14.21559960    0.00000000     1  F False  F False sp2 16,44,70
C        5.95560641       3.75473084      14.66585568    0.00000000     1  F False  F False sp2 13,14,22
C        7.30363122      11.11584393      15.15254867    0.00000000     2  F False  F False sp2 27,34,55
C        3.91995115      11.91561715      14.00999133    0.00000000     0  F False  F False sp2 11,43,66
C        9.81111279      -8.13031965      15.20720404    0.00000000     0  F False  F False sp 21,48
C        6.67554436       9.77079556      14.96255622    0.00000000     1  F False  F False sp2 8,24,31
C        7.02691403      -8.15416288      14.09067305    0.00000000     1  F False  F False sp2 20,36,38
H        7.64734471      -8.82234653      14.26244705    0.00000000     0  F False  F False -  35
C        7.53266340       1.46834448      14.92091404    0.00000000     1  F False  F False sp2 6,12,50
C        5.79600907      -8.45115390      13.60918533    0.00000000     1  F False  F False sp2 7,35,54
C        6.83940936      -4.53229267      14.35093668    0.00000000     1  F False  F False sp2 9,15,25
C       11.43466213      -1.72389112      15.49349403    0.00000000     1  F False  F False sp2 28,68,74
C        9.07468675      -3.60651639      15.04584058    0.00000000     0  F False  F False sp2 25,26,42
H        9.92439269      -3.90821419      15.27487258    0.00000000     0  F False  F False -  41
C        2.79137612      11.31267266      13.52329833    0.00000000     0  F False  F False sp 32,67
C        3.82086998       5.17992733      14.24422860    0.00000000     1  F False  F False sp2 13,29,45
H        3.22931723       4.47965539      14.09067305    0.00000000     0  F False  F False -  44
C        6.63310756      13.41511550      14.88707977    0.00000000     1  F False  F False sp2 27,47,57
H        6.01157843      14.08105127      14.69188204    0.00000000     0  F False  F False -  46
C        9.69508909      -6.67471914      15.18378031    0.00000000     0  F False  F False sp2 17,33,52
C        8.84614760      12.77572850      15.63924166    0.00000000     1  F False  F False sp2 4,55,57
C        6.20607879       1.37660440      14.56175023    0.00000000     1  F False  F False sp2 14,37,51
H        5.82951540       0.53738410      14.43422105    0.00000000     0  F False  F False -  50
C       10.80593425      -6.08479116      15.67047330    0.00000000     0  F False  F False sp 48,71
N        3.57693768      14.52964802      13.93191224    0.00000000     0  F True  F True sp 66
C        4.82207830      -7.51971991      13.35933225    0.00000000     1  F False  F False sp2 5,18,38
C        8.54565550      11.38932834      15.52472567    0.00000000     1  F False  F False sp2 31,49,56
H        9.17516692      10.72635130      15.69649966    0.00000000     0  F False  F False -  55
C        7.90186957      13.72429683      15.25144885    0.00000000     1  F False  F False sp2 10,46,49
C        9.95528592       4.12084246      15.77718139    0.00000000     0  F False  F False sp3 2,82,92,93
C        9.61364076       0.05730766      15.38158067    0.00000000     1  F False  F False sp2 12,28,60
H       10.18321497       0.75342332      15.61842057    0.00000000     0  F False  F False -  59
C        4.44028598       8.83949570      14.34573141    0.00000000     0  F False  F False sp2 16,24,62
H        3.59856232       9.14415223      14.09327569    0.00000000     0  F False  F False -  61
C        1.36050608       7.96121649      14.73352422    0.00000000     1  F False  F False sp2 64,70,72
H        1.83520169       8.45851442      15.35815694    0.00000000     0  F False  F False -  63
C        3.56496951       1.11807679      13.77575406    0.00000000     0  F False  F False sp3 3,76,94,95
C        3.75824991      13.40157668      13.96834915    0.00000000     0  F False  F False sp 32,53
N        1.84230117      10.81552852      13.11728707    0.00000000     0  F True  F True sp 43
C       12.13091906      -2.56625298      14.60078977    0.00000000     1  F False  F False sp2 40,69,77
H       11.66841920      -2.96108721      13.89547533    0.00000000     0  F False  F False -  68
C        2.05356230       6.92177557      14.05683878    0.00000000     1  F False  F False sp2 29,63,80
N       11.74970934      -5.60066352      16.07648457    0.00000000     0  F True  F True sp 52
C        0.11448416       8.26467546      14.54092914    0.00000000     1  F False  F False sp2 63,73,79
H       -0.26906006       8.91712111      15.08227749    0.00000000     0  F False  F False -  72
C       12.23458227      -1.16260884      16.49550902    0.00000000     1  F False  F False sp2 40,75,85
H       11.84239345      -0.54683353      17.07069164    0.00000000     0  F False  F False -  74
H        2.64434312       1.23232210      13.49239024    0.00000000     0  F False  F False sp3 65
C       13.39165812      -2.79425468      14.73872950    0.00000000     1  F False  F False sp2 68,78,83
H       13.76239138      -3.41920718      14.15834160    0.00000000     0  F False  F False -  77
C       -0.66892361       7.67788533      13.58055633    0.00000000     1  F False  F False sp2 72,84,87
C        1.26292704       6.28994159      13.03400271    0.00000000     1  F False  F False sp2 70,81,87
H        1.65431682       5.61768141      12.52128335    0.00000000     0  F False  F False -  80
H       10.91016813       4.04194930      15.92842898    0.00000000     0  F False  F False sp3 58
C       14.21071075      -2.25166627      15.60020212    0.00000000     1  F False  F False sp2 77,85,89
C       -2.08801995       8.03144096      13.23180307    0.00000000     0  F False  F False sp3 79,90,96,97
C       13.53735716      -1.45578589      16.67769356    0.00000000     1  F False  F False sp2 74,83,86
H       13.99742525      -1.17484045      17.43506073    0.00000000     0  F False  F False -  85
C       -0.02691577       6.62844102      12.78154698    0.00000000     1  F False  F False sp2 79,80,88
H       -0.50219328       6.19755446      12.10746417    0.00000000     0  F False  F False -  87
C       15.64422048      -2.62996450      15.84484993    0.00000000     0  F False  F False sp3 83,91,98,99
H       -2.69566358       7.49319533      13.76280294    0.00000000     0  T None  F None sp3 84
H       15.67939059      -3.41561717      16.41266411    0.00000000     0  T None  F None sp3 89
H        9.53632672       4.49922749      16.56597665    0.00000000     0  T None  F None -  58
H        9.79848851       4.70232192      15.01678925    0.00000000     0  T None  F None -  58
H        3.59945805       0.57833263      14.58097874    0.00000000     0  T None  F None -  65
H        4.07661692       0.68588853      13.07409158    0.00000000     0  T None  F None -  65
H       -2.24196265       8.97092827      13.41772039    0.00000000     0  T None  F None -  84
H       -2.24198924       7.85830208      12.28988142    0.00000000     0  T None  F None -  84
H       16.10235100      -1.89491410      16.28156189    0.00000000     0  T None  F None -  89
H       16.07629716      -2.82356608      14.99825193    0.00000000     0  T None  F None -  89
                                                                          /\
                                                                          ||
                                                       This column is the focus of the ReJig Program.
```

In the 7<sup>th</sup> column of the ``xyz`` file above, the boolean describes the ``added_or_modified`` tag, indicating if the atom has been added or modified to get the molecule to this state. 

!!! warning

	The ``added_or_modified`` tag is not always in the 7<sup>th</sup> column of the ``xyz`` file. It can be potentially in any column. To determine while column it is in, count were the ``added_or_modified`` tag is in the second line of the ``xyz`` file. 

In this case, these are methyl groups that have been added to the molecule (as highlighted in the image of molecule 1 below): 

<figure markdown="span">
	<img alt="ARUJOP_mol_1.png" src="Images/Using_The_ReJig_Program/ARUJOP_mol_1.png?raw=true" width="700" />
  <figcaption>This is a molecule that we have added two methyl groups to.</figcaption>
</figure>

The ``ReJig`` program is designed to create the files that will allow selected atoms in the molecule (those that have been added or modified) to locally relax using either Gaussian or ORCA. 

The ``ReJig`` program will:

1. Input the crystal file (for example, the ``ARUJOP.xyz``/``ARUJOP_with_sidechains_removed.xyz`` file as obtained from the ``ACSD``, ``ReCrystal``, and ``RSGC`` programs) and read it.
2. Separate the crystal into the molecules that make up the crystal. 
3. Determine which molecules have had atoms added or modified based on the ``added_or_modified`` tag. 
4. For those that have had added or modified atoms, create a Gaussian or ORCA file where all the atoms in the molecule have been frozen except for those that have been added or modified. 


## The ``Run_ReJig.py`` script

The ``Run_ReJig.py`` script contains the information required to allow you to run the ``Run_ReJig`` to obtain the Gaussian/ORCA files. These files will allow you to geometrically relax those atoms that have either been added or modified in the molecule. 

Below is an example of a python script called ``Run_ReJig.py`` that contains the instructions given by the user to obtain these Gaussian/ORCA files.

???+ example "``Run_ReJig.py`` python script"

	```python title="Run_ReJig.py" linenums="1"
	--8<-- "docs/Files/Using_The_ReJig_Program/Run_ReJig.py"
	```

Below we describe the ``Run_ReJig.py`` python script above so you can understand how it works.

### Part I: Crystal database folder and computational details

In the first section, we give all the information we want to give to the ReJig program. Change these settings to the settings you want to use for performing geometric optimisations on your crystals. These are:

* ``crystal_database_dirname``: The name of the folder containing the database of crystals we want to analyse. 

* ``calc_parameters``: These are the settings you want to give for Gaussian/ORCA. These settings include:
	* ``'mem'``: The amount of memory you want to allocate to Gaussian/ORCA.
	* ``'method'``: This is the functional you want to use.
	* ``'basis'``: This is the basis set you want to use. 
	* ``'temp_folder_path'``: This is the path to save temporary files into. This setting is just for Gaussian.
	* ``'extra'``: These are any extra settings you want to include for the Gaussian/ORCA calculation.

* ``'submission_information'``: This is the information you want to give in the ``submit.sl`` file for submitting ReJig jobs to slurm. These settings include:
	* ``'cpus_per_task'``: This is the number of cpus you want to assign to your Gaussian\ORCA jobs.
	* ``'mem'``: This is the amount of memory to assign to this job. This should be slightly more than ``calc_parameters['mem']``, as Gaussian/ORCA can slightly go over the memory allocated in ``calc_parameters['mem']``. 
	* ``'time'``: This is the amount of time you want to assign to these jobs. 
	* ``'partition'``: This is the partition you want to run these jobs on.
	* ``'constraint'``: [See the slurm website here](https://slurm.schedmd.com/sbatch.html#OPT_constraint) to see what this feature means in slurm. 
	* ``'email'``: This is the email that you want information about this job to be sent too. 

An example of the code for ``PART I`` is shown below:

```python title="Part I of Run_ReJig.py: Get the names of the crystals you want to remove sidegroups from" show_lines="13:36" linenums="13"
--8<-- "docs/Files/Using_The_ReJig_Program/Run_ReJig.py"
```

### Part II: Database checks

In the second section, check that the crystal databases exist. You can leave this as is, or modify it as you would like. An example of the code for ``PART II`` is shown below:

```python title="Part II of Run_ReJig.py: Database checks" show_lines="36:43" linenums="36"
--8<-- "docs/Files/Using_The_ReJig_Program/Run_ReJig.py"
```

### Part III: Gather the paths to the crystal files

In the third section, gather all the paths of the crystal files you want to remove. You can leave this as is, or modify it as you would like. An example of the code for ``PART III`` is shown below:

```python title="Part III of Run_ReJig.py: Gather the paths to the crystal files" show_lines="43:62" linenums="43"
--8<-- "docs/Files/Using_The_ReJig_Program/Run_ReJig.py"
```

### Part IV: Remove existing files from previous ReJig runs

In the fourth section, remove any existing files that were produced during previous ReJig runs. You can leave this as is, or modify it as you would like.  An example of the code for ``PART IV`` is shown below:

```python title="Part IV of Run_ReJig.py: Remove existing files from previous ReJig runs" show_lines="62:70" linenums="62"
--8<-- "docs/Files/Using_The_ReJig_Program/Run_ReJig.py"
```

### Part V: Run the ReJig program

In the fifth section, the ReJig program will create all the Gaussian/ORCA and slurm files for performing geometric optimisation calculations. You can leave this as is, or modify it as you would like. An example of the code for ``PART V`` is shown below:

```python title="Part V of Run_ReJig.py: Run the ReJig program" show_lines="70:95" linenums="70"
--8<-- "docs/Files/Using_The_ReJig_Program/Run_ReJig.py"
```

