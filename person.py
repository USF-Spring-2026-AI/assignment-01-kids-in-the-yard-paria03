class Person:
    def __init__(self, name, last_name, gender,year_born, year_died=None):
        self.name = name
        self.last_name=last_name
        self.gender=gender
        self.year_born=int(year_born)
        self.year_died=year_died
        self.partner=None
        self.children=[]

    # getters
    def get_name(self):
        return self.name
    def get_last_name(self):
        return self.last_name
    def get_gender(self):
        return self.gender
    def get_year_born(self):
        return self.year_born
    def get_year_died(self):
        return self.year_died
    def get_partner(self):
        return self.partner
    def get_children(self):
        return self.children

    # setters
    def set_name(self, name):
        self.name=name
    def set_last_name(self, last_name):
        self.last_name=last_name
    def set_gender(self, gender):
        self.gender=gender
    def set_year_born(self, year_born):
        self.year_born=year_born
    def set_year_died(self,year_died):
        self.year_died=year_died
    def set_partner(self, partner):
        self.partner=partner
    def set_children(self, children):
        self.children=children
