import glob
import os
import re
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

def data_importer(inputcsv):
    inputdf = pd.read_csv(inputcsv)
    # print(inputdf)

    ori_path = os.getcwd()
    path = 'X://PLC//Prod Docs//Qual//qrw_script//'
    extension = "xlsm"
    os.chdir(path)
    all_xlsx_files = glob.glob('*.{}'.format(extension))
    return_arr = []
    for xlsx_file in all_xlsx_files:
        if str('test_initiator') in xlsx_file and '~$' not in xlsx_file:
            return_arr.append(xlsx_file)
    return_arr = ntSort(return_arr)
    return_path = path + return_arr[-1]
    os.chdir(ori_path)
    limits_path = return_path
    
    initiator = limits_path
    initiator_df = pd.read_excel(initiator, sheet_name = 'product_id')
    
    result_df = inputdf.loc[(inputdf['Test Hours_Cycles'] == 1000)]
    # print(result_df)
    result_datecodes_list = result_df['YYWW_datecode'].tolist()
    result_datecodes_list = list(dict.fromkeys(result_datecodes_list))
    
    product_id_list = []
    part_list = result_df['product'].tolist()
    for part in part_list:
        part_result_df = initiator_df.loc[(initiator_df['product'] == part)]
        prod_id = part_result_df['die']
        product_id_list.append(prod_id.to_string(index=False))
    product_id_list_cleaned = list(dict.fromkeys(product_id_list))
    product_id_list_len = len(product_id_list)
    pd.options.mode.chained_assignment = None  # default='warn'
    result_df.loc[:,"die"] = product_id_list
    pd.options.mode.chained_assignment = 'warn'  # default='warn'

    df_list = []
    for region, df_region in result_df.groupby('die'):
        df_list.append(df_region)

    # fig, axes = plt.subplots(1, len(df_list), figsize=(15, 5), sharey=True)
    plt.figure(figsize=(16, 6))
    sns.set_theme(style="whitegrid")
    for i in range(len(df_list)):
        plotname = 'plt_' + str(i)
        # plotname = sns.boxplot(ax=axes[i], x="YYWW_datecode", y="Rdson_aging", data=df_list[i], width=0.5)
        plotname = sns.boxplot(x="YYWW_datecode", y="Rdson_aging", data=df_list[i], width=0.5)
        # axes[i].set_title(str(product_id_list_cleaned[i]))
        plotname.set_title(str(product_id_list_cleaned[i]))
        plotname.set_xticklabels(plotname.get_xticklabels(),rotation = 30)
        plt.show()

#natural sort
def ntSort(input): 
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(input, key = alphanum_key)

if __name__ == "__main__":
    inputcsv = askopenfilename()
    data_importer(inputcsv)
