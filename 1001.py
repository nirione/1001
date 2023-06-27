"""
A terminal-based application used to track the 1001 films you need to see.

reconsider: filmGetter loop, seems a bit too long and too nested

TODOs:
    -> listing seen films, listing unrated films (rate=0)
    -> implement a function to change rating of the film
    -> stats for films
    
Possible further dev:
    -> better interaction with the films (imdb API reading etc) eg query about a film: get a plot description, director, actors etc
"""
import os
import random
import json
import pyperclip as pc

def filmGetter(films):    # loops thru the film list, continues if the film is in seen_list
    select = False          # possible options: seen, not seen, not wanna see
    while not select:       # if seen, then ask to rate, if not seen, then copy to clipboard, if not wanna see, then reroll   
        film =  films[random.randint(0, len(films)-1)]
        while True:
            if checkIfSeen(film) == True:
                print("Already seen {0}!".format(film))
                break

            print("Selected film:")
            print(" ", film)
            print("1 - Watchlist | 2 - Seen | 3 - skip")
            inp = input()

            match inp:
                case "1":
                    try:
                        pc.copy(film)
                        print("Copied title to clipboard!")
                    except:
                        print("Seems like you are missing the \"pyperclip\" module on your machine...")
                        print("Selected film:")
                        print(" ", film)
                    select = True
                    break
                case "2":
                    filmRater(film)
                    break
                case "3":
                    print("Randomizing the film...")
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
        inp = input("Please rate (0-10): ")
        print(film)
        try:
            rate = int(inp)
            if rate > 10:
                rate = 10
            filmRated = filmEntry(film, rate)       # creates a dictionary with title and rate of the film
            filmAdder(film, rate)                   # adds the rated film to the seen.json
            print("Successfully rated the film {0} with {1}/10".format(filmRated["title"], filmRated["rating"]))
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

