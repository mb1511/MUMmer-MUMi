'''
Generates MUMmer file and returns MUMi value for all possible
pairwise comparisons in a given directory
'''

from __future__ import print_function

import glob
import os
import numpy as np
import subprocess as sp
import tempfile
from multiprocessing import cpu_count

import give_mumi
import multi
import fasta

__author__ = 'Matt Brewer'
__contact__ = 'mb1511@bristol.ac.uk'

mummer = 'path_to/mummer'

def single_run(genome1, genome2, name1='genome1', name2='genome2', k=19):
    '''Sinlge pairwise analysis'''
    return next(run([genome1, genome2, name1, name2, k]))

def batch_run(directory, ext='fna', num_threads=8, k=19):
    '''Run MUMi on mulitple CPUs'''
            
    assert num_threads <= cpu_count()

    files = glob.glob(directory + '/*.%s' % ext)
    n_map = []
    
    # add all files in 1 to all files in 2 (without overlap) to
    # array to be mapped to run function
    tri = np.triu(files)
    for i, row in enumerate(tri):
        for f1, f2 in ((row[i], f) for f in row):
            if f1 and f2:
                n1_nam = os.path.splitext(os.path.basename(f1))[0]
                n2_nam = os.path.splitext(os.path.basename(f2))[0]
                n_map.append((f1, f2, n1_nam, n2_nam))
    
    return '\n'.join(run(arg_list=n_map, k=k, cores=num_threads))

@multi.map_list
def run(n1, n2, n1_nam='genome1', n2_nam='genome2', k=19):
    '''Return MUMi value for 2 genomes'''
    # seq generators
    n1_s = fasta.fasta_read(n1)
    n2_s = fasta.fasta_read(n2)
    
    n2_l = 0
    n1_l = 0
    
    # concatenate files, beacause mumi cannot process multiple contigs
    with tempfile.NamedTemporaryFile(delete=True) as f1:
        with tempfile.NamedTemporaryFile(delete=True) as f2:
            f1.write('>temp_seq_1\n')
            for seq in n1_s:
                f1.write(seq.seq)
                
            f2.write('>temp_seq_2\n')
            for seq in n2_s:
                f2.write(seq.seq)
            
            cmd = [
                mummer, '-mum', 
                '-b', 
                '-c', 
                '-l', 
                '%d' % k,
                f1.name,
                f2.name]
              
            # run MUMmer
            output = sp.Popen(
                cmd,
                stdout=sp.PIPE,
                stderr=sp.PIPE)
            
            o, e = output.communicate()
            
            # get genome lengths
            for line in e.splitlines():
                if not n1_l:
                    if f1.name in line and 'length' in line:
                        n1_l = int(line[line.rfind(' ') + 1:])
                if not n2_l:
                    if f2.name in line and 'length' in line:
                        n2_l = int(line[line.rfind(' ') + 1:])
                        
            # get MUMi
            m = str(give_mumi.get(from_text=o, l1=n1_l, l2=n2_l))
    
    return '\t'.join((n1_nam, n2_nam, m))
