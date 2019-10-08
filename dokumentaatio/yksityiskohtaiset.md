# Yksityiskohtaiset käyttötapaukset

Automaattisesti generoitavat SQL-kyselyt on tässä esitetty siinä muodossa kuin ne toteutetaan SQLite-tietokantaan. Käsin tehdyt kyselyt ovat siinä muodossa kuin ne ovat koodissa.

## Foorumin käyttäjänä (yhteisön jäsenenä) haluan...

### lukea viestejä

Viestin sisällön ja kaikki viestiin liittyvät tiedot ovat nähtävissä viestin omalla sivulla /viestit/<viesti_id>

Viestin sisältö, perustiedot ja kirjoittajan nimi haetaan seuraavalla SQL-kyselyllä:

Lisäksi haetaan erillisillä kyselyillä tieto siitä, ovatko kaikki käyttäjät lukeneet viestin, viestistä, johon näytettävä viesti on vastaus (jos viesti on vastaus) samat tiedot kuin viestien listassa näytetään ja näytettävään viestiin kirjoitetuista vastauksista samat tiedot kuin viestien listauksessa näytetään. Näihin tarvittavat kyselyt on esitelty kohdissa "Haluan nähdä ovatko kaikki käyttäjät lukeneet viestin", "Haluan nähdä mihin viestiin viesti on vastaus" ja "Haluan nähdä viestiin kirjoitetut vastaukset".

Itse viesti ja kirjoittajan nimi haetaan SQL-kyselyllä

```
SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika, viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko, viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id, viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id, kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus, kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash", kayttaja_1.admin AS kayttaja_1_admin
FROM viesti LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE viesti.id = ?
```

Jos kirjautunut käyttäjä ei ole aiemmin lukenut viestiä, hänet lisätään lukijoiden luetteloon SQL-kyselyllä

```
INSERT INTO luetut (viesti_id, lukija_id) VALUES (?, ?)
```

### Haluan nähdä uusimmat viestit tarvitsematta ensin hakea niitä, jotta voin lukea niitä

Viestien listaus on saatavilla osoitteessa /viestit . Viestit listataan oletuksena aikajärjestyksessä uusin ensin. Tietokannasta haetaan ja näytetään 20 viestiä kerrallaan.

Viestit haetaan SQL-kyselyllä

```
SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika, viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko, viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id, viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id, kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus, kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash", kayttaja_1.admin AS kayttaja_1_admin
FROM viesti LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id ORDER BY viesti.kirjoitusaika DESC
LIMIT ? OFFSET ?

```

Paginate-oliossa on tieto sivujen kokonaismäärästä, joka selviää SQL-kyselyllä

```
SELECT count(*) AS count_1
FROM (SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika, viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko, viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id, viesti.vastattu_id AS viesti_vastattu_id
```

Lisäksi haetaan jokaista viestiä kohden erikseen tieto siitä, onko käyttäjä lukenut viestin ja ovatko kaikki käyttäjät lukeneet viestin. Tähän tarvittavat kyselyt on eritelty käyttötapausten "haluan nähdä olenko jo lukenut viestin" ja "haluan nähdä ovatko kaikki käyttäjät lukeneet viestin" alla.

### haluan hakea tiettyä aihetta käsitteleviä viestejä, jotta voin lukea niitä

Viestejä listaavalla sivulla avautuu hakulomake, jolla viestejä voi hakea mm. aiheen perusteella. Hakutuloksia näytetään 20 viestin erissä kirjoitusajan mukaan järjestettyinä uusin ensin.

Kun haetaan pelkän aiheen perusteella, käytetään seuraavaa SQL-kyselyä:

```

SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika, viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko, viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id, viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id, kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus, kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash", kayttaja_1.admin AS kayttaja_1_admin
FROM viesti JOIN viestiaihe AS viestiaihe_1 ON viesti.id = viestiaihe_1.viesti_id JOIN aihe ON aihe.id = viestiaihe_1.aihe_id LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE aihe.aihe = ? ORDER BY viesti.kirjoitusaika DESC
LIMIT ? OFFSET ?

```

