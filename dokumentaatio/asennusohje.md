# Asennusohje

Foorumi on python-ohjelmisto, jonka voit asentaa paikallisesti kehitysversiona tai tuotantoversiona Herokuun tai muuhun pilvipalveluun.

## Sovelluksen asentaminen paikallisesti

Kloonaa repositorio tai lataa sovelluksen lähdekoodi koneellesi. Anna seuraavat komennot sovelluksen hakemistossa. Tässä oletetaan, että koneellesi on jo asennettuna python3.

Luo sovellukselle virtuaaliympäristö komennolla `python3 -m venv venv`

Aktivoi virtuaaliympäristö komennolla `source venv/bin/activate`

Asenna sovelluksen riippuvuudet komennolla `pip install -r requirements.txt`

Käynnistä sovellus komennolla `python run.py`

Paikallisesti asennettuna sovellus käyttää SQLite-tietokantaa. Sovellus luo tietokantatiedoston omaan hakemistoonsa, kun sovellus käynnistetään ensimmäistä kertaa.

## Sovelluksen asentaminen Herokuun

Kloonaa repositorio ja anna seuraavat komennot sovelluksen hakemistossa. Tässä oletetaan, että koneellesi on jo asennettuna heroku-cli ja git.

Luo Herokuun paikka sovellukselle heroku-cli:n komennolla `heroku create antamasinimi` (tai Herokun web-käyttöliittymästä).

Ota Herokussa käyttöön PostgreSQL-tietokanta komennolla `heroku addons:add heroku-postgresql:hobby-dev`

Aseta Herokuun ympäristömuuttuja HEROKU komennolla `heroku config:set HEROKU=1`

Yhdistä kloonaamasi repositorio herokuun komennolla `git remote add heroku https://heroku.com/antamasinimi`

Lataa sovellus Herokuun komennolla `git push heroku master`

Jos asennat sovelluksen muuhun pilvipalveluun kuin Herokuun, noudata valitsemasi palvelun ohjeita. Aseta ympäristömuuttuja HEROKU, vaikka käyttäisit muuta pilvipalvelua. Aseta tarvittaessa myös ympäristömuuttuja DATABASE_URL osoittamaan käyttämääsi PostgreSQL-tietokantaa. (Heroku asettaa tämän muuttujan automaattisesti.)

## Ylläpitäjän tunnuksen luominen

Kun sovellus käynnistetään ensimmäisen kerran, on aluksi luotava ylläpitäjän käyttäjätunnus (valikon kohta "Lisää käyttäjä"). Ylläpitäjälle on annettava tunnus ja salasana. Ensimmäisen käyttäjän jälkeen luotavat käyttäjät ovat tavallisia käyttäjiä, joilla ei ole ylläpitäjän oikeuksia.
