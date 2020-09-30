import sys
import csv
import os
import pandas as pd
import numpy as np
import tldextract

# APELARE: python3 csvv.py filter.csv 0(or 1 or 2)

def main(argv):
    if argv[1] == '0':
        i = 0
        outFile = ''
        for file in os.listdir(os.path.dirname(os.path.abspath(__file__))):
            if file.endswith(".csv") and file != "filter.csv":
                f = os.path.dirname(os.path.abspath(__file__)) + "/" + file
                print(f)
                if i == 0:
                    outFile = "Merged.csv"
                    fil = pd.read_csv(file)
                    i = 1
                else:
                    fil2 = pd.read_csv(file)
                    fil = pd.concat([fil,fil2]).drop_duplicates().reset_index(drop=True)
        fil.to_csv(outFile, index=False)

        filterAggresive(outFile, argv[0])

    elif argv[1] == '1':
        filterFiles(argv[0]) #filterCrit

    elif argv[1] == '2':
        dropDupl()

def extractDomain(x):
    ext = tldextract.extract(x)
    if ext.subdomain == '':
        s = ext.domain
    else:
        s = ' '.join(ext[:2])
    return s.capitalize()

# filter data and split files containing certain columns (or added from filter.csv)
def filterAggresive(inputFileName, filterCriteriaFileName):
    excluded = ['data','dpo','privacy','gdpr'] # from generic
    excluded = [f"^{x}.*" for x in excluded]

    for F in range(0,3,1):
        # crating tables
        print(F)
        
        # init
        y, z, outFile = init(F, inputFileName)

        inFilterfile = open(filterCriteriaFileName, "r")
        filterCriteriaList = csv.reader(inFilterfile)

        for x in filterCriteriaList:
            x.pop()
            x = y + x
            if x[-1] == '':
                x.pop()
            filtered = pd.read_csv(inputFileName, usecols=x)
            filtered_df = filtered[~filtered[z].isnull()]

            if F == 2:
                df = filtered[~filtered['Other Company Email Address'].isnull()]
                filtered_df = filtered_df.combine_first(df)
                z = [z, 'Other Company Email Address']

            if F != 0:
                types = ['Generic Company Email Address','Other Company Email Address','Emails from other domains']
                for email in types:
                    for e in excluded:
                        try:
                            filtered_df = filtered_df[~filtered_df[email].str.contains(f"^{e}.*", na = False)]
                        except:
                            continue

            # sorting data frames
            filtered_df, r = sort_df(filtered_df, F, z)

            # filling up company names
            df1 = pd.DataFrame(columns=['Website'])
            df1['Website'] = filtered_df['Website'].copy()
            df1['Website'] = df1['Website'].apply(extractDomain)
            filtered_df['Company Name'] = np.where(filtered_df['Company Name'].isnull(), df1['Website'], filtered_df['Company Name'])

            # clearing mail duplicates - no more than 5
            filtered_df = dupl(filtered_df, F, r)

            # reverting '' with nan cause i did it earlier to work with split
            if F == 2:
                filtered_df['Other Company Email Address'] = filtered_df['Other Company Email Address'].replace('', np.nan, regex=True)
                filtered_df['Emails from other domains'] = filtered_df['Emails from other domains'].replace('', np.nan, regex=True)

            # saving
            filtered_df.to_csv(outFile, index=False)

# init
def init(F, inputFileName):
    y = ['Website','Company Name']

    if F == 0:
        y.append('First Name')
        y.append('Personal Email Address')
        y.append('Job Title')
        z ='Personal Email Address'
        outFile = inputFileName.split(".")[0] + '_Personal.csv'
    elif F == 1:
        y.append('Generic Company Email Address')
        z ='Generic Company Email Address'
        outFile = inputFileName.split(".")[0] + '_Generic.csv'
    else:
        y.append('First Name')
        y.append('Other Company Email Address')
        y.append('Emails from other domains')
        z ='Emails from other domains'
        outFile = inputFileName.split(".")[0] + '_Other.csv'

    return y, z, outFile

# sorting data frame
def sort_df(filtered_df, F, z):
    filtered_df = filtered_df.drop_duplicates(subset=z, keep='first')
    if F == 0:
        r = filtered_df.columns.get_loc('Personal Email Address')
        filtered_df = filtered_df.sort_values(by=['Website','Personal Email Address'], ascending=True)
    elif F == 1:
        r = filtered_df.columns.get_loc('Generic Company Email Address')
        filtered_df = filtered_df.sort_values(by=['Website','Generic Company Email Address'], ascending=True)
    else:
        r = filtered_df.columns.get_loc('Other Company Email Address')
        filtered_df = filtered_df.sort_values(by=['Website','Other Company Email Address','Emails from other domains'], ascending=True)
        filtered_df['Other Company Email Address'] = filtered_df['Other Company Email Address'].replace(np.nan, '', regex=True)
        filtered_df['Emails from other domains'] = filtered_df['Emails from other domains'].replace(np.nan, '', regex=True)
    filtered_df = filtered_df.reset_index(drop=True)
    return filtered_df, r

# clearing mail duplicates - no more than 5
def dupl(filtered_df, F, r):
    mail = ''
    mail2 = ''
    first = ''
    second = ''
    web = ''
    i = 0

    for index, row in filtered_df.iterrows():
        if row[r]:
            mail = row[r].split("@")[0]
        elif F == 2:
            mail2 = row[filtered_df.columns.get_loc('Emails from other domains')].split("@")[0]

        if i > 3:
            if first == mail and web == row[0]:
                filtered_df = filtered_df.drop(index)
                continue
            elif F == 2 and second == mail2 and web == row[0]:
                filtered_df = filtered_df.drop(index)
                continue

        if mail and first != mail:
            first = mail
            web = row[0]
            i = 0
        elif F == 2 and mail2 and second != mail2:
            second = mail2
            web = row[0]
            i = 0
        else:
            i = i + 1
    return filtered_df

