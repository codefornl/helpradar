# High level requirements & roadmap
This document is aimed at providing a high level overview in what various stages we can segment the development of this application. All with the aim of providing value as soon as possible. In essence this entails two things: Data Entry and Visualisation.

_At this stage this document is primarily a high level braindump of possible (non functional) requirements and features_

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
* _What can they do to (make this system) provide value for the responding community thus closing a gap?_
* _What (information) would bring most value for profressional organisations?_
* _What kind of visualisation of this information would aid in executing their responsiblities?_

## Crisis management
* _What are the specific types of data that are relevant in scenario evaluation?_
  * _Does the government has a taxonomy for segmenting civil organisations and is this relevant in this case?_
  * _What kind of aid categories/classifications for initiatives are important and/or crucial to have insights in?_
* _What kind of visualisation of this information would aid in executing their responsiblities?_
* _Which information if relevant over time? And at what frequency?_
* _What timeframes for intial delivery are we looking at right now?_
* _Are there any other systems with which interfaces are desired?_

## Responding community
* _What are their needs?_
  * _Where do they usually lack experience?_
* _What types of (relevant) organisations can we distinguish?_
* _Which types of organisations in the responding community are most likely to provide help? This in focussing data collection effort_
* _Which types of organisations in the responding community are most likely to be succesful in their help efforts? This in focussing data collection effort_
* _At what scales are different types of organisations._

## Data collectors
* _Do we have any idea or can we make an estimate of the amount of initiatives?_
* _Would they be doing the collection from home with a mobile phone?_
* _Is there capacity to coordinate the data collection region based?_
* _Would a script be helpful for calling?_
* _Is there a potential network throughout the country that can assist in the collection? VNG, Provinces, NGOs?_
* _Could we charter people within national organisations with regional branches themselves as proxy data collectors?_
* _Assuming anyone can be a data collector. Would it a simple report initiative form be helpful? 'Official' collectors can then follow up on this._

# Non functionals
* Infrastructure
  * Has to run on kubernetes infrastructure supplied by Code for NL.
* Maintainability
  * Dominant technology stack that is prevalent in the Code for NL community.
  * Necessary (community) coding standards are enforced in a CI pipeline.
  * Necessary minimum test automation in place to aid in continuous delivery.
* Testablity
  * Test environment availability.
* Security / Privacy _Any pentesters and security experts in the Code For NL community?_
  * Obviously has to adhere to AVG/GDPR where applicable.
  * Designed & built using OWASP guidelines.
* Interoperability
  * Has an open documented (Swagger) API for the public part of the data.
  * Integrate or export to [Humanitarian Data Exchange](https://data.humdata.org/)

# Features
Sections below describe a list of possible features for a solution.

## [Setup Project & Automation](https://github.com/codefornl/helpradar/milestone/1)
Initially the setup of this project is required. Given the desire for rapid development of this project
having the neccesary infrastructure & automation in place to achieve this is crucial.

* At least have test and production infrastructure in place. this implies:
  * Web servers
  * Data stores
* Setup project skeleton
* Setup test & delivery pipeline
* Setup internationalization
* Add Authentication

## [Initial Data Entry](https://github.com/codefornl/helpradar/milestone/2)
In order to start testing and collecting the desired data An MVP that allows for this should be constructed.

**Goal:** Setup an easy and quick data entry process that aids in a sane dataset.

Given the aim to crowdsource a lot of the data we can assume that if we don't take measures the data contains errors and duplicates. The idea is to leverage already available data on maps for instance. So one can search for a certain type of organisation and add that as an initiative.

* Identify / search potential organisations that setup civil initiatives on map
* Prevent duplicate entries by showing already known initiatieves.
* Report initiative (Maybe just a simple form which can then be further investigated/validated)
* Add initiative
* Update initiative
* Close initiative
* Add parent initiative/organisation
* Basic Call/Enquiry Script
* Have basic feedback in place

## Data Visualisation
* Show initiaves on a map 
_Could be relevant for search and thus go to earlier milestone_
* Visualize regional capacities
* Filter initiatives by ??
* Help Documentation

## Assistance
Merely providing the tools is probably not enough on the longer term. In order to bridge the gap between the responding community and the responding professionals allowing them to share knowledge and best practices is probably helpful. It's probably best to use off the shelf solutions for that such as message boards and wiki's.

* Add Discussion Board
* Provide Best Practices
* Add reader role (so professionals can get in touch with initiatives using private info)

## Collect follow up data
* Provide list of follow up tasks.
* Claim follow-up.
* Add follow up.
* Data Collection Endpoint.
* Api Key Management for the above.
* Scrapers

## AI Identification
What can ben helpful is that algorithms can scour the internet to identify possible initiatives which can then be validated and tracked bu humans.

## Gamification
This is me dreaming of mobilizing the crowd to provide the data by giving them some significance and extra motivation when they collaborate with us.