# Käyttöohje

## Asentaminen

### Sovelluksen asentaminen Herokuun

Sovellusta Herokuun asennettaessa on Herokuun asetettava ympäristömuuttuja HEROKU ja otettava Herokussa käyttöön PostgreSQL-tietokanta. Muutoin toimitaan kuten yleensäkin sovelluksia herokuun asennettaessa.

### Sovelluksen asentaminen muualle kuin Herokuun

Mitään ympäristömuuttujia ei tarvita. Sovelluksen riippuvuudet on asennettava requirements.txt -tiedostosta komennolla pip install -r requirements.txt . Sovellus käynnistyy antamalla sovelluksen hakemistossa komento python3 run.py . Muualla kuin Herokussa sovellus käyttää SQLite-tietokantaa.

### Ylläpitäjän tunnuksen luominen

Kun sovellus käynnistetään ensimmäisen kerran, se luo itselleen tietokannan. Ensimmäiseksi on luotava ylläpitäjän käyttäjätunnus (valikon kohta "Lisää käyttäjä"). Ylläpitäjälle on annettava tunnus ja salasana. Ensimmäisen käyttäjän jälkeen luotavat käyttäjät ovat tavallisia käyttäjiä, joilla ei ole ylläpitäjän oikeuksia.
