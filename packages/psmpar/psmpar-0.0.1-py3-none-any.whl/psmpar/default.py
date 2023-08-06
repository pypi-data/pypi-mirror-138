#!/usr/bin/env python

from os import path


# psmpar package root dir
psmpar_root_dir = path.dirname(path.abspath(__file__))


# psmpar database dir
database = path.join(psmpar_root_dir, 'database')
# default 16S_rRNA blast database
blast_database = path.join(database, 'blast_database', 'rna')
# default bgc database
bgc_database = path.join(database, 'bgc_distribution_database', 'bgc_database.tsv.gz')
