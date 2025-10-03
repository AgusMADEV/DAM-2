from datetime import datetime

inicio = int(datetime.now().timestamp())

for i in range(0,16):
    numero = 1.00000098
    print("OH SH*T HERE WE GO AGAIN")
    for i in range(0,100000000):
        numero *= 1.0000000000654
    final = int(datetime.now().timestamp())
    
print("he tardado "+str(final-inicio)+" segundos")




    
