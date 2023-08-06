# SEQLinkage
> Collapsed Haplotype Pattern Method for Linkage Analysis of Next-Generation Sequencing Data


## Pre-requisites

Make sure you install the pre-requisited before running seqlink:

```
conda install -c conda-forge xeus-cling
conda install -c anaconda swig 
conda install -c conda-forge gsl
pip install egglib
git clone https://github.com/statgenetics/cstatgen.git
cd cstatgen
python setup.py install
```

## Install

`pip install SEQLinkage`

## How to use

### 1. Test on seqlinkage-example

```
seqlink --fam seqlinkage-example.fam --vcf seqlinkage-example.vcf.gz -f MERLIN --output RMBPt8 --jobs 8

seqlink --fam seqlinkage-example.fam --vcf seqlinkage-example.vcf.gz -f MERLIN --output RMB0 --jobs 8 --bin 0

seqlink --fam seqlinkage-example.fam --vcf seqlinkage-example.vcf.gz -f MERLIN --output RMB1 --jobs 8 --bin 1

seqlink --fam seqlinkage-example.fam --vcf seqlinkage-example.vcf.gz --freq EVSEAAF -o LinkageAnalysis -K 0.001 --moi AR -W 0 -M 1 --theta-max 0.5 --theta-inc 0.05 -j 8 --run-linkage
```

### 2. Test on AD family

```
seqlink --fam data/mwe_normal_fam.csv --vcf data/first1000snp_full_samples.vcf.gz -f LINKAGE --blueprint data/genemap.hg38.txt --freq AF -K 0.001 --moi AD -W 0 -M 1

seqlink --fam data/mwe_normal_fam.csv --vcf data/first1000snp_full_samples.vcf.gz -f MERLIN --blueprint data/genemap.hg38.txt --freq AF
```

```
./seqlink --fam seqlinkage-example/seqlinkage-example.fam --vcf seqlinkage-example/seqlinkage-example.vcf.gz -f MERLIN --blueprint data/genemap.txt --freq EVSEAAF -o seqtest
./seqlink --fam data/new_trim_ped_famless17.fam --vcf data/first1000snp_full_samples.vcf.gz -f MERLIN --blueprint data/genemap.hg38.txt --freq AF
```

./seqlink --fam data/new_trim_ped_famless17.fam --vcf data/first1000snp_full_samples.vcf.gz -f MERLIN --blueprint data/genemap.hg38.txt --freq AF -K 0.001 --moi AD -W 0 -M 1 --run-linkage

./seqlink --fam data/Example_data/pedigree.fam --vcf data/Example_data/example.vcf.gz -f MERLIN MEGA2 PLINK LINKAGE --build hg38 --chrom-prefix chr --freq AF -o data/Example_data/output -K 0.001 --moi AD -W 0 -M 1


./seqlink --fam data/mwe_normal_fam.csv --vcf data/first1000snp_full_samples.vcf.gz --anno data/first1000_chr1_multianno.csv --pop data/full_sample_fam_pop.txt -f MERLIN MEGA2 PLINK LINKAGE --build hg38 --freq AF -o data/first1000test -K 0.001 --moi AD -W 0 -M 1

./seqlink --fam data/new_trim_ped_famless17_no\:xx.fam --vcf /mnt/mfs/statgen/alzheimers-family/linkage_files/geno/full_sample/vcf/full_sample.vcf.gz --anno MWE/annotation/EFIGA_NIALOAD_chr1.hg38.hg38_multianno.csv --pop data/full_sample_fam_pop.txt -f MERLIN MEGA2 PLINK LINKAGE --build hg38 --freq AF -o data/fullchr1data -K 0.001 --moi AD -W 0 -M 1 -j 4
