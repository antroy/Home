def rota(people):
    _people = list(people)
    current = 0
    while len(_people):
        yield _people[current]
        current = (current + 1) % len(_people)


if __name__ == "__main__":
    
    people = ["Ant", "Bernard", "Carly", "Deb", "Englebert"]
    r = rota(people)

    for i in range(10):
        print "It's %s's turn." % r.next()

        


