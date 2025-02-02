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
    """
    Get and validate integer input from user.
    """
    while True:
        num = input(prompt)
        negative = False

        # Check if input is negative
        if num[0] == '-':
            negative = True
            num = num[1:]

        # Validate numeric input
        if num.isnumeric():
            num = int(num)
            # Correct negative number
            if negative:
                num = num * -1
            return num

        print("Invalid input.")

def get_poke_dict_by_id(pokemon_id):
    """
    Return Pokemon dict by id
    """
    # Verify valid range of input
    if pokemon_id < 1 or pokemon_id > 135:
        print("ID {0} not found in Honen data.".format(pokemon_id))
        return None
    # Return dict of Pokemon from data
    else: return HOENN_DATA[pokemon_id - 1]

def get_poke_dict_by_name(name):
    """
    Return Pokemon dict by name
    """
    # Find Pokemon name in data
    for pokemon in HOENN_DATA:
        if pokemon['Name'].lower() == name.lower():
            return pokemon
    return None

def gather_all_owners(root, array):
    """
    Create and return array of all owners
    """
    # If no more owners in branch return the array
    if root is None:
        return array

    # Add current owner node to array
    array.append(root)

    # Continue gathering from both sides
    if root['left']:
        array = gather_all_owners(root['left'], array)
    if root['right']:
        array = gather_all_owners(root['right'], array)

    # Return full array
    return array

def filter_pokedex(filter_type, pokedex):
    """
    Filter list of Pokemon by filter type input
    """
    pokemon_list = []

    # Use correct filter fo input
    # Filter by Pokemon type
    if filter_type == 1:
        pokemon_type = input("Which Type? (e.g. GRASS, WATER): ").lower()
        for pokemon in pokedex:
            if pokemon['Type'].lower() == pokemon_type:
                pokemon_list.append(pokemon)
    # Filter by evolvable Pokemon
    elif filter_type == 2:
        for pokemon in pokedex:
            if pokemon['Can Evolve'] == "TRUE":
                pokemon_list.append(pokemon)
    # Filter by attack value
    elif filter_type == 3:
        attack = read_int_safe("Enter Attack threshold: ")
        for pokemon in pokedex:
            if pokemon['Attack'] > attack:
                pokemon_list.append(pokemon)
    # Filter by HP value
    elif filter_type == 4:
        hp = read_int_safe("Enter HP threshold: ")
        for pokemon in pokedex:
            if pokemon['HP'] > hp:
                pokemon_list.append(pokemon)
    # Filter by starting letters
    elif filter_type == 5:
        name_start = input("Starting letter(s): ").lower()
        for pokemon in pokedex:
            if pokemon['Name'].lower().startswith(name_start):
                pokemon_list.append(pokemon)
    # Show all Pokemon unfiltered
    elif filter_type == 6:
        pokemon_list = pokedex

    return pokemon_list


########################
# 2) Owners BST Operations
########################

def create_owner_node(owner_name, first_pokemon=None):
    """
    Create owner from starting parameters
    """
    # Fill owner data in structre
    pokedex = [first_pokemon]
    owner = {'name': owner_name, 'pokedex': pokedex, 'left': None, 'right': None}

    return owner

def insert_owner_bst(new_node, root):
    """
    Insert owner node to the BST
    """
    # If first owner
    if root is None:
        global ownerRoot
        ownerRoot = new_node
        return 1

    # Adjust names for sorting
    root_name = root['name'].lower()
    new_name = new_node['name'].lower()

    # "Smaller" names go left
    if root_name > new_name:
        if root['left'] is None:
            root['left'] = new_node
            return True
        else: return insert_owner_bst(new_node, root['left'])
    # "Bigger" names go right
    elif root_name < new_name:
        if root['right'] is None:
            root['right'] = new_node
            return True
        else: return insert_owner_bst(new_node, root['right'])
    # If name already exists
    else:
        return False

def find_owner_bst(root, owner_name):
    """
    Find owner in BST by name
    """
    # If no owners in BST
    if root is None:
        return None

    # Continue search direction by name
    if root['name'].lower() > owner_name.lower():
        return find_owner_bst(root['left'], owner_name)
    elif root['name'].lower() < owner_name.lower():
        return find_owner_bst(root['right'], owner_name)
    else: return root

def delete_owner_bst(root, owner_name):
    """
    Delete owner node from BST
    """
    # If owner found rewire BST without deleted owner
    if root['name'].lower() == owner_name.lower():
        if root['right']:
            if root['left']:
                insert_owner_bst(root['left'], root['right'])
            root = root['right']
        elif root['left']:
            root = root['left']
        else: root = None
        return root

    # If owner not found continue search in name direction
    elif owner_name.lower() > root['name'].lower() and root['right']:
        root['right'] = delete_owner_bst(root['right'], owner_name)
    elif owner_name.lower() < root['name'].lower() and root['left']:
        root['left'] = delete_owner_bst(root['left'], owner_name)

    return root


