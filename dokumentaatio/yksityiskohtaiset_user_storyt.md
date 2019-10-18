# Yksityiskohtaiset User Storyt

Automaattisesti generoitavat SQL-kyselyt on tässä esitetty siinä muodossa kuin ne toteutetaan SQLite-tietokantaan. Käsin tehdyt kyselyt ovat siinä muodossa kuin ne ovat koodissa.

Rekisteröitymistä ja kirjautumista lukuunottamatta kaikki sovelluksen toiminnot vaativat käyttäjän olevan kirjautuneena. Kirjautumisen tarkistamisen yhteydessä haetaan käyttäjän tiedot kyselyllä

```sql
SELECT kayttaja.id AS kayttaja_id, kayttaja.nimi AS kayttaja_nimi, kayttaja.tunnus AS kayttaja_tunnus,
kayttaja."salasanaHash" AS "kayttaja_salasanaHash", kayttaja.admin AS kayttaja_admin
FROM kayttaja
WHERE kayttaja.id = ?
```

## Foorumin käyttäjänä (yhteisön jäsenenä)

### Haluan lukea viestejä

Viestin sisällön ja kaikki viestiin liittyvät tiedot ovat nähtävissä viestin omalla sivulla /viestit/<viesti_id>

Viestin sisältö, perustiedot ja kirjoittajan nimi haetaan seuraavalla SQL-kyselyllä:

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

Jos kirjautunut käyttäjä ei ole aiemmin lukenut viestiä, hänet lisätään lukijoiden luetteloon. Aluksi tarkastetaan, onko käyttäjä jo lukenut viestin käyttäen SQL-kyselyä

```sql
SELECT kayttaja.id AS kayttaja_id, kayttaja.nimi AS kayttaja_nimi, kayttaja.tunnus AS kayttaja_tunnus,
kayttaja."salasanaHash" AS "kayttaja_salasanaHash", kayttaja.admin AS kayttaja_admin
FROM kayttaja, luetut
WHERE ? = luetut.viesti_id AND kayttaja.id = luetut.lukija_id
```

Itse viestin lukeneiden luetteloon lisääminen tapahtuu SQL-kyselyllä

```sql
INSERT INTO luetut (viesti_id, lukija_id) VALUES (?, ?)
```

Jos käyttäjä on lisätty lukijoihin, haetaan templatea varten vielä erikseen viestin lukeneen käyttäjän, viestin ja viestin kirjoittajan tiedot, ilmeisesti sen takia, että välissä on kutsuttu commit() -funktiota. Lukijan ja kirjoittajan tiedot haetaan kahdella seuraavanlaisella kyselyllä:

```sql
SELECT kayttaja.id AS kayttaja_id, kayttaja.nimi AS kayttaja_nimi, kayttaja.tunnus AS kayttaja_tunnus,
kayttaja."salasanaHash" AS "kayttaja_salasanaHash", kayttaja.admin AS kayttaja_admin
FROM kayttaja
WHERE kayttaja.id = ?
```

Viestin tiedot haetaan kyselyllä

```sql
SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika,
viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko,
viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id,
viesti.vastattu_id AS viesti_vastattu_id
FROM viesti
WHERE viesti.id = ?

```

Lisäksi haetaan erillisillä kyselyillä tieto siitä, ovatko kaikki käyttäjät lukeneet viestin, viestistä, johon näytettävä viesti on vastaus (jos viesti on vastaus) samat tiedot kuin viestien listassa näytetään, ja näytettävään viestiin kirjoitetuista vastauksista samat tiedot kuin viestien listauksessa näytetään. Näihin tarvittavat kyselyt on esitelty kohdissa "Haluan nähdä ovatko kaikki käyttäjät lukeneet viestin", "Haluan nähdä mihin viestiin viesti on vastaus" ja "Haluan nähdä viestiin kirjoitetut vastaukset".

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

Tämä kysely tehdään, jos sivuja on enemmän kuin yksi.

Lisäksi haetaan jokaista viestiä kohden erikseen tieto siitä, onko käyttäjä lukenut viestin ja ovatko kaikki käyttäjät lukeneet viestin. Tähän tarvittavat kyselyt on eritelty käyttötapausten "haluan nähdä olenko jo lukenut viestin" ja "haluan nähdä ovatko kaikki käyttäjät lukeneet viestin" alla.

### Haluan hakea viestejä aiheen perusteella, jotta voin lukea minua kiinnostavia viestejä

