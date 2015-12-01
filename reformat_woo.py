import os


f1 = open( "woo-modules-index.txt" , "r" )
f2 = open( "woo-modules-rewrite.txt" , "w" )
d = f1.readlines()
f1.seek(0)
string = ""
for l in d:
      if l != "" and l[0] != " " and len(l)>5:
            string += l.rstrip('\n')+","
f2.write(string)
f1.close()
f2.close()
      

