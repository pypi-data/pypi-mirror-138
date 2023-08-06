import json
import logging

from melter.triggers import get_cases_that_need_new_analysis
from melter.utils import run_command


LOG = logging.getLogger(__name__)


def check_load_on_cluster(cases: list[str]) -> list[str]:
    """
    Adjust the number of cases to start based
    on computational resources available
    """
    return [cases[0]]


def start_jobs(cases: list[str]) -> None:
    """
    Start an analysis for the given cases
    """
    cases_to_start: list[str] = check_load_on_cluster(cases=cases)
    for case in cases_to_start:
        LOG.info("Starting analysis for %s" % case)


# from bson.json_util import loads


def get_monitored_cases() -> dict:
    """
    Return a list of cases that are monitored
    """
    output_cli_call: str = run_command(
        ["scout", "export", "cases", "--json", "--rerun-monitor"]
    )
    return json.loads(output_cli_call)


def run_workflow() -> None:
    """
    Run all the steps needed for perpetual
    genomic monitoring:
    - Find all monitored cases
    - Identify monitored cases that need new analysis
    - Start the analyses
    """
    LOG.info("Requesting cases marked for monitoring in scout")
    monitored_cases: dict = get_monitored_cases()

    LOG.info("Identifying cases which need a new analysis")
    cases_that_need_new_analysis: list[str] = get_cases_that_need_new_analysis(
        cases=monitored_cases
    )

    LOG.info("Starting analyses")
    start_jobs(cases=cases_that_need_new_analysis)
