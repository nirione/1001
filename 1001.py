"""
A terminal-based application used to track the 1001 films you need to see.

TODOs:
    -> stats for films
    -> in main(): check for existance of seen.json in local folder, if false ask to create it
    -> listing seen films, listing unrated films (rate=0)
    
Possible further dev:
    -> better interaction with the films (imdb API reading etc) eg query about a film: get a plot description, director, actors etc
"""
import os
import random
import json

def randomFilm(films):      # returns a random film from the list
    return films[random.randint(0, len(films)-1)]

def filmGetter(filmList):    # loops thru the film list, continues if the film is in seen_list
    ansY = ["Y", "y", "yes", "Yes", "YES"]
    ansN = ["N", "n", "no", "No", "NO"]
    while True:
        film = randomFilm(filmList)
        print("I've selected this: ", film)

        if checkIfSeen(film):
            print("Already seen!")
            continue
        else:
            print("Have you seen it? [Y/N]")
            inp = input()
            if inp in ansY:
                filmRater(film)
                continue
            elif inp in ansN:
                break
            break

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
    
    try:       # tries to open seen.json, should ask to create such file if non-existent
        with open('seen.json', 'r') as f:
            seen_list = json.load(f)
    except:
        print("Seems like its the first time using this program. The list of seen films doesnt exist")
        print("Create one? [Y/N]")
        conf = input()
        print("I dont work yet :(")
        pass

    while True:     # main loop of the program
        print("1 - Select a random film | 2 - List seen films")
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