Viestejä listaavalla sivulla avautuu hakulomake, jolla viestejä voi hakea mm. aiheen perusteella. Hakutermi voi olla myös aiheen osa eikä kirjainkokoa huomioida. Hakutuloksia näytetään 20 viestin erissä kirjoitusajan mukaan järjestettyinä uusin ensin.

Kun haetaan pelkän aiheen perusteella, käytetään seuraavaa SQL-kyselyä siten, että ensimmäinen parametri (aihe tai sen osa) on käyttäjän antama hakutermi ympäröitynä %-merkeillä (esim "%marjat%").

```sql
SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika,
viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko,
viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id,
viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id,
kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus,
kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash", 
kayttaja_1.admin AS kayttaja_1_admin
FROM viesti
JOIN viestiaihe AS viestiaihe_1 ON viesti.id = viestiaihe_1.viesti_id
JOIN aihe ON aihe.id = viestiaihe_1.aihe_id
LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE lower(aihe.aihe) LIKE lower(?)
ORDER BY viesti.kirjoitusaika DESC
LIMIT ? OFFSET ?
```

Jos hakutuloksia on enemmän kuin 20, haetaan myös hakutulosten kokonaismäärä. Tämä kysely on esitelty edellisessä kohdassa. Tämän lisäksi tehdään vielä jokaista näytettävää viestiä kohden kyselyt, joilla selvitetään ovatko kaikki käyttäjät lukeneet viestin. Nämä kyselyt on eritelty kohdassa "Haluan nähdä ovatko kaikki käyttäjät lukeneet viestin".

### Haluan hakea viestejä niiden kirjoittajan ryhmään kuulumisen perusteella, jotta voin lukea minua kiinostavia viestejä

Viestejä listaavalla sivulla avautuu hakulomake, jolla viestejä voi hakea mm. kirjoittajan ryhmän perusteella. Hakutermi voi olla myös ryhmän nimen osa eikä kirjainkokoa huomioida. Hakutuloksia näytetään 20 viestin erissä kirjoitusajan mukaan järjestettyinä uusin ensin.

Kun haetaan pelkän kirjoittajan ryhmän perusteella, käytetään seuraavaa SQL-kyselyä siten, että ensimmäinen parametri (ryhmän nimi tai sen osa) on käyttäjän antama hakutermi ympäröitynä %-merkeillä (esim. "%kalastajat%").

```sql
SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika,
viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko,
viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id,
viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id,
kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus,
kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash",
kayttaja_1.admin AS kayttaja_1_admin
FROM viesti
JOIN kayttaja ON kayttaja.id = viesti.kirjoittaja_id
JOIN kayttajaryhma AS kayttajaryhma_1 ON kayttaja.id = kayttajaryhma_1.kayttaja_id
JOIN ryhma ON ryhma.id = kayttajaryhma_1.ryhma_id
LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE lower(ryhma.nimi) LIKE lower(?)
ORDER BY viesti.kirjoitusaika DESC
LIMIT ? OFFSET ?
```

Jos hakutuloksia on enemmän kuin 20, haetaan myös hakutulosten kokonaismäärä.
Tämä kysely on esitelty kohdassa "Haluan nähdä uusimmat viestit tarvitsematta hakea niitä ensin". Tämän lisäksi tehdään vielä jokaista näytettävää viestiä kohden kyselyt, joilla selvitetään ovat kaikki käyttäjät lukeneet viestin. Nämä kyselyt on eritelty kohdassa "Haluan nähdä ovatko kaikki käyttäjät lukeneet viestin".

### Haluan hakea viestejä niiden kirjoittajan perusteella, jotta voin lukea minua kiinnostavia viestejä

Viestejä listaavalla sivulla avautuu hakulomake, jolla viestejä voi hakea mm. kirjoittajan nimen perusteella. Hakutermi voi olla myös kirjoittajan nimen osa eikä kirjainkokoa huomioida. Hakutuloksia näytetään 20 viestin erissä kirjoitusajan mukaan järjestettyinä uusin ensin.

Kun haetaan pelkän kirjoittajan nimen perusteella, käytetään seuraavaa SQL-kyselyä siten, että ensimmäinen parametri (kirjoittajan nimi tai sen osa) on käyttäjän antama hakutermi ympäröitynä %-merkeillä (esim. "%Otso Kontio%").

```sql
SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika,
viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko,
viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id,
viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id,
kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus,
kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash",
kayttaja_1.admin AS kayttaja_1_admin
FROM viesti
JOIN kayttaja ON kayttaja.id = viesti.kirjoittaja_id
LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE lower(kayttaja.nimi) LIKE lower(?)
ORDER BY viesti.kirjoitusaika DESC
LIMIT ? OFFSET ?
```

Jos hakutuloksia on enemmän kuin 20, haetaan myös hakutulosten kokonaismäärä.
Tämä kysely on esitelty kohdassa "Haluan nähdä uusimmat viestit tarvitsematta hakea niitä ensin". Tämän lisäksi tehdään vielä jokaista näytettävää viestiä kohden kyselyt, joilla selvitetään ovat kaikki käyttäjät lukeneet viestin. Nämä kyselyt on eritelty kohdassa "Haluan nähdä ovatko kaikki käyttäjät lukeneet viestin".

### Haluan hakea tietyllä aikavälillä kirjoitettuja viestejä, jotta voin lukea niitä

Viestejä listaavalla sivulla avautuu hakulomake, jolla viestejä voi hakea mm. aikavälin perusteella. Haussa voi määritellä päivän, jona kirjoitetuista alkaen viestejä haetaan ja/tai päivän jona kirjoitettuihin asti haetaan. Hakutuloksia näytetään 20 viestin erissä kirjoitusajan mukaan järjestettyinä uusin ensin.

Kun haetaan tietyltä aikaväliltä eli on määritelty sekä haun alkupäivä että haun viimeinen päivä, käytetään seuraavaa SQL-kyselyä. Ensimmäisenä parametrina on käyttäjän syöttämä alkaen-päivämäärä datetime-muodossa kellonaikana vuorokauden alku. Toisena parametrina on käyttäjän syöttämä asti-päivämäärä datetime-muodossa ja kellonaika säädettynä millisekuntia vaille keskiyöhön.

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
WHERE viesti.kirjoitusaika >= ? AND viesti.kirjoitusaika <= ?
ORDER BY viesti.kirjoitusaika DESC
LIMIT ? OFFSET ?
```

Jos hakutuloksia on enemmän kuin 20, haetaan myös hakutulosten kokonaismäärä.
Tämä kysely on esitelty kohdassa "Haluan nähdä uusimmat viestit tarvitsematta hakea niitä ensin". Tämän lisäksi tehdään vielä jokaista näytettävää viestiä kohden kyselyt, joilla selvitetään ovat kaikki käyttäjät lukeneet viestin. Nämä kyselyt on eritelty kohdassa "Haluan nähdä ovatko kaikki käyttäjät lukeneet viestin".

### Haluan yhdistelllä erilaisia hakuja

Viestejä listaavalla sivulla avautuu hakulomake, jolla viestejä voi hakea aiheen, kirjoittajan nimen, kirjoittajan ryhmän ja aikavälin (alkamisajankohdan ja loppumisajankohdan) perusteella. Näitä kyselyitä voi vapaasti yhdistellä, kuitenkin niin, että kullakin hakutyypillä on vain yksi hakuarvo. Hakutuloksia näytetään 20 viestin erissä kirjoitusajan mukaan järjestettyinä uusin ensin.

Kun haetaan kaikilla hakutyypeillä yhtaikaisesti, käytetään seuraavaa SQL-kyselyä siten, että käyttäjän syöttämät aihe, kirjoittaja ja ryhmä ympäröidään %-merkeillä (esim. "%Otso Kontio%").

```sql
SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika,
viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko,
viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id,
viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id,
kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus,
kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash",
kayttaja_1.admin AS kayttaja_1_admin
FROM viesti
JOIN viestiaihe AS viestiaihe_1 ON viesti.id = viestiaihe_1.viesti_id
JOIN aihe ON aihe.id = viestiaihe_1.aihe_id
JOIN kayttaja ON kayttaja.id = viesti.kirjoittaja_id
JOIN kayttajaryhma AS kayttajaryhma_1 ON kayttaja.id = kayttajaryhma_1.kayttaja_id
JOIN ryhma ON ryhma.id = kayttajaryhma_1.ryhma_id
LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE lower(aihe.aihe) LIKE lower(?)
AND lower(kayttaja.nimi) LIKE lower(?)
AND lower(ryhma.nimi) LIKE lower(?)
AND viesti.kirjoitusaika >= ?
AND viesti.kirjoitusaika <= ?
ORDER BY viesti.kirjoitusaika DESC
LIMIT ? OFFSET ?
```

Jos hakutuloksia on enemmän kuin 20, haetaan myös hakutulosten kokonaismäärä.
Tämä kysely on esitelty kohdassa "Haluan nähdä uusimmat viestit tarvitsematta hakea niitä ensin". Tämän lisäksi tehdään vielä jokaista näytettävää viestiä kohden kyselyt, joilla selvitetään ovat kaikki käyttäjät lukeneet viestin. Nämä kyselyt on eritelty kohdassa "haluan nähdä ovatko kaikki käyttäjät lukeneet viestin".

### Haluan nähdä olenko jo lukenut viestin

Viestien listauksessa ja yksittäisen viestin sivulla vastatun viestin ja viestiin kirjoitettujen vastausten kohdalla näytetään, onko kirjautunut käyttäjä lukenut viestin. Tämä tieto haetaan tarkistamalla onko käyttäjä viestin lukeneiden käyttäjien joukossa. Tämä ei aiheuta erillistä hakua tietokannasta.

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

Tämän lisäksi haetaan kullekin vastaukselle erikseen tieto siitä, ovatko kaikki käyttäjät jo lukeneet ne. Tähän käytettävä SQL-kysely esitellään kohdassa "Haluan tietää ovatko kaikki käyttäjät lukeneet viestin".

### Haluan nähdä mihin viestiin viesti on vastannut, jotta voin seurata viestiketjua taaksepäin

Yksittäisen viestin sivulla näytetään linkkinä sen viestin otsaketiedot, johon näytettävä viesti on vastannut, jos sellainen on. Tiedot haetaan SQL-kyselyllä:

```sql
SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika,
viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko,
viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id,
viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id,
kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus,
kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash", kayttaja_1.admin AS kayttaja_1_admin
FROM viesti
LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE viesti.id = ?

```

Tämän lisäksi haetaan tieto siitä, ovatko kaikki käyttäjät jo lukeneet viestin, johon näytettävä viesti on vastannut. Tähän käytettävä SQL-kysely esitellään kohdassa "Haluan tietää ovatko kaikki käyttäjät lukeneet viestin".

### Haluan kirjoittaa viestin, jotta muut voivat lukea sen

Uuden viestiketjun aloittavan viestin kirjoittamiseen on oma sivunsa /viestit/uusi .

Aluksi haetaan luettelo kaikista valittavissa olevista aihetunnisteista seuraavalla SQL-kyselyllä:

```sql
SELECT aihe.id AS aihe_id, aihe.aihe AS aihe_aihe
FROM aihe ORDER BY aihe.aihe
```

Tämä tehdään sekä luotaessa lomaketta, johon vastaus kirjoitetaan, että (syötteen validointia varten) otettaessa uutta viestiä vastaan.

Viestin tallentaminen tietokantaan tapahtuu seuraavalla SQL-kyselyllä:

```sql
INSERT INTO viesti (kirjoitusaika, muokkausaika, otsikko, teksti, kirjoittaja_id, vastattu_id)
VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?)
```

Viestin kirjoittaja lisätään viestin lukeneisiin käyttäjiin, jottei itse kirjoitettu viesti näkyisi uutena. Tähän käytetään SQL-kyselyä

```sql
INSERT INTO luetut (viesti_id, lukija_id) VALUES (?, ?)
```

Lisäksi tallennetaan tieto viestiin liittyvistä aihetunnisteista. Tarvittava SQL-kysely on esitelty kohdassa "Haluan liittää viestiini aihetunnisteita".

### Haluan vastata toisen käyttäjän viestiin, jotta toinen käyttäjä ja muut voivat lukea sen

Yksittäisen viestin näkymässä avautuu lomake, johon vastausviesti kirjoitetaan.

Aluksi haetaan luettelo kaikista valittavissa olevista aihetunnisteista. 
Vastauksen ja siihen liittyvien aihetunnisteiden tallentaminen tietokantaan ja kirjoittajan merkitseminen viestin lukeneeksi tapahtuu samoin kuin erillistä viestiä tallennettaessa. Näihin liittyvät SQL-kyselyt on esitelty yllä.

### Haluan muokata itse kirjoittamiani viestejä

Muokkauspyynnön tullessa palvelimelle haetaan ensin viesti (samalla tarkistetaan, että se on olemassa) kyselyllä

```sql
SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika,
viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko,
viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id,
viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id,
kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus,
kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash", kayttaja_1.admin AS kayttaja_1_admin
FROM viesti
LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE viesti.id = ?
```

Itse viestin muokkaaminen tapahtuu kyselyllä

```sql
UPDATE viesti SET muokkausaika=CURRENT_TIMESTAMP, otsikko=?, teksti=? WHERE viesti.id = ?

