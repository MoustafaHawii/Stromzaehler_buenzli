# Stromzaehler_buenzli

Stromzaehler Buenzli is a web application used for visualising electricity meter data with highcharts js. Backend is build using the python Flask framework. Meter data is stored in xml format and parsed using the xml.dom.minidom library.

### Instalation
```bash
pip3 install Flask
pip3 install python-dateutil
```
Additionally the xml files have to be uploaded to `static/files/ESL-files` and `static/files/SDAT-files` directories.

### Run
```bash
python main.py
python app.py
```