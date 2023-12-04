import random
import datetime

class PassportGenerator:
    def __init__(self):
        self.used_keys = {}  # Словарь для отслеживания использованных серий

    def generate(self):
        key = self._generate_unique_key()
        if key in self.used_keys:
            self.used_keys[key] += 1
        else:
            self.used_keys[key] = 1
        return "{:04d}".format(key) + " {:06d}".format(self.used_keys[key])

    def _generate_unique_key(self):
        # Генерация серии из 4 цифр
        key = random.randrange(10**4 - 1) + 1
        return key
    
class SnilsGenerator:
    def __init__(self):
        self.autoinc = 0

    def generate(self):
        key = self._generate_unique_key()
        self.autoinc += 1
        return "{:09d} ".format(self.autoinc) + "{:02d}".format(key)

    def _generate_unique_key(self):
        # Генерация последних 2
        key = random.randrange(10**2)
        return key
    
class NamesGenerator:
    def __init__(self, names, lastnames, patronymics):
        self.names = names
        self.lastnames = lastnames
        self.patronymics = patronymics
        
    def generate(self):
        return " ".join([
            random.choice(self.names), 
            random.choice(self.lastnames), 
            random.choice(self.patronymics)
            ])
        
class SamplesGenerator:
    def __init__(self, symptoms, k):
        self.symptoms = symptoms
        self.k = k
        
    def generate(self):
        return ", ".join(random.sample(self.symptoms, k=self.k))
    
class DatetimeGenerator:
    def __init__(self):
        self.last = 0
    
    def generate(self):
        return (self._generate_date() + self._generate_time()).strftime('%Y-%m-%dT%H:%M%z')

    def _generate_date(self):
        if self.last == 0:
            rnd_days_ago = random.randrange(300)
            date = datetime.datetime.now() - datetime.timedelta(days=rnd_days_ago)
            if date.weekday() >= 5:
                date = date - datetime.timedelta(days=2)
            self.last = date
            return date
        else:
            date = self.last + datetime.timedelta(days=1)
            if date.weekday() >= 5:
                date = self.last + datetime.timedelta(days=2)
            self.last = 0
            return date

    def _generate_time(self):
        time = datetime.timedelta(minutes=(random.randrange(9*60)+2*60))
        return time

class CardGenerator:
    def __init__(self, banks, systems, keys):
        self.banks = banks
        self.systems = systems
        self.keys = keys
        self.used = {}
                
    def _generate_key(self, p_dict):
        rnd = random.uniform(0, 1)
        accum = 0
        for key in p_dict:
            accum += p_dict[key]
            if rnd <= accum:
                return key
        return ""
    
    def generate(self):
        bank = self._generate_key(self.banks)
        system = self._generate_key(self.systems)
        key = str(self.keys[bank+"_"+system])
        if key in self.used:
            self.used[key] += 1
        else:
            self.used[key] = 1
        card = key + "{:010d}".format(self.used[key])
        card_splited = []
        for i in range(4):
            card_splited.append(card[i*4:(i+1)*4])
        return " ".join(card_splited)

    
if __name__ == "__main__":
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
    
    print("Enter output filename:")
    outFile = input()
    
    out = open(outFile, "w")
    
    print("Enter database size:")
    n = int(input())
    
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
        
