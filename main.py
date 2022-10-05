import os
import xml.dom.minidom
import dateutil.parser as dp
from dateutil.relativedelta import *
from data import Data
import json

# Get element value using selector
def get_element_value(element, selector):
    return element.getElementsByTagName(selector)[0].firstChild.nodeValue


# Calculate the needed absolute values
def get_searched_row_value(row_values):
    sum_feedA = 0
    sum_usgA = 0
    for r in row_values:
        if r.getAttribute("obis") == "1-1:1.8.1":
            sum_usgA += float(r.getAttribute("value"))
        if r.getAttribute("obis") == "1-1:1.8.2":
            sum_usgA += float(r.getAttribute("value"))
        if r.getAttribute("obis") == "1-1:2.8.1":
            sum_feedA += float(r.getAttribute("value"))
        if r.getAttribute("obis") == "1-1:2.8.2":
            sum_feedA += float(r.getAttribute("value"))

    return [sum_feedA, sum_usgA]


def get_highest_absolute_value_from_esl_files():
    sum_feedA = 0
    sum_usgA = 0
    highest_time = 0.0
    # Path to the ESL-Files
    path_of_the_directory = os.getcwd() + "/static/files/ESL-Files"
    # Iterate through the files in this directory
    for filename in os.listdir(path_of_the_directory):
        f = os.path.join(path_of_the_directory, filename)
        if os.path.isfile(f):
            # Open file
            with open(f, "r") as file:
                # Make file to dom
                with xml.dom.minidom.parse(file) as dom:
                    time_period = dom.getElementsByTagName("TimePeriod")
                    row_values = dom.getElementsByTagName("ValueRow")
                    for t in time_period:
                        # Convert ISO 8601 timestamp to UNIX timestamp
                        if highest_time < dp.parse(t.getAttribute("end")).timestamp():
                            values = get_searched_row_value(row_values)
                            sum_feedA = values[0]
                            sum_usgA = values[1]
                            highest_time = dp.parse(t.getAttribute("end")).timestamp()

    return [sum_usgA, sum_feedA, highest_time]


def parse_sdat(path=os.getcwd() + "/static/files/SDAT-Files"):
    dict = {}
    for file in os.listdir(path):
        fullname = os.path.join(path, file)
        dom = xml.dom.minidom.parse(fullname)
        # ID of the Meter
        id = get_element_value(dom, "rsm:DocumentID")[-3:]
        # Start Datetime of the Observation-List
        start_datetime = get_element_value(dom, "rsm:StartDateTime")

        date = dp.parse(start_datetime)

        # Über alle Einträge in der Liste der Observations iterieren und einen Eintrag erstellen.
        observation_list = dom.getElementsByTagName("rsm:Observation")
        for observation in observation_list:
            value = get_element_value(observation, "rsm:Volume")
            value = round(float(value), 3)
            # print(id, date, value)
            date += relativedelta(minutes=+15)
            key = int(date.timestamp() * 1000)
            if key not in dict:
                dict[key] = {}
            if id == "742":
                dict[key]["usgR"] = value
            else:
                dict[key]["feedR"] = value
    return dict


def dict_to_json(data):
    arr = []
    for key in sorted(data.keys()):
        value = data[key]
        arr.append({"ts": key, **value})
    return arr


if __name__ == "__main__":
    print("Getting 1 ESL value....")
    usgA, feedA, ts = get_highest_absolute_value_from_esl_files()
    print("Found!")
    data = parse_sdat()
    print(json.dumps(dict_to_json(data), indent=4))
