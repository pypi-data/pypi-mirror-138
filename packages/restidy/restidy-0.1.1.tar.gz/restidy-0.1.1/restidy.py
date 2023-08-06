import os
import argparse
import pandas as pd
import numpy as np


def args_parse():
    "Parse the input argument, use '-h' for help."
    parser = argparse.ArgumentParser(
        usage='resfidner_tidy.py -i <resfinder_sum_file> -o <output_file_name>')
    parser.add_argument("-i", help="<input_file>: resfinder_sum_file")
    parser.add_argument("-o", help="<output_file_path>: output_file_path")
    return parser.parse_args()


def mapping_dict(file):
    df_map = pd.read_csv(file, names=['Database', 'Gene'], sep='\t')
    mapping_dict = dict(zip(df_map['Gene'], df_map['Database']))
    return mapping_dict


def main():
    args = args_parse()
    input_file = args.i

    # Get the directory of script and read mapping file
    script_path = os.path.split(os.path.realpath(__file__))[0]
    # print("Script path:", script)
    mapping_file = os.path.join(script_path, 'db/gene_db_mapping.tsv')
    map_dict = mapping_dict(mapping_file)

    # print(input_file)
    input_file = os.path.abspath(input_file)

    # print(df_map)

    # print(mapping_dict)
    if not os.path.exists(args.o):
        os.mkdir(args.o)
    output_file_path = os.path.abspath(args.o)
    output_file = os.path.join(output_file_path, 'resfinder_sum.csv')
    print(output_file)
    df = pd.read_csv(input_file, sep='\t',
                     names=['Strain', 'Resistance gene', 'Identity', 'Alignment Length/Gene Length', 'Coverage', 'Position in reference', 'Contig',  'Position in contig', 'Phenotype', 'Accession no.'])
    # df['Phenotype'] = df['Phenotype'].replace(' resistance', '')
    df['Database'] = df['Resistance gene'].map(map_dict)
    df_final = df.pivot_table(index='Strain', columns=[
                              'Database', 'Resistance gene'], values='Identity', aggfunc=lambda x: ','.join(map(str, x)))
    # print(df_final)
    df_final.to_csv(output_file)


if __name__ == '__main__':
    main()
