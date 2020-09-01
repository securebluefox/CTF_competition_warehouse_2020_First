from secret import flag

print 'Welcome to XM crypto system!\n'
print 'Please give me 100 (x,y) which satisfies x **2 = ( 1**2 + 2**2 + ... + y**2) / y\n'
anss = []
mark = 0
for i in range(100):
    print "[>] x: "
    x = getdata
    print "[>] y: "
    y = getdata
    if x <=0 or y <= 0 :
        mark = 1
        print "This is not what i want!\n"
        break
    if x **2 != ( 1**2 + 2**2 + ... + y**2)/y :
        mark = 1
        print "This is not what i want!\n"
        break
    ans = (x, y)
    if ans in anss:
        mark = 1
        print "This is not what i want!\n"
        break
    else:
        print "You are right!\n"
        anss.append(ans)
if mark == 0:
    print "flag is: " + flag + "\n"
else:
    print "Something wrong!\n"
