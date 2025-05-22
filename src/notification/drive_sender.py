import json
import time

from notification.isender import ISender
from schemas import ReportConfig


class DriveSender(ISender):
    highlight_tags = ("__", "__")

    def __init__(self, report_config: ReportConfig) -> None:
        self.hide_filters = report_config.hide_filters
        self.header_text = report_config.header_text
        self.footer_text = report_config.footer_text
        self.no_results_found_text = report_config.no_results_found_text

    def send(self, search_report: list, report_date: str = None):
        """Parse the content, and save contents in Drive"""
        print("SEND")
        print("RESULTS")
        print(search_report)
        search_report.append({"timestamp": time.time()})
        with open("drive/results.json", "w") as file:
            json.dump(search_report, file)
