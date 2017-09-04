import mumi
if __name__ == '__main__':
	print 'Batch Run:'
	print mumi.batch_run('files', ext='fna', num_threads=4, k=19)
	print 'Single Comparison:'
	print mumi.single_run('files/genome_a.fna', 'files/genome_b.fna', name1='genome_a', name2='genome_b', k=19)