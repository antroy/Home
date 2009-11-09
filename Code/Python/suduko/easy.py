import sd

successes = 0
total = 0

easy_probs = file("easy_probs.txt")
for i, line in enumerate(easy_probs):
    total += 1
    g = sd.grid(line.strip())
    g.print_grid()
    #out = sd.ariadnes_thread(g, True)
    out = sd.solve(g)
    g.print_grid()#r"c:\0\zzzzz-%d.txt" % i)
    print "Problem %d:" % i, 
    if out:
        print "Success!"
        successes +=1
    else:
        print "Failure!"
    break
easy_probs.close()

print "%d out of %d successful!" % (successes, total)
