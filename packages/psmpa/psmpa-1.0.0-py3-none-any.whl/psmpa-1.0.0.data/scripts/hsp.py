#!python


import argparse
import sys
import os
from psmpa.wrap_hsp import castor_hsp_workflow
from psmpa.util import make_output_dir_for_file, check_files_exist
from psmpa.default import default_tables
from Bio import SeqIO
import pandas as pd

HSP_METHODS = ['mp', 'emp_prob', 'pic', 'scp', 'subtree_average']

parser = argparse.ArgumentParser(

    description="This script performs hidden state prediction on tips in "
                "the input tree with unknown trait values. Typically this "
                "script is used to predict the copy number of gene families "
                "present in the predicted genome for each amplicon sequence "
                "variant, given a tree and a set of known trait values. "
                "This script outputs a table of trait predictions.",
    epilog='''
Usage example:
hsp.py -t out.tre -o 16S_predicted_BGCs.tsv.gz --processes 1

''', formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('-t', '--tree', metavar='PATH', required=True, type=str,
                    help='The full reference tree in newick format containing '
                         'both study sequences (i.e. ASVs or OTUs) and '
                         'reference sequences.')

parser.add_argument('-o', '--output', metavar='PATH', type=str, required=True,
                    help='Output table with predicted abundances per study '
                         'sequence in input tree. If the extension \".gz\" '
                         'is added the table will automatically be gzipped.')

parser.add_argument('-m', '--hsp_method', default='mp',
                    choices=HSP_METHODS,
                    help='HSP method to use.' +
                    '"mp": predict discrete traits using max parsimony. '
                    '"emp_prob": predict discrete traits based on empirical '
                    'state probabilities across tips. "subtree_average": '
                    'predict continuous traits using subtree averaging. '
                    '"pic": predict continuous traits with phylogentic '
                    'independent contrast. "scp": reconstruct continuous '
                    'traits using squared-change parsimony (default: '
                    '%(default)s).')

parser.add_argument('--chunk_size', default=500, type=int,
                    help='Number of functions to run at a time on one '
                         'processor. Note that you should consider how many '
                         'processes you have specified before changing this '
                         'option. E.g. if you specify the chunk_size to be '
                         'the total number of functions, 1 processor will '
                         'be used even if you specified more so the job will '
                         'be substantially slower (default: %(default)d).')

parser.add_argument('--check', default=False, action='store_true',
                    help='Check input trait table before HSP.')

parser.add_argument('-p', '--processes', default=1, type=int,
                    help='Number of processes to run in parallel (default: '
                    '%(default)d).')

parser.add_argument('--seed', default=100, type=int,
                    help='Seed to make output reproducible, which is '
                         'necessary for the emp_prob method '
                         '(default: %(default)d).')

parser.add_argument('--verbose', default=False, action='store_true',
                    help='If specified, print out wrapped commands and other '
                         'details to screen.')

parser.add_argument('-s', '--study_fasta', metavar='PATH', required=True,
                    type=str, help='FASTA of unaligned study sequences (i.e. '
                                   'OTUs or ASVs).')


def query_seqid(study_fasta):
    query_id = [seq_record.id for seq_record in SeqIO.parse(study_fasta, "fasta")]
    query_seqid = pd.DataFrame({'qseqid': query_id})
    return query_seqid

def main():

    args = parser.parse_args()
    trait_table = default_tables['BGCs']

    # Check that input filenames exist.
    check_files_exist([args.tree, trait_table])

    hsp_table, ci_table = castor_hsp_workflow(tree_path=args.tree,
                                              trait_table_path=trait_table,
                                              hsp_method=args.hsp_method,
                                              chunk_size=args.chunk_size,
                                              check_input=args.check,
                                              num_proc=args.processes,
                                              ran_seed=args.seed,
                                              verbose=args.verbose)

    
    # merge entries without results into the hsp_table
    study_fasta=args.study_fasta
    hsp_table_dropzero = hsp_table.loc[:, (hsp_table != 0).any(axis=0)]
    hsp_result = pd.merge(query_seqid(study_fasta), hsp_table_dropzero, how='left',
                                  left_on=['qseqid'], right_on=['qseqid'])
    




    # Output the table to file.
    make_output_dir_for_file(args.output)
    hsp_result.to_csv(path_or_buf=args.output, index=False, sep="\t")
    


if __name__ == "__main__":
    main()
