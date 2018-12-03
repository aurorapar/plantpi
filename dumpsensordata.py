import mysql.connector
# import fuzzyplant
import re

def dumpSensorData():
    db = ''
    try:
        db = mysql.connector.connect(host="localhost", user="plantpi", passwd="softwareengineering", database="plantproject", autocommit=True)
    except Exception as e:
        print("Database connection failed:\n\t%s" % str(e))
        exit()
    
    cursor = db.cursor()

    cursor.execute("SELECT type, value from sensor ORDER BY time")

    results = cursor.fetchall()
    # fp = FuzzyPlantSystem()
    file = open("fuzzyoutput.txt", "w+")
    
    for row in results:
        deviceType = row["type"]
        if deviceType == "dht11":
            m = re.search("^\(\s*(\d+(?:\.\d+))\s*,\s*(\d+(?:\.\d+))\s*\)$", row["value"])
            humidity = int(m[0])
            temperature = int(m[1])
            file.write("humidity = %s, temperature = %s" % (humidity, temperature))

        elif deviceType == "watersensor":
            waterLevel = int(row["value"])
            file.write("water level = %s" % waterLevel)

    file.close()


    # dht11, watersensor

