"""
A terminal-based application used to track the 1001 films you need to see.

TODOs:
    -> add an option to remove a certain film from seen list
    
Possible further dev:
    -> stats for films
    -> better interaction with the films (imdb API reading etc) eg query about a film: get a plot description, director, actors etc
"""
import os
import random
import json
import pyperclip as pc

def filmGetter(films):    # loops thru the film list, continues if the film is in seen_list
    select = False   
    while not select:     # if seen, then ask to rate, if not seen, then copy to clipboard, if not wanna see, then reroll   
        film =  films[random.randint(0, len(films)-1)]
        while True:
            if checkIfSeen(film) == True:
                print("  Already seen {0}!".format(film))
                break

            print("  Selected film:")
            print("-> ", film)
            print("1 - Watchlist | 2 - Seen | 3 - skip | e - stop")
            inp = input()

            match inp:
                case "1":
                    try:
                        pc.copy(film + " imdb")
                        print("  Copied title to clipboard!")
                    except:
                        print(" ", film)
                    select = True
                    break
                case "2":
                    filmRater(film)
                    break
                case "3":
                    print("  Randomizing the film...")
                    break
                case "e":
                    select = True
                    break
                case _:
                    print("this will keep the loop going")
                    continue

def checkIfSeen(ttl):       # checks if a title is already in seen list
    seen = False
    try:
        with open('seen.json', 'r', encoding='utf-8') as f:
            seen_list = json.load(f)
        for i in seen_list:
            if i["title"] == ttl:
                seen = True
                break
            else:
                seen = False
    except:
        pass

    return seen

def filmAdder(ttl, rat=0):      # adds a film to the seen_list
    seen_list =[]

    try:
        with open('seen.json', 'r') as f:
            seen_list = json.load(f)
    except:
        pass

    seen_list.append(filmEntry(ttl, rat))
    
    with open('seen.json', 'w') as f:
        json.dump(seen_list, f, indent=4)
           
def filmEntry(ttl, rat=0):      # creates a dictionary to add to the list of seen films, a separate function to reuse later in changing the rate of a film
    return dict(title = ttl, rating = rat)

def filmRater(film):        # rates a film and adds it to the seen.json
    while True:
        inp = input("  Please rate (0-10): ")
        print(film)
        try:
            rate = int(inp)
            if rate > 10:
                rate = 10
            filmRated = filmEntry(film, rate)       # creates a dictionary with title and rate of the film
            filmAdder(film, rate)                   # adds the rated film to the seen.json
            print("  Successfully rated the film {0} with {1}/10".format(filmRated["title"], filmRated["rating"]))
            break
        except:
            print("  Please type an integer 0-10")
            continue

def filmsSeen():
    not_rated_list = []
    try:
        with open('seen.json', 'r', encoding='utf-8') as f:
            seen_list = json.load(f)
        
        for i in seen_list:
            if i["rating"] == 0:
                not_rated_list.append(i)

        print("  You've seen these films:")
        for i in seen_list:
            print("  {0}, rated {1}".format(i["title"], i["rating"]))

    except:
      print("  You haven't seen any film yet!")

    return not_rated_list

def filmsNotRated():
    not_rated_list = []
    try:
        with open('seen.json', 'r', encoding='utf-8') as f:
            seen_list = json.load(f)
        
        for i in seen_list:
            if i["rating"] == 0:
                not_rated_list.append(i)
       
        if len(not_rated_list) == 0:
            print("  No unrated film detected!")
        else:
            print("  Not rated films:")
            for i in not_rated_list:
                print("  "+i["title"])
    except: 
      print("  You haven't seen any film yet!")

    return len(not_rated_list)


def filmRateChanger():
    with open('seen.json', 'r') as f:
        seen_list = json.load(f)
    
    if filmsNotRated() > 0:
        while True:
            print("  Which film do you want to rate?")
            ttl = input()
            print("  Please rate:")
            rat = input()
            for i in seen_list:
                if i["title"] == ttl:
                    print(i)
                    i["rating"] = rat
                    print(i)
            break

    with open('seen.json', 'w') as f:
        json.dump(seen_list, f, indent=4)

def main():
    with open('the_list.txt', 'r', encoding='utf-8') as f:      # reads all films on the list
        filmList = f.read().splitlines()
    
    try:       # tries to open seen.json, asks to create such file if non-existent
        with open('seen.json', 'r') as f:
            seen_list = json.load(f)
    except:
        print("   Seems like its the first time using this program.")
        print("   The list of seen films doesnt exist")
        print("   Creating database for seen films...")
        with open("seen.json", "w") as f:
            pass

    while True:     # main loop of the program
        print("_____")
        print("1 - Select a random film | 2 - List seen films | 3 - List not rated films | 4 - Rate an unrated film | e - exit")
        print("What do you want to do?")
        choice = input()
        print("")
        print("___")
        match choice:
            case "1":
                filmGetter(filmList)
            case "2":
                filmsSeen()
            case "3":
                filmsNotRated()
            case "4":
                filmRateChanger()
            case "e":
                break
            case _:
                continue

if __name__ == "__main__":
    main()

