Descriere scripturi

Pentru a iesi un rezultat bun acestea se folosesc in ordinea in care a fost descrisa mai jos:

Webscraper pt membrii grupului
modifyNmaeHref_about_fromFb.py pt a scoate hreful corect cu "/about",
Se ia toata lista din output si se pune in sitemapul de webscraper intre [] de la startUrl
merge.py pentru a uni datele din members cu cele din about
scrapeForLinkedIn.py pentru output final

modifyNameHref_about_fromFb.py
	- modifica name-reful din fisier pregatind-ul pentru LinkedIn search

	- utilizare: python3 modifyNameHref_about_fromFb.py fisier.csv

merge.py
	- pune datele (work, education, location) din al doilea fisier in primul fisier(care contine name,
		job_or_location, href)
	
	- utilizare: python3 merge.py fisier_cu_membrii.csv fisier_cu_about.csv

scrapeForLinkedIn.py

	- cauta LinkedIn-ul la fisierele care contin urmatoarele coloane, in ordine aleatorie:
		name, work, education, location, job_or_location href
	- salveaza rezultatul in fisier_final.csv(daca aterminat scriptul de rulat), si in fisier_partial.csv
		(daca scriptul nu a fost lasat sa se termine)

	- utilizare: python3 scrapeForLinkedIn.py fisier.csv

