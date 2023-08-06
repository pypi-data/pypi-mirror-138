import os
import argparse
import pandas as pd
import numpy as np


def args_parse():
    "Parse the input argument, use '-h' for help."
    "Author: Cui (Zhangqi Shen Lab, China Agricultural University)"
    parser = argparse.ArgumentParser(
        usage='resfidner_tidy.py -i <resfinder_result_directory> -o <output_file_directory>')
    parser.add_argument("-i", help="<input_path>: resfinder_result_path")
    parser.add_argument("-o", help="<output_file_path>: output_file_path")
    return parser.parse_args()


def mapping_dict(file):
    df_map = pd.read_csv(file, names=['Database', 'Gene'], sep='\t')
    mapping_dict = dict(zip(df_map['Gene'], df_map['Database']))
    return mapping_dict


def join(f):
    return os.path.join(os.path.dirname(__file__), f)


# def make_sure_path_exists(path):
#     try:
#         os.path.isdir(path)
#     except OSError as exception:
#         if exception.errno != errno.EEXIST:
#             raise


def res_concate(path):
    df_point_final = pd.DataFrame()
    df_resistance_final = pd.DataFrame()
    print(path)
    for file in os.listdir(path):
        if os.path.isdir(file):
            point_file = os.path.join(file, 'PointFinder_results.txt')
            resistance_file = os.path.join(file, 'ResFinder_results_tab.txt')
            if os.path.isfile(point_file):
                df_point_tmp = pd.read_csv(point_file, sep='\t')
                df_point_tmp['Strain'] = file
                df_point_final = pd.concat([df_point_final, df_point_tmp])
            if os.path.isfile(resistance_file):
                df_resistance_tmp = pd.read_csv(resistance_file, sep='\t')
                df_resistance_tmp['Strain'] = file
                df_resistance_final = pd.concat(
                    [df_resistance_final, df_resistance_tmp])
    return df_point_final, df_resistance_final


def main():
    args = args_parse()
    input_path = args.i

    # Get the directory of script and read mapping file
    mapping_file = join("gene_db_mapping.tsv")
    # print("Script path:", script)

    map_dict = mapping_dict(mapping_file)

    # print(input_file)
    input_path = os.path.abspath(input_path)
    df_point, df_resistance = res_concate(input_path)

    # print(mapping_dict)
    if not os.path.exists(args.o):
        os.mkdir(args.o)
    output_file_path = os.path.abspath(args.o)
    output_resistance_file = os.path.join(
        output_file_path, 'resfinder_sum.csv')
    output_point_file = os.path.join(output_file_path, 'point_sum.csv')
    print(output_resistance_file)
    print(output_point_file)
    # mapping resistance gene to database
    df_resistance['Database'] = df_resistance['Resistance gene'].map(map_dict)
    df_resistance_final = df_resistance.pivot_table(index='Strain', columns=[
        'Database', 'Resistance gene'], values='Identity', aggfunc=lambda x: ','.join(map(str, x)))

    # tidy point mutation results
    df_point_final = df_point.groupby(['Strain'])['Mutation'].apply(
        lambda x: ','.join(x)).to_frame()

    # print(df_final)
    df_resistance_final.to_csv(output_resistance_file)
    df_point_final.to_csv(output_point_file)


if __name__ == '__main__':
    main()