```

### Haluan poistaa itse kirjoittamiani viestejä

Yksittäisen viestin sivulla on viestin kirjoittajalle näkyvissä nappi, josta voi poistaa kyseisen viestin.

Aluksi haetaan viesti (ja tarkistetaan samalla, että se on olemassa) kyselyllä

```sql
SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika,
viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko,
viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id,
viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id,
kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus,
kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash", kayttaja_1.admin AS kayttaja_1_admin
FROM viesti
LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE viesti.id = ?
```

SQLAlchemy poistaa automaattisesti tiedot viestin lukeneista ja viestiin liitetyistä aihetunnisteista.
Aluksi haetaan tiedot viestiin kirjoitetuista vastauksista, vaikka niitä ei muutetakaan mitenkään:

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

Tiedot viestin lukeneista haetaan kyselyllä

```sql
SELECT kayttaja.id AS kayttaja_id, kayttaja.nimi AS kayttaja_nimi, 
kayttaja.tunnus AS kayttaja_tunnus, kayttaja."salasanaHash" AS "kayttaja_salasanaHash",
kayttaja.admin AS kayttaja_admin
FROM kayttaja, luetut
WHERE ? = luetut.viesti_id AND kayttaja.id = luetut.lukija_id
```

Tiedot viestiin liitetyistä aihetunisteista haetaan kyselyllä

```sql
SELECT aihe.id AS aihe_id, aihe.aihe AS aihe_aihe
FROM aihe, viestiaihe
WHERE ? = viestiaihe.viesti_id AND aihe.id = viestiaihe.aihe_id
```

Sitten poistetaan löydetyt tiedot lukijoista kyselyllä

```sql
DELETE FROM luetut WHERE luetut.viesti_id = ? AND luetut.lukija_id = ?
```

Viestin ja siihen liitetyn aihetunnisteen yhteydet poistetaan kyselyllä

```sql
DELETE FROM viestiaihe WHERE viestiaihe.viesti_id = ? AND viestiaihe.aihe_id = ?
```

Itse viesti poistetaan kyselyllä

```sql
DELETE FROM viesti WHERE viesti.id = ?
```

### Haluan kirjautua sisään foorumiin, jotta kirjoittamani viestit tunnistuvat minun (ja ryhmäni jäsenen) kirjoittamikseni ja näen mitkä viestit olen jo lukenut

Kun sovellus saa pyynnön kirjautua sisään, haetaan kirjautumassa olevan käyttäjän tiedot tietokannasta seuraavalla SQL-kyselyllä:

```sql
SELECT kayttaja.id AS kayttaja_id, kayttaja.nimi AS kayttaja_nimi, 
kayttaja.tunnus AS kayttaja_tunnus, kayttaja."salasanaHash" AS "kayttaja_salasanaHash",
kayttaja.admin AS kayttaja_admin
FROM kayttaja
WHERE kayttaja.tunnus = ?
LIMIT ? OFFSET ?
```

### Haluan kirjautua ulos foorumista, jotta muut eivät pääse käyttämään tunnustani

Sovelluksessa on oma osoite uloskirjautumiseen: /logout .
Uloskirjaamiseen käytettävä flask-login:in logout_user -funktio hakee uloskirjattavan käyttäjän tiedot kyselyllä

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

Salasanan vaihtamiseen on oma sivunsa /kayttajat/salasananvaihto .

Salasana vaihdetaan SQL-kyselyllä

```sql
UPDATE kayttaja SET "salasanaHash"=? WHERE kayttaja.id = ?
```

### Haluan merkitä viestini aihetunnisteilla, jotta niistä kiinnostuneet löytävät ne helpommin

Lisättävät aihetunnisteet haetaan ensin kerralla tietokannasta viestiolioon liitettäviksi kyselyllä

```sql
SELECT aihe.id AS aihe_id, aihe.aihe AS aihe_aihe
FROM aihe
WHERE aihe.id IN (?, ?, ?, ?, ?)
```

Tieto viestiin liittyvistä aihetunnisteista tallennetaan liitostauluun viestin muiden tietojen tallentamisen jälkeen kyselyllä

```sql
INSERT INTO viestiaihe (viesti_id, aihe_id) VALUES (?, ?)
```

### Haluan nähdä mitä aihetunnisteita foorumissa on jo käytössä

Aihetunnisteiden tarkasteluun on oma sivunsa /aiheet . Aiheet haetaan aakkosjärjestyksessä enintään 20 aihetta kerrallaan.

Aihetunnisteet haetaan SQL-kyselyllä

```sql
SELECT aihe.id AS aihe_id, aihe.aihe AS aihe_aihe
FROM aihe ORDER BY aihe.aihe
LIMIT ? OFFSET ?
```

Jos aiheita on yli 20, hakee SQLAlchemy automaattisesti myös aiheiden määrän sivumäärän selvittämiseksi seuraavalla kyselyllä:

```sql
SELECT count(*) AS count_1
FROM (SELECT aihe.id AS aihe_id, aihe.aihe AS aihe_aihe
FROM aihe) AS anon_1
```

### Haluan luoda uusia aihetunnisteita, jotta voin liittää viestiini sopivan aihetunnisteen

Uusia aihetunnisteita voi lisätä aiheiden sivulta.

Syötettä validoitaessa tarkastetaan, onko samannimistä aihetta jo tietokannassa kyselyllä

```sql
SELECT aihe.id AS aihe_id, aihe.aihe AS aihe_aihe
FROM aihe
WHERE aihe.aihe = ?
 LIMIT ? OFFSET ?
```

Itse aiheen lisäämiseen käytetään SQL-kyselyä

```sql
INSERT INTO aihe (aihe) VALUES (?)
```

### Haluan nähdä mitä ryhmiä foorumissa on

Ryhmien tarkasteluun on oma sivunsa /ryhmat . Ryhmiä näytetään aakkosjärjestyksessä enintään kaksikymmentä kerrallaan. Ryhmien tiedot haetaan SQL-kyselyllä

```sql
SELECT ryhma.id AS ryhma_id, ryhma.nimi AS ryhma_nimi
FROM ryhma ORDER BY ryhma.nimi
LIMIT ? OFFSET ?
```

Jos ryhmiä on enemmän kuin kaksikymmentä flask-SQLAlchemy hakee sivutusoliolle myös sivujen kokonaismäärää varten ryhmien määrän kyselyllä

```sql
SELECT count(*) AS count_1
FROM (SELECT ryhma.id AS ryhma_id, ryhma.nimi AS ryhma_nimi
FROM ryhma) AS anon_1
```

### Haluan nähdä, keitä ryhmiin kuuluu

Ryhmien jäseniä voi tarkastella yksittäisen ryhmän sivulta /ryhmat/<ryhma_id> .

Ryhmän nimi haetaan kyselyllä

```sql
SELECT ryhma.id AS ryhma_id, ryhma.nimi AS ryhma_nimi
FROM ryhma
WHERE ryhma.id = ?
```

Lisäksi jokaisen ryhmän jäsenen tiedot haetaan erikseen kyselyllä

```sql
SELECT kayttaja.id AS kayttaja_id, kayttaja.nimi AS kayttaja_nimi,
kayttaja.tunnus AS kayttaja_tunnus, kayttaja."salasanaHash" AS "kayttaja_salasanaHash",
kayttaja.admin AS kayttaja_admin
FROM kayttaja
```

### Haluan nähdä tilastoja foorumin käytöstä

Tilastot näytetään tilastosivulla /tilastot

#### Haluan nähdä suosituimmat aiheet

Näytetään 5 suosituinta aihetta suosituimmuusjärjestyksessä ja niillä merkittyjen viestien määrät. Käytetään SQL-kyselyä

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

Kaikissa ylläpitäjän oikeuksia vaativissa toiminnoissa tarkistetaan onko rekisteröityneellä käyttäjällä ylläpitäjän oikeudet käyttäen kyselyä

```sql
SELECT kayttaja.id AS kayttaja_id, kayttaja.nimi AS kayttaja_nimi,
kayttaja.tunnus AS kayttaja_tunnus, kayttaja."salasanaHash" AS "kayttaja_salasanaHash",
kayttaja.admin AS kayttaja_admin
FROM kayttaja, kayttajaryhma
WHERE ? = kayttajaryhma.ryhma_id AND kayttaja.id = kayttajaryhma.kayttaja_id
```

### Haluan poistaa muiden kirjoittamia viestejä, jotta asiattomat viestit saadaan poistetuksi foorumista

Ylläpitäjälle näkyy jokaisen yksittäisen viestin sivulla nappi, josta kyseisen viestin voi poistaa. Tarvittavat SQL-kyselyt on esitelty kohdassa "Haluan poistaa itse kirjoittamiani viestejä".

### Haluan muokata muiden kirjoittamia viestejä, jotta voin poistaa viesteistää asiatonta sisältöä

Ylläpitäjällä on jokaisen yksittäisen viestin sivulla napista aukeava muokkauslomake. Tarvittavat SQL-kyselyt on esitelty kohdassa "Haluan muokata itse kirjoittamiani viestejä"

### Haluan hallita käyttäjien jäsenyyksiä ryhmissä

#### Haluan luoda ryhmiä

Ylläpitäjälle mäkyy ryhmien listauksessa lomake, jolla voidaan lisätä ryhmiä.

Lomakkeen syötettä verifioitaessa tarkastetaan onko samannimistä ryhmää jo olemassa kyselyllä

```sql
SELECT ryhma.id AS ryhma_id, ryhma.nimi AS ryhma_nimi
FROM ryhma
WHERE ryhma.nimi = ?
 LIMIT ? OFFSET ?
