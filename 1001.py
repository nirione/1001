import os
import random
import json

def filmEntry(ttl, rat=0):
    return dict(title = ttl, rating = rat)

def randomFilm(films):
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
            if inp in ansY:    # should probably be a separate function
                filmRater(film)
                continue
            elif inp in ansN:
                break
            break

def checkIfSeen(ttl):    # checks if a title is already in seen list
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

def filmAdder(ttl, rat=0):    # adds a film to the seen_list
    seen_list =[]

    try:
        with open('seen.json', 'r') as f:
            seen_list = json.load(f)
    except:
        pass

    seen_list.append(filmEntry(ttl, rat))
    
    with open('seen.json', 'w') as f:
        json.dump(seen_list, f, indent=4)

def filmRater(film):
    while True:
        inp = input("Please rate (0-10): ")
        print(film)
        try:
            rate = int(inp)
            if rate > 10:
                rate = 10
            print("rated {0}".format(rate))    # should add the film to seen list with rate
            filmRated = filmEntry(film, rate)
            filmAdder(film, rate)
            print("Successfully rated the film:")
            print(filmRated["title"])
            break
        except:
            print("Please type an integer 0-10")    # should return false
            continue

def main():
    with open('the_list.txt', 'r', encoding='utf-8') as f:
        filmList = f.read().splitlines()
    
    try:
        with open('seen.json', 'r') as f:
            seen_list = json.load(f)
    except:
        pass

    while True:
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

#    print("Checking if a movie was seen:")
#    print("Aliens: ", checkIfSeen("Aliens (1986)"))
#    print("The Assistant (2019)", checkIfSeen("The Assistant (2019)"))

#    filmAdder("Aliens (1986)", 10)

if __name__ == "__main__":
    main()

