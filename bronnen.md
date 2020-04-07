# Platforms
Lijst van online bronnen voor initiatieven.

- [X] [Heldnodig](https://heldnodig.nl/)
- [X] [NL Voor Elkaar](https://www.nlvoorelkaar.nl/coronahulp/)
- [X] [Gewoon Mensen](https://www.gewoonmensendiemensenwillenhelpen.nl/)
- [ ] [Niet Alleen](https://nietalleen.nl/)
- [ ] [Corona Helpers](https://www.coronahelpers.nl/) __anti scrape mechanisme in werking, niet legaal om verder te gaan__
- [X] https://nijmegen-oost.nl/elkaar-helpen
- [X] https://puurpapendrecht.nl/
- [X] https://wijamsterdam.nl
- [ ] https://www.coronahulp.com/
- [ ] https://cooperatiewehelpen.nl/
- [ ] https://www.bezorg-dezorg.nl/ - __afgesloten met user/password/volledige persoonsgegevens__
- [ ] https://studentenhelpenscholieren.nl/
- [X] https://zorgheldenauto.nl



### Extra informatie
**api address:**: https://api-server-271218.appspot.com/v1/tasks?zipcode=1945RP&taskTypeId=32ea2942-68be-11ea-bc55-0242ac130003
Can't query without zipcode. Doing it for each zipcode implies millions of requests. 

**api address:**: https://www.coronahelpers.nl/api/deeds?query=&page=1&causes=&activities=&date=&pageSize=18&withOrganization=true
Uses paging where total amount of pages is returned in the response.
Accept: application/json
X-Requested-With: XMLHttpRequest
