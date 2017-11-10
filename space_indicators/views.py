# from django.shortcuts import render
from .api_connections import RequestSpacesRawData
from .models import PerOccupationArea
from .models import LastUpdateDate
from project_indicators.views import clean_url
from quero_cultura.views import ParserYAML
from datetime import datetime

DEFAULT_INITIAL_DATE = "2012-01-01 15:47:38.337553"


def populate_per_occupation_area():
    if len(LastUpdateDate.objects) == 0:
        LastUpdateDate(DEFAULT_INITIAL_DATE).save()

    index = LastUpdateDate.objects.count()
    last_update = LastUpdateDate.objects[index - 1].create_date

    parser_yaml = ParserYAML()
    urls = parser_yaml.get_multi_instances_urls

    for url in urls:
        request = RequestSpacesRawData(last_update, url).data
        new_url = clean_url(url)

        for space in request:
            for area in space["terms"]["area"]:
                PerOccupationArea(new_url, area).save()

    LastUpdateDate(str(datetime.now())).save()
