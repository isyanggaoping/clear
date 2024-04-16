import datetime

import pandas as pd
import os.path as op
if __name__ == '__main__':

    df = pd.read_excel(op.dirname(op.abspath(__file__))+'\\new_file\\aa.xlsx',sheet_name=3)

    df = df.T.iloc[5:]
    print(df)
