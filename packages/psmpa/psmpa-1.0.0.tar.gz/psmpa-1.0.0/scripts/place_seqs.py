#!/usr/bin/env python


import argparse
import sys
import os
from psmpa.place_seqs import place_seqs_pipeline
from psmpa.util import make_output_dir, TemporaryDirectory, restricted_float

parser = argparse.ArgumentParser(

    description="Script to run EPA-ng and GAPPA to place study sequences "
                "(i.e. OTUs or ASVs) into a reference tree. This is "
                "typically done to prep for subsequent hidden-state "
                "prediction with PICRUSt2. Requires unaligned FASTA of study "
                "sequences. Users can specify a non-default reference files "
                "if needed.",
    epilog='''
Usage example:
place_seqs.py -s study_seqs.fna -o placed_seqs.tre --processes 1 --intermediate placement_working
           ''',
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('-s', '--study_fasta', metavar='PATH', required=True,
                    type=str, help='FASTA of unaligned study sequences.')

parser.add_argument('-t', '--placement_tool', metavar='epa-ng|sepp',
                    choices=['epa-ng', 'sepp'], default="epa-ng",
                    help='Placement tool to use when placing sequences into '
                         'reference tree. One of \"epa-ng\" or \"sepp\" '
                         'must be input (default: %(default)s)')

parser.add_argument('-o', '--out_tree', metavar='PATH', required=True,
                    type=str, help='Name of final output tree.')

parser.add_argument('-p', '--processes', type=int, default=1,
                    help='Number of processes to run in parallel (default: '
                         '%(default)d). Note that this refers to '
                         'multithreading rather than multiprocessing when '
                         'running EPA-ng and GAPPA.')

parser.add_argument('--intermediate', metavar='PATH', type=str, default=None,
                    help='Output folder for intermediate files (will be '
                         'deleted otherwise).')

parser.add_argument('--min_align', type=restricted_float, default=0.8,
                    help='Proportion of the total length of an input query '
                         'sequence that must align with reference sequences. '
                         'Any sequences with lengths below this value after '
                         'making an alignment with reference sequences will '
                         'be excluded from the placement and all subsequent '
                         'steps. (default: %(default).2f).')

parser.add_argument('--chunk_size', type=int, default=5000,
                    help='Number of query seqs to read in at once for EPA-ng '
                         '(default: %(default)d).')

parser.add_argument('--verbose', default=False, action='store_true',
                    help='If specified, print out wrapped commands and other '
                         'details to screen.')



def main():

    args = parser.parse_args()

    # If intermediate output directory set then create and output there.
    # Otherwise make a temporary directory for the intermediate files.
    if args.intermediate:

        make_output_dir(args.intermediate)

        place_seqs_pipeline(study_fasta=args.study_fasta,
                            placement_tool=args.placement_tool,
                            out_tree=args.out_tree,
                            threads=args.processes,
                            out_dir=args.intermediate,
                            min_align=args.min_align,
                            chunk_size=args.chunk_size,
                            verbose=args.verbose)

    else:
        with TemporaryDirectory() as temp_dir:
                place_seqs_pipeline(study_fasta=args.study_fasta,
                                    placement_tool=args.placement_tool,
                                    out_tree=args.out_tree,
                                    threads=args.processes,
                                    out_dir=temp_dir,
                                    min_align=args.min_align,
                                    chunk_size=args.chunk_size,
                                    verbose=args.verbose)


if __name__ == "__main__":
    main()
