# foorumi

Tietokantasovellus -kurssin harjoitustyö.

[Tietokantakaavio](dokumentaatio/Tietokantakaavio.png)

## Kuvaus

Keskustelufoorumisovellus. Sovelluksella voi luoda yhteisön sisäiseen käyttöön tarkoitettuja foorumeita ja käyttää niitä. Foorumit ovat erillisiä toisistaan, käyttäjän on luotava erillinen käyttäjätunnus kuhunkin foorumiin, johon hän liittyy.

Käyttäjä voi lukea fooruminsa kirjoituksia (viestejä) ja lisätä uusia kirjoituksia, jotka voivat olla myös vastauksia aiempiin viesteihin. Kirjoituksia voi hakea kirjoittajan nimen tai kirjoituksen aiheen tai iän perusteella. Lukija voi myös seurata viestiketjuja.

Käyttäjän tulee olla kirjautunut sovellukseen nähdäkseen viestit tai lisätäkseen niitä. Oletusarvoisesti lukijalle näytetään tuoreimmat kirjoitukset. Käyttäjä näkee onko lukenut viestin, ja ovatko kaikki muut foorumin käyttäjät lukeneet viestin. Tieto siitä,ketkä ovat lukeneet viestin, on nähtävissä kaikille kirjautuneille käyttäjille.

Kirjautuneilla Käyttäjillä on pääsy myös tilastonäkymään. Siinä näytetään, miten kirjoitukset jakautuvat eri aiheiden kesken, miten eri ryhmien jäsenten kirjoitukset jakautvat aiheittain, sekä aktiivisimmin kirjoittavat käyttäjät ja ryhmät.

Foorumia luotaessa sille luodaan ylläpitäjä-tunnus. Foorumin ylläpitäjällä on oma näkymä, josta ylläpidetään foorumin käyttäjien tietoja, kuulumista eri ryhmiin, ja määritellään aiheita, joiden perusteella kirjoituksia voidaan merkitä ja hakea.

### Toimintoja:

- Foorumin perustaminen
- Käyttäjän lisääminen foorumiin
- Kirjautuminen
- Viestien näyttäminen (oletusnäkymä, erilaiset haut)
- Viestin lisääminen (erillisenä ja vastauksena)
- Tilastonäkymän näyttäminen
- Käyttäjätietojen muokkaaminen
- Ryhmien lisääminen , muokkaus ja poistaminen,
- Ryhmäjäsenyyden lisääminen ja poistaminen
- Viestin poistaminen
- Aiheiden määrittely, muokkaus ja poisto
