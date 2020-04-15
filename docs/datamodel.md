# Data Model Draft
Voor de technische lezers is een database model dat als uitgangspunt dient te vinden in [datamodel.dbml](datamodel.dbml) maar ook visueel te bekijken op. Dit document is meer een uiteenzetting van ideeën over een model en stamgegevens die bedoeld zijn voor specificatie van initiatieven.

_Dit document was eerst in het Engels maar is overgegaan op Nederlands nadat dit voor alle communicatie en documentatie gebruikt werd. Uitzondering is hierbij de code / technische documentatie omdat het gebruikelijk en meestal eenvoudiger & overdraagbaarder is om dit in het engels te doen._

# Initiative
There are various granularities in initiatives. There's different scenario's to take into account:

## Different types of initiative relations
Initiatives(organisations) can relate to each other in various ways. Local organisations can be a **child of** national organisations and vice versa. Local initiatives are **present on** national platforms. Local initiatives can **collaborate**. A few of these are already explained below.

### Local branches of national organisations
Offline initiatives can be assumed to be local where some of these local initiatives are part of a bigger national regional of national organisation. When crowdsourcing it could be relevant to exploit this hierachy and thus store information on different levels because there's relevant contact information. Wether or not and at what stage this hierarchy is actually stored and at what granularity (will we even go down as far as individuals?) is open for debate. It probably delays to much when doing this to early. But this is the reason there is already a ParentInitiativeID.

### Tracking information on a local level of national online platforms
An online platform is essentially a national organisation. In order to track information on a regional level (city probably) we can split the platform in local initiatives using the same logic as above. Information can then be tracked on this level.


# Model
Het ontwerp in [datamodel.dbml](datamodel.dbml) gaat uit van een eindsituatie zoals we de wensen zouden kunnen
vangen in een database. Echter gebruiken we Ushahidi om input en redactie van de data te faciliteren. Het feit dat dit een tool
is met meer flexibiliteit betekent dat het noodzakelijk wordt om te bedenken hoe we het eindmodel kunnen mappen op een model in Ushahidi. Daarnaast dient dit document als startpunt voor de definitie van stamgegegevens zoals categoriën, tags en andere classificaties.

## Uitdaging
Het datamodel tracht een balans te zoeken tussen bruikbaarheid en complexiteit. De voornaamste complexiteit zit hem in het netwerk aspect en de definitie van initiatief. In principe kan een facebook groep bijvoorbeeld een initiatief van een organisatie zijn, we kunnen die organisatie ook als initiatief beschouwen als deze zich op verschillende platformen presenteert. Het model faciliteert een simpele weergave waarbij de organisatie gewoon als velden is opgenomen in het initiatief. Het biedt echter ook de mogelijkheid om de initiatieven op te splitsen. Dit is echter vanuit beheersoogpunt met Ushahidi enkel in beperkte mate mogelijk. Hier over meer in de mapping.

## Data Definities
De volgende sectie doen een voorstel voor invulling van verschillende elementen voor classificatie.

### Organisatiesoort
* Religieus
* (Sport)Vereniging
* Buurthuis
* Welzijn
* Overheid _Het niveau van de overheid zou duidelijk moeten worden uit andere data zoals de schaal_
* Verzorgingshuis
* Bedrijf/ZZP  _Een ZZP'er is een individu maar opereert uit naam van z'n initiatief_
* NGO
* Online Platform
* Individu

_Buurthuis en Welzijn zijn vaak twee handen op één buik, dus wellicht is dat soms lastig in het onderscheid. Het is mogelijk om hier nog veel dieper onderscheid te maken. De vraag is in hoeverre dit wenselijk is in relatie tot het invoerproces_

### Types
* marketplace (bij elkaar brengen)
* mobilisatie/actie (vanuit initiatief actie)
* monitor/beeld (informatie bij elkaar brengen),
* grouping (zelf-help binnen de groep) _Dit is dan bijvoorbeeld een whatsapp groep in de peergroup van familie oid?_

### Categorieën
Van de aandachtskaart van LOT-C (Staat alleen in Drive):
1. (Medische) verzorging
1. Distribueren goederen en diensten
1. Opvang,boodschapdoen
1. Levensreddende handelingen
1. (Online) bijscholing
1. Mentaal ondersteunen van de samenleving (muziek maken op balkons, spontane steunuitingen aan zorgverleners)
1. Informatie en communicatie / contact onderhouden
_Wat moet ik me hier concreet bij voorstellen? Een website met algemene informatie? Willen we dit soort 'hulp' ook in kaart brengen?_
1. Delen/beschikbaar stellen lokale kennis
1. Handelingsperspectief (scholen, sporten, oefeningen, mindfulness)
_Het lastige vind ik dat handelingsperspectief misschien niet makkelijk uit te leggen is aan vrijwilligers. Daarom staat het in onderstaand voorstel allemaal onder mentaal / vermaak_

**Vertaald naar categorieën & aanvullingen:**  
Dit is geen definitieve of uitputtende lijst maar eerder een initiële inventarisatie van mogelijke categorieën.

* Zorg
  * Medisch
  * Ouderen
  * Gehandicapten
  * Kinderopvang
* Distributie
  * Goederen
  * Voedsel
  * Diensten
  * Personen
* Huishoudelijk
  * Schoonmaken
  * Boodschappen
  * Tuin
  * Onderhoud
* Onderwijs
  * Bijscholing
* Kennis
  * Lokaal
  * Onderzoek
* Geestelijk
  * Psychisch
  * Religieus
* Mentaal / vermaak
  * Muziek
  * Theater
  * Sport
  * Steunbetuiging
  * Coaching
* Productie
  * Gekwalificeerde hulpmiddelen
  * Ongekwalificeerd hulpmiddelen
* Onderdak
  * Daklozen
  * Hulpverleners

### Tags
Het idee is dat tags faciliteren in het flexibel verder classificeren van initiatieven met (binaire) eigenschappen zoals:
* Betaald
* IsOffline
* AdHoc
* Whatsapp, Facebook _Niet binair in die zin_
_Initiatief technisch zou dit ook kunnen betekenen dat een initiatief verschillende presence_on links zou hebben naar facebook groepen e.d. die als los initiatief opgenomen zijn_

## Mapping
Deze sectie beoogt invulling te geven aan hoe het datamodel en stamgegevens in Ushahidi worden opgenomen.