import openpyxl  # We'll parse the xlsx with openpyxl

# Global BST root
ownerRoot = None

########################
# 0) Read from XLSX -> HONEN_DATA
########################

def readHonenXlsx(filename):
    """
    Reads 'Honen_Pokedex.xlsx' and returns a list of dicts:
      [ { "ID": int, "Name": str, "Type": str, "HP": int,
          "Attack": int, "Can Evolve": "TRUE"/"FALSE" },
        ... ]
    """
    wb = openpyxl.load_workbook(filename)
    sheet = wb.active

    data_list = []
    first_row = True
    for row in sheet.iter_rows(values_only=True):
        if first_row:
            first_row = False
            continue
        if row[0] is None:
            break  # empty row => stop

        # row => (ID, Name, Type, HP, Attack, Can Evolve)
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

# This actually loads the data from the file:
HONEN_DATA = readHonenXlsx("Honen_Pokedex.xlsx")

########################
# 1) Helper Functions
########################

def readIntSafe(prompt):
    """
    Prompt the user for an integer, re-prompting on invalid input.
    """
    pass

def getPokeDictByID(ID):
    """
    Return a copy of the Pokemon dict from HONEN_DATA by ID, or None if not found.
    """
    pass

def getPokeDictByName(name):
    """
    Return a copy of the Pokemon dict from HONEN_DATA by name, or None if not found.
    """
    pass

def displayPokemonList(pokeList):
    """
    Display a list of Pokemon dicts, or a message if empty.
    """
    pass

########################
# 2) BST (By Owner Name)
########################

def createOwnerNode(ownerName, firstPokemon=None):
    """
    Create and return a BST node dict with keys: 'owner', 'pokedex', 'left', 'right'.
    """
    pass

def insertOwnerBST(root, newNode):
    """
    Insert a new BST node by ownerName (alphabetically). Return updated root.
    """
    pass

def findOwnerBST(root, ownerName):
    """
    Locate a BST node by ownerName. Return that node or None if missing.
    """
    pass

def minNode(node):
    """
    Return the leftmost node in a BST subtree.
    """
    pass

def deleteOwnerBST(root, ownerName):
    """
    Remove a node from the BST by ownerName. Return updated root.
    """
    pass

########################
# 3) BST Traversals
########################

def bfsTraversal(root):
    """
    BFS level-order traversal. Print each owner's name and # of pokemons.
    """
    pass

def preOrder(root):
    """
    Pre-order traversal (root -> left -> right). Print data for each node.
    """
    pass

def inOrder(root):
    """
    In-order traversal (left -> root -> right). Print data for each node.
    """
    pass

def postOrder(root):
    """
    Post-order traversal (left -> right -> root). Print data for each node.
    """
    pass

########################
# 4) Pokedex Operations
########################

def addPokemonToOwner(ownerNode):
    """
    Prompt user for a Pokemon ID, find the data, and add to this owner's pokedex if not duplicate.
    """
    pass

def releasePokemonByName(ownerNode):
    """
    Prompt user for a Pokemon name, remove it from this owner's pokedex if found.
    """
    pass

def evolvePokemonByName(ownerNode):
    """
    Evolve a Pokemon by name:
    1) Check if it can evolve
    2) Remove old
    3) Insert new
    4) If new is a duplicate, remove immediately
    """
    pass

########################
# 5) Sorting Owners by # of Pokemon
########################

def gatherAllOwners(root, arr):
    """
    Collect all BST nodes into a list (arr).
    """
    pass

def sortOwnersByNumPokemon():
    """
    Gather owners, sort them by (#pokedex size, then alpha), print results.
    """
    pass

########################
# 6) Print All
########################

def printAllOwners():
    """
    Let user pick BFS, Pre, In, or Post. Print each owner's data/pokedex accordingly.
    """
    pass

def preOrderPrint(node):
    """
    Helper to print data in pre-order.
    """
    pass

def inOrderPrint(node):
    """
    Helper to print data in in-order.
    """
    pass

def postOrderPrint(node):
    """
    Helper to print data in post-order.
    """
    pass

########################
# 7) The Display Filter Sub-Menu
########################

def displayFilterSubMenu(ownerNode):
    """
    1) Only type X
    2) Only evolvable
    3) Only Attack above
    4) Only HP above
    5) Only name starts with
    6) All
    7) Back
    """
    pass

########################
# 8) Sub-menu & Main menu
########################

def existingPokedex():
    """
    Ask user for an owner name, locate the BST node, then show sub-menu:
    - Add Pokemon
    - Display (Filter)
    - Release
    - Evolve
    - Back
    """
    pass

def mainMenu():
    """
    Main menu for:
    1) New Pokedex
    2) Existing Pokedex
    3) Delete a Pokedex
    4) Sort owners
    5) Print all
    6) Exit
    """
    pass

def main():
    """
    Entry point: calls mainMenu().
    """
    pass

if __name__ == "__main__":
    main()
