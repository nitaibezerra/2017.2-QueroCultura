from .api_connection import RequestAgentsRawData
from django.shortcuts import render
from .models import PercentIndividualAndCollectiveAgent
from .models import AmountAgentsRegisteredPerMonth
from .models import PercentAgentsPerAreaOperation
from datetime import datetime
import json
import yaml
from celery.decorators import task
from quero_cultura.views import build_temporal_indicator
from quero_cultura.views import build_operation_area_indicator

DEFAULT_INITIAL_DATE = "2013-01-01 15:47:38.337553"


def index(request):
    update_agent_indicator()
    index = PercentIndividualAndCollectiveAgent.objects.count()

    per_type = PercentIndividualAndCollectiveAgent.objects[index-1]
    per_area = PercentAgentsPerAreaOperation.objects[index-1]
    temporal = AmountAgentsRegisteredPerMonth.objects[index-1]

    per_area = per_area.total_agents_area_oreration
    temporal = temporal.total_agents_registered_month

    total_per_type = per_type.total_individual_agent
    total_per_type += per_type.total_collective_agent
    percent_indivividual = per_type.total_individual_agent/total_per_type * 100
    percent_collective = per_type.total_collective_agent / total_per_type * 100
    per_type_keys = ["Individual", "Coletivo"]
    per_type_values = [round(percent_indivividual, 2), round(percent_collective, 2)]

    per_area_keys = []
    per_area_values = []

    for area in per_area:
        if area == area.capitalize():
            per_area_keys.append(area)
            per_area_values.append(per_area[area])

    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    last_year = 2013 + len(temporal)
    growthing = 0

    temporal_keys = []
    temporal_values = []
    temporal_growth = []

    for year in range(2013, last_year):
        for month in months:
            if (month in temporal[str(year)]):
                temporal_keys.append(str(year) + "-" + month)
                temporal_values.append(temporal[str(year)][month])

                growthing += temporal[str(year)][month]
                temporal_growth.append(growthing)

    context = {
        'per_area_keys': json.dumps(per_area_keys),
        'per_area_values': json.dumps(per_area_values),
        'per_type_keys': json.dumps(per_type_keys),
        'per_type_values': json.dumps(per_type_values),
        'temporal_keys': json.dumps(temporal_keys),
        'temporal_values': json.dumps(temporal_values),
        'temporal_growth': json.dumps(temporal_growth),
    }

    return render(request, 'agents_indicators/agents-indicators.html', context)


def build_type_indicator(new_data):
    per_type = {}

    for agent in new_data:
        if not (agent["type"]["name"] in per_type):
            per_type[agent["type"]["name"]] = 1
        else:
            per_type[agent["type"]["name"]] += 1

    return per_type


#@task(name="update_agent_indicator")
def update_agent_indicator():
    if len(PercentIndividualAndCollectiveAgent.objects) == 0:
        PercentIndividualAndCollectiveAgent(0, DEFAULT_INITIAL_DATE, 0, 0).save()
        PercentAgentsPerAreaOperation(0, DEFAULT_INITIAL_DATE, {"Literatura": 0}).save()
        AmountAgentsRegisteredPerMonth({"2015": {"01": 0}}, DEFAULT_INITIAL_DATE).save()

    index = PercentAgentsPerAreaOperation.objects.count()

    last_per_area = PercentAgentsPerAreaOperation.objects[index-1]
    last_type = PercentIndividualAndCollectiveAgent.objects[index-1]
    last_temporal = AmountAgentsRegisteredPerMonth.objects[index-1]

    urls_files = open("./urls.yaml", 'r')
    urls = yaml.load(urls_files)

    new_per_area = last_per_area.total_agents_area_oreration
    new_individual = last_type.total_individual_agent
    new_collective = last_type.total_collective_agent
    new_temporal = last_temporal.total_agents_registered_month

    new_total = last_per_area.total_agents

    for url in urls:
        request = RequestAgentsRawData(last_per_area.create_date, url)
        print("\n\n\nteste\n\n\n")

        new_per_area = build_operation_area_indicator(request.data, new_per_area)
        new_temporal = build_temporal_indicator(request.data, new_temporal)
        new_type = build_type_indicator(request.data)

        if "Individual" in new_type:
            new_individual += new_type["Individual"]

        if "Coletivo" in new_type:
            new_collective += new_type["Coletivo"]

        new_total += request.data_length

    new_create_date = datetime.now().__str__()

    AmountAgentsRegisteredPerMonth(new_per_month, new_create_date).save()
    PercentIndividualAndCollectiveAgent(new_total, new_create_date, new_individual, new_collective).save()
    PercentAgentsPerAreaOperation(new_total, new_create_date, new_per_area).save()
