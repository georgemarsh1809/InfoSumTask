# Import 2 CSV files

# Calculate:   
#   The count of keys in each file
#   The count of distinct keys in each file
#   The count of the overlap (how many keys are in both files)
#   The product of the overlap (the count of each overlapping key in each file, multiplied together, then totalled)

import csv
from collections import Counter

file1, file2 = './Data/A_f.csv', './Data/B_f.csv'

def open_files(file1, file2):
    file_one_keys = []
    file_two_keys = []      

    with open(file1, "r") as f:
        # I used the csv library so I had access to more csv specific functions, which will allow for easier scaling if new fields are introduced
        csv1 = csv.reader(f) 
        for line in csv1:
            key = line[0]  # In the event that a csv is uploaded that has more than 1 column, only the first column will be read
            if key != "": # Removes all empty keys, since they don't need to be compared
                file_one_keys.append(key) # Adding keys to an array for easier iteration in other functions

    with open(file2, "r") as f:
        csv2 = csv.reader(f)
        for line in csv2:
            key = line[0]
            if key != "":
                file_two_keys.append(key)

    return file_one_keys, file_two_keys


def key_count(file1_keys, file2_keys):
    file1_key_count = len(file1_keys)
    file2_key_count = len(file2_keys)

    return file1_key_count, file2_key_count


def distinct_key_count(file1_keys, file2_keys):
    # The set function takes an iterable (such as an array\list) and returns a set of distinct elements 
    # By using a Set, only distinct elements are added and counted

    # Something to consider is that every time the set is created, the order isn't guaranteed to be the same. 
    # For the purposes of this task, the order of elements isn't relevant

    file1_set = set(file1_keys)
    file2_set = set(file2_keys)

    file1_distinct_key_count = len(file1_set)
    file2_distinct_key_count = len(file2_set)

    return file1_distinct_key_count, file2_distinct_key_count


def get_overlap(file1_keys, file2_keys):
    # First, get the set (an array of unique keys) for each file:
    file1_set, file2_set = set(file1_keys), set(file2_keys)

    # Initialise an empty array to contain the keys that overlap:
    overlap_array = []

    # Iterate over set1, and check if each key is in set2:
    for key in file1_set:
        if key in file2_set:
            # ...if the key is in both sets, add it to the overlap_array:
            overlap_array.append(key)

    overlap_count = len(overlap_array)

    return overlap_count


def calculate_overlap_product(file1_keys, file2_keys):
    # By using the Counter method from the collections module, we don't have to iterate over the key arrays for each item in the array and get the count of each

    # Counter creates a dictionary object where the keys are unique elements, and values are the counts (how many times they show up)
    # We now have something to lookup the number of occurrences for each key, which is MUCH faster
    file1_dict = Counter(file1_keys)
    file2_dict = Counter(file2_keys)

    # They don't need to be created into sets, since the Counter method creates a dictionary with only unique keys
    # We can then create an object of the intersection of the overlapping keys:
    overlapping_keys = file1_dict.keys() & file2_dict.keys()

    # Initialise overlap_product to 0...
    overlap_product = 0

    # For every key in the overlap:
    for key in overlapping_keys:
        # Increment the overlap_product by the amount of times the key shows up in each array:
        overlap_product += file1_dict[key] * file2_dict[key]

    return overlap_product


def execute_and_profile():
    # Load keys into arrays
    file1_keys, file2_keys = open_files(file1=file1, file2=file2)

    # Calculate the count of all keys in each file (omitting empty keys - handled in open_files)
    file1_key_count, file2_key_count = key_count(file1_keys, file2_keys)
    print("Key Count")
    print("File 1: ", f'{file1_key_count:,}', "| File 2: ", f'{file2_key_count:,}',  "\n")

     # Calculate the count of distinct keys in each file 

    file1_distinct_key_count, file2_distinct_key_count = distinct_key_count(file1_keys, file2_keys)
    print("Distinct Key Count")
    print("File 1: ", f'{file1_distinct_key_count:,}', "| File 2: ", f'{file2_distinct_key_count:,}', "\n")

    # Calculate the count of the distinct overlap
    print ("Key Overlap Count: ")
    print(f'{get_overlap(file1_keys, file2_keys):,}', "\n")

    # Calculate the overlap product
    print("Overlap Product: ")
    overlap_product = calculate_overlap_product(file1_keys, file2_keys)
    print(f'{overlap_product:,}')

execute_and_profile()

    


