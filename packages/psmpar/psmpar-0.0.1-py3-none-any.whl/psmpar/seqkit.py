#!/usr/bin/env python


from Bio import SeqIO
from Bio.SeqUtils import GC
import pandas as pd

class GenerateSeqFeature():
    def __init__(self, query):
        self.qseqid = []
        self.qseqlen= []
        self.gc_content = []
        self.seq_feature = pd.DataFrame()
        self.generate_seq_feature(query=query)
        self.compose_df()

    def generate_seq_feature(self, query):
        """Input a fasta sequence file and output a feature table. """
        for seq_record in SeqIO.parse(query, "fasta"):
            qseqid = seq_record.id
            gc_content = GC(seq_record.seq)
            qseqlen = len(seq_record)
            self.qseqid.append(qseqid)
            self.qseqlen.append(qseqlen)
            self.gc_content.append(gc_content)

    def compose_df(self):
        self.seq_feature['qseqid'] = self.qseqid
        self.seq_feature['qseqlen'] = self.qseqlen
        self.seq_feature['gc_content'] = self.gc_content
        self.seq_feature.set_index(['qseqid'], inplace=True)
