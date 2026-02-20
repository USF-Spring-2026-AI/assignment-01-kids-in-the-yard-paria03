from person import Person
import random
import csv
import math


class PersonFactory:
    """
        Responsible for creating Person objects and handling all logic related to reading data files,
        choosing names, genders, life expectancy, partners, and children.
        This class acts as a helper/factory that FamilyTree uses to
        generate people based on probabilities and CSV data.
    """

    def __init__(self):
        """
            Initialize the PersonFactory by reading all required CSV files
            into memory.
        """
        self.first_names = self.read_csv("first_names.csv")
        self.last_names = self.read_csv("last_names.csv")
        self.gender_probs = self.read_csv("gender_name_probability.csv")
        self.life_expectancy = self.read_csv("life_expectancy.csv")
        self.birth_marriage = self.read_csv("birth_and_marriage_rates.csv")
        self.rank_probs = self.read_as_list("rank_to_probability.csv")


    def create_person(self, first_name, last_name, gender, year_born,year_died):
        """
            Create and return a Person object with the given attributes.
        """
        return Person(first_name, last_name, gender, year_born,year_died)


    def read_csv(self, path):
        """
            Read a CSV file and return its contents as a list of dictionaries.
            Each row in the CSV becomes a dictionary where keys are column
            headers and values are the corresponding cell values.
        """
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f)) #used Chat GPT


    def read_as_list(self, path): #Used Chat GPT
        """
            Read a single-row CSV file and return it as a list of floats.
            This is used for rank-to-probability mappings.
        """
        with open(path, newline="") as f:
            row=next(csv.reader(f))
            return [float(x) for x in row]


    def decade_of(self,year):
        """
            Convert a year into its corresponding decade.
            Example: 1956 -> 1950
        """
        return (year // 10) * 10



    def compute_year_died(self,year_born):
        """
            Compute a person's year of death based on life expectancy data.
            The method looks up the life expectancy for the birth year
            and adds a small random variation.
        """
        expectancy = 0.0
        for row in self.life_expectancy:
            if int(row["Year"]) == year_born:
                expectancy = float(row["Period life expectancy at birth"])
                break
        x=int(year_born+expectancy)
        return random.randint(x-10,x+10)


    def can_have_partner(self, year_born):
        """
            Determine whether a person can have a partner based on
            marriage rates for their birth decade.
        """
        decade=self.decade_of(year_born)
        marriage_rate = None
        for row in self.birth_marriage:
            if int(row["decade"].rstrip("s")) == decade:
                marriage_rate = float(row["marriage_rate"])
                break
        return random.random() < marriage_rate


    def create_partner(self, year_born):
        """
            Create a partner for a person with a birth year close to
            the original person's birth year.
        """
        year_born= random.randint(year_born-10,year_born+10)
        return self.create_person(self.choose_first_name(year_born),self.choose_last_name(year_born),self.choose_gender(),year_born,self.compute_year_died(year_born))


    def choose_gender(self):
        """
            Randomly choose a gender with a 50/50 probability.
        """
        return random.choice(["male","female"])


    def num_children(self,year_born):
        """
            Determine the number of children a person can have based on
            birth rates for their birth decade.
        """
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
        """
            Generate a list of birth years for k children, evenly spaced
            between ages 25 and 45 of the parent.
        """
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
        """
            Create child Person objects given the number of children
            and their birth years.
        """
        children = []
        for num in range(num_children):
            year_born=years[num]
            if year_born < 2120:
                children.append(self.create_person(self.choose_first_name(year_born),"Jones",self.choose_gender(),year_born,self.compute_year_died(year_born)))
        return children


    def choose_first_name(self,year_born):
        """
            Choose a random first name based on birth decade and
           name frequency.
        """
        decade=self.decade_of(year_born)
        names=[]
        weights=[]
        for row in self.first_names:
            if int(row["decade"].rstrip("s")) == decade:
                names.append(row["name"])
                weights.append(float(row["frequency"]))
        return random.choices(names,weights,k=1)[0]


    def choose_last_name(self,year_born):
        """
            Choose a random last name based on decade and rank probabilities.
        """
        decade=self.decade_of(year_born)
        last_names=[]
        probs=self.rank_probs
        for row in self.last_names:
            if int(row["Decade"].rstrip("s")) == decade:
                last_names.append(row["LastName"])

        return random.choices(last_names,probs,k=1)[0]

