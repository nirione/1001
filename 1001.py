"""
A terminal-based application used to track the 1001 films you need to see.

reconsider: filmGetter loop, seems a bit too long and too nested

TODOs:
    -> implement a function to change rating of the film
    -> shorten the prompts in filmGetter: print out the possible options already 
        eg 1 - want to see, 2 - seen, 3 - rate, 4 - skip
    -> stats for films
    -> in main(): check for existance of seen.json in local folder, if false ask to create it
    -> listing seen films, listing unrated films (rate=0)
    
Possible further dev:
    -> better interaction with the films (imdb API reading etc) eg query about a film: get a plot description, director, actors etc
"""
import os
import random
import json
import pyperclip as pc

ansY = ["Y", "y", "yes", "Yes", "YES"]
ansN = ["N", "n", "no", "No", "NO"]
ex = ["e", "E", "exit", "EXIT", "Exit"]

def randomFilm(films):      # returns a random film from the list
    return films[random.randint(0, len(films)-1)]

def filmGetter(filmList):    # loops thru the film list, continues if the film is in seen_list
    select = False
    while not select:
        film = randomFilm(filmList)
    
        while True:
            print("I've selected this: ", film)

            if checkIfSeen(film):
                print("Already seen!")
                continue
            else:
                print("Have you seen it? [Y/N]")
                inp = input()
                if inp in ansY:         # change all this to match case statement
                    filmRater(film)
                    break
                elif inp in ansN:
                    print("Want to see it? [Y/N]")
                    inp2 = input()
                    if inp2 in ansY:
                        print("Copied title to clipbaord!")
                        pc.copy(film)
                        select = True
                        break
                    elif inp2 in ansN:
                        print("Not wanna see it...")
                        break
                    elif inp2 == "e":
                        select = True
                        break
                    else:
                        print("Invalid input")
                        continue
                elif inp == "e":
                    select = True
                    break
                else:
                    print("Invalid input")
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
        inp = input("Please rate (0-10): ")
        print(film)
        try:
            rate = int(inp)
            if rate > 10:
                rate = 10
            print("rated {0}".format(rate))
            filmRated = filmEntry(film, rate)       # creates a dictionary with title and rate of the film
            filmAdder(film, rate)                   # adds the rated film to the seen.json
            print("Successfully rated the film:")
            print(filmRated["title"])
            break
        except:
            print("Please type an integer 0-10")
            continue

def main():
    with open('the_list.txt', 'r', encoding='utf-8') as f:      # reads all films on the list
        filmList = f.read().splitlines()
    
    try:       # tries to open seen.json, asks to create such file if non-existent
        with open('seen.json', 'r') as f:
            seen_list = json.load(f)
    except:
        print("Seems like its the first time using this program.")
        print("The list of seen films doesnt exist")
        print("Creating database for seen films...")
        with open("seen.json", "w") as f:
            pass

    while True:     # main loop of the program
        print("1 - Select a random film | 2 - List seen films | e - exit")
        print("What do you want to do?")
        choice = input()
    
        match choice:
            case "1":
                filmGetter(filmList)
            case "2":
                print("This will show you the list of films youve seen!")
            case "e":
                break
            case _:
                continue

if __name__ == "__main__":
    main()

