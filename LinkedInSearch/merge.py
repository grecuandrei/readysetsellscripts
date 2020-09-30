import sys, os
import pandas as pd
import re

def main(argv):
    merge(argv[0], argv[1])

def merge(file, file1):
    df = pd.read_csv(file)
    print(file)
    df1 = pd.read_csv(file1)
    print(file1)
    df = df[["name", "job_or_location", "href"]]
    df1 = df1[["web-scraper-start-url",	"Work", "education", "location"]]
    df['work'] = ""
    df['education'] = ""
    df['location'] = ""
    for index, row in df.iterrows():
        print(str(index) + " " + str(row[0]))
        for index1, row1 in df1.iterrows():
            if (str(row[2]) == str(row1[0]) or str(row[2]) + "/about" == str(row1[0])):
                df.at[index, 'work'] = str(row1[1])
                df.at[index, 'education'] = str(row1[2])
                df.at[index, 'location'] = str(row1[3])
                break
    df.to_csv(file[:-4]+"_Merged.csv", index=False)
    print("FINISHED!")


if __name__ == "__main__":
    main(sys.argv[1:])