import logging
import re
import datetime
from dateutil import parser

from typing import Generator

from bs4 import BeautifulSoup

from models.initiatives import InitiativeImport, InitiativeGroup
from .scraper import Scraper, PlatformSource, PlatformSourceConfig, ScrapeException


class CoronaPioniersSourceConfig(PlatformSourceConfig):
    _LIST_ENDPOINT = "posts/geojson?has_location=mapped&limit=200&offset=0&order=desc&order_unlocked_on_top=true&orderby=created&source%5B%5D=sms&source%5B%5D=twitter&source%5B%5D=web&source%5B%5D=email&status%5B%5D=published&status%5B%5D=draft"
    _API_URL = "https://coronapioniers.vpro.nl/api/v3/"
    
    def __init__(self, group, url):
        super().__init__(
            self._API_URL,
            self._LIST_ENDPOINT,
            None
        )
        self.group = group
        self.url = url

    def get_api_list_url(self):
        return self._API_URL + self._LIST_ENDPOINT

    def get_api_post_url(self, post_id):
        return self._API_URL + "posts/" + str(post_id)

    def get_api_category_tags_url(self):
        return self._API_URL + "tags"
    
    def get_api_media_url(self, media_id):
        return self._API_URL + "media/" + str(media_id)

class CoronaPioniersSource(PlatformSource):

    def __init__(self, config: CoronaPioniersSourceConfig):
        super().__init__(config)

    def initiatives(self) -> Generator[InitiativeImport, None, None]:
        self.category_dict = self.get_category_dict()

        url = self.config.get_api_list_url()
        page = PlatformSource.get(url)

        try:
            result = page.json()
            for feature in result['features']:
                initiative = InitiativeImport(
                    name=feature['properties']['title'],
                    description=feature['properties']['description'],
                    group= self.config.group,
                    source=self.config.url,
                    source_id=feature['properties']['id'],
                    source_uri=feature['properties']['url'].replace('/api/v3', ""),
                    longitude=feature['geometry']['geometries'][0]['coordinates'][0],
                    latitude=feature['geometry']['geometries'][0]['coordinates'][1]
                )
                yield initiative
        except Exception as ex:
            msg = f"Error reading contents from {url}"
            raise ScrapeException(msg) from ex

    def complete(self, initiative: InitiativeImport):
        post_url = self.config.get_api_post_url(initiative.source_id)
        detail = PlatformSource.get(post_url)

        try:
            initiative_url_guid = '75aa5e4d-fe98-4a7a-94ec-adab2f7f9b88'

            result = detail.json()
            initiative.created_at=parser.parse(result['created'])
            initiative.scraped_at=datetime.datetime.now()
            
            initiative.name=result['title']
            initiative.description=result['content']

            if initiative_url_guid in result['values']:
                initiative.url = result['values'][initiative_url_guid][0]
            
            initiative.extra_fields = self.parse_extra_fields(result)

            category_list = []
            for tag in result['tags']:
                category_list.append(self.category_dict[tag['id']])
            s = ', '
            initiative.category = s.join(category_list)

        except Exception as ex:
            msg = f"Error in complete function for initiative {initiative.source_id}"
            raise ScrapeException(msg) from ex
    
    def parse_extra_fields(self, result):
            video_url_guid = 'eb9426ec-4951-426c-97f6-77f1e099df1c'
            image_url_guid = '9509810c-6489-47e4-9192-5af926609e08'

            extra_fields = dict()
            if image_url_guid in result['values']:
                if result['values'][image_url_guid]:
                    image_id=result['values'][image_url_guid][0]
                    image_api_url = self.config.get_api_media_url(image_id)
                    image_response = PlatformSource.get(image_api_url)
                    image_response_json = image_response.json()
                    if image_response_json['original_file_url']:
                        image_url = image_response_json['original_file_url']
                        extra_fields['image'] = image_url
            if video_url_guid in result['values']:
                if result['values'][video_url_guid]:
                    video_url = result['values'][video_url_guid][0]
                    extra_fields['video'] = video_url

            if extra_fields:
                return str(extra_fields)
            else:
                return None

    def get_category_dict(self):
        category_dict = dict()
        category_tags_url = self.config.get_api_category_tags_url()
        category_tags = PlatformSource.get(category_tags_url)

        try:
            result = category_tags.json()
            for tag in result['results']:
                tag_id = tag['id']
                tag_tag = tag['tag']
                category_dict[tag_id] = tag_tag
            return category_dict
        except Exception as ex:
            msg = f"Error processing categories from tag api"
            raise ScrapeException(msg) from ex

class CoronaPioniers(Scraper):
    """Corona Pioniers scraper die zowel vraag als aanbod ophaalt"""

    def __init__(self):
        super().__init__("https://coronapioniers.vpro.nl", 'Corona Pioniers', "copi")
        self.add_source(CoronaPioniersSource(
            CoronaPioniersSourceConfig(
                InitiativeGroup.SUPPLY,
                self.platform_url)))

    def scrape(self):
        # Could better use template method on base class instead of require super call
        super().scrape()

    def get_logger(self) -> logging.Logger:
        return logging.getLogger("platformen.coronapioniers")

    def set_group(self, group: InitiativeGroup):
        super(CoronaPioniers, self).set_group(group)
        delete_source = next((g for g in self._sources if g.config.group is not group), None)
        if delete_source:
            self.remove_source(delete_source)

    def supports_group(self, group):
        return True
