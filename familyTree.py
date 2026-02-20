from person import Person
from personFactory import PersonFactory
import queue
class FamilyTree:
    """
        Represents the entire family tree.

        This class is responsible for:
        - Creating the initial founder generation
        - Generating partners and children
        - Traversing the family tree using a queue (BFS)
        - Providing summary statistics such as total count,
          count by decade, and duplicate names
    """
    def __init__(self):
        self.people=[]
    def generate_tree(self):
        """
            Generate the family tree starting from two founders
            and expanding forward by creating partners and children.
            The tree generation uses a queue-based breadth-first
            traversal to ensure each person is processed in order.
        """
        factory = PersonFactory()

        p1 = Person("Desmond", "Jones", "male", 1950)
        p2 = Person("Molly", "Jones", "female",1950)

        p1.year_died = factory.compute_year_died(p1.year_born)
        p2.year_died = factory.compute_year_died(p2.year_born)

        # Set founders as partners
        p1.set_partner(p2)
        p2.set_partner(p1)

        # Add founders to the tree
        self.people.append(p1)
        self.people.append(p2)

        # Queue for breadth-first traversal
        family_q = queue.Queue()
        family_q.put(p1)
        family_q.put(p2)
        while family_q.qsize() > 0:
            person = family_q.get()
            # Stop generating beyond the upper year limit
            if person.get_year_born() > 2120:
                break
            if person.children_created:#if already has children, then don't create again
                continue
            elder_parent = person.year_born

            # Possibly create a partner
            if person.get_partner() is None:
                partner_flag = factory.can_have_partner(person.year_born)
                if partner_flag:
                    partner = factory.create_partner(person.year_born)
                    partner.set_partner(person)
                    person.set_partner(partner)
                    elder_parent = min(partner.year_born, person.year_born)
            else:
                elder_parent = min(person.year_born, person.get_partner().year_born)

            # Generate children
            children_num=factory.num_children(elder_parent)
            years=factory.child_birth_years(elder_parent, children_num)
            children=factory.create_children(children_num, years)
            person.set_children(children)
            person.set_children_created=True

            # Assign children to partner as well
            if person.get_partner() is not None:
                person.get_partner().set_children(children)
            for child in children:
                family_q.put(child)
                self.people.append(child)
        return

    def count_total(self):
        """
            Return the total number of people in the family tree.
        """
        return len(self.people)

    def count_by_decade(self):
        """
              Count how many people were born in each decade.
              Returns:
                  dict: {decade: count}
        """
        counts = {}
        for person in self.people:
            decade = (person.year_born // 10) * 10
            counts[decade] = counts.get(decade, 0) + 1
        return counts

    def duplicate_full_names(self):
        """
                Find duplicate full names (first + last) in the tree.
                Returns:
                    set of strings containing duplicate full names
        """
        seen = set()
        dupes = set()
        for person in self.people:
            full_name = f"{person.name} {person.last_name}"
            if full_name in seen:
                dupes.add(full_name)
            else:
                seen.add(full_name)
        return dupes