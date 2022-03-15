import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

def data_importer(inputcsv):
    inputdf = pd.read_csv(inputcsv)
    # print(inputdf)

    initiator = askopenfilename()
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
    product_id_list_len = len(list(dict.fromkeys(product_id_list)))
    print(product_id_list_len)
    pd.options.mode.chained_assignment = None  # default='warn'
    result_df.loc[:,"die"] = product_id_list
    pd.options.mode.chained_assignment = 'warn'  # default='warn'

    for region, df_region in result_df.groupby('die'):
        print(df_region)

    plt.figure(figsize=(16, 6))
    sns.set_theme(style="whitegrid")
    ax = sns.boxplot(x="YYWW_datecode", y="Rdson_aging", data=result_df, width=0.5)
    ax.set_xticklabels(ax.get_xticklabels(),rotation = 30)
    plt.show()

if __name__ == "__main__":
    inputcsv = askopenfilename()
    data_importer(inputcsv)
