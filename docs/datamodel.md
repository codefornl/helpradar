# Data Model Draft
This is a draft of the data being stored. It's merely a list of possible things I can come up with. This it might contain a lot more privacy related information than what is really necessary. At this stage we can safely assume a lot of unknowns. 

## Initiative
There are various granularities in initiatives. Many are the offline initiatives can be assumed to be local where some of these local initiatives are part of a bigger national regional of national organisation. When crowdsourcing it could be relevant to exploit this hierachy and thus store information on different levels because there's relevant contact information. Wether or not and at what stage this hierarchy is actually stored is open for debate. It probably delays to much when doing this to early. But this is the reason there is a ParentInitiativeID.

_I'm curious as to what is helpful for data scientists_

* Id
* ParentInitiativeId
* Name
* Type
  * Religous Centre
  * Sports Club
  * Community Center
  * Nursing Home
  * Commercial
  * NGO's (This are pro and possibly not belong in this list.)
  * Online Platform
* Ad-hoc or existing?
* Categories _A Tagging system that allows for multiple options, what granularity is valuable here?_
  * Transport
  * Healthcare
  * Care
  * Medical Supplies
  * Food
  * Non Food
  * Social
  * Psychological
  * Entertainment
* Url
* Location
  * Address
  * Neighbourhood
  * Municipality
  * Province / Region
  * Geolocation
* Remarks
* Stats {0..*}
* Contacts {0..*}

## Stat
Here there is a lot unclarity. Initial conversations made clear that it is relevant to get a picture over time. Since initiatives come, grow and go or merge together. So time and scale are relevant here. But there's still a lot unclear in what ways to possibly expres that. For online platforms it could be relevant to store a daily **resolution capacity** in terms of cases. For offline initiatives merely their activity and/or the size of the initiative in terms of (active) members is probably enough since other numbers aren't tracked_

* RecordDate
* IsActive
* Volunteercount
* Resolution capacity 

## Contact
Given infomation over time is desired. These contacts are either the ones being called periodically to check in or otherwise people that are themselves responsible for data entry.
* Name
* Organisational Role
* Phone
* Email
