import random
import pandas
from generators import *


def compute(n, out_file, banks_p, systems_p):
    dictPath = "dictionary"

    names1 = [
        i.replace("\n", "")
        for i in (open(dictPath + "/names_1.txt", "r", encoding="utf-8").readlines())
    ]
    names2 = [
        i.replace("\n", "")
        for i in (open(dictPath + "/names_2.txt", "r", encoding="utf-8").readlines())
    ]

    lastnames1 = [
        i.replace("\n", "")
        for i in (
            open(dictPath + "/lastnames_1.txt", "r", encoding="utf-8").readlines()
        )
    ]
    lastnames2 = [
        i.replace("\n", "")
        for i in (
            open(dictPath + "/lastnames_2.txt", "r", encoding="utf-8").readlines()
        )
    ]

    patronymics1 = [
        i.replace("\n", "")
        for i in (
            open(dictPath + "/patronymics_1.txt", "r", encoding="utf-8").readlines()
        )
    ]
    patronymics2 = [
        i.replace("\n", "")
        for i in (
            open(dictPath + "/patronymics_2.txt", "r", encoding="utf-8").readlines()
        )
    ]

    doctors = [
        i.replace("\n", "")
        for i in (open(dictPath + "/doctors.txt", "r", encoding="utf-8").readlines())
    ]

    symptoms = [
        i.replace("\n", "")
        for i in (open(dictPath + "/symptoms.txt", "r", encoding="utf-8").readlines())
    ]

    analyzis = [
        i.replace("\n", "")
        for i in (open(dictPath + "/analyzis.txt", "r", encoding="utf-8").readlines())
    ]

    card_keys = {}
    for i in open(dictPath + "/card_keys.txt", "r", encoding="utf-8").readlines():
        row = i.replace("\n", "").split(" ")
        card_keys[row[0] + "_" + row[1]] = row[2]

    namesGen = [
        NamesGenerator(names1, lastnames1, patronymics1),
        NamesGenerator(names2, lastnames2, patronymics2),
    ]

    passportGen = PassportGenerator()
    snilsGen = SnilsGenerator()

    sympGen = SamplesGenerator(symptoms, 5)
    analyzisGen = SamplesGenerator(analyzis, 8)

    dateGen = DatetimeGenerator()

    cardGen = CardGenerator(banks_p, systems_p, card_keys)

    data = {
        "Name": [],
        "Passport": [],
        "Snils": [],
        "Symptoms": [],
        "Analyzis": [],
        "Doctor": [],
        "DateStart": [],
        "DateEnd": [],
        "Price": [],
        "Card": [],
    }

    for i in range(n):
        data["Name"].append(namesGen[random.randrange(2)].generate())
        data["Passport"].append(passportGen.generate())
        data["Snils"].append(snilsGen.generate())
        data["Symptoms"].append(sympGen.generate())
        data["Analyzis"].append(analyzisGen.generate())
        data["Doctor"].append(random.choice(doctors))
        data["DateStart"].append(dateGen.generate())
        data["DateEnd"].append(dateGen.generate())
        data["Price"].append(str(random.randint(10, 100) * 100))
        data["Card"].append(cardGen.generate())

    df = pandas.DataFrame(data)
    df.to_csv(f"{out_file}.csv", index=False)
