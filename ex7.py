import csv
# from random import choice

# Global BST root
ownerRoot = None

########################
# 0) Read from CSV -> HOENN_DATA
########################


def read_hoenn_csv(filename):
    """
    Reads 'hoenn_pokedex.csv' and returns a list of dicts:
      [ { "ID": int, "Name": str, "Type": str, "HP": int,
          "Attack": int, "Can Evolve": "TRUE"/"FALSE" },
        ... ]
    """
    data_list = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')  # Use comma as the delimiter
        first_row = True
        for row in reader:
            # It's the header row (like ID,Name,Type,HP,Attack,Can Evolve), skip it
            if first_row:
                first_row = False
                continue

            # row => [ID, Name, Type, HP, Attack, Can Evolve]
            if not row or not row[0].strip():
                break  # Empty or invalid row => stop
            d = {
                "ID": int(row[0]),
                "Name": str(row[1]),
                "Type": str(row[2]),
                "HP": int(row[3]),
                "Attack": int(row[4]),
                "Can Evolve": str(row[5]).upper()
            }
            data_list.append(d)
    return data_list

HOENN_DATA = read_hoenn_csv("hoenn_pokedex.csv")

########################
# 1) Helper Functions
########################

def read_int_safe(prompt):
    num = input(prompt)
    while not num.isnumeric() or int(num) < 1:
        print("Invalid input")
        num = input(prompt)
    return int(num)

def get_poke_dict_by_id(pokemon_id):
    if pokemon_id > 135 or pokemon_id < 1:
        print("ID {0} not found in Honen data.".format(pokemon_id))
        return False
    else: return HOENN_DATA[pokemon_id]

