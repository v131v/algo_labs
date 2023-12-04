import random

from generators import *

def compute(n, out_file, banks_p, systems_p):
    dictPath = "dictionary"

    names1 = [i.replace("\n", "") for i in (open(dictPath+"/names_1.txt", 'r', encoding='utf-8').readlines())]
    names2 = [i.replace("\n", "") for i in (open(dictPath+"/names_2.txt", 'r', encoding='utf-8').readlines())]

    lastnames1 = [i.replace("\n", "") for i in (open(dictPath+"/lastnames_1.txt", 'r', encoding='utf-8').readlines())]
    lastnames2 = [i.replace("\n", "") for i in (open(dictPath+"/lastnames_2.txt", 'r', encoding='utf-8').readlines())]

    patronymics1 = [i.replace("\n", "") for i in (open(dictPath+"/patronymics_1.txt", 'r', encoding='utf-8').readlines())]
    patronymics2 = [i.replace("\n", "") for i in (open(dictPath+"/patronymics_2.txt", 'r', encoding='utf-8').readlines())]
    
    doctors = [i.replace("\n", "") for i in (open(dictPath+"/doctors.txt", 'r', encoding='utf-8').readlines())]

    symptoms = [i.replace("\n", "") for i in (open(dictPath+"/symptoms.txt", 'r', encoding='utf-8').readlines())]

    analyzis = [i.replace("\n", "") for i in (open(dictPath+"/analyzis.txt", 'r', encoding='utf-8').readlines())]
    
    banks_p = {}
    for i in (open(dictPath+"/banks.txt", 'r', encoding='utf-8').readlines()):
        row = i.replace("\n", "").split(" ")
        banks_p[row[0]] = float(row[1])
        
    systems_p = {}
    for i in (open(dictPath+"/payment_systems.txt", 'r', encoding='utf-8').readlines()):
        row = i.replace("\n", "").split(" ")
        systems_p[row[0]] = float(row[1])
        
    card_keys = {}
    for i in (open(dictPath+"/card_keys.txt", 'r', encoding='utf-8').readlines()):
        row = i.replace("\n", "").split(" ")
        card_keys[row[0]+"_"+row[1]] = row[2]
        
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
    
    out = open(out_file, "w")
    
    for i in range(n):
        name = namesGen[random.randrange(2)].generate()
        passport = passportGen.generate()
        snils = snilsGen.generate()
        curSymptoms = sympGen.generate()
        curAnalyzis = analyzisGen.generate()
        doctor = random.choice(doctors)
        start = dateGen.generate()
        end = dateGen.generate()
        price = str(random.randint(10, 100) * 100)
        card = cardGen.generate()
        
        out.write("\n".join([
            name,
            passport,
            snils,
            curSymptoms,
            doctor,
            start,
            curAnalyzis,
            end,
            price,
            card,
            "\n",
        ]))
        
    out.close()