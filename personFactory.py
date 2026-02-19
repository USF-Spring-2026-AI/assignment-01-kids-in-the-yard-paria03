from person import Person
import random
import csv
import math

class PersonFactory:
    def __init__(self):
        self.first_names = self.read_csv("first_names.csv")
        self.last_names = self.read_csv("last_names.csv")
        self.gender_probs = self.read_csv("gender_name_probability.csv")
        self.life_expectancy = self.read_csv("life_expectancy.csv")
        self.birth_marriage = self.read_csv("birth_and_marriage_rates.csv")
        self.rank_probs = self.read_as_list("rank_to_probability.csv")

    def create_person(self, first_name, last_name, gender, year_born,year_died):
        return Person(first_name, last_name, gender, year_born,year_died)

    def read_csv(self, path):
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f)) #used Chat GPT

    def read_as_list(self, path): #Used Chat GPT
        with open(path, newline="") as f:
            row=next(csv.reader(f))
            return [float(x) for x in row]
    def decade_of(self,year):
        return (year // 10) * 10

    def compute_year_died(self,year_born):
        expectancy = 0.0
        for row in self.life_expectancy:
            if int(row["Year"]) == year_born:
                expectancy = float(row["Period life expectancy at birth"])
                break
        x=int(year_born+expectancy)
        return random.randint(x-10,x+10)

    def can_have_partner(self, year_born):
        decade=self.decade_of(year_born)
        marriage_rate = None
        for row in self.birth_marriage:
            if int(row["decade"].rstrip("s")) == decade:
                marriage_rate = float(row["marriage_rate"])
                break
        return random.random() < marriage_rate

    def create_partner(self, year_born):
        year_born= random.randint(year_born-10,year_born+10)
        return self.create_person(self.choose_first_name(year_born),self.choose_last_name(year_born),self.choose_gender(),year_born,self.compute_year_died(year_born))

    def choose_gender(self):
        return random.choice(["male","female"])

    def num_children(self,year_born):
        decade=self.decade_of(year_born)
        birth_rate = None
        for row in self.birth_marriage:
            if int(row["decade"].rstrip("s")) == decade:
                birth_rate = float(row["birth_rate"])
                break
        min_children=math.ceil(birth_rate-1.5)
        max_children=math.ceil(birth_rate+1.5)
        return random.randint(min_children,max_children)

    def child_birth_years(self,parent_birth_year, k):
        if k==0:
            return []
        start_year=parent_birth_year+25
        end_year=parent_birth_year+45
        if k==1:    #somewhere in the middle
            return [(start_year+end_year)//2]
        # spread the ages evenly:
        step = (end_year - start_year) / (k - 1)
        years=[]
        for i in range (k):
            year = round(start_year + i * step)
            years.append(year)
        return years

    def create_children(self,num_children,years):
        children = []
        for num in range(num_children):
            year_born=years[num]
            if year_born < 2120:
                children.append(self.create_person(self.choose_first_name(year_born),"Jones",self.choose_gender(),year_born,self.compute_year_died(year_born)))
        return children



    # pick a ramdom name from the list
    def choose_first_name(self,year_born):
        decade=self.decade_of(year_born)
        names=[]
        weights=[]
        for row in self.first_names:
            if int(row["decade"].rstrip("s")) == decade:
                names.append(row["name"])
                weights.append(float(row["frequency"]))
        return random.choices(names,weights,k=1)[0]

    def choose_last_name(self,year_born):
        decade=self.decade_of(year_born)
        last_names=[]
        probs=self.rank_probs
        for row in self.last_names:
            if int(row["Decade"].rstrip("s")) == decade:
                last_names.append(row["LastName"])

        return random.choices(last_names,probs,k=1)[0]

