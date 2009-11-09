import sd

successes = 0
total = 0

hard_probs = file("hard_probs.txt")
for i, line in enumerate(hard_probs):
    total += 1
    g = sd.grid(line.strip())
    out = sd.ariadnes_thread(g, True)
    g.print_grid(r"c:\0\zzzzz-%d.txt" % i)
    print "Problem %d:" % i, 
    if out:
        print "Success!"
        successes +=1
    else:
        print "Failure!"
    
hard_probs.close()

print "%d out of %d successful!" % (successes, total)
