import os
import xml.dom.minidom
import dateutil.parser as dp


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
    path_of_the_directory= os.getcwd() + "/static/files/ESL-Files"
    # Iterate through the files in this directory
    for filename in os.listdir(path_of_the_directory):
        f = os.path.join(path_of_the_directory,filename)
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


def parse_sdat(path = os.getcwd() + "/static/files/SDAT-Files"):
    cnt = 0
    for file in os.listdir(path):
        fullname = os.path.join(path, file)
        dom = xml.dom.minidom.parse(fullname)
        # ID of the Meter
        id = dom.getElementsByTagName('rsm:DocumentID')[0].firstChild.nodeValue[-3:]
        # Start Datetime of the Observation-List
        start_datetime = dom.getElementsByTagName("rsm:StartDateTime")[1].firstChild.nodeValue

        # Über alle Einträge in der Liste der Observations iterieren und einen Eintrag erstellen.
        observation_list = dom.getElementsByTagName("rsm:Observation")
        for observation in observation_list:
            value = observation.getElementsByTagName("rsm:Volume")[0].firstChild.nodeValue
            cnt+=1
            print(value)
        print(id)
        print(start_datetime)
    print(cnt)


if __name__ == "__main__":
    print("Getting 1 ESL value....")
    usgA, feedA, ts = get_highest_absolute_value_from_esl_files()
    print("Found!")
    output = {ts: [None, None, feedA, usgA]}
    parse_sdat()
    
    print(output)