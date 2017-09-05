# MUMmer & MUMi Python API

# Description:

Simple script to perform multiple pairwise comparisons of > 1 genomes using MUMmer and MUMi
Works best with shorter genomes (< 5 M bases)

114 ~2.2 M base genomes on intel i7-4790 @3.6 GHz with 8 threads approx. 1 hour to produce 6555
MUMi values

See paper below for information about MUMmer and MUMi:

A genomic distance based on MUM indicates discontinuity between most bacterial species and genera. 
Deloger M, El Karoui M, Petit MA. J Bacteriol. 2009 Jan; 191(1):91-9. doi: 10.1128/JB.01202-08

# Installation:

Download and install MUMmer from: http://mummer.sourceforge.net/
	
If not already installed, run:

	pip install dill
	pip install numpy

Run:

	./setup.py install path_to/mummer_executable


# Usage:

	import mumi

	if __name__ == '__main__':
		mumi.batch_run(directory='PATH_TO/DIRECTORY', ext='fna', num_threads=4, k=19)
		mumi.single_run('PATH_TO/genome1', 'PATH_TO/genome2', name1='genome1', name2='genome2', k=19)

num_threads = number of cpus to use (only applies to batch_run)

ext = file extension to use within directory e.g. .fna, .fasta, .fas (only applies to batch_run)

k = minimum unique match length for mummer

name1/name2 = return names (only applies to single_run; names for batch_run are simply input files)

IMPORTANT:

use 

	if __name__ == '__main__':
		...

statement to prevent infinite process spawning!
	
# Bugs & Changes:

Please report any bugs with (preferably) or w/o suggested fixes

Contact me at mb1511@bristol.ac.uk for any more information
	
# Other Notes:
	
give_mumi.py is directly translated from the included Perl script (give_mumi.pl) in the mummer 
package, but optimised for speed and efficiency as it is easier to communicate with from the
main script. The result is slightly (but not hugely) different with 3 significant figures of
similarity most of the time. I have much less experience with Perl, so please feel free to point
out any errors in translation.

The __init__.py, multi.py and fasta.py are tools and utils from a larger project and have been 
stripped of some code, but feel free to use what is there for your own endeavours :)
