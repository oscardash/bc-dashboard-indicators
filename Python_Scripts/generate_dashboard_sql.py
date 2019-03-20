import collections
import json
import os
import xml.etree.ElementTree


CONFIG_FILENAME = "config.json"


class Indicator(object):
    def __init__(self, name):
        self.name = name


class IndicatorParser(object):
    def parse_indicator(self, filehandle):
        tree = xml.etree.ElementTree.parse(filehandle)
        root = tree.getroot()

        name = root.find("./heading/name").text

        return Indicator(name)


class SQLGenerator(object):
    def generate_indicator_insert_statement(self, indicator):
        return ""


class SQLWriter(object):
    def write(self, indicators, output_filehandle):
        pass


class IndicatorRepository(object):
    def __init__(self):
        self.script_directory = os.path.dirname(__file__)
        self.root_directory = os.path.dirname(self.script_directory)

        config_filepath = os.path.join(self.script_directory, CONFIG_FILENAME)
        with open(config_filepath, "r") as filehandle:
            self.config_data = json.load(filehandle)

    def get_dashboard_names(self):
        return self.config_data["dashboards"]

    def get_indicator_paths(self, dashboard):
        indicator_paths = []

        dashboard_directory = os.path.join(self.root_directory, dashboard)
        for filename in os.listdir(dashboard_directory):
            if filename.endswith("xml"):
                indicator_path = os.path.join(dashboard_directory, filename)
                indicator_paths.append(indicator_path)

        return indicator_paths


def main():
    indicator_repository = IndicatorRepository()
    dashboards = indicator_repository.get_dashboard_names()

    dashboard_indicators = collections.defaultdict(list)

    parser = IndicatorParser()
    for dashboard in dashboards:
        indicator_paths = indicator_repository.get_indicator_paths(dashboard)
        for path in indicator_paths:
            with open(path, "rb") as indicator_filehandle:
                indicator = parser.parse_indicator(indicator_filehandle)
                dashboard_indicators[dashboard].append(indicator)

    for dashboard in dashboard_indicators:
        for indicator in dashboard_indicators[dashboard]:
            print("{} {}".format(dashboard, indicator.name))


if __name__ == "__main__":
    main()