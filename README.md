[![Coverage Status](https://coveralls.io/repos/github/codefornl/helpradar/badge.svg?branch=master)](https://coveralls.io/github/codefornl/helpradar?branch=master) [![Build Status](https://travis-ci.org/codefornl/helpradar.svg?branch=master)](https://travis-ci.org/codefornl/helpradar)

# Wat is helpradar?
Helpradar is een digitaal platform waar initiatieven in de samenleving, waarin mensen en bedrijven hulp aan elkaar bieden en elkaar om hulp vragen, in beeld worden gebracht. Helpradar is een platform waarin bestaande online platformen "aan elkaar worden geknoopt" en worden aangevuld met locatie, contactgegevens, verzorgingsgebied, schaal, capaciteit en andere indicatoren die informatie over de initiatieven bruikbaar maken in bredere zin.

# Waarom helpradar?
Tijdens een crisis, zoals momenteel met Corona, maakt onze overheid gebruik van een crisismanagement proces. In dit proces zijn alle professionele hulpverleners betrokken en druk bezig met het uitwisselen van digitale gegevens.

Een zeer actieve groep blijft echter buiten beeld; bedrijven en gewone mensen die elkaar de hand reiken en steunen in moeilijke tijden. Deze steun kent vele vormen. Zo is er de directe hulp aan elkaar, geestelijke bijstand en contact op afstand, maar ook "grotere" hulp in de vorm van geimproviseerde productie (bijv. van mondkapjes), het opschalen van bestaande productie (bijv. het maken van meer sterilisatie middelen) en een verschuiving in (logistieke) capaciteit (bijv. taxibedrijven die artsen van en naar nood-ziekenhuizen verplaatsen, boeren die rechtstreeks aan mensen leveren).

Wij denken dat het goed is als de "professionele organisaties" weten wat de "initiatieven uit de samenleving" zijn en doen, zodat kan worden gekeken of deze de professionele hulpverlening kan versterken.

# Hoe werkt helpradar?
1. Een (ongeorganiseerd) team van vrijwilligers speurt het internet af naar platformen met hulp initiatieven op internet.
2. De platformen worden vervolgens in een verwerkingsschema geplaatst. 
3. Van alle platformen wordt gekeken of het hulp- vraag en aanbod geautomatiseerd kan worden verwerkt.
4. De automatische verwerking "dumpt" het hulp- vraag en aanbod in een "ruwe" index
5. De ruwe index wordt vervolgens vereikt met locatie informatie
6. De ruwe index wordt middels [NLP](https://en.wikipedia.org/wiki/Natural_language_processing) geanalyseerd om zo trends te ontdekken in het vraag en aanbod
7. Op basis van de trends worden gecategoriseerd en bepaald welke informatie bruikbaar is
8. Van de bruikbare informatie worden de bronnen benaderd en wordt hen gevraagd of ze bereid zijn vermeld te worden en indicatoren te delen.
9. De informatie die vervolgens beschikbaar is en kwalitatief goed is kan (geautomatiseerd) worden gedeeld met professionele hulpverleners

# Wie werken er aan helpradar?
Vanuit de Community van Code For NL is het initiatief gestart. In onze ogen valt een systeem als helpradar onder de [commons](https://en.wikipedia.org/wiki/Digital_commons_(economics)) en is het zaak dat dit een product is van de samenleving dat niet door de overheid, bedrijven of personen economisch of anderszins kan worden uitgebaat. De regie over een database met helpbieders en hulpvragers dient uiterst zorgvuldig te worden georganiseerd. Wij werken dan ook samen met onafhankelijke partijen die een duidelijke visie hebben met betrekking tot privacy en commons en kunnen faciliteren in een veilige en goed beveiligde omgeving die desondanks de samenleving en individuele personen regie geeft over de eigen en de gemeenschappelijke informatie.

## Help Helpradar!
We kunnen zeker wel wat handjes gebruiken op de korte en lange termijn. Voor ontwikkelaars die willen helpen:
zie de [Contribution Guidelines](CONTRIBUTING.md).

We kunnen sowieso al hulp gebruiken van:
* **Developers & Data scientists** Om zoveel mogelijk data van online & social media platformen binnen te halen en te analyseren.
* **Designers** Voor een logo, simpele website maar vooral een visueel concept neer te zetten wat dit kan worden.

# Visie
Dit is een tijd waarin mensen vanuit intrinsieke motivatie allerlei hulp bieden. We verlangen naar een wereld waarin mensen co-creëren voor het welzijn van de samenleving vanuit deze stimulerende intrinsieke motivatie. Wij willen een veilige omgeving bieden om hulp te delen.

## Missie
Het doel is inzicht te bieden in de beweging van mensen en professionals om deze (en anderen) te helpen in tijd van een crisis effectief te werk te gaan en een nationaal inzicht te creëren.

Door te laten zien welke initiatieven er zijn willen we anderen motiveren ook actief te worden. Door in werkelijke behoefte te voorzien en alle geweldige dingen te laten zien die mensen kunnen brengen als ze samen meedoen om te creëren en/of te bieden wat het hardste nodig is.

## Principes
Bij het ontwerp en de ontwikkeling van dit project hanteren we de volgende principes:
* Privacygevoelige informatie wordt tot een absoluut minimum beperkt.
* Alle niet-privacyspecifieke informatie is voor iedereen zichtbaar.
* Open source en open ontwikkeling waar mogelijk volgens de methode: [standard for public code](https://standard.publiccode.net/).
* Samen praten, samen werken, samen doen. Wij hebben vooral technische kennis, maar werken samen met onafhankelijke digitaal maatschappelijke organisaties die dezelfde grondbeginselen van een vrij en veilig internet hanteren.

## Succes criteria
Betrokkenheid en actieve deelname door:
* Digitale platformen die bereid zijn hulp- vraag en aanbod te delen
* Ontwikkelaars en digitaal deskundigen
* Professionele hulporganisaties
* Maatschappelijke organisaties
* Steun vanuit de overheid

Begeleiding en aansturing vanuit de behoeftestelling door:
* Het landelijk operationeel team


# Specificaties
Een wijziging in de strategie heeft er toe geleid dat we nu met name focussen op meer data 
verzamelen van verschillende platformen en middels een iteratief proces met het LOT-C 
bepalen of/wanneer kwaliteit van data belangrijker wordt dat de kwantiteit. Veel va de 
documenten in de docs folder zijn dan ook niet meer helemaal actueel. De focus ligt nu 
op de specificaties in de issues in het Mining Project: https://github.com/codefornl/helpradar/projects/2
en de milestone: https://github.com/codefornl/helpradar/milestone/3