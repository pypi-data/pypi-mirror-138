# -*- coding: UTF-8 -*-

# from importlib.resources import path
from os import path
import os
import shutil
import warnings
import pandas as pd
import subprocess
from psmpa.util import sample_bgc_calculate, read_seqabun, create_output_folder
from Bio import SeqIO
from psmpa.default import default_psmpa2_dir, default_psmpa2_database_dir, default_psmpa2_database_files, default_psmpa2_database_lineage


warnings.simplefilter("ignore")



def query_seqid(study_fasta):
    query_id = [seq_record.id for seq_record in SeqIO.parse(study_fasta, "fasta")]
    query_seqid = pd.DataFrame({'qseqid': query_id})
    return query_seqid

def add_lineage_info(psmpa2_result, lineage_info):
    lineage = pd.read_csv(lineage_info, sep='\t', compression='gzip')
    psmpa2_with_lineage = pd.merge(psmpa2_result,lineage,how='left',left_on='sseqid',right_on='id').drop(columns=['id'])
    lineage_col = psmpa2_with_lineage['lineage']
    psmpa2_with_lineage.drop(columns=['lineage'], inplace=True)
    psmpa2_with_lineage.insert(3, 'lineage', lineage_col)
    return psmpa2_with_lineage

def full_pipeline(study_fasta,
                  input_table,
                  output_folder,
                  force,
                  method,
                #   processes,
                  threshold,
                  verbose):

    # Check output folder
    if force:
        try:
            create_output_folder(output_folder)
        except:
            shutil.rmtree(output_folder)
            os.makedirs(output_folder)
    else:
        create_output_folder(output_folder)
    

    # Blast analysis
    try:
        # run blastn
        if verbose:
            print('Blastn is runing, please wait...')

        blast_database = path.join(default_psmpa2_database_dir, 'rna')
        blast_output = path.join(output_folder,'blast_result.tsv')
        if threshold:
            os.system('blastn -query ' + study_fasta + ' -db ' + blast_database + ' -out ' + blast_output + ' -outfmt 6 -perc_identity ' + threshold+ ' -max_hsps 1 -max_target_seqs 1 -num_threads 8')  # only one result is printed
        else:
            os.system('blastn -query ' + study_fasta + ' -db ' + blast_database + ' -out ' + blast_output + ' -outfmt 6 -max_hsps 1 -max_target_seqs 1 -num_threads 8')  # only one result is printed

        if verbose:
            print('Blastn finished')  # blastn output file is blast_result.tsv
    except:
        # build blast database
        if verbose:
            print('Database initializing...')
        os.chdir(default_psmpa2_database_dir)
        subprocess.check_output(['makeblastdb', '-in', '16SrRNA.fasta', '-dbtype', 'nucl', '-input_type', 'fasta', '-out', 'rna', '-parse_seqids'])
        os.chdir(path.dirname(path.abspath(__file__)))  # back to directory
        if verbose:
            print('Database initialization finished')

        # run blastn
        if verbose:
            print('Blastn is runing, please wait...')
        if threshold:
            os.system('blastn -query ' + study_fasta + ' -db ' + blast_database + ' -out ' + blast_output + ' -outfmt 6 -perc_identity ' + threshold+ ' -max_hsps 1 -max_target_seqs 1 -num_threads 8')  # only one result is printed
        else:
            os.system('blastn -query ' + study_fasta + ' -db ' + blast_database + ' -out ' + blast_output + ' -outfmt 6 -max_hsps 1 -max_target_seqs 1 -num_threads 8')  # only one result is printed
        if verbose:
            print('Blastn finished 分析数据完成')  # blastn output file is blast_result.tsv


    # Load PSMPA-BGC database
    if verbose:
        print('Loading necessary data 加载必要数据中...')
    # Read the file containing assembly_accession and antiSMASH results
    if method == 'mean_int':
        refseqid_antiSMASH = pd.read_csv(path.join(default_psmpa2_dir,default_psmpa2_database_files[1]), sep='\t', compression='gzip')
    elif method == 'median_float':
        refseqid_antiSMASH = pd.read_csv(path.join(default_psmpa2_dir,default_psmpa2_database_files[2]), sep='\t', compression='gzip')
    elif method == 'median_int':
        refseqid_antiSMASH = pd.read_csv(path.join(default_psmpa2_dir,default_psmpa2_database_files[3]), sep='\t', compression='gzip')
    else:
        refseqid_antiSMASH = pd.read_csv(path.join(default_psmpa2_dir,default_psmpa2_database_files[0]), sep='\t', compression='gzip')
    if verbose:
        print('Loading necessary data succeed')


    # Prediction analysis
    if verbose:
        print('Data analyzing...')
    blast_format6_header = ['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen',
                            'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']  # blast_result.tsv header
    blast_result = pd.read_csv(path.join(output_folder,'blast_result.tsv'), sep='\t',
                               names=blast_format6_header)[['qseqid', 'sseqid', 'pident']]

    psmpa2_out = pd.merge(blast_result, refseqid_antiSMASH, how='left',
                          left_on=['sseqid'], right_on=['id']).drop(columns=['id']).dropna(axis=1, how='all').fillna(0)

    # merge query seqid and blast result to solve the problem of missing blast result(s)
    psmpa2_result = pd.merge(query_seqid(study_fasta), psmpa2_out, how='left',
                                  left_on=['qseqid'], right_on=['qseqid'])
    # add lineage information to psmpa2 result
    psmpa2_result_with_lineage = add_lineage_info(psmpa2_result, default_psmpa2_database_lineage)
    psmpa2_result_with_lineage.to_csv(path.join(output_folder,'psmpa2_result.tsv'), sep='\t', index=False)
    

    # Sample analysis
    if input_table:
        # pretreatment of bgc table
        bgc_table = psmpa2_result.drop(columns=['sseqid', 'pident']).set_index(['qseqid']).fillna(0)
        feature_table = read_seqabun(input_table)
        sample_result = sample_bgc_calculate(feature_table, bgc_table)
        sample_result.to_csv(path.join(output_folder,'psmpa2_sample_result.tsv'), sep='\t')


    print('Analysis finished 分析完成')