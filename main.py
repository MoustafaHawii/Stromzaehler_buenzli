import os
import xml.dom.minidom
import dateutil.parser as dp
from dateutil.relativedelta import *
import json

# Get element value using selector
def get_element_value(element, selector):
    return element.getElementsByTagName(selector)[0].firstChild.nodeValue

# Calculate required absolute values
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

# Get all absolute values from esl files
def get_absolute_values_from_esl():
    dict = {}
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
                        timestamp = dp.parse(t.getAttribute("end")).timestamp()
                        timestamp = int(timestamp) * 1000
                        values = get_searched_row_value(row_values)
                        dict[timestamp] = values
    return dict

# get first absolute value where relative value is present
def get_first_absolute_where_relative(sdat, esl):
    for ts in sorted(sdat.keys()):
        if ts in esl:
            return [ts, *esl[ts]]

# get relative values from sdat files
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

# convert dict to json format
def dict_to_json(data, absolute_ts):
    list = []
    abs_index = 0
    for index, (key, value) in enumerate(sorted(data.items())):
        if key == absolute_ts:
            abs_index = index
        list.append({"ts": key, **value})

    return calculate_abs(list, abs_index)

# calculate absolute values for dict using one absolute
def calculate_abs(list, abs_index):
    feed = list[abs_index]["feedA"]
    usg = list[abs_index]["usgA"]
    for i in range(abs_index - 1, -1, -1):
        feed -= list[i]["feedR"]
        usg -= list[i]["usgR"]
        list[i]["feedA"] = round(feed, 2)
        list[i]["usgA"] = round(usg, 2)

    feed = list[abs_index - 1]["feedA"]
    usg = list[abs_index - 1]["usgA"]
    for i in range(abs_index + 1, len(list)):
        feed += list[i]["feedR"]
        usg += list[i]["usgR"]
        list[i]["feedA"] = round(feed, 2)
        list[i]["usgA"] = round(usg, 2)

    return list

if __name__ == "__main__":
    dict = parse_sdat()
    esl_val = get_absolute_values_from_esl()

    [ts, feedA, usgA] = get_first_absolute_where_relative(dict, esl_val)

    dict[ts]["feedA"] = feedA
    dict[ts]["usgA"] = usgA

    jsdat = dict_to_json(dict, ts)
    print(json.dumps(jsdat, indent=4))
