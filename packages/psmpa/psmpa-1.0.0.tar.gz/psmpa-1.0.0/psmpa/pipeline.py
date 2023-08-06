#!/usr/bin/env python

# __copyright__ = "Copyright 2021-2024, The PSMPA Project"
# __license__ = "GPL"
# __version__ = "1.0.0"

from os import path
import pandas as pd
import shutil
import sys, os
from psmpa.default import (default_tables)
from psmpa.place_seqs import identify_ref_files
from psmpa.util import (make_output_dir, check_files_exist, read_fasta,
                        system_call_check, read_seqabun, sample_bgc_calculate, create_output_folder)



def full_pipeline(study_fasta,
                  input_table,
                  output_folder,
                  processes,
                  placement_tool,
                  min_align,
                  hsp_method,
                  remove_intermediate,
                  force,
                  verbose):
    '''Function that contains wrapper commands for full psmpa pipeline.
    Descriptions of all of these input arguments/options are given in the
    psmpa1.py script.'''
    
    # Check output folder
    if force:
        try:
            create_output_folder(output_folder)
        except:
            shutil.rmtree(output_folder)
            os.makedirs(output_folder)
    else:
        create_output_folder(output_folder)



    out_tree = path.join(output_folder, "out.tre")

    # Check that all input files exist.
    project_dir = path.dirname(path.abspath(__file__))
    ref_dir = path.join(project_dir, "default_files", "bacteria", "pro_ref")
    ref_msa, tree, hmm, model = identify_ref_files(ref_dir, placement_tool)
    files2check = [study_fasta, ref_msa, tree, hmm, model]

    # This will throw an error if any input files are not found.
    check_files_exist(files2check)

    # Check that sequence names in FASTA overlap with input table.
    # if input_table:
        # check_overlapping_seqs(study_fasta, input_table, verbose)

    # Check that output folder not exist.
    # if path.exists(output_folder):
        # sys.exit("Stopping since output directory " + output_folder +
                #  " already exists.")

    # Make output folder.
    # make_output_dir(output_folder)

    if verbose:
        print("Placing sequences onto reference tree", file=sys.stderr)

    # Define folders for intermediate files (unless --remove_intermediate set).
    if remove_intermediate:
        place_seqs_intermediate = ""
        
    else:
        intermediate_dir = path.join(output_folder, "intermediate")
        make_output_dir(intermediate_dir)
        place_seqs_intermediate = path.join(intermediate_dir, "place_seqs")
        

    # Run place_seqs.py.
    place_seqs_cmd = ["place_seqs.py",
                      "--study_fasta", study_fasta,
                      "--out_tree", out_tree,
                      "--processes", str(processes),
                      "--intermediate", place_seqs_intermediate,
                      "--min_align", str(min_align),
                      "--chunk_size", str(5000),
                      "--placement_tool", placement_tool]

    if verbose:
        place_seqs_cmd.append("--verbose")
    
    system_call_check(place_seqs_cmd, print_command=verbose,
                      print_stdout=verbose, print_stderr=True)

    if verbose:
        print("Finished placing sequences on output tree: " + out_tree,
              file=sys.stderr)

    # Get predictions for all specified functions and keep track of outfiles.
    # bgc_outfile = {}

    hsp_outfile = path.join(output_folder, "psmpa1_result.tsv")

    # Keep track of output filename for next step of pipeline.
    # bgc_outfile['BGCs'] = hsp_outfile
    # bgc_tables = default_tables
    
    # Run hsp.py for each function database.
    hsp_cmd = ["hsp.py",
               "--tree", out_tree,
               "--output", hsp_outfile,
               "--hsp_method", hsp_method,
               "--seed", "100",
               "--study_fasta", study_fasta]

    system_call_check(hsp_cmd, print_command=verbose,
                      print_stdout=verbose, print_stderr=True)

    if input_table:
        bgc_table = pd.read_csv(path.join(output_folder,'psmpa1_result.tsv'), sep='\t').set_index(['qseqid']).fillna(0)
        feature_table = read_seqabun(input_table)
        sample_result = sample_bgc_calculate(feature_table, bgc_table)
        sample_result.to_csv(path.join(output_folder,'psmpa1_sample_result.tsv'), sep='\t')


    return hsp_outfile


def check_overlapping_seqs(in_seq, in_tab, verbose):
    '''Check that ASV ids overlap between the input FASTA and sequence
    abundance table. Will throw an error if none overlap and will otherwise
    print number of overlapping ids to STDERR. Also throw warning if input
    ASV table contains a column called taxonomy'''

    FASTA_ASVs = set(read_fasta(in_seq).keys())

    in_table = read_seqabun(in_tab)

    table_ASVs = set(in_table.index.values)

    num_ASV_overlap = len(table_ASVs.intersection(FASTA_ASVs))

    if 'taxonomy' in in_table.columns:
        print("Warning - column named \"taxonomy\" in abundance table - if "
              "this corresponds to taxonomic labels this should be removed "
              "before running this pipeline.", file=sys.stderr)

    # Throw error if 0 ASVs overlap between the two files.
    if num_ASV_overlap == 0:
        sys.exit("Stopping - no ASV ids overlap between input FASTA and "
                 "sequence abundance table")

    # Otherwise print to STDERR how many ASVs overlap between the two files
    # if verbose set.
    if verbose:
        print(str(num_ASV_overlap) + " of " + str(len(table_ASVs)) +
              " sequence ids overlap between input table and FASTA.\n",
              file=sys.stderr)