Tämän lisäksi tehdään vielä jokaista näytettävää viestiä kohden kyselyt, joilla selvitetään ovat kaikki käyttäjät lukeneet viestin. Nämä kyselyt on eritelty kohdassa "haluan nähdä ovatko kaikki käyttäjät lukeneet viestin".

### hakea tietyn ryhmän jäsenten jättämiä viestejä, jotta voin lukea niitä

Viestejä listaavalla sivulla avautuu hakulomake, jolla viestejä voi hakea mm. kirjoittajan ryhmän perusteella. Hakutuloksia näytetään 20 viestin erissä kirjoitusajan mukaan järjestettyinä uusin ensin.

Kun haetaan pelkän kirjoittajan ryhmän perusteella, käytetään seuraavaa SQL-kyselyä:

```

SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika, viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko, viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id, viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id, kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus, kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash", kayttaja_1.admin AS kayttaja_1_admin
FROM viesti JOIN kayttaja ON kayttaja.id = viesti.kirjoittaja_id JOIN kayttajaryhma AS kayttajaryhma_1 ON kayttaja.id = kayttajaryhma_1.kayttaja_id JOIN ryhma ON ryhma.id = kayttajaryhma_1.ryhma_id LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE ryhma.nimi = ? ORDER BY viesti.kirjoitusaika DESC
LIMIT ? OFFSET ?

```

Tämän lisäksi tehdään vielä jokaista näytettävää viestiä kohden kyselyt, joilla selvitetään ovat kaikki käyttäjät lukeneet viestin. Nämä kyselyt on eritelty kohdassa "haluan nähdä ovatko kaikki käyttäjät lukeneet viestin".

### hakea tietyn käyttäjän kirjoittamia viestejä, jotta voin lukea niitä

Viestejä listaavalla sivulla avautuu hakulomake, jolla viestejä voi hakea mm. kirjoittajan nimen perusteella. Hakutuloksia näytetään 20 viestin erissä kirjoitusajan mukaan järjestettyinä uusin ensin.

Kun haetaan pelkän kirjoittajan nimen perusteella, käytetään seuraavaa SQL-kyselyä:

```

SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika, viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko, viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id, viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id, kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus, kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash", kayttaja_1.admin AS kayttaja_1_admin
FROM viesti JOIN kayttaja ON kayttaja.id = viesti.kirjoittaja_id LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE kayttaja.nimi = ? ORDER BY viesti.kirjoitusaika DESC
LIMIT ? OFFSET ?

```

Tämän lisäksi tehdään vielä jokaista näytettävää viestiä kohden kyselyt, joilla selvitetään ovat kaikki käyttäjät lukeneet viestin. Nämä kyselyt on eritelty kohdassa "haluan nähdä ovatko kaikki käyttäjät lukeneet viestin".

### hakea tietyllä aikavälillä kirjoitettuja viestejä, jotta voin lukea niitä

Viestejä listaavalla sivulla avautuu hakulomake, jolla viestejä voi hakea mm. aikavälin perusteella. Haussa voi määritellä päivän, jona kirjoitetuista alkaen viestejä haetaan ja/tai päivän jona kirjoitettuihin asti haetaan. Hakutuloksia näytetään 20 viestin erissä kirjoitusajan mukaan järjestettyinä uusin ensin.

Kun haetaan tietyltä aikaväliltä eli on määritelty sekä haun alkupäivä että haun viimeinen päivä, käytetään seuraavaa SQL-kyselyä:

```

SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika, viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko, viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id, viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id, kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus, kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash", kayttaja_1.admin AS kayttaja_1_admin
FROM viesti LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE viesti.kirjoitusaika >= ? AND viesti.kirjoitusaika <= ? ORDER BY viesti.kirjoitusaika DESC
LIMIT ? OFFSET ?

```

Tämän lisäksi tehdään vielä jokaista näytettävää viestiä kohden kyselyt, joilla selvitetään ovat kaikki käyttäjät lukeneet viestin. Nämä kyselyt on eritelty kohdassa "haluan nähdä ovatko kaikki käyttäjät lukeneet viestin".

### haluan yhdistelllä erilaisia hakuja

Viestejä listaavalla sivulla avautuu hakulomake, jolla viestejä voi hakea aiheen, kirjoittajan nimen, kirjoittajan ryhmän ja aikavälin (alkamisajankohdan ja loppumisajankohdan) perusteella. Näitä kyselyitä voi vapaasti yhdistellä, kuitenkin niin, että kullakin hakutyypillä on vain yksi hakuarvo. Hakutuloksia näytetään 20 viestin erissä kirjoitusajan mukaan järjestettyinä uusin ensin.

Kun haetaan kaikilla hakutyypeillä yhtaikaisesti, käytetään seuraavaa SQL-kyselyä:

```

SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika, viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko, viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id, viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id, kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus, kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash", kayttaja_1.admin AS kayttaja_1_admin
FROM viesti JOIN viestiaihe AS viestiaihe_1 ON viesti.id = viestiaihe_1.viesti_id JOIN aihe ON aihe.id = viestiaihe_1.aihe_id JOIN kayttaja ON kayttaja.id = viesti.kirjoittaja_id JOIN kayttajaryhma AS kayttajaryhma_1 ON kayttaja.id = kayttajaryhma_1.kayttaja_id JOIN ryhma ON ryhma.id = kayttajaryhma_1.ryhma_id LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE aihe.aihe = ? AND kayttaja.nimi = ? AND ryhma.nimi = ? AND viesti.kirjoitusaika >= ? AND viesti.kirjoitusaika <= ? ORDER BY viesti.kirjoitusaika DESC
LIMIT ? OFFSET ?

```

Tämän lisäksi tehdään vielä jokaista näytettävää viestiä kohden kyselyt, joilla selvitetään ovat kaikki käyttäjät lukeneet viestin. Nämä kyselyt on eritelty kohdassa "haluan nähdä ovatko kaikki käyttäjät lukeneet viestin".

### haluan nähdä olenko jo lukenut viestin

Viestien listauksessa ja yksittäisen viestin sivulla vastatun viestin ja viestiin kirjoitettujen vastausten kohdalla näytetään, onko kirjautunut käyttäjä lukenut viestin. Tämä tieto haetaan seuraavilla SQL-kyselyillä:

### haluan nähdä ovatko kaikki muut jo lukeneet viestin

Viestien listauksessa ja yksittäisen viestin sivulla itse viestin,vastatun viestin ja viestiin kirjoitettujen vastausten kohdalla näytetään, ovatko kaikki käyttäjät lukeneet viestin. Tämä tieto haetaan seuraavilla SQL-kyselyillä:

Haetaan käyttäjien kokonaismäärä:

### nähdä ketkä ovat lukeneet viestin

Yksittäisen viestin sivulla näytetään niiden käyttäjien nimet, jotka ovat jo lukeneet viestin. Nämä haetaan seuravalla SQL-kyselyllä:

```

SELECT kayttaja.id AS kayttaja_id, kayttaja.nimi AS kayttaja_nimi, kayttaja.tunnus AS kayttaja_tunnus, kayttaja."salasanaHash" AS "kayttaja_salasanaHash", kayttaja.admin AS kayttaja_admin
FROM kayttaja, luetut
WHERE ? = luetut.viesti_id AND kayttaja.id = luetut.lukija_id

```

### nähdä viestiin kirjoitetut vastaukset, jotta voin seurata viestiketjua

Yksittäisen viestin sivulla listataan viestille kirjoitettujen vastausten otsaketiedot linkkeinä, joista pääsee kyseisen viestin sivulle. Tiedot haetaan seuraavalla SQL-kyselyllä:

```

2019-10-08 12:30:56,269 INFO sqlalchemy.engine.base.Engine (2,)
2019-10-08 12:30:56,272 INFO sqlalchemy.engine.base.Engine SELECT aihe.id AS aihe_id, aihe.aihe AS aihe_aihe
FROM aihe, viestiaihe
WHERE ? = viestiaihe.viesti_id AND aihe.id = viestiaihe.aihe_id
2019-10-08 12:30:56,272 INFO sqlalchemy.engine.base.Engine (15,)
2019-10-08 12:30:56,275 INFO sqlalchemy.engine.base.Engine SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika, viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko, viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id, viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id, kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus, kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash", kayttaja_1.admin AS kayttaja_1_admin
FROM viesti LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE ? = viesti.vastattu_id

```

### nähdä mihin viestiin viesti on vastannut, jotta voin seurata viestiketjua taaksepäin

```

```

### kirjoittaa viestin, jotta muut voivat lukea sen

Aluksi haetaan luettelo kaikista valittavissa olevista aihetunnisteista seuraavalla SQL-kyselyllä:

```

SELECT aihe.id AS aihe_id, aihe.aihe AS aihe_aihe
FROM aihe ORDER BY aihe.aihe

```

Tämä tehdään sekä luotaessa lomaketta, johon vastaus kirjoitetaan, että (syötteen validointia varten) otettaessa uutta viestiä vastaan.

```

```

### vastata toisen käyttäjän viestiin, jotta toinen käyttäjä ja muut voivat lukea sen

Yksittäisen viestin näkymässä avautuu lomake, johon vastausviesti kirjoitetaan.

ALuksi haetaan luettelo kaikista valittavissa olevista aihetunnisteista seuraavalla SQL-kyselyllä, ks. erittely ja syyt yllä.

Vastauksen tallentaminen tietokantaan tapahtuu seuraavalla SQL-kyselyllä:

```

```

### kirjautua sisään foorumiin, jotta kirjoittamani viestit tunnistuvat minun (ja ryhmäni jäsenen) kirjoittamikseni ja näen mitkä viestit olen jo lukenut

```

```

### nähdä olenko kirjautuneena

Kirjautuneen käyttäjän nimi on esillä kaikilla sivuilla (navigaatiopalkissa), silloin kun käyttäjä on kirjautuneena.

Nimi haetaan SQL-kyselyllä

```

SELECT kayttaja.id AS kayttaja_id, kayttaja.nimi AS kayttaja_nimi, kayttaja.tunnus AS kayttaja_tunnus, kayttaja."salasanaHash" AS "kayttaja_salasanaHash", kayttaja.admin AS kayttaja_admin
FROM kayttaja
WHERE kayttaja.id = ?

```

### luoda itselleni käyttäjätunnuksen, jotta voin käyttää foorumia

```

```

### vaihtaa salasanani

```

```

### merkitä viestini aihetunnisteilla, jotta niistä kiinnostuneet löytävät ne helpommin

```

```

### nähdä mitä aihetunnisteita foorumissa on jo käytössä

```

```

### luoda uusia aihetunnisteita, jotta voin liittää viestiini sopivan aihetunnisteen

```

```

### nähdä mitä ryhmiä foorumissa on

```

```

### nähdä, keitä ryhmiin kuuluu

```

```

### nähdä tilastoja foorumin käytöstä

- kaikkien kirjoitusten jakautuminen eri aiheiden kesken
- eri ryhmien jäsenten kirjoitusten jakautuminen aiheittain
- aktiivisimmin kirjoittavat käyttäjät
- aktiivisimmin kirjoittavat ryhmät

## Foorumin ylläpitäjänä haluan lisäksi...

- poistaa tai muokata asiattomia viestejä
- hallita käyttäjien jäsenyyksiä ryhmissä
  - luoda ryhmiä
  - liittää käyttäjän ryhmään
  - poistaa käyttäjän ryhmästä
  - muokata ryhmän nimeä
  - poistaa ryhmiä
- hallita aihetunnisteita

  - muokata aihetunnisteita
  - poistaa aihetunnisteita

- luoda itselleni ylläpitäjän tunnuksen foorumia käyttöönotettaessa

```

```

```

```
