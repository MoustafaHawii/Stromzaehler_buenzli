# Stromzaehler_buenzli

Stromzaehler Buenzli is a web application used for visualising electricity meter data with highcharts js. Backend is built using the python Flask framework. Meter data is stored in XML format, parsed using the xml.dom.minidom library and save in a JSON file.

### Installation
```bash
git clone https://github.com/MoustafaHawii/Stromzaehler_buenzli.git
cd Stromzaehler_buenzli/
pip install -r requirements.txt
```
Additionally the xml files have to be uploaded to `static/files/ESL-files` and `static/files/SDAT-files` directories.

### Create a virtual environment for python (venv)
```bash
python -m venv venv
virtualenv venv
```

### Activate venv
```bash
source venv/bin/activate
```

### Run flask app
```bash
python app.py
```
