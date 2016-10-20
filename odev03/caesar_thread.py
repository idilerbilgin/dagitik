import threading

MAX_KEY_SIZE = 26

def caesar(key, thr ,length):
    with open('metin.txt', 'r') as myfile: 
        data="".join(line.rstrip() for line in myfile) #metinden aldığımız string
    datalist=list(data) #stringin her karakterini listeye attık
    myfile.close() 
    #dosyadaki yazılanları okuduk alt satır belirtisi \n'leri çıkarttık ve dosyayı kapattık
    cipher=''
    for i in datalist[length]:
        c=(ord(i)+key)%126
        if c<32:
            c+=31
        cipher +=chr(c)
    i+=length
    #istenen isimle yeni bir dosya oluşturduk
    filename= 'crypted_'+key+'_'+thr+'_'+length+'.txt'
    file=open(filename, 'w')
    file.write(cipher)
    
def getkey():
    key=0
    print "Enter the key value between 0 and 26:"
    key= int(input())
    if(key>=1 and key<=MAX_KEY_SIZE):
        return key
    else:
        getkey()
    
thread_list = []
print "Welcome to the Caesar Cifer"

key=getkey() 
    
print "Enter the number of threads you want to use:"
thr= int(input())

print "Enter the length:"
length=int(input())

for i in range(1, thr):
    t = threading.Thread(target=caesar, args=(key,thr,length,))
    thread_list.append(t)

# threadler başladı
for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()