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
    for pokemon in HOENN_DATA:
        if pokemon['Name'].lower() == name.lower():
            return pokemon
    return None

def display_pokemon_list(owner):
    filter_type = display_menu()
    while filter_type != 7:
        filtered_list = filter_pokedex(filter_type, owner['pokedex'])

        if len(filtered_list) == 0:
            print("There are no Pokemons in this Pokedex that match the criteria.")

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

    if root['name'].lower() == owner_name.lower():
        if root['right']:
            if root['left']:
                insert_owner_bst(root['left'], root['right'])
            root = root['right']
        elif root['left']:
            root = root['left']
        else: root = None
        return root

    elif owner_name > root['name'].lower and root['right'].lower:
        root['right'] = delete_owner_bst(root['right'], owner_name)
    elif owner_name < root['name'].lower and root['left'].lower:
        root['left'] = delete_owner_bst(root['left'], owner_name)

    return root
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
    print("Pokemon {0} (ID {1}) added to {2}'s Pokedex.".format(new_pokemon['Name'], new_pokemon['ID'], owner['name']))
    pass

def release_pokemon_by_name(owner):
    pokemon_name = input("Enter Pokemon Name to release: ").lower()

    for pokemon in owner['pokedex']:
        if pokemon['Name'].lower() == pokemon_name.lower():
            print("Releasing {0} from {1}.".format(pokemon['Name'], owner['name']))
            owner['pokedex'].remove(pokemon)
            return

    print("No pokemon named '{0}' in {1}'s Pokedex.".format(pokemon_name, owner['name']))
    pass

def evolve_pokemon_by_name(owner):
    pokemon_name = input("Enter Pokemon Name to evolve: ").lower()
    pokemon = None

    for pokemon_node in owner['pokedex']:
        if pokemon_node['Name'].lower() == pokemon_name:
            pokemon = pokemon_node
    if not pokemon:
        print("No Pokemon named '{0}' in {1}'s Pokedex.".format(pokemon_name, owner['name']))
        return
    if pokemon['Can Evolve'] == 'FALSE':
        print("{0} cannot evolve.".format(pokemon['Name']))
        return

    evolution = get_poke_dict_by_id(pokemon['ID'])
    duplicate = None

    for pokemon_node in owner['pokedex']:
        if pokemon_node == evolution:
            duplicate = pokemon_node

    owner['pokedex'].append(evolution)
    owner['pokedex'].remove(pokemon)
    print("Pokemon evolved from {0} (ID {1}) to {2} (ID {3})."\
          .format(pokemon['Name'], pokemon['ID'], evolution['Name'], evolution['ID']))

    if duplicate:
        print("{0} was already present; releasing it immediately.".format(duplicate['Name']))
        owner['pokedex'].pop()
    pass


########################
# 5) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, array):
    if root is None:
        return array

    array.append(root)

    if root['left']:
        array = gather_all_owners(root['left'], array)
    if root['right']:
        array = gather_all_owners(root['right'], array)


    return array
    pass

def sort_owners_by_num_pokemon():
    """
    Gather owners, sort them by (#pokedex size, then alpha), print results.
    """
    pass


########################
# 6) Print All
########################

def print_owner(owner):
    print("\nOwner: {0}".format(owner['name']))
    if len(owner['pokedex']) == 0:
        print("There are no Pokemons in this Pokedex that match the criteria.")
        return

    for pokemon in owner['pokedex']:
        print("ID: {0}, Name: {1}, Type: {2}, HP: {3}, Attack: {4}, Can Evolve: {5}"\
              .format(pokemon['ID'], pokemon['Name'], pokemon['Type'],
                      pokemon['HP'], pokemon['Attack'], pokemon['Can Evolve']))

def bfs_print(node):
    if node is None:
        return

    owners = [node]

    while len(owners) > 0:
        print_owner(owners[0])
        if owners[0]['left']:
            owners.append(owners[0]['left'])
        if owners[0]['right']:
            owners.append(owners[0]['right'])
        owners.pop(0)

    pass

def pre_order_print(node):
    if node is None:
        return

    print_owner(node)
    pre_order_print(node['left'])
    pre_order_print(node['right'])
    pass

def in_order_print(node):
    if node is None:
        return

    pre_order_print(node['left'])
    print_owner(node)
    pre_order_print(node['right'])
    pass

def post_order_print(node):
    if node is None:
        return

    pre_order_print(node['left'])
    pre_order_print(node['right'])
    print_owner(node)
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
            display_pokemon_list(owner)
        elif choice == 3:
            release_pokemon_by_name(owner)
        elif choice == 4:
            evolve_pokemon_by_name(owner)
        choice = pokedex_menu(owner['name'])

    pass

########################
# 8) Menu Printing Functions
########################

def display_menu():
    print("\n-- Display Filter Menu --\n\
    1. Only a certain Type\n\
    2. Only Evolvable\n\
    3. Only Attack above __\n\
    4. Only HP above __\n\
    5. Only names starting with letter(s)\n\
    6. All of them!\n\
    7. Back\n\
    ")
    return read_int_safe("Your choice: ")

def pokedex_menu(name):
    print("\n-- {0}'s Pokedex Menu --\n\
    1. Add Pokemon\n\
    2. Display Pokedex\n\
    3. Release Pokemon\n\
    4. Evolve Pokemon\n\
    5. Back to Main\n\
    ".format(name))

    return read_int_safe("Your choice: ")

def print_owners_menu():
    print("1) BFS\n\
2) Pre-Order\n\
3) In-Order\n\
4) Post-Order\n\
")
    return read_int_safe("Your choice: ")

def main_menu():
    print("\n=== Main Menu ===\n\
    1. New Pokedex\n\
    2. Existing Pokedex\n\
    3. Delete a Pokedex\n\
    4. Display owners by number of Pokemon\n\
    5. Print All\n\
    6. Exit\n\
    ")
    return read_int_safe("Your choice: ")

########################
# 9) Main Functions
########################

def add_pokedex():

    owner_name = input("Owner name: ")

    print("Choose your starter Pokemon:\n\
    1) Treecko\n\
    2) Torchic\n\
    3) Mudkip\n\
    ")
    starter = read_int_safe("Your choice: ")
    first_pokemon = HOENN_DATA[starter * 3 - 3]

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

def delete_pokedex():
    global ownerRoot

    owner_name = input("Enter owner to delete: ")
    print("Deleting {0}'s entire Pokedex...")

    if ownerRoot is None:
        print("No owners to delete.")
        return
    if not find_owner_bst(ownerRoot, owner_name):
        print("Owner '{0}' not found.".format(owner_name))
        return

    ownerRoot = delete_owner_bst(ownerRoot, owner_name)
    pass

def print_sorted_owners():
    if ownerRoot is None:
        print("No owners at all.")
        return

    owners_list = []
    owners_list = gather_all_owners(ownerRoot, owners_list)

    sorted_list = sorted(owners_list, key=lambda owner_node: owner_node['name'])
    sorted_list = sorted(sorted_list, key=lambda owner_node: len(owner_node['pokedex']))

    print("=== The Owners we have, sorted by number of Pokemons ===")
    for owner in sorted_list:
        print("Owner: {0} (has {1} Pokemon)".format(owner['name'], len(owner['pokedex'])))

def print_all_owners():
    global ownerRoot
    if ownerRoot is None:
        print("No owners in the BST.")
        return

    choice = print_owners_menu()

    if choice == 1:
        bfs_print(ownerRoot)
    elif choice == 2:
        pre_order_print(ownerRoot)
    elif choice == 3:
        in_order_print(ownerRoot)
    elif choice == 4:
        post_order_print(ownerRoot)
    pass



def main():
    choice = main_menu()

    while choice != 6:
        if choice == 1:
            add_pokedex()
        elif choice == 2:
            enter_pokedex()
        elif choice == 3:
            delete_pokedex()
        elif choice == 4:
            print_sorted_owners()
        elif choice == 5:
            print_all_owners()
        choice = main_menu()
    print("Goodbye!")
    pass

if __name__ == "__main__":
    main()
