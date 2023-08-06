import datetime
import logging
import requests


LOG = logging.getLogger(__name__)


def get_last_panel_update(panel_name: str) -> datetime:
    """
    Return a datetime object for when a panel was updated last time
    """

    url = "".join(["http://localhost:5000/api/v1/panels/", panel_name])
    headers = {"Accept": "application/json"}
    output_cli_call: requests.Response = requests.get(url, headers)
    panel_infos: list = output_cli_call.json()

    latest_update: datetime = panel_infos[0]["date"]

    panel_info: dict
    for panel_info in panel_infos:
        if panel_info["date"] > latest_update:
            latest_update = panel_info["date"]

    return latest_update


def check_if_gene_panel_updated(cases: dict) -> list[str]:
    """
    Check which cases that had their gene panel updated since
    the most recent analysis
    """
    cases_with_updated_gene_panel = []
    for i in range(len(cases)):
        if cases[i]["_id"] in cases_with_updated_gene_panel:
            continue
        for panel in cases[i]["panels"]:
            panel_last_update: datetime = get_last_panel_update(
                panel_name=panel["panel_name"]
            )
            if panel_last_update > cases[i]["analysis_date"]:
                cases_with_updated_gene_panel.append(cases[i]["_id"])
                break
    return cases_with_updated_gene_panel


def get_cases_that_need_new_analysis(cases: dict) -> list[str]:
    """
    Find cases that qualify for a new
    analysis among the monitored cases
    """
    cases_that_need_new_analysis: list[str] = check_if_gene_panel_updated(cases=cases)
    return cases_that_need_new_analysis
