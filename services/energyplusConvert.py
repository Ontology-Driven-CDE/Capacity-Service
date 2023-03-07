from pathlib import Path
import json
from datetime import datetime
import uuid


def results():
    # Load the JSON data from the file
    with open('Public/flow_ali_prescriptive.json') as resultsFile:
        data = json.load(resultsFile)

    # Access the "Cols" list
    cols = data["Cols"]
    rows = data["Rows"]

    thermalZones = []
    ventDemands = []



    # Iterate over the elements in "Cols" and add them to the thermal zone list
    for col in cols:
        variable = col["Variable"]
        zone = variable[:7]
        thermalZones.append(zone)

        ventDemandID = str(uuid.uuid4())
        ventDemands.append(ventDemandID)

    stringData = [
        "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .",
    "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> ." ,
    "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> ." ,
    "@prefix bot: <https://w3id.org/bot#> ." ,
    "@prefix fso: <https://w3id.org/fso#> ." ,
    "@prefix inst: <https://example.com/inst#> ." ,
    "@prefix ex: <https://example.com/ex#> ." ,
    "@prefix fpo:<https://w3id.org/fpo#> ." ,
    "@prefix caso:<http://www.w3id.org/def/caso#> ." ,
    "@prefix time:<http://www.w3.org/2006/time#> ." 
]

    for index, item in enumerate(thermalZones):
        stringData.append(f"inst:{thermalZones[index]} ex:hasDesignAirflowDemand inst:{ventDemands[index]} . ")

    for row in rows:
        for time_stamp, values in row.items():
            for index, value in enumerate(values):
                stateID = uuid.uuid4()
                
                #Convert the string to a datetime object
                hour =time_stamp[6:]
                if (hour == "24:00:00"):
                    newHour ="00:00:00"
                    newTime =time_stamp[:6]+newHour
                    dt = datetime.strptime("2022-" +newTime, "%Y-%m/%d %H:%M:%S")
                    xsd_datetime = dt.strftime("%Y-%m-%dT%H:%M:%S")
            
                if (hour != "24:00:00"):
                    dt = datetime.strptime("2022-" +time_stamp, "%Y-%m/%d %H:%M:%S")
                    xsd_datetime = dt.strftime("%Y-%m-%dT%H:%M:%S")
                
                stringData.append(f"inst:{ventDemands[index]} caso:hasState inst:{stateID} .")
                stringData.append(f"inst:{stateID} fpo:hasValue '{value*1000}'^^xsd:decimal ." )
                stringData.append(f"inst:{stateID} time:inXSDDateTime '{xsd_datetime}'^^xsd:dateTime .")
                stringData.append(f"inst:{stateID} fpo:hasUnit 'Liters per second'^^xsd:string .")

    joinedStringData = "\r\n".join(stringData)

    return joinedStringData 
