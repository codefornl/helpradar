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

# Data Definities
De volgende sectie doen een voorstel voor invulling van verschillende elementen voor classificatie.

### Organisatiesoort
* Religieus
* (Sport)Vereniging
* Buurthuis
* Stichting Welzijn
* School
* Overheid _Het niveau van de overheid zou duidelijk moeten worden uit andere data zoals de schaal_
* Verzorgingstehuis
* Bedrijf/ZZP  _Een ZZP'er is een individu maar opereert uit naam van z'n initiatief_
* Non-Profit
* NGO
* Online Platform
* Individu

_Buurthuis en Welzijn zijn vaak twee handen op één buik, dus wellicht is dat soms lastig in het onderscheid. Het is mogelijk om hier nog veel dieper onderscheid te maken. De vraag is in hoeverre dit wenselijk is in relatie tot het invoerproces_

### Types
* marketplace (bij elkaar brengen)
* mobilisatie (vanuit initiatief actie)
* monitor (informatie bij elkaar brengen),
* peergroup (zelf-help binnen de groep) _Dit is dan bijvoorbeeld een whatsapp groep in de peergroup van familie oid?_

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
  * Kinderopvang _Gewoon oppas of andere professionele vormen van kinderopvang_
* Transport
  * Goederen
  * Voedsel
  * Dienstverleners _In feite vervoer van niet burgers ofwel professionals zoals zorgverleners bijvoorbeeld._
  * Burgers
* Huishoudelijk
  * Schoonmaken
  * Boodschappen
  * Onderhoud _Klussen in huis of tuin_
* Onderwijs
  * Bijscholing
* Kennis
  * Lokaal _Mensen die kennis hebben van lokale organisaties, netwerken of regelgeving._
  * Onderzoek _Met kennis bij kunnen dragen aan onderzoeken._
* Geestelijk
  * Psychisch
  * Religieus
* Mentaal / vermaak
  * Muziek
  * Theater
  * Sport
  * Steunbetuiging _Acties als het versturen van kaartjes, zingen of klappen._
  * Coaching
* Productie _Productie van goederen ten behoeve van bijvoorbeeld hulpverleners of hulpbehoevenden._
  * Gekwalificeerde hulpmiddelen _Hulpmiddelen die zijn goedgekeurd voor professioneel gebruik_
  * Ongekwalificeerd hulpmiddelen _Hulpmiddelen zonder keurmerk of goedkeuring._
  * Voedsel _Productie van voedsel (bijvoorbeeld restaurants die nu wel thuis bezorgen._
* Onderdak
  * Daklozen
  * Hulpverleners
* Personeel

### Tags
Het idee is dat tags faciliteren in het flexibel verder classificeren van initiatieven met (binaire) eigenschappen zoals:
* Betaald
* IsOffline
* AdHoc
* Whatsapp, Facebook _Niet binair in die zin_
_Initiatief technisch zou dit ook kunnen betekenen dat een initiatief verschillende presence_on links zou hebben naar facebook groepen e.d. die als los initiatief opgenomen zijn_

# Ushahidi Mapping
Deze sectie beoogt invulling te geven aan hoe het datamodel en stamgegevens in Ushahidi worden opgenomen.

## Beperkingen
Er zijn een aantal beperkingen die enerzijds lastig zijn en anderzijds mogelijkheden bieden.

* Is met name goed in losse locatiegebaseerde informatie met als uitgangspunt een gebeurtenis.
  * Een initiatief is nog te beschouwen als een gebeurtenis. Maar een contact of een meetmoment hebben hier niet zo heel veel meer mee te maken. 
* Kan geen data inhoudelijk valideren, enkel verplichten ja of nee.
* Niet echt geschikt om relaties te leggen. Althans, die mogelijkheid is beperkt tot relaties tussen verschillende type posts.
  * Het is echter wel mogelijk om vanuit een taak hangend aan een survey relaties te leggen naar types van surveys van hetzelfde type!

## Uitzonderingen
De vertaling van velden in het datamodel naar de veldnamen in ushahidi zou mapping vrij eenvoudig moeten maken. Ik ga hier met name even in op hoe we uitzonderingen (kunnen) vormgeven in Ushahidi.

### Tags
Ushahidi kent niet het concept van tags. Checkboxes komen misschien het dichts bij maar zijn niet flexibel. Om te voorkomen dat mensen maar vrijelijk allerlei tags toe kunnen voegen doen we het met twee velden. Een checkboxes veld Tags en een korte tekst veld 'Tags Nieuw'

### Initiative Links
De enige manier om relaties te leggen naar posts van eenzelfde type is door taken te maken. In zo'n taak kan wel een link naar een post van het type initiatief gemaakt worden. Voor iedere link type zouden we dan een taak aan kunnen maken. Dit heeft wel als effect dat de informatie niet als zodanig publiek te verkrijgen is en waarschijnlijk ook niet te exporteren.

Per taak kunnen we dan één of meerdere relatievelden aanmaken. Maar dit moet zich allemaal nog gaan vormen.

Taken:
* Aanwezig op _Hier beginnen we mee omdat dit in feit voor iedere entry op een platform hoort_
* Kind van
* Werkt samen met
* Verwijst naar

### Contacten
Ushahidi is hier niet heel erg geschikt voor. Bij voorkeur zoeken we hier een andere tool voor. We zouden dit voor nu in een vrij tekstveld op kunnen nemen. Maar ook dit is wel weer privacygevoelige informatie! We kunnen contacten ook al posttype opnemen, maar deze mogen dan niet gepubliceerd worden en zijn ook eigenlijk niet te vinden op deze manier.