# FreelanceFlow


## Koraci za pokretanje projekta
### Git
```
# Setup
git clone https://github.com/svantip/FreelanceFlow/
cd FreelanceFlow
git checkout [svan/deni]-branch
git branch
# Sinkroniziranje promjena sa brancha ili maina
git pull origin main

# Commitanje
git add file1 file2
git commit -m "Description of what you changed"
git push origin [svan/deni]-branch

# Merganje
git pull origin main
git merge main

# Konflikti
git add resolved-file
git rebase --continue
```
### Postavljanje virtualnog okruzenja
```
# Windows:
python -m venv venv
venv\Scripts\activate

# macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```
### Instaliranje python zavisnosti
```
pip install -r requirements.txt
```
### Prvi terminal - hot reload
```
python manage.py tailwind build
python manage.py tailwind start
```
### Drugi terminal - django server
```
python manage.py runserver
```

## Additional Requirements
- Tailwind CSS (`npm install tailwindcss`)



## Faze
1. **faza**: Korisnik može kreirati, uređivati, brisati i pregledavati projekte i zadatke. Također, može se registrirati i prijaviti u sustav. Sustav se sastoji od web poslužitelja i relacijske baze podataka.

3. **faza**: Korisniku je omogućena napredna upravljačka ploča za pretraživanje i filtriranje projekata i zadataka te generiranje jednostavnih tjednih izvještaja o broju dovršenih zadataka. Za optimizaciju performansi koristi se sustav za predmemoriju (Redis), uz postojeće web poslužitelj i relacijsku bazu podataka.

5. **faza**: Aplikacija uvodi obavijesti u stvarnom vremenu o nadolazećim rokovima i promjenama na zadacima, sustav za prikupljanje logova korisničkih aktivnosti te obradu podataka u stvarnom vremenu. Dodani su NoSQL baza podataka za logove i polustrukturirane podatke te sustav za strujanje podataka za obradu u stvarnom vremenu.

7. **faza AI**: Implementiraju se AI funkcionalnosti poput prediktivne analitike za procjenu rokova projekta, preporuka zadataka i potencijalnih suradnika te analize sentimenta povratnih informacija korisnika.
