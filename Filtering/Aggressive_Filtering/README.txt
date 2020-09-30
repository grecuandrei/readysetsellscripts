	Grecu Andrei George ®2020 Automatica&Calculatoare@UPB

		Aggressive Filtering (ONLY for .csv files)
	
	Prerequisites:
		python 3.6 or above (check: python3 --verion)
		pip 9.0.1 or above (generally installed with python | check: pip3 --version)
		pandas 1.0.5 or above (command: pip3 install pandas | check: pip3 list | look for pandas)
		tldextract 2.2.2 or above (command: pip3 install pandas | check: pip3 list | look for tldextract)
		numpy 1.18.1 or above (command: pip3 install numpy | check: pip3 list | look for numpy)

	Usage:
		python3 csvv.py filter.csv 0(or 1 or 2)

		For the script to WORK it needs to be (with filter.csv also) in the SAME DIRECTORY as the .csv
			files you want to filter.

		filter.csv = file that contains additional COLUMNS that need to pe printed in output
			Used like this: ,    				(when empty - for 0 setting) (default)
					Job Title, Company Name,	(with filters)

		____Settings____

		0 = 	used for selecting if you just want to merge initial files and split them in three
			categories (and the corresponding .csv files) : Personal, Generic and Other
			
			(REMEMBER to empty, or update with according columns, the filter.csv if the script
			was used already with the 1 setting, as it does NOT work with filters from 1)

		1 =	used for selecting only the important data you enter in filter.csv
				e.g: Let's say you want only managers=> put in filter.csv 	Manager,
					And the output will be one file .csv that contains:
					->For Personal the entries with Manager as Job Title
					->For the Generic and Other, entries with "manager" in e-mail
			
			(REMEMBER to update filter.csv as it does not work with columns from 0)

		2 =	drops duplicates from every files marked with _Personal, _Generic, _Other and keeps
			the entries with priority in Personal, then Other, then Generic
				e.g: Let's say you have office@acr.ro both in Personal file and Generic/Other
				This setting gets rid of the entry from Generic/Other and keeps it in Personal
 
	Output:
		After 0 setting:
			Merged.csv
			Merged_Personal.csv
			Merged_Generic.csv
			Merged_Other.csv

		After 1 setting:
			Merged_Customed_Filtered.csv

		After 2 settign:
			The files will be saved in place (same files)













