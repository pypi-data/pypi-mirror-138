#!/usr/bin/env python

# __copyright__ = "Copyright 2018-2021, The PICRUSt Project"
# __license__ = "GPL"
# __version__ = "2.4.1"

from os import path

project_dir = path.dirname(path.abspath(__file__))

# psmpa2 default files directory
default_psmpa2_dir = path.join(project_dir, "default_files", "psmpa2")

default_psmpa2_database_dir = path.join(default_psmpa2_dir, "database")

default_psmpa2_database_files = ['psmpa2_database_mean_float.tsv.gz',
                                'psmpa2_database_mean_int.tsv.gz',
                                'psmpa2_database_median_float.tsv.gz',
                                'psmpa2_database_median_int.tsv.gz']

default_psmpa2_database_lineage = path.join(default_psmpa2_dir, 'psmpa2_database_lineage.tsv.gz')

# psmpa2 default files directory
default_ref_dir = path.join(project_dir, "default_files", "bacteria", "pro_ref")

default_fasta = path.join(default_ref_dir, "pro_ref.fna")

default_tree = path.join(default_ref_dir, "pro_ref.tre")

default_hmm = path.join(default_ref_dir, "pro_ref.hmm")

default_model = path.join(default_ref_dir, "pro_ref.model")

default_raxml_info = path.join(default_ref_dir, "pro_ref.raxml_info")


# Inititalize default trait table files for hsp.py.
bacteria_dir = path.join(project_dir, "default_files", "bacteria")

default_tables = {"BGCs": path.join(bacteria_dir, "BGCs.txt.gz")}


# Initialize default mapfiles to be used with add_descriptions.py
map_dir = path.join(project_dir, "default_files", "description_mapfiles")

default_map = {"METACYC": path.join(map_dir,
                                "metacyc_pathways_info.txt.gz"),

                  "COG": path.join(map_dir, "cog_info.tsv.gz"),

                  "EC": path.join(map_dir, "ec_level4_info.tsv.gz"),

                  "KO": path.join(map_dir, "ko_info.tsv.gz"),

                  "PFAM": path.join(map_dir, "pfam_info.tsv.gz"),

                  "TIGRFAM": path.join(map_dir, "tigrfam_info.tsv.gz")}
