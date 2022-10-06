import os
import xml.dom.minidom
import dateutil.parser as dp

# Get element value using selector
def get_element_value(element, selector):
    return element.getElementsByTagName(selector)[0].firstChild.nodeValue

def del_sdat_files():
    path = os.getcwd() + "/static/files/SDAT-Files"
    for file in os.listdir(path):
        fullname = os.path.join(path, file)
        dom = xml.dom.minidom.parse(fullname)
        date = dp.parse(get_element_value(dom, "rsm:StartDateTime")).timestamp()
        if date <= 1543610700:
            print("Deleted: " + file)
            os.remove(fullname)
            
def del_esl_files():
    path = os.getcwd() + "/static/files/ESL-Files"
    for file in os.listdir(path):
        fullname = os.path.join(path, file)
        dom = xml.dom.minidom.parse(fullname)
        
        time_period = dom.getElementsByTagName("TimePeriod")
        for t in time_period:
            timestamp = dp.parse(t.getAttribute("end")).timestamp()
            if timestamp <= 1543610700:
                print("Deleted: " + file)
                os.remove(fullname)
        
    
if __name__ == "__main__":
    del_sdat_files()
    del_esl_files()