from datetime import date

import random

m_or_f = True
date = date.today()

print (date)


rand = random.randint(0,1)
print(rand)


gender='f'
if rand == 1:
    gender='m'
else:
    gender:'f'
print (gender)