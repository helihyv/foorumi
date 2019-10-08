# Yksityiskohtaiset käyttötapaukset

Automaattisesti generoitavat SQL-kyselyt on tässä esitetty siinä muodossa kuin ne toteutetaan SQLite-tietokantaan. Käsin tehdyt kyselyt ovat siinä muodossa kuin ne ovat koodissa.

## Foorumin käyttäjänä (yhteisön jäsenenä)

### Haluan lukea viestejä

Viestin sisällön ja kaikki viestiin liittyvät tiedot ovat nähtävissä viestin omalla sivulla /viestit/<viesti_id>

Viestin sisältö, perustiedot ja kirjoittajan nimi haetaan seuraavalla SQL-kyselyllä:

Lisäksi haetaan erillisillä kyselyillä tieto siitä, ovatko kaikki käyttäjät lukeneet viestin, viestistä, johon näytettävä viesti on vastaus (jos viesti on vastaus) samat tiedot kuin viestien listassa näytetään ja näytettävään viestiin kirjoitetuista vastauksista samat tiedot kuin viestien listauksessa näytetään. Näihin tarvittavat kyselyt on esitelty kohdissa "Haluan nähdä ovatko kaikki käyttäjät lukeneet viestin", "Haluan nähdä mihin viestiin viesti on vastaus" ja "Haluan nähdä viestiin kirjoitetut vastaukset".

Itse viesti ja kirjoittajan nimi haetaan SQL-kyselyllä

```sql
SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika,
viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko,
viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id,
viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id,
kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus,
kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash",
kayttaja_1.admin AS kayttaja_1_admin
FROM viesti
LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE viesti.id = ?
```

Jos kirjautunut käyttäjä ei ole aiemmin lukenut viestiä, hänet lisätään lukijoiden luetteloon SQL-kyselyllä

```sql
INSERT INTO luetut (viesti_id, lukija_id) VALUES (?, ?)
```

### Haluan nähdä uusimmat viestit tarvitsematta ensin hakea niitä, jotta voin lukea niitä

Viestien listaus on saatavilla osoitteessa /viestit . Viestit listataan oletuksena aikajärjestyksessä uusin ensin. Tietokannasta haetaan ja näytetään 20 viestiä kerrallaan.

Viestit haetaan SQL-kyselyllä

```sql
SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika,
viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko,
viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id,
viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id,
kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus,
kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash", kayttaja_1.admin AS kayttaja_1_admin
FROM viesti
LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
ORDER BY viesti.kirjoitusaika DESC
LIMIT ? OFFSET ?

```

Paginate-oliossa on tieto sivujen kokonaismäärästä, joka selviää SQL-kyselyllä

```sql
SELECT count(*) AS count_1
FROM (SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika,
viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko,
viesti.teksti AS viesti_teksti,  viesti.kirjoittaja_id AS viesti_kirjoittaja_id,
viesti.vastattu_id AS viesti_vastattu_id
```

Lisäksi haetaan jokaista viestiä kohden erikseen tieto siitä, onko käyttäjä lukenut viestin ja ovatko kaikki käyttäjät lukeneet viestin. Tähän tarvittavat kyselyt on eritelty käyttötapausten "haluan nähdä olenko jo lukenut viestin" ja "haluan nähdä ovatko kaikki käyttäjät lukeneet viestin" alla.

### Haluan hakea tiettyä aihetta käsitteleviä viestejä, jotta voin lukea niitä

Viestejä listaavalla sivulla avautuu hakulomake, jolla viestejä voi hakea mm. aiheen perusteella. Hakutuloksia näytetään 20 viestin erissä kirjoitusajan mukaan järjestettyinä uusin ensin.

Kun haetaan pelkän aiheen perusteella, käytetään seuraavaa SQL-kyselyä:

```sql
SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika,
viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko,
viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id,
viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id,
kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus,
kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash", kayttaja_1.admin AS kayttaja_1_admin
FROM viesti JOIN viestiaihe AS viestiaihe_1 ON viesti.id = viestiaihe_1.viesti_id
JOIN aihe ON aihe.id = viestiaihe_1.aihe_id
LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE aihe.aihe = ? ORDER BY viesti.kirjoitusaika DESC
LIMIT ? OFFSET ?
```

Tämän lisäksi tehdään vielä jokaista näytettävää viestiä kohden kyselyt, joilla selvitetään ovat kaikki käyttäjät lukeneet viestin. Nämä kyselyt on eritelty kohdassa "haluan nähdä ovatko kaikki käyttäjät lukeneet viestin".

### Haluan hakea tietyn ryhmän jäsenten jättämiä viestejä, jotta voin lukea niitä

Viestejä listaavalla sivulla avautuu hakulomake, jolla viestejä voi hakea mm. kirjoittajan ryhmän perusteella. Hakutuloksia näytetään 20 viestin erissä kirjoitusajan mukaan järjestettyinä uusin ensin.

Kun haetaan pelkän kirjoittajan ryhmän perusteella, käytetään seuraavaa SQL-kyselyä:

```sql
SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika,
viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko,
viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id,
viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id,
kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus,
kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash", kayttaja_1.admin AS kayttaja_1_admin
FROM viesti
JOIN kayttaja ON kayttaja.id = viesti.kirjoittaja_id
JOIN kayttajaryhma AS kayttajaryhma_1 ON kayttaja.id = kayttajaryhma_1.kayttaja_id
JOIN ryhma ON ryhma.id = kayttajaryhma_1.ryhma_id
LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE ryhma.nimi = ? ORDER BY viesti.kirjoitusaika DESC
LIMIT ? OFFSET ?
```

Tämän lisäksi tehdään vielä jokaista näytettävää viestiä kohden kyselyt, joilla selvitetään ovat kaikki käyttäjät lukeneet viestin. Nämä kyselyt on eritelty kohdassa "haluan nähdä ovatko kaikki käyttäjät lukeneet viestin".

### Haluam hakea tietyn käyttäjän kirjoittamia viestejä, jotta voin lukea niitä

Viestejä listaavalla sivulla avautuu hakulomake, jolla viestejä voi hakea mm. kirjoittajan nimen perusteella. Hakutuloksia näytetään 20 viestin erissä kirjoitusajan mukaan järjestettyinä uusin ensin.

Kun haetaan pelkän kirjoittajan nimen perusteella, käytetään seuraavaa SQL-kyselyä:

```sql
SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika,
viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko,
viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id,
viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id, kayttaja_1.nimi
AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus,
kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash", kayttaja_1.admin AS kayttaja_1_admin
FROM viesti
JOIN kayttaja ON kayttaja.id = viesti.kirjoittaja_id
LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE kayttaja.nimi = ? ORDER BY viesti.kirjoitusaika DESC
LIMIT ? OFFSET ?
```

Tämän lisäksi tehdään vielä jokaista näytettävää viestiä kohden kyselyt, joilla selvitetään ovat kaikki käyttäjät lukeneet viestin. Nämä kyselyt on eritelty kohdassa "haluan nähdä ovatko kaikki käyttäjät lukeneet viestin".

### Haluan hakea tietyllä aikavälillä kirjoitettuja viestejä, jotta voin lukea niitä

Viestejä listaavalla sivulla avautuu hakulomake, jolla viestejä voi hakea mm. aikavälin perusteella. Haussa voi määritellä päivän, jona kirjoitetuista alkaen viestejä haetaan ja/tai päivän jona kirjoitettuihin asti haetaan. Hakutuloksia näytetään 20 viestin erissä kirjoitusajan mukaan järjestettyinä uusin ensin.

Kun haetaan tietyltä aikaväliltä eli on määritelty sekä haun alkupäivä että haun viimeinen päivä, käytetään seuraavaa SQL-kyselyä:

```sql
SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika,
viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko,
viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id,
viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id,
kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus,
kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash", kayttaja_1.admin AS kayttaja_1_admin
FROM viesti
LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE viesti.kirjoitusaika >= ? AND viesti.kirjoitusaika <= ?
ORDER BY viesti.kirjoitusaika DESC
LIMIT ? OFFSET ?
```

Tämän lisäksi tehdään vielä jokaista näytettävää viestiä kohden kyselyt, joilla selvitetään ovat kaikki käyttäjät lukeneet viestin. Nämä kyselyt on eritelty kohdassa "haluan nähdä ovatko kaikki käyttäjät lukeneet viestin".

### Haluan yhdistelllä erilaisia hakuja

Viestejä listaavalla sivulla avautuu hakulomake, jolla viestejä voi hakea aiheen, kirjoittajan nimen, kirjoittajan ryhmän ja aikavälin (alkamisajankohdan ja loppumisajankohdan) perusteella. Näitä kyselyitä voi vapaasti yhdistellä, kuitenkin niin, että kullakin hakutyypillä on vain yksi hakuarvo. Hakutuloksia näytetään 20 viestin erissä kirjoitusajan mukaan järjestettyinä uusin ensin.

Kun haetaan kaikilla hakutyypeillä yhtaikaisesti, käytetään seuraavaa SQL-kyselyä:

```sql
SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika,
viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko,
viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id,
viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id,
kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus,
kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash", kayttaja_1.admin AS kayttaja_1_admin
FROM viesti
JOIN viestiaihe AS viestiaihe_1 ON viesti.id = viestiaihe_1.viesti_id
JOIN aihe ON aihe.id = viestiaihe_1.aihe_id
JOIN kayttaja ON kayttaja.id = viesti.kirjoittaja_id
JOIN kayttajaryhma AS kayttajaryhma_1 ON kayttaja.id = kayttajaryhma_1.kayttaja_id
JOIN ryhma ON ryhma.id = kayttajaryhma_1.ryhma_id
LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE aihe.aihe = ? AND kayttaja.nimi = ? AND ryhma.nimi = ? AND viesti.kirjoitusaika >= ?
AND viesti.kirjoitusaika <= ?
ORDER BY viesti.kirjoitusaika DESC
LIMIT ? OFFSET ?
```

Tämän lisäksi tehdään vielä jokaista näytettävää viestiä kohden kyselyt, joilla selvitetään ovat kaikki käyttäjät lukeneet viestin. Nämä kyselyt on eritelty kohdassa "haluan nähdä ovatko kaikki käyttäjät lukeneet viestin".

### Haluan nähdä olenko jo lukenut viestin

Viestien listauksessa ja yksittäisen viestin sivulla vastatun viestin ja viestiin kirjoitettujen vastausten kohdalla näytetään, onko kirjautunut käyttäjä lukenut viestin. Tämä tieto haetaan seuraavilla SQL-kyselyillä:

### Haluan nähdä ovatko kaikki muut jo lukeneet viestin

Viestien listauksessa ja yksittäisen viestin sivulla itse viestin,vastatun viestin ja viestiin kirjoitettujen vastausten kohdalla näytetään, ovatko kaikki käyttäjät lukeneet viestin. Tämä tieto haetaan kahdella SQL-kyselyllä:

Ensin haetaan käyttäjien kokonaismäärä:

```sql
SELECT COUNT(kayttaja.id) FROM kayttaja
```

Sitten haetaan viestin lukeneiden käyttäjien määrä:

```sql
SELECT COUNT(kayttaja.id) FROM kayttaja
JOIN luetut ON kayttaja.id = luetut.lukija_id
WHERE luetut.viesti_id = :viesti_id
```

Jos viestin lukeneiden käyttäjien määrä on sama kuin kaikkien käyttäjien yhteismäärä, kaikki ovat lukeneet viestin.

### Haluan nähdä ketkä ovat lukeneet viestin

Yksittäisen viestin sivulla näytetään niiden käyttäjien nimet, jotka ovat jo lukeneet viestin. Nämä haetaan seuravalla SQL-kyselyllä:

```sql
SELECT kayttaja.id AS kayttaja_id, kayttaja.nimi AS kayttaja_nimi, kayttaja.tunnus AS kayttaja_tunnus,
kayttaja."salasanaHash" AS "kayttaja_salasanaHash", kayttaja.admin AS kayttaja_admin
FROM kayttaja, luetut
WHERE ? = luetut.viesti_id AND kayttaja.id = luetut.lukija_id
```

### Haluan nähdä viestiin kirjoitetut vastaukset, jotta voin seurata viestiketjua

Yksittäisen viestin sivulla listataan viestille kirjoitettujen vastausten otsaketiedot linkkeinä, joista pääsee kyseisen viestin sivulle. Tiedot haetaan seuraavalla SQL-kyselyllä:

```sql
SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika,
viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko,
viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id,
viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id,
kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus,
kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash", kayttaja_1.admin AS kayttaja_1_admin
FROM viesti
LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE ? = viesti.vastattu_id
```

### Haluan nähdä mihin viestiin viesti on vastannut, jotta voin seurata viestiketjua taaksepäin

```sql

```

### Haluan kirjoittaa viestin, jotta muut voivat lukea sen

Aluksi haetaan luettelo kaikista valittavissa olevista aihetunnisteista seuraavalla SQL-kyselyllä:

```sql
SELECT aihe.id AS aihe_id, aihe.aihe AS aihe_aihe
FROM aihe ORDER BY aihe.aihe
```

Tämä tehdään sekä luotaessa lomaketta, johon vastaus kirjoitetaan, että (syötteen validointia varten) otettaessa uutta viestiä vastaan.

```sql

```

### Haluan vastata toisen käyttäjän viestiin, jotta toinen käyttäjä ja muut voivat lukea sen

Yksittäisen viestin näkymässä avautuu lomake, johon vastausviesti kirjoitetaan.

ALuksi haetaan luettelo kaikista valittavissa olevista aihetunnisteista seuraavalla SQL-kyselyllä, ks. erittely ja syyt yllä.

Vastauksen tallentaminen tietokantaan tapahtuu seuraavalla SQL-kyselyllä:

```sql

```

### Haluan kirjautua sisään foorumiin, jotta kirjoittamani viestit tunnistuvat minun (ja ryhmäni jäsenen) kirjoittamikseni ja näen mitkä viestit olen jo lukenut

Kun sovellus saa pyynnön kirjautua sisään, haetaan kirjautumassa olevan käyttäjän tiedot tietokannasta seuraavalla SQL-kyselyllä:

```sql
SELECT kayttaja.id AS kayttaja_id, kayttaja.nimi AS kayttaja_nimi, kayttaja.tunnus AS kayttaja_tunnus, kayttaja."salasanaHash" AS "kayttaja_salasanaHash", kayttaja.admin AS kayttaja_admin
FROM kayttaja
WHERE kayttaja.tunnus = ?
LIMIT ? OFFSET ?
```

### Haluan nähdä olenko kirjautuneena

Kirjautuneen käyttäjän nimi on esillä kaikilla sivuilla (navigaatiopalkissa), silloin kun käyttäjä on kirjautuneena.

Nimi haetaan SQL-kyselyllä

```sql
SELECT kayttaja.id AS kayttaja_id, kayttaja.nimi AS kayttaja_nimi, kayttaja.tunnus AS kayttaja_tunnus,
kayttaja."salasanaHash" AS "kayttaja_salasanaHash", kayttaja.admin AS kayttaja_admin
FROM kayttaja
WHERE kayttaja.id = ?
```

### Haluan luoda itselleni käyttäjätunnuksen, jotta voin käyttää foorumia

Käyttäjää luotaessa tarkistetaan, onko ylläpitäjän käyttäjätunnus jo luotu, ja tarvittaessa luodaan sellainen. Tarkistukseen liittyvä SQL-kysely on esitelty kohdassa "Haluan luoda itselleni ylläpitäjän käyttäjätunnuksen".

Käyttäjää luotaessa tarkistetaan, ettei käyttäjätunnus ole jo varattu. Tämä selvitetään SQL-kyselyllä

```sql
SELECT kayttaja.id AS kayttaja_id, kayttaja.nimi AS kayttaja_nimi,
kayttaja.tunnus AS kayttaja_tunnus, kayttaja."salasanaHash" AS "kayttaja_salasanaHash",
kayttaja.admin AS kayttaja_admin
FROM kayttaja
WHERE kayttaja.tunnus = ?
LIMIT ? OFFSET ?
```

Käyttäjän tiedot tallennetaan tietokantaan SQL-kyselyllä

```sql
INSERT INTO kayttaja (nimi, tunnus, "salasanaHash", admin) VALUES (?, ?, ?, ?)
```

### Haluan vaihtaa salasanani

```sql

```

### Haluan merkitä viestini aihetunnisteilla, jotta niistä kiinnostuneet löytävät ne helpommin

```sql

```

### Haluan nähdä mitä aihetunnisteita foorumissa on jo käytössä

```sql

```

### Haluan luoda uusia aihetunnisteita, jotta voin liittää viestiini sopivan aihetunnisteen

```sql

```

### Haluan nähdä mitä ryhmiä foorumissa on

```sql

```

### Haluan nähdä, keitä ryhmiin kuuluu

```sql

```

### Haluan nähdä tilastoja foorumin käytöstä

Tilastot näytetään tilastosivulla /tilastot

#### Haluan nähdä suosituimmat aiheet

Näytetään 5 suosituinta aihetta suosituimmuusjärkjestyksessä ja niillä merkittyjen viestien määrät. Käytetään SQL-kyselyä

```sql
SELECT aihe.aihe, COUNT(viestiaihe.viesti_id) AS viestilkm FROM aihe
LEFT JOIN viestiaihe ON aihe.id = viestiaihe.aihe_id
GROUP BY aihe.id
ORDER BY viestilkm DESC
LIMIT 5

```

#### Haluan nähdä eri ryhmien jäsenten kirjoitusten jakautuminen aiheittain

Näytetään taulukkona eri ryhmien eri aihetunnisteilla merkitsemien kirjoitusten määrät.

Käytetään SQL-kyselyä

```sql
SELECT ryhma.nimi, aihe.aihe, COUNT(viestiaihe.viesti_id) AS viestilkm FROM aihe
JOIN Viestiaihe ON aihe.id = Viestiaihe.aihe_id
JOIN viesti ON viestiaihe.viesti_id = viesti.id
JOIN kayttaja ON viesti.kirjoittaja_id = kayttaja.id
JOIN kayttajaryhma ON kayttaja.id = kayttajaryhma.kayttaja_id
JOIN ryhma ON kayttajaryhma.ryhma_id = ryhma.id
GROUP BY ryhma.id, aihe.aihe
ORDER BY ryhma.nimi ASC, viestilkm DESC
```

#### Haluan nähdä eniten viestejä kirjoittaneet käyttäjät

Näytetään viisi eniten viestejä kirjoittanutta käyttäjää ja heidän kirjoittamiensa viestien määrät. Käytetään SQL-kyselyä

```sql
SELECT kayttaja.nimi, COUNT(viesti.kirjoittaja_id) AS viestilkm FROM kayttaja
LEFT JOIN viesti ON kayttaja.id = viesti.kirjoittaja_id
GROUP BY kayttaja.id
ORDER BY viestilkm DESC
LIMIT 5
```

#### Haluan nähdä eniten viestejä kirjoittaneet ryhmät

Näytetään viisi eniten viestejä kirjoittanutta ryhmää ja näiden ryhmien kirjoittamien viestien määärät.

```sql
SELECT ryhma.nimi, COUNT(viesti.kirjoittaja_id) AS viestilkm FROM ryhma
LEFT JOIN kayttajaryhma ON ryhma.id = kayttajaryhma.ryhma_id
LEFT JOIN viesti ON kayttajaryhma.kayttaja_id = viesti.kirjoittaja_id
GROUP BY ryhma.id
ORDER BY viestilkm DESC
LIMIT 5
```

## Foorumin ylläpitäjänä

Haluan tehdä myös kaiken, minkä tavallinen käyttäjäkin haluaa tehdä.

### Haluan poistaa viestejä, jotta asiattomat viestit saadaan poistetuksi foorumista

```sql

```

### Haluan muokata viestejä, jotta voin poistaa viesteistää asiatonta sisältöä

```sql

```

### Haluan hallita käyttäjien jäsenyyksiä ryhmissä

#### Haluan luoda ryhmiä

```sql

```

#### Haluan liittää käyttäjän ryhmään

```sql

```

#### Haluan poistaa käyttäjän ryhmästä

```sql

```

#### Haluan muokata ryhmän nimeä

```sql

```

#### Haluan poistaa ryhmiä

```sql

```

### Haluan hallita aihetunnisteita

#### Haluan muokata aihetunnisteita

```sql

```

#### Haluan poistaa aihetunnisteita

```sql

```

### Haluan luoda itselleni ylläpitäjän tunnuksen foorumia käyttöönotettaessa

Rekisteröitymissivulle mentäessä tarkistetaan, onko ylläpitäjän käyttäjätunnusta jo luotu, ja muokataan käyttäjälle näytettävää tekstiä sen mukaan. Sama tarkistus tehdään, kun saadaan pyyntö luoda uusi käyttäjä. Jos ylläpitäjän käyttäjätunnusta ei vielä ole, luodaan sellainen. Jos ylläpitäjän tunnus on jo olemassa, luodaan tavallinen käyttäjä. Ylläpitäjän tunnuksen olemassaolo tarkistetaan kyselyllä

```sql
SELECT EXISTS (SELECT 1
FROM kayttaja
WHERE kayttaja.admin = 1) AS anon_1
LIMIT ? OFFSET ?
```

Tämän jälkeen tarkistetaan, ettei käyttäjätunnus ole jo varattu, tallennetaan käyttäjän tiedot tietokantaan ja kirjataan käyttäjä sisään. Näihin liittyvät SQL-kyselyt on esitelty kohdissa "Haluan rekisteröityä foorumille" ja "Haluan kirjautua sisään foorumille".
