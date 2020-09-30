import sys
import csv
import os
import pandas as pd
import re

def main(argv):
    file1 = argv[0]
    print(file1)
    df = pd.read_csv(file1, encoding='windows-1252')
    df =df[["name", "job_or_location", "name-href"]]
    df["href"] = ''
    df["name_href"] = ''
    for index, row in df.iterrows():
        ref = re.split('fref', str(row[2]))[0]
        print(ref[:-1])
        df.at[index, 'href'] = ref[:-1]
        df.at[index, 'name_href'] = ''.join(('"',ref[:-1],'/about",'))

    df.to_csv(file1 + "_final.csv", index=False)

if __name__ == "__main__":
    main(sys.argv[1:])