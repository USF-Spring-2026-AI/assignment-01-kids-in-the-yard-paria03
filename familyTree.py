from person import Person
from personFactory import PersonFactory
import queue
class FamilyTree:

    def __init__(self):
        self.people=[]
    def generate_tree(self):
        factory = PersonFactory()

        p1 = Person("Desmond", "Jones", "male", 1950)
        p2 = Person("Molly", "Jones", "female",1950)

        p1.year_died = factory.compute_year_died(p1.year_born)
        p2.year_died = factory.compute_year_died(p2.year_born)

        p1.set_partner(p2)
        p2.set_partner(p1)

        self.people.append(p1)
        self.people.append(p2)

        family_q = queue.Queue()
        family_q.put(p1)
        family_q.put(p2)
        while family_q.qsize() > 0:
            person = family_q.get()
            if person.get_year_born() > 2120:
                break
            if person.children_created:#if already has children, then don't create again
                continue
            elder_parent = person.year_born
            if person.get_partner() is None:
                partner_flag = factory.can_have_partner(person.year_born)
                if partner_flag:
                    partner = factory.create_partner(person.year_born)
                    partner.set_partner(person)
                    person.set_partner(partner)
                    elder_parent = min(partner.year_born, person.year_born)
            else:
                elder_parent = min(person.year_born, person.get_partner().year_born)

            children_num=factory.num_children(elder_parent)
            years=factory.child_birth_years(elder_parent, children_num)
            children=factory.create_children(children_num, years)
            person.set_children(children)
            person.set_children_created=True
            if person.get_partner() is not None:
                person.get_partner().set_children(children)
            for child in children:
                family_q.put(child)
                self.people.append(child)
        return
    def count_total(self):
        return len(self.people)

    def count_by_decade(self):
        counts = {}
        for person in self.people:
            decade = (person.year_born // 10) * 10
            counts[decade] = counts.get(decade, 0) + 1
        return counts

    def duplicate_full_names(self):
        seen = set()
        dupes = set()
        for person in self.people:
            full_name = f"{person.name} {person.last_name}"
            if full_name in seen:
                dupes.add(full_name)
            else:
                seen.add(full_name)
        return dupes