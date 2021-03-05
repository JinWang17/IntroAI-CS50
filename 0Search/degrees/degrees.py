#!/usr/bin/env python
# coding: utf-8

##################################################################
# Jin Wang
# Feb 24, 2021
# The following has been changed to the source code degrees.py:
# 1) Add the logic for shortest path 
# TODO: 
##################################################################
import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
# names = {Name(lowercase): ID (multiple ID is fine)}
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
# people = {ID: name, birth, movies}
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()   
                # what does this line do? This is an empty set used to store unique elements later
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass 
            # Q: Why would there be any error??
            # A: When the star.csv contains movies/ poeple that are not listed in the people.csv or movie.csv
            # The Python KeyError is a type of LookupError exception and denotes that there was an issue retrieving the key you were looking for. 
            # When you see a KeyError , the semantic meaning is that the key being looked for could not be found.



def main():
    # TODO: What is the difference between main() and directly writing out the main lines as in src0.py?
    
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"
    # default is to use "large"
    # USAGE: XX = ... if ... else ... 

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path 
        # path is like a matrix, first element is the movie that connects with last person; second element is the person's name
        # movie name and person name is in ID 
        for i in range(degrees): # 0, 1, 2, ..., degrees
            person1 = people[path[i][1]]["name"]  # access name by ID
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"] # access title by ID
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")
            # print(f"{Variables to be replaces} Variables to be displayed")


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set())) 
    # dict.get(key[, value]) is the same as dict[key] most of the time
    # Difference: get() method returns a default value if the key is missing.
    # However, if the key is not found when you use dict[key], KeyError exception is raised.
    # Here, we ask the code to return an empty set when there is no such person in the dictionary "names"
     
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    
    # Initialize frontier to just the source person ID
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)
    
    # Initialize an empty explored set
    explored = set()
    
    # Keep looping until solution found
    while True:
        
        # print("a new loop")
        # If nothing left in frontier, then no path
        if frontier.empty():
            return
        
        # Choose a node from the frontier
        node = frontier.remove()
        # print(f"person_ID: {node.state}")
        # print(f"movie_ID: {node.action}")
        # Mark node as explored
        explored.add(node.state)

        # Add neighbors to frontier
        for action, state in neighbors_for_person(node.state):
            if not frontier.contains_state(state) and state not in explored:
                # check if node is the target; if yes, then we have a solution
                
                # set_trace()
                # Type “n” and hit Enter to run the next line of code (The → arrow shows you the current position). 
                # Use “c” to continue until the next breakpoint. “q” quits the debugger and code execution.
                
                if state == target:
                    # print("hit target")
                    solution = [(action, state)]
                    # actions is the movie list; cells is the movie star list 
                    while node.parent is not None:
                        solution.append((node.action, node.state))
                        node = node.parent
                    solution.reverse()
                    #print(solution)
                    return(list(solution))
                
                # if not the target person, add this to the frontier
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)



if __name__ == "__main__":
    main()

