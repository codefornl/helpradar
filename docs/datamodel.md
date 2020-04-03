# Data Model Draft
This is a draft of the data being stored. It's merely a list of possible things I can come up with. This it might contain a lot more privacy related information than what is really necessary. At this stage we can safely assume a lot of unknowns. 

## Initiative
There are various granularities in initiatives. There's different scenario's to take into account:

### Local branches of national organisations
Offline initiatives can be assumed to be local where some of these local initiatives are part of a bigger national regional of national organisation. When crowdsourcing it could be relevant to exploit this hierachy and thus store information on different levels because there's relevant contact information. Wether or not and at what stage this hierarchy is actually stored and at what granularity (will we even go down as far as individuals?) is open for debate. It probably delays to much when doing this to early. But this is the reason there is already a ParentInitiativeID.

### Tracking information on a local level of national online platforms
An online platform is essentially a national organisation. In order to track information on a regional level (city probably) we can split the platform in local initiatives using the same logic as above. Information can then be tracked on this level.

### Model
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
* Ad-hoc or existing?
* IsOffline (_There is no data available/open online_)
* Url (_Having a url does not neccesarily mean the data is online_)
* Location
  * Address
  * Neighbourhood
  * Municipality
  * Province / Region
  * Geolocation
* Date Added
* Date Closed (If the initiative no longer is active)
* Remarks
* Stats {0..*}
* Contacts {0..*}
* _Maybe a potential network between initiatives exists?_

## Stat
Here there is a lot unclarity. Initial conversations made clear that it is relevant to get a picture over time. Since initiatives come, grow and go or merge together. So time and scale are relevant here. But there's still a lot unclear in what ways to possibly expres that. For online platforms it could be relevant to store a daily **resolution capacity** in terms of cases. For offline initiatives merely their activity and/or the size of the initiative in terms of (active) members is probably enough since other numbers aren't tracked_

* RecordDate
* Type/Domain (Healthcare, Transport...)
* Number
* Name/Code (_This is tricky for manual data entry, maybe should be based on definition in initiative_)
* RecordType (Total, Delta)
* Unit (This is most probably defined by the type)
* (Resolution)capacity
  * _Looking at this from a broader perspective. The capacity in terms of (medical) supplies is not defined in people but in products and their types. This is a different ballgame and on the other hand it's not. The capicity as is listed here is the amount of products produced or cases resolved since the last report_

## Contact
Given infomation over time is desired. These contacts are either the ones being called periodically to check in or otherwise people that are themselves responsible for data entry.
* Name
* Organisational Role
* Phone
* Email