def get_poke_dict_by_name(name):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by name, or None if not found.
    """
    pass

def display_pokemon_list(pokedex):
    filter_type = display_menu()
    while filter_type != 7:
        filtered_list = filter_pokedex(filter_type, pokedex)

        if len(filtered_list) == 0:
            print("There are no Pokemons in this Pokedex that match the criteria.")
            continue

        for pokemon in filtered_list:
            print("ID: {0}, Name: {1}, Type: {2}, HP: {3}, Attack: {4}, Can Evolve: {5}"\
                  .format(pokemon['ID'], pokemon['Name'], pokemon['Type'], pokemon['HP'], pokemon['Attack'], pokemon['Can Evolve']))

        filter_type = display_menu()

    pass

def filter_pokedex(filter_type, pokedex):
    pokemon_list = []

    if filter_type == 1:
        pokemon_type = input("Which Type? (e.g. GRASS, WATER): ").lower()
        for pokemon in pokedex:
            if pokemon['Type'].lower() == pokemon_type:
                pokemon_list.append(pokemon)
    elif filter_type == 2:
        for pokemon in pokedex:
            if pokemon['Can Evolve']:
                pokemon_list.append(pokemon)
    elif filter_type == 3:
        attack = read_int_safe("Enter Attack threshold: ")
        for pokemon in pokedex:
            if pokemon['Attack'] > attack:
                pokemon_list.append(pokemon)
    elif filter_type == 4:
        hp = read_int_safe("Enter HP threshold: ")
        for pokemon in pokedex:
            if pokemon['HP'] > hp:
                pokemon_list.append(pokemon)
    elif filter_type == 5:
        name_start = input("Starting letter(s): ").lower()
        for pokemon in pokedex:
            if pokemon['Name'].lower().startswith(name_start):
                pokemon_list.append(pokemon)
    elif filter_type == 6:
        pokemon_list = pokedex

    return pokemon_list


########################
# 2) BST (By Owner Name)
########################

def create_owner_node(owner_name, first_pokemon=None):
    pokedex = [first_pokemon]
    owner = {'name': owner_name, 'pokedex': pokedex, 'left': None, 'right': None}

    return owner

def insert_owner_bst(new_node, root):
    if root is None:
        global ownerRoot
        ownerRoot = new_node
        return 1

    root_name = root['name'].lower()
    new_name = new_node['name'].lower()

    if root_name > new_name:
        if root['left'] is None:
            root['left'] = new_node
            return True
        else: return insert_owner_bst(new_node, root['left'])
    elif root_name < new_name:
        if root['right'] is None:
            root['right'] = new_node
            return True
        else: return insert_owner_bst(new_node, root['right'])
    else:
        return False
    pass

def find_owner_bst(root, owner_name):
    if root is None:
        return None

    if root['name'] > owner_name:
        return find_owner_bst(root['left'], owner_name)
    elif root['name'] < owner_name:
        return find_owner_bst(root['right'], owner_name)
    else: return root

def min_node(node):
    """
    Return the leftmost node in a BST subtree.
    """
    pass

def delete_owner_bst(root, owner_name):
    """
    Remove a node from the BST by owner_name. Return updated root.
    """
    pass


########################
# 3) BST Traversals
########################

def bfs_traversal(root):
    """
    BFS level-order traversal. Print each owner's name and # of pokemons.
    """
    pass

def pre_order(root):
    """
    Pre-order traversal (root -> left -> right). Print data for each node.
    """
    pass

def in_order(root):
    """
    In-order traversal (left -> root -> right). Print data for each node.
    """
    pass

def post_order(root):
    """
    Post-order traversal (left -> right -> root). Print data for each node.
    """
    pass


########################
# 4) Pokedex Operations
########################

def add_pokemon_to_owner(owner):
    index = read_int_safe("Enter Pokemon ID to add: ")
    for pokemon in owner['pokedex']:
        if pokemon['ID'] == index:
            print("Pokemon already in the list. No changes made.")
        return

    new_pokemon = HOENN_DATA[index - 1]

    owner['pokedex'].append(new_pokemon)
    pass

def release_pokemon_by_name(owner_node):
    """
    Prompt user for a Pokemon name, remove it from this owner's pokedex if found.
    """
    pass

def evolve_pokemon_by_name(owner_node):
    """
    Evolve a Pokemon by name:
    1) Check if it can evolve
    2) Remove old
    3) Insert new
    4) If new is a duplicate, remove it immediately
    """
    pass


########################
# 5) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, arr):
    """
    Collect all BST nodes into a list (arr).
    """
    pass

def sort_owners_by_num_pokemon():
    """
    Gather owners, sort them by (#pokedex size, then alpha), print results.
    """
    pass


########################
# 6) Print All
########################

def print_all_owners():
    """
    Let user pick BFS, Pre, In, or Post. Print each owner's data/pokedex accordingly.
    """
    pass

def pre_order_print(node):
    """
    Helper to print data in pre-order.
    """
    pass

def in_order_print(node):
    """
    Helper to print data in in-order.
    """
    pass

def post_order_print(node):
    """
    Helper to print data in post-order.
    """
    pass


########################
# 7) Sub-menu & Main menu
########################

def existing_pokedex(owner):
    choice = pokedex_menu(owner['name'])
    while choice != 5:
        if choice == 1:
            add_pokemon_to_owner(owner)
        elif choice == 2:
            display_pokemon_list(owner['pokedex'])
        choice = pokedex_menu(owner['name'])

    pass

########################
# 8) Menu Printing Functions
########################

def display_menu():
    print("-- Display Filter Menu --\n\
    1. Only a certain Type\n\
    2. Only Evolvable\n\
    3. Only Attack above __\n\
    4. Only HP above __\n\
    5. Only names starting with letter(s)\n\
    6. All of them!\n\
    7. Back\n\
    ")
    num = read_int_safe("Your choice: ")
    return num

def pokedex_menu(name):
    print("-- {0}'s Pokedex Menu --\n\
    1. Add Pokemon\n\
    2. Display Pokedex\n\
    3. Release Pokemon\n\
    4. Evolve Pokemon\n\
    5. Back to Main\n\
    ".format(name))

    num = read_int_safe("Your choice: ")
    return num

def main_menu():
    print("=== Main Menu ===\n\
    1. New Pokedex\n\
    2. Existing Pokedex\n\
    3. Delete a Pokedex\n\
    4. Display owners by number of Pokemon\n\
    5. Print All\n\
    6. Exit\n\
    ")
    pass

########################
# 9) Main Functions
########################

def add_pokedex():
    print("Choose your starter Pokemon:\n\
    1) Treecko\n\
    2) Torchic\n\
    3) Mudkip\n\
    ")

    starter = read_int_safe("Your choice: ")
    first_pokemon = HOENN_DATA[starter * 3 - 3]
    owner_name = input("Owner name: ")

    global ownerRoot
    new_owner = create_owner_node(owner_name, first_pokemon)
    success = insert_owner_bst(new_owner, ownerRoot)

    if success:
        print("New Pokedex created for {0} with starter {1}.".format(owner_name, first_pokemon['Name']))
    else: print("Owner '{0}' already exists. No new Pokedex created.".format(owner_name))

def enter_pokedex():
    global ownerRoot
    name = input("Owner name: ")

    owner = find_owner_bst(ownerRoot, name)
    if owner is None:
        print("Owner '{0}' not found.".format(name))
        return

    existing_pokedex(owner)



def main():
    main_menu()
    choice = read_int_safe("Your choice: ")

    while choice != 6:
        if choice == 1:
            add_pokedex()
        elif choice == 2:
            enter_pokedex()
        main_menu()
        choice = read_int_safe("Your choice: ")
    print("Goodbye!")
    pass

if __name__ == "__main__":
    main()
