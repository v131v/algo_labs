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