########################
# 3) Pokedex List Operations
########################

def add_pokemon_to_owner(owner):
    """
    Get ID input from user and add Pokemon to owner
    """
    index = read_int_safe("Enter Pokemon ID to add: ")

    # Check if Pokemon already in owner's Pokedex
    for pokemon in owner['pokedex']:
        if pokemon['ID'] == index:
            print("Pokemon already in the list. No changes made.")
            return

    # Find Pokemon by ID
    new_pokemon = get_poke_dict_by_id(index)
    # If Pokemon not found exit function
    if new_pokemon is None:
        return

    # Add Pokemon to owner's Pokedex
    owner['pokedex'].append(new_pokemon)
    print("Pokemon {0} (ID {1}) added to {2}'s Pokedex.".format(new_pokemon['Name'], new_pokemon['ID'], owner['name']))

def release_pokemon_by_name(owner):
    pokemon_name = input("Enter Pokemon Name to release: ").lower()

    for pokemon in owner['pokedex']:
        if pokemon['Name'].lower() == pokemon_name.lower():
            print("Releasing {0} from {1}.".format(pokemon['Name'], owner['name']))
            owner['pokedex'].remove(pokemon)
            return

    print("No Pokemon named '{0}' in {1}'s Pokedex.".format(pokemon_name, owner['name']))

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

    evolution = get_poke_dict_by_id(pokemon['ID'] + 1)
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


########################
# 4) Data Printing Functions
########################

def print_owner(owner):
    """
    Print owner's name and full Pokedex
    """
    # Print owner name
    print("\nOwner: {0}".format(owner['name']))
    # Check if Pokedex empty
    if len(owner['pokedex']) == 0:
        print("There are no Pokemons in this Pokedex that match the criteria.")
        return

    # Print each Pokemon in Pokedex
    for pokemon in owner['pokedex']:
        print("ID: {0}, Name: {1}, Type: {2}, HP: {3}, Attack: {4}, Can Evolve: {5}"\
              .format(pokemon['ID'], pokemon['Name'], pokemon['Type'],
                      pokemon['HP'], pokemon['Attack'], pokemon['Can Evolve']))

def bfs_print(node):
    """
    BFS print all owners
    """
    # Create list with first owner
    owners = [node]

    # While there are still owners - print
    while len(owners) > 0:
        print_owner(owners[0])
        # If owner has children add them to the list
        if owners[0]['left']:
            owners.append(owners[0]['left'])
        if owners[0]['right']:
            owners.append(owners[0]['right'])
        # Remove owner from list after printing
        owners.pop(0)

def pre_order_print(node):
    """
    Print all owners in pre-order
    """
    # In end of branch - return
    if node is None:
        return

    # First print owner then children
    print_owner(node)
    pre_order_print(node['left'])
    pre_order_print(node['right'])

def in_order_print(node):
    """
    Print all owners in in-order
    """
    # In end of branch - return
    if node is None:
        return

    # Print left, then owner, then right
    in_order_print(node['left'])
    print_owner(node)
    in_order_print(node['right'])

def post_order_print(node):
    """
    Print all owners in post-order
    """
    # In end of branch - return
    if node is None:
        return

    # Print children first then owner
    post_order_print(node['left'])
    post_order_print(node['right'])
    print_owner(node)

def display_pokemon_list(owner):
    """
    Display list of Pokemon by filter
    """
    # Print filter menu
    filter_type = display_menu()

    while filter_type != 7:
        # Filter list by given input
        filtered_list = filter_pokedex(filter_type, owner['pokedex'])

        # Verify list not empty
        if len(filtered_list) == 0:
            print("There are no Pokemons in this Pokedex that match the criteria.")

        # Print filtered list of Pokemon
        for pokemon in filtered_list:
            print("ID: {0}, Name: {1}, Type: {2}, HP: {3}, Attack: {4}, Can Evolve: {5}"\
                  .format(pokemon['ID'], pokemon['Name'], pokemon['Type'], pokemon['HP'], pokemon['Attack'], pokemon['Can Evolve']))

        filter_type = display_menu()

    print("Back to Pokedex Menu.")


########################
# 5) Pokedex Sub-menu
########################

def existing_pokedex(owner):
    """
    Enter existing Pokedex of owner
    """
    choice = pokedex_menu(owner['name'])
    # Direct to function from menu by input
    while choice != 5:
        # Add Pokemon
        if choice == 1:
            add_pokemon_to_owner(owner)
        # Go to display Pokemon menu
        elif choice == 2:
            display_pokemon_list(owner)
        # Release Pokemon from Pokedex
        elif choice == 3:
            release_pokemon_by_name(owner)
        # Evolve Pokemon in Pokedex
        elif choice == 4:
            evolve_pokemon_by_name(owner)
        else: print("Invalid choice.")
        choice = pokedex_menu(owner['name'])

    print("Back to Main Menu.")


########################
# 6) Menu Printing Functions
########################

def display_menu():
    """
    Print filter options for displaying Pokedex and get input
    """
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
    """
    Print menu for owner's Pokedex and get input
    """
    print("\n-- {0}'s Pokedex Menu --\n\
    1. Add Pokemon\n\
    2. Display Pokedex\n\
    3. Release Pokemon\n\
    4. Evolve Pokemon\n\
    5. Back to Main\n\
    ".format(name))
    return read_int_safe("Your choice: ")

def print_owners_menu():
    """
    Print sorting options for displaying owners and get input
    """
    print("1) BFS\n\
    2) Pre-Order\n\
    3) In-Order\n\
    4) Post-Order\n\
    ")
    return read_int_safe("Your choice: ")

def main_menu():
    """
    Print main menu and get input
    """
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
# 7) Sub Functions
########################

def add_pokedex():
    """
    Add a new owner to the database
    """
    # Get owner name
    owner_name = input("Owner name: ")
    # Get first Pokemon
    print("Choose your starter Pokemon:\n\
    1) Treecko\n\
    2) Torchic\n\
    3) Mudkip\n\
    ")
    starter = read_int_safe("Your choice: ")
    # Create node for first Pokemon
    first_pokemon = HOENN_DATA[starter * 3 - 3]

    # Create owner node and insert to BST
    global ownerRoot
    new_owner = create_owner_node(owner_name, first_pokemon)
    success = insert_owner_bst(new_owner, ownerRoot)

    if success:
        print("New Pokedex created for {0} with starter {1}.".format(owner_name, first_pokemon['Name']))
    else: print("Owner '{0}' already exists. No new Pokedex created.".format(owner_name))

def enter_pokedex():
    """
    Go to owner's Pokedex by name
    """
    global ownerRoot
    name = input("Owner name: ")

    # Find owner in the BST
    owner = find_owner_bst(ownerRoot, name)
    if owner is None:
        print("Owner '{0}' not found.".format(name))
        return

    # Go to Pokedex
    existing_pokedex(owner)

def delete_pokedex():
    """
    Delete Owner from database
    """
    global ownerRoot

    # Check if there are any owners
    if ownerRoot is None:
        print("No owners to delete.")
        return

    # Get owner name to delete
    owner_name = input("Enter owner to delete: ")
    # Find owner in BST
    owner = find_owner_bst(ownerRoot, owner_name)
    if not owner:
        print("Owner '{0}' not found.".format(owner_name))
        return

    # Delete owner from BST
    print("Deleting {0}'s entire Pokedex...".format(owner['name']))
    ownerRoot = delete_owner_bst(ownerRoot, owner_name)
    print("Pokedex deleted.")

def print_sorted_owners():
    """
    Print owners by name and number of Pokemon
    """
    # Check if there are any owners
    if ownerRoot is None:
        print("No owners at all.")
        return

    # Create list of all owners
    owners_list = []
    owners_list = gather_all_owners(ownerRoot, owners_list)

    # sort list by name and number of Pokemon
    sorted_list = sorted(owners_list, key=lambda owner_node: owner_node['name'].lower())
    sorted_list = sorted(sorted_list, key=lambda owner_node: len(owner_node['pokedex']))

    # Print sorted owners
    print("=== The Owners we have, sorted by number of Pokemons ===")
    for owner in sorted_list:
        print("Owner: {0} (has {1} Pokemon)".format(owner['name'], len(owner['pokedex'])))

def print_all_owners():
    """
    Print all owners by selected order
    """
    # Check if there are any owners
    if ownerRoot is None:
        print("No owners in the BST.")
        return
    # Print menu and get sorting type
    choice = print_owners_menu()

    # Direct to correct ordering type
    if choice == 1:
        bfs_print(ownerRoot)
    elif choice == 2:
        pre_order_print(ownerRoot)
    elif choice == 3:
        in_order_print(ownerRoot)
    elif choice == 4:
        post_order_print(ownerRoot)


########################
# MAIN FUNCTION
########################

def main():
    """
    MAIN FUNCTION
    """
    # Print main menu and get input
    choice = main_menu()

    # Direct to correct function by input
    while choice != 6:
        # Add new owner
        if choice == 1:
            add_pokedex()
        # Go to owner's Pokedex
        elif choice == 2:
            enter_pokedex()
        # Delete owner from BST
        elif choice == 3:
            delete_pokedex()
        # Print owners ordered by # of Pokemon
        elif choice == 4:
            print_sorted_owners()
        # Print all owners by requested order
        elif choice == 5:
            print_all_owners()
        else: print("Invalid choice.")
        choice = main_menu()
    print("Goodbye!")

if __name__ == "__main__":
    main()
