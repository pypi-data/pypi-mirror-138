#!/usr/bin/env python


from Bio.Blast.Applications import NcbiblastnCommandline
import pandas as pd



def blastn_runner(query, db, out, evalue=1e-5, outfmt=6):
    blastn_cline = NcbiblastnCommandline(query=query, db=db, evalue=evalue, outfmt=outfmt, out=out)
    stdout, stderr = blastn_cline()
    return stdout, stderr


class BlastFeatureGenrator():
    """Parse a format6 blast result with multiple query sequences. """

    def __init__(self, tsv):
        self.groupby_qseqid = self.blastn_format6_groupby_qseqid(tsv)
        self.qseqids = list(self.groupby_qseqid.groups.keys())

    def blastn_format6_groupby_qseqid(self, tsv):
        """Read the format6 blast result and return 'DataFrameGroupBy' object. """

        blastn_format6_header = ['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen',
                                 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']
        if tsv.endswith('.tsv.gz'):
            blastn_format6_df = pd.read_csv(tsv, sep='\t', names=blastn_format6_header, compression='gzip')
        else:
            blastn_format6_df = pd.read_csv(tsv, sep='\t', names=blastn_format6_header)

        groupby_qseqid = blastn_format6_df.groupby(by='qseqid')
        return groupby_qseqid

    def feature_col(self):
        """Define the columns of feature data. """
        feature_col_index = ['pident', 'length', 'mismatch', 'gapopen', 'evalue', 'bitscore']
        return feature_col_index

    def generate_feature_df(self, df):
        """Return the dataframe of feature data. """
        feature_names = self.feature_col()
        feature_df = df[feature_names]
        return feature_df

    def get_feature_df(self, qseqid):
        """Return the feature dataframe according to qseqid. """
        qseqid_group = self.groupby_qseqid.get_group(qseqid)
        feature_df = self.generate_feature_df(qseqid_group)
        return feature_df

    def get_sseqid(self, qseqid):
        """return the sseqid column according to qseqid. """
        qseqid_group = self.groupby_qseqid.get_group(qseqid)
        sseqid = qseqid_group['sseqid']
        return sseqid
