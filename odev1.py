import numpy as np
import matplotlib.pyplot as plt

import random as rd


fig = plt.figure()

wd=0
#random sayılar oluşturuldu
mu1= rd.uniform(-5,5)
sigma1= rd.uniform(0.5,1.5)

mu2=rd.uniform(-5,5)
sigma2=rd.uniform(0.5,1.5)

#gaussian olarak 1000er sayılı diziler yapıldı
q = mu1+sigma1*np.random.randn(10000)
p= mu2+sigma2*np.random.randn(10000)

#rastgele oluşturulmuş diziler en yakın sayıya yuvarlandı
a= np.around(q)
b= np.around(p)

y1,x1, _= plt.hist(a, 40,range= (-20,20),normed=1, color='green')
y2, x2, _ = plt.hist(b, 40,  range=(-20,20),normed=1, color='red')

#değerleri 1 arttırdım ama kullanılacak yeri kavrayamadığım için commentledim
#y1yeni=[x+1 for x in y1]
#y2yeni=[x+1 for x in y2]

y1deneme=[x for x in y1]
y2deneme=[x for x in y2]

y11=[x for x in y1]
y22=[x for x in y2]

#Wasserstein metric'e göre farklarını hesaplamayı DENEDİM
for i in range(0,40):
    if y11[i] != 0:
        for j in range(0,40):
            if y22[j]!=0:
                if y11[i]> y22[j]:
                    y11[i]-=y2[j]
                    y22[j]=0
                    wd+=abs(i-j)*y22[j]
                elif y22[j]> y11[i]:
                    y22[j]-=y11[i]
                    y11[i]=0
                    wd+=abs(i-j)*y11[i]
                    i=0
                    break
                else: #eşit olduğunda yani en son stepte
                    wd += abs(i-j)*y11[i]
                

#ahis=np.digitize(a,bins = range(-20,21,1))



plt.show()
