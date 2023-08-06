#! /usr/bin/env python


from os import path


# test root dir
test_root_dir = path.dirname(path.abspath(__file__))

testdata_dir = path.join(test_root_dir, 'testdata')
testout_dir = path.join(test_root_dir, 'testout')
rna_fasta = path.join(testdata_dir, '16S.fna')
seq_fasta = path.join(testdata_dir, 'sequences.fasta')
feature_biom = path.join(testdata_dir, 'feature-table.biom')

bgc_table = path.join(testdata_dir, 'bgc_database_demo.tsv.gz')