# setting 1 : filter after a criteria in e-mail or job title
def filterFiles(filterCriteriaFileName):
    headers = pd.read_csv("Merged.csv")
    fin = pd.DataFrame(columns=headers.columns)

    filter = pd.read_csv(filterCriteriaFileName)
    flist = list(filter.columns)
    flist.pop()
    F = 0
    for file in os.listdir(os.path.dirname(os.path.abspath(__file__))):
        if file.endswith(".csv") and file != "filter.csv":
            print(file)

            if "Merged_Generic.csv" in file:
                F = F + 1
                gen = pd.read_csv(file)
                gen['Generic Company Email Address'] = gen['Generic Company Email Address'].replace(np.nan, '', regex=True)
                for x in flist:
                    x = x.lower()
                    gen = gen[gen['Generic Company Email Address'].str.contains(x)]
                gen['Generic Company Email Address'] = gen['Generic Company Email Address'].replace('', np.nan, regex=True)

            if "Merged_Other.csv" in file:
                F = F + 1
                o = pd.read_csv(file)
                o['Other Company Email Address'] = o['Other Company Email Address'].replace(np.nan, '', regex=True)
                o['Emails from other domains'] = o['Emails from other domains'].replace(np.nan, '', regex=True)
                for x in flist:
                    x = x.lower()
                    o = o[o['Other Company Email Address'].str.contains(x) | o['Emails from other domains'].str.contains(x)]
                o['Other Company Email Address'] = o['Other Company Email Address'].replace('', np.nan, regex=True)
                o['Emails from other domains'] = o['Emails from other domains'].replace('', np.nan, regex=True)

            if "Merged_Personal.csv" in file:
                F = F + 1
                pers = pd.read_csv(file)
                pers['Job Title'] = pers['Job Title'].replace(np.nan, '', regex=True)
                for x in flist:
                    pers = pers[pers['Job Title'].str.contains(x)]
                pers['Job Title'] = pers['Job Title'].replace('', np.nan, regex=True)

            # export as one .csv file
            if F == 3:
                fin = pd.concat([fin,gen]).drop_duplicates().reset_index(drop=True)
                fin = pd.concat([fin,o]).drop_duplicates().reset_index(drop=True)
                fin = pd.concat([fin,pers]).drop_duplicates().reset_index(drop=True)
                fin = fin.dropna(how='all', axis=1)
                fin.to_csv("Merged_Customed_Filtered.csv", index=False)

# drop duplicates from every files marked with _Personal, _Generic, _Other
def dropDupl():
    for file1 in os.listdir(os.path.dirname(os.path.abspath(__file__))):
        if file1.endswith(".csv") and file1 != "filter.csv" and ("_Personal" in file1 or "_Generic" in file1 or "_Other" in file1):
            for file2 in os.listdir(os.path.dirname(os.path.abspath(__file__))):
                if  file2.endswith(".csv") and file2 != "filter.csv" and ("_Personal" in file2 or "_Generic" in file2 or "_Other" in file2) and file2 != file1:
                    f1 = pd.read_csv(file1)
                    f2 = pd.read_csv(file2)

                    if "_Personal" in file2 and "_Personal" not in file1:
                        if "_Generic" in file1:
                            f1 = f1[~f1['Generic Company Email Address'].isin(f2['Personal Email Address'])]
                            f1.to_csv(file1, index=False)
                        elif "_Other" in file1:
                            f1 = f1[~f1['Emails from other domains'].isin(f2['Personal Email Address'])]
                            f1 = f1[~f1['Other Company Email Address'].isin(f2['Personal Email Address'])]
                            f1.to_csv(file1, index=False)

                    else:
                        if 'Personal Email Address' in f1.columns:
                            if 'Generic Company Email Address' in f2.columns:
                                f1 = f1[~f1['Personal Email Address'].isin(f2['Generic Company Email Address'])]
                                f1.to_csv(file1, index=False)
                            elif 'Emails from other domains' in f2.columns:
                                f1 = f1[~f1['Personal Email Address'].isin(f2['Emails from other domains'])]
                                f1 = f1[~f1['Personal Email Address'].isin(f2['Other Company Email Address'])]
                                f1.to_csv(file1, index=False)
                        elif 'Generic Company Email Address' in f1.columns:
                            if 'Personal Email Address' in f2.columns:
                                f1 = f1[~f1['Generic Company Email Address'].isin(f2['Personal Email Address'])]
                                f1.to_csv(file1, index=False)
                            elif 'Emails from other domains' in f2.columns:
                                f1 = f1[~f1['Generic Company Email Address'].isin(f2['Emails from other domains'])]
                                f1 = f1[~f1['Generic Company Email Address'].isin(f2['Other Company Email Address'])]
                                f1.to_csv(file1, index=False)
                        elif 'Emails from other domains' in f1.columns:
                            if 'Personal Email Address' in f2.columns:
                                f1 = f1[~f1['Emails from other domains'].isin(f2['Personal Email Address'])]
                                f1 = f1[~f1['Other Company Email Address'].isin(f2['Personal Email Address'])]
                                f1.to_csv(file1, index=False)
                            elif 'Generic Company Email Address' in f2.columns:
                                f1 = f1[~f1['Emails from other domains'].isin(f2['Generic Company Email Address'])]
                                f1 = f1[~f1['Other Company Email Address'].isin(f2['Generic Company Email Address'])]
                                f1.to_csv(file1, index=False)

if __name__ == "__main__":
    main(sys.argv[1:])

    