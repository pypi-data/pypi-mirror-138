# PSMPA

PSMPA is a Python pipeline to predict secondary metabolism potential using amplicans  for a single strain or microbial communities.

![]( https://cdn.jsdelivr.net/gh/BioGavin/Pic/imgpsmpa_logo2.png)

# Requirements
Specific libraries are required for PSMPA. We provide a requirements file to install everything at once.
Here, We recommende Conda for environment deployment.
```shell
conda create --file requirements.txt -n psmpa
# or
conda env create -f psmpa.yaml
```
If you have successfully created this environment, don't forget to activate it.
```shell
conda activate psmpa
```

# Installation & Help
Install the PSMPA package to the environment.
```shell
pip install psmpa
```
So far, if you installed successfully, you can run this command for more help information.
```shell
psmpa1 -h
```
or
```shell
psmpa2 -h
```

# Sample
## *psmpa1*

Usage:
- 16S rRNA sequence analysis
```shell
psmpa1 -s test/test_data/16S.fna -o test/psmpa1_test_out
```

- environment sample analysis
```shell
psmpa1 -s test/test_data/sequences.fasta -i test/test_data/feature-table.biom -o test/psmpa1_sample_test_out
```


## *psmpa2*
Usage:
- 16S rRNA sequence analysis
```shell
psmpa2 -s test/test_data/16S.fna -o test/psmpa2_test_out
```

- environment sample analysis
```shell
psmpa2 -s test/test_data/sequences.fasta -i test/test_data/feature-table.biom -o test/psmpa2_sample_test_out
```


# Attention
If empty rows appear in the BGCs predicted result, the likely reason is that the BLAST analysis did not match any sequences. So, if sample analysis is performed, sequences with no results are ignored.
