Scriptul sterge emailurile din campania aleasa.

Campania trebuie sa aiba numele legat sau cu underscore: Nume_Campanie.

fisier_cu_domenii_de_sters.csv contine intr-o coloana toate domeniile care trebuie sterse din Nume_Campanie.
Exemplu: test1.csv

Rularea este: python3 reaply.py Nume_Campanie fisier_cu_domenii_de_sters.csv fisier_cu_toate_emailurile_de_pe_reply.csv

La rulare daca apare alt cod decat 200 inseamna ca este o problema in comunicarea cu API-ul, dar scriptul nu se va opri va continua
cu celelalte domenii.
Ex.: nu e scris corect domeniul sau nu mai exista
      nu e scris corect numele companiei
Orice alt motiv de oprire al scriptului e o problema la comunicarea cu API ul sau la input
