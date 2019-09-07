# foorumi

Tietokantasovellus -kurssin harjoitustyö.

[Sovellus toiminnassa herokussa](https://still-everglades-81805.herokuapp.com)

[Tietokantakaavio](dokumentaatio/Tietokantakaavio.png)

[User Stories](dokumentaatio/UserStories.md)

## Kuvaus

Keskustelufoorumisovellus yhteisön sisäiseen käyttöön.

Käyttäjä voi lukea fooruminsa kirjoituksia (viestejä) ja lisätä uusia kirjoituksia, jotka voivat olla myös vastauksia aiempiin viesteihin. Kirjoituksia voi hakea kirjoittajan nimen tai ryhmän tai kirjoituksen aiheen tai iän perusteella. Lukija voi myös seurata viestiketjuja.

Käyttäjän tulee olla kirjautunut sovellukseen nähdäkseen viestit tai lisätäkseen niitä. Oletusarvoisesti lukijalle näytetään tuoreimmat kirjoitukset. Käyttäjä näkee onko lukenut viestin, ja ovatko kaikki muut foorumin käyttäjät lukeneet viestin. Tieto siitä,ketkä ovat lukeneet viestin, on nähtävissä kaikille kirjautuneille käyttäjille.

Kirjautuneilla Käyttäjillä on pääsy myös tilastonäkymään. Siinä näytetään, miten kirjoitukset jakautuvat eri aiheiden kesken, miten eri ryhmien jäsenten kirjoitukset jakautvat aiheittain, sekä aktiivisimmin kirjoittavat käyttäjät ja ryhmät.

Sovellusta käyttöönotettaessa sille luodaan ylläpitäjä-tunnus. Foorumin ylläpitäjällä on oma näkymä, josta ylläpidetään foorumin ryhmiä ja käyttäjien kuulumista niihin, sekä määritellään aiheita, joiden perusteella kirjoituksia voidaan merkitä ja hakea. Foorumin ylläpitäjä voi myös poistaa tai muokata asiattomia viestejä.
