from familyTree import FamilyTree

MENU = """Are you interested in:
(T)otal number of people in the tree
Total number of people in the tree by (D)ecade
(N)ames duplicated
(Q)uit
> """
def main():
    print("Reading files...")
    tree = FamilyTree()
    print("Generating family tree...")
    tree.generate_tree()

    while True:
        choice = input(MENU).strip().upper()

        if choice == "N":
            duplicates = tree.duplicate_full_names()  # returns a set or list of duplicate full-name strings
            print(f"There are {len(duplicates)} duplicate names in the tree:")
            for name in sorted(duplicates):
                print(f"* {name}")

        elif choice == "D":
            counts = tree.count_by_decade()  # returns dict {decade_int: count}
            for decade in sorted(counts):
                print(f"{decade}: {counts[decade]}")

        elif choice == "T":
            total = tree.count_total()
            print(f"The tree contains {total} people in total")

        else:
            if choice in {"Q", "QUIT", "EXIT"}:
                break
            print("Bad Input. Please choose one of the options in Menu:")
            continue
if __name__ == "__main__":
    main()
