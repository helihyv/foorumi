# foorumi

Tietokantasovellus -kurssin harjoitustyö.

[Sovellus toiminnassa herokussa](https://still-everglades-81805.herokuapp.com)

Sovelluksessa on Herokussa valmiina testikäyttäjiä:

- tunnus kraakku salasanalla tsohakraakku (ylläpitäjä)
- tunnus otso salasanalla tsohaotso (tavallinen käyttäjä)
- tunnus meri salasanalla tsohameri (tavallinen käyttäjä)

Tavallisia käyttäjiä voi luoda itse lisää valikon linkistä "Lisää käyttäjä".

[Asennusohje](dokumentaatio/asennusohje.md)

[Käyttöohje](dokumentaatio/ohje.md)

[Tietokantakaavio](dokumentaatio/Tietokantakaavio.png)

[Tietokannan rakenne](dokumentaatio/tietokannan_rakenne.md) (Sisältää CREATE TABLE -lauseet.)

[User Stories](dokumentaatio/UserStories.md)

[Yksityiskohtaiset User Storyt](dokumentaatio/yksityiskohtaiset_user_storyt.md) (Sisältää käytetyt SQL-kyselyt.)

[Jatkokehitysideoita](dokumentaatio/jatkokehitysideoita.md)

## Kuvaus

Keskustelufoorumisovellus yhteisön sisäiseen käyttöön.

Käyttäjä voi lukea foorumin kirjoituksia (viestejä) ja lisätä uusia kirjoituksia, jotka voivat olla myös vastauksia aiempiin viesteihin. Kirjoituksia voi hakea kirjoittajan nimen tai ryhmän tai kirjoituksen aiheen tai iän perusteella. Lukija voi myös seurata viestiketjuja.

Käyttäjän tulee olla kirjautunut sovellukseen nähdäkseen viestit tai lisätäkseen niitä. Oletusarvoisesti lukijalle näytetään tuoreimmat kirjoitukset. Käyttäjä näkee onko lukenut viestin, ja ovatko kaikki muut foorumin käyttäjät lukeneet viestin. Tieto siitä, ketkä ovat lukeneet viestin, on nähtävissä kaikille kirjautuneille käyttäjille.

Kirjautunut käyttäjä voi myös lisätä sovellukseen aiheita, joiden perusteella kirjoituksia voidaan merkitä ja hakea. Käyttäjän tulee olla kirjautunut sovellukseen nähdäkseen foorumin aiheet, ryhmät ja ryhmien jäsenet.

Kirjautuneilla käyttäjillä on pääsy myös tilastonäkymään. Siinä näytetään eniten viestejä kirjoittaneet käyttäjät ja ryhmät, suosituimmat aiheet ja se, miten ryhmien kirjoitukset jakautuvat eri aiheiden kesken.

Sovellusta käyttöönotettaessa sille luodaan ylläpitäjän tunnus. Foorumin ylläpitäjä voi perustaa foorumille ryhmiä, lisätä niihin käyttäjiä, poistaa niistä käyttäjiä ja poistaa ryhmiä. Ylläpitäjä voi muokata ja poistaa foorumilla käytössä olevia aiheita. Foorumin ylläpitäjä voi myös poistaa ja muokata asiattomia viestejä.
