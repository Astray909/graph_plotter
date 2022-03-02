import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

def data_importer(inputcsv):
    inputdf = pd.read_csv(inputcsv)
    # print(inputdf)
    
    result_df = inputdf.loc[(inputdf['Test Hours_Cycles'] == 1000)]
    # print(result_df)
    result_datecodes_list = result_df['YYWW_datecode'].tolist()
    result_datecodes_list = list(dict.fromkeys(result_datecodes_list))
    print(result_datecodes_list)

    plt.figure(figsize=(16, 6))
    sns.set_theme(style="whitegrid")
    ax = sns.boxplot(x="YYWW_datecode", y="Rdson_aging", data=result_df, width=0.5)
    ax.set_xticklabels(ax.get_xticklabels(),rotation = 30)
    plt.show()

if __name__ == "__main__":
    inputcsv = askopenfilename()
    data_importer(inputcsv)
