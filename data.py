def polynomial(x):
    return (x * x * x) + (x * x)

NVAR = 1.0
NRAND = 1.0
MINRAND = -1.0
MAXRAND = 1.0
NFITCASES = 50


inp = (MAXRAND - MINRAND) / NFITCASES
#print(inp)
x = MINRAND
f = open('data', 'w')
f.write("%d %d" % (NVAR, NFITCASES))
for i in range(0,NFITCASES):
    f.write("\n")
    y = polynomial(x)
    #print(y)
    f.write(("%f %f") % (x, y))
    x = x + inp
f.close()




