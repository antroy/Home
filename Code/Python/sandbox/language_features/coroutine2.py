def rota(people):
    _people = list(people)
    current = 0
    while len(_people):
        command = yield _people[current]
        current = (current + 1) % len(_people)
        if command:
            comm, name = command
            if comm == "add":
                _people.append(name)
            elif comm == "remove" and name in _people:
                _people.remove(name)

def printname(name):
    print "It's %s's turn." % name

if __name__ == "__main__":
    
    people = ["Ant", "Bernard", "Carly", "Deb", "Englebert"]
    r = rota(people)

    for i in range(6):
        printname(r.next())

    printname(r.send(("add", "Fred")))

    for i in range(7):
        printname(r.next())

    printname(r.send(("remove","Deb")))

    for i in range(6):
        printname(r.next())

    

        



