# High level requirements & roadmap
This document is aimed at providing a high level overview in what various stages we can segment the development of this application. All with the aim of providing value as soon as possible. In essence this entails two things: Data Entry and Visualisation.

_At this stage this document is primarily a high level braindump of possible (non functional) requirements or features_

# Context
This solution sets out to map the civil initiatives (responding community) from various perspectives like location, type, size and time. This to aid the responding professionals and government(crisis management) in providing support and decision making. One of the main challenges in achieving this is the fact that a large part of these civil initiatives is situated offline. There is virtually no benefit for these organisation to spend time in reporting their activities online. So it is largely required to go and get that information.

So the stakeholders in this system will be:
* Responding professionals
* Crisis management
* Responding community
* Data collectors
   
The primary objective sets out to aid the first two. The aim in designing the system however is to add value for
all of these groups. Providing added benefit for the responding community can reduce the burden on data collectors thus increasing the chances of higher quality data.

## Responding professionals
* _What can they do to make this system provide value for the responding community this closing a gap?_
* _What (information) would bring them most value?_

## Crisis management
* _What are the specific types of data that are relevant in scenario evaluation?_
* _Which information if relevant over time? And at what frequency?_
* _What timeframes for intial delivery are we looking at right now?_
* _Are there any other systems with which interfaces are desired?_

## Responding community
* _What are their needs?_
* _Which types of organisations in the responding community are most likely to provide help? This in focussing data collection effort_

## Data collectors
* _Do we have any idea or can we make an estimate of the amount of initiatives?_
* _Would they be doing the collection from home with a mobile phone?_
* _Is there capacity to coordinate the data collection region based?_
* _Would a script be helpful for calling?_
* _Is there a potential network throughout the country that can assist in the collection?_
* _Could we charter people within national organisations with regional branches themselves as proxy data collectors?_

# Non functionals
* Infrastructure
  * Has to run on kubernetes infrastructure supplied by Code for NL.
* Maintainability
  * Dominant technology stack that is prevalent in the Code for NL community.
  * Necessary (community) coding standards are enforced in a CI pipeline.
  * Necessary minimum test automation in place to aid in continuous delivery.
* Testablity
  * Test environment availability.
* Security / Privacy
  * Obviously has to adhere to AVG/GDPR where applicable.

# Iterations

## Setup Project
Initially the setup of this project is requirement. Given the desire for rapid development of this project
having the neccesary infrastructure & automation in place to achieve this is crucial.
* At least have test and production infrastructure in place. this implies:
  * Web servers
  * Data stores
* Setup project skeleton
* Setup test & delivery pipeline

## Initial Data Entry
The sooner we can start collecting data the better.

* Identify / search potential organisations that setup civil initiatives on map
* Prevent duplicate entries by showing already known initiatieves.
* Add initiative
* Edit initiative
* Add parent initiative/organisation

## Data Visualisation
* Show initiaves on a map
* Visualize regional capacities
* Filter initiatives by ??

## Collect follow up data
* Provide list of follow up tasks.
* Claim follow-up.
* Add follow up.
