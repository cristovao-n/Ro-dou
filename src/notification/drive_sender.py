import json
import time
import re
from notification.isender import ISender
from schemas import ReportConfig


class DriveSender(ISender):
    highlight_tags = ("__", "__")

    def __init__(self, report_config: ReportConfig) -> None:
        self.hide_filters = report_config.hide_filters
        self.header_text = report_config.header_text
        self.footer_text = report_config.footer_text
        self.no_results_found_text = report_config.no_results_found_text

        self.output = []  # Collect messages here

    def send(self, search_report: list, report_date: str = None):
        """Parse the content and collect messages"""

        if self.header_text:
            header_text = self._remove_html_tags(self.header_text)
            self.send_text(header_text)

        for search in search_report:
            if search["header"]:
                self.send_text(f'**{search["header"]}**')

            for group, search_results in search["result"].items():
                if not self.hide_filters and group != "single_group":
                    self.send_text(f"**Grupo: {group}**")

                for term, term_results in search_results.items():
                    if not self.hide_filters:
                        if not term_results:
                            self.send_text(f"**{self.no_results_found_text}**")
                        else:
                            self.send_text(f"\n*Resultados para: {term}*")

                    for department, results in term_results.items():
                        if not self.hide_filters and department != "single_department":
                            self.send_text(f"{department}")

                        self.send_embeds(results)

        if self.footer_text:
            footer_text = self._remove_html_tags(self.footer_text)
            self.send_text(footer_text)
        self.send_text(time.time())
        with open("drive/results.json", "w") as file:
            file.write("\n".join(str(item) for item in self.output))
        
    def send_text(self, content):
        self.output.append(content)

    def send_embeds(self, items):
        for item in items:
            line = f"{item['title']}\n{item['abstract']}\n{item['href']}\n"
            self.output.append(line)

    def _remove_html_tags(self, text):
        return re.sub(r"<.*?>", "", text)