```

Ryhmä lisätään tietokantaan kyselyllä

```sql
INSERT INTO ryhma (nimi) VALUES (?)
```

Tämän jälkeen haetaan ryhmän tietokannasta saama id ryhmän sivulle uudelleenohjausta varten kyselyllä

```sql
SELECT ryhma.id AS ryhma_id, ryhma.nimi AS ryhma_nimi
FROM ryhma
WHERE ryhma.id = ?
```

#### Haluan liittää käyttäjän ryhmään

Yksittäisen ryhmän näkymässä on ylläpitäjällä lomake käyttäjän lisäämiseen. Lomaketta varten haetaan tieto niistä käyttäjistä, jotka eivät vielä kuulu ryhmään kyselyllä

```sql
SELECT kayttaja.id AS kayttaja_id, kayttaja.nimi AS kayttaja_nimi,
kayttaja.tunnus AS kayttaja_tunnus, kayttaja."salasanaHash" AS "kayttaja_salasanaHash",
kayttaja.admin AS kayttaja_admin
FROM kayttaja
WHERE kayttaja.id NOT IN (?, ?)
```

Käyttäjän ryhmään lisäämispyyntöä käsiteltäessä haetaan ryhmä, johon käyttäjää ollaan liittämässä. Samalla tarkistetaan onko ryhmää olemassa. Kyselynä on

```sql
SELECT ryhma.id AS ryhma_id, ryhma.nimi AS ryhma_nimi
FROM ryhma
WHERE ryhma.id = ?
```

Sitten haetaan kaikki lisättävät käyttäjät kerralla kyselyllä

```sql
SELECT kayttaja.id AS kayttaja_id, kayttaja.nimi AS kayttaja_nimi, kayttaja.tunnus AS kayttaja_tunnus, kayttaja."salasanaHash" AS "kayttaja_salasanaHash", kayttaja.admin AS kayttaja_admin
FROM kayttaja
WHERE kayttaja.id IN (?, ?)
```

Varsinainen käyttäjien lisääminen ryhmään tapahtuu SQL-kyselyllä

```sql
INSERT INTO kayttajaryhma (kayttaja_id, ryhma_id) VALUES (?, ?)
```

Tällä kyselyllä lisätään kerralla kaikki lisättävät käyttäjät.

#### Haluan poistaa käyttäjän ryhmästä

Ryhmän jäsenten luettelossa on ylläpitäjällä nappi jäsenen poistamiseksi ryhmästä.

Aluksi tarkistetaan että ryhmä on olemassa ja haetaan se käyttäen kerran kyselyä

```sql
SELECT ryhma.id AS ryhma_id, ryhma.nimi AS ryhma_nimi
```

Sitten tarkistetaan, että poistettava käyttäjä on ryhmän jäsen kyselyllä

```sql
SELECT kayttaja.id AS kayttaja_id, kayttaja.nimi AS kayttaja_nimi, kayttaja.tunnus AS kayttaja_tunnus,
kayttaja."salasanaHash" AS "kayttaja_salasanaHash", kayttaja.admin AS kayttaja_admin
FROM kayttaja, kayttajaryhma
WHERE ? = kayttajaryhma.ryhma_id AND kayttaja.id = kayttajaryhma.kayttaja_id
```

Lopuksi poistetaan käyttäjä ryhmästä kyselyllä

```sql
DELETE FROM kayttajaryhma WHERE kayttajaryhma.kayttaja_id = ? AND kayttajaryhma.ryhma_id = ?
```

#### Haluan muokata ryhmän nimeä

Ylläpitäjä voi muokata ryhmän nimeä yksittäisen ryhmän sivulla.

Ensin haetaan ryhmä ja tarkistetaan että se on olemassa kyselyllä

```sql
SELECT ryhma.id AS ryhma_id, ryhma.nimi AS ryhma_nimi
FROM ryhma
WHERE ryhma.id = ?
```

Varsinainen nimen muuttaminen tehdään kyselyllä

```sql
UPDATE ryhma SET nimi=? WHERE ryhma.id = ?
```

#### Haluan poistaa ryhmiä

Ylläpitäjä voi poistaa ryhmän yksittäisen ryhmän sivulta.

Ensin haetaan ryhmä (ja tarkistetaan että se on olemassa) kyselyllä

```sql
SELECT ryhma.id AS ryhma_id, ryhma.nimi AS ryhma_nimi
```

SQLAlchemy poistaa automaattisesti kaikki käyttäjät poistettavasta ryhmästä kyselyllä

```sql
DELETE FROM kayttajaryhma WHERE kayttajaryhma.kayttaja_id = ? AND kayttajaryhma.ryhma_id = ?
```

Lopuksi poistetaan itse ryhmä kyselyllä

```sql
DELETE FROM ryhma WHERE ryhma.id = ?
```

### Haluan hallita aihetunnisteita

#### Haluan muokata aihetunnisteita

Aihetunnistetta voi muokata yksittäisen aihetunnisteen sivulta /aiheet/<aihe_id>

Aluksi haetaan muokattava aihe (tarkistaen samalla, että se on olemassa) kyselyllä

```sql
SELECT aihe.id AS aihe_id, aihe.aihe AS aihe_aihe
FROM aihe
WHERE aihe.id = ?
```

Itse aiheen muokkaaminen tapahtuu kyselyllä

```sql
UPDATE aihe SET aihe=? WHERE aihe.id = ?
```

#### Haluan poistaa aihetunnisteita

Aluksi haetaan aihe (ja tarkistetaan samalla että se on olemassa)

```sql
SELECT aihe.id AS aihe_id, aihe.aihe AS aihe_aihe
FROM aihe
WHERE aihe.id = ?

```

SQLAlchemy poistaa automaattisesti aiheen kaikista viesteistä aiheen poistamisen yhteydessä. Aluksi haetaan aiheeseen liittyvät viestit kyselyllä

```sql
SELECT viesti.id AS viesti_id, viesti.kirjoitusaika AS viesti_kirjoitusaika,
viesti.muokkausaika AS viesti_muokkausaika, viesti.otsikko AS viesti_otsikko,
viesti.teksti AS viesti_teksti, viesti.kirjoittaja_id AS viesti_kirjoittaja_id,
viesti.vastattu_id AS viesti_vastattu_id, kayttaja_1.id AS kayttaja_1_id,
kayttaja_1.nimi AS kayttaja_1_nimi, kayttaja_1.tunnus AS kayttaja_1_tunnus,
kayttaja_1."salasanaHash" AS "kayttaja_1_salasanaHash", kayttaja_1.admin AS kayttaja_1_admin
FROM viestiaihe, viesti
LEFT OUTER JOIN kayttaja AS kayttaja_1 ON kayttaja_1.id = viesti.kirjoittaja_id
WHERE ? = viestiaihe.aihe_id AND viesti.id = viestiaihe.viesti_id

```

Seuraavaksi poistetaan aihe näistä viesteistä kerralla kyselyllä

```sql
DELETE FROM viestiaihe WHERE viestiaihe.viesti_id = ? AND viestiaihe.aihe_id = ?

```

Lopuksi poistetaan itse aihe kyselyllä

```sql
DELETE FROM aihe WHERE aihe.id = ?

```

### Haluan luoda itselleni ylläpitäjän tunnuksen foorumia käyttöönotettaessa

Rekisteröitymissivulle mentäessä tarkistetaan, onko ylläpitäjän käyttäjätunnusta jo luotu, ja muokataan käyttäjälle näytettävää tekstiä sen mukaan. Sama tarkistus tehdään, kun saadaan pyyntö luoda uusi käyttäjä. Jos ylläpitäjän käyttäjätunnusta ei vielä ole, luodaan sellainen. Jos ylläpitäjän tunnus on jo olemassa, luodaan tavallinen käyttäjä. Ylläpitäjän tunnuksen olemassaolo tarkistetaan kyselyllä

```sql
SELECT EXISTS
(SELECT 1
FROM kayttaja
WHERE kayttaja.admin = 1)
AS anon_1
LIMIT ? OFFSET ?
```

Tämän jälkeen tarkistetaan, ettei käyttäjätunnus ole jo varattu, tallennetaan käyttäjän tiedot tietokantaan ja kirjataan käyttäjä sisään. Näihin liittyvät SQL-kyselyt on esitelty kohdissa "Haluan rekisteröityä foorumille" ja "Haluan kirjautua sisään foorumille".
