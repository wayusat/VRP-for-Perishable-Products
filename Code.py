'''
Created on 11 Des 2020

@author: User
'''
import copy


'''                             P A R A M E T E R                            '''

#============Variable setiap entitas=============#
#n1 = jumlah retailer pada cluster 1 Singkawang
n1 = 40
#n2 = jumlah retailer pada cluster 2 Pontianak & Kubu Raya
n2 = 75
#n3 = jumlah retailer pada cluster 3 Mempawah
n3 = 25
#n4 = jumlah retailer pada cluster 4 Anjungan & Pinoh
n4 = 20
#n5 = jumlah retailer pada cluster 5 Sambas
n5 = 25
#n6 = jumlah retailer pada cluster 6 Pemangkat
n6 = 15
#total jumlah retailer
totjumlahretailer = n1+n2+n3+n4+n5+n6
#v = jumlah kendaraan
n7 = 5


#Depot
Depot = [0]
#himpunan indeks untuk retailer cluster 1 singkawang
N1 =[i for i in range (1,n1+1)]
#himpunan indeks untuk retailer cluster 2 pontianak & kubu raya
N2 =[i for i in range (n1+1,n1+n2+1)]
#himpunan indeks untuk retailer cluster 3 mempawah
N3 =[i for i in range (n1+n2+1,n1+n2+n3+1)]
#himpunan indeks untuk retailer cluster 4 pinoh & anjungan
N4 =[i for i in range (n1+n2+n3+1,n1+n2+n3+n4+1)]
#himpunan indeks untuk retailer cluster 5 Sambas
N5 =[i for i in range (n1+n2+n3+n4+1,n1+n2+n3+n4+n5+1)]
#himpunan indeks untuk retailer cluster 5 Sambas
N6 =[i for i in range (n1+n2+n3+n4+n5+1,n1+n2+n3+n4+n5+n6+1)]
#Himpunan indeks untuk seluruh retailer
N = N1 + N2 + N3 + N4 + N5 + N6
#himpunan indeks untuk kendaraan
V =[i for i in range (n1+n2+n3+n4+n5+n6+1, n1+n2+n3+n4+n5+n6+n7+1)]
#himpunan jejaring transportasi kendaraan
truckNetw = Depot+N


import numpy as np
rnd = np.random
rnd.seed(0)
#kapasitas setiap retailer
CapaRetailer_N={i:rnd.randint(1,20)for i in N}
#kapasitas setiap truck
CapaTruck_V={i:100 for i in V}
#demand setiap retailer
DemandRetailer_N = {}
for i in N:
    capmax = CapaRetailer_N[i]
    DemandRetailer_N[i] = rnd.randint(1,capmax+1)


#Membangkitkan koordinat lokasi retailer
rnd.seed(1)
custPositionTruck = {i:(rnd.randint(0,15001),(rnd.randint(106500,106500+15001)))for i in [0]+N1}
custPositionTruck.update({i:(rnd.randint(35000,35000+9501),(rnd.randint(0,14001))) for i in N2})
custPositionTruck.update({i:(rnd.randint(0,3501),(rnd.randint(54000,54000+2501))) for i in N3})
custPositionTruck.update({i:(rnd.randint(10000,10000+13001),(rnd.randint(47000,47000+9001))) for i in N4})
custPositionTruck.update({i:(rnd.randint(35000,35000+5001),(rnd.randint(164000,164000+4501))) for i in N5})
custPositionTruck.update({i:(rnd.randint(3500,3500+2001),(rnd.randint(140000,140000+1501))) for i in N6})

import math
distanceMatrix = {(i,j):math.ceil(math.sqrt((custPositionTruck[i][0]-custPositionTruck[j][0])**2 
                                      + (custPositionTruck[i][1]-custPositionTruck[j][1])**2) 
                                      /10 * 1/40 *60) for i in custPositionTruck for j in custPositionTruck if i!=j}
#print('distanceMatrix',distanceMatrix)
print('V',V)
#print('CapaRetailer_N',CapaRetailer_N)
print('DemandRetailer_N',DemandRetailer_N)
#print('koordinat',custPositionTruck)

import matplotlib.pyplot as plt
x=[]
y=[]
for i in custPositionTruck:
    x.append(custPositionTruck[i][0])
    y.append(custPositionTruck[i][1])
plt.scatter(x, y, s=3)
for i in range(0,totjumlahretailer+1):
    xy=(x[i],y[i])
    s=i
    plt.annotate(s, xy)
plt.show()



'''                             GREEDY HEURISTIC                            '''

def PostofVehicle (JumlahTruck, Koordinat):
    truk_lokasi_awal = {i: Depot for i in JumlahTruck}
    return truk_lokasi_awal

def SortingRetailerDemand(RetailerDemand):
    Sort = {i:j for i, j in sorted(RetailerDemand.items(), key=lambda x:x[1])}
    return Sort

def SchedulingTruck(i, StartPosition, StartTime, CapacityofTruck, DemandRetailers, DistMatrix):
    TruckPositionTime = {i: [(StartPosition,StartTime, CapacityofTruck)]}
    a = copy.deepcopy(DemandRetailers)
    for i in TruckPositionTime:
        while bool(a) == True :
            dest = list(a.keys())[0]
            dist = DistMatrix[(StartPosition, dest)]
            time_jalan = int(dist/20)
            time_spent = StartTime + time_jalan
            dropamount = list(a.values())[0]
            sisa_muatan = CapacityofTruck - dropamount
            newroute = (dest, time_spent, sisa_muatan)
            TruckPositionTime.setdefault(i,[]).append(newroute)
            StartPosition = dest
            StartTime = time_spent
            CapacityofTruck = sisa_muatan
            del a[dest]
            if CapacityofTruck <= list(a.values())[0] :
                break
        return TruckPositionTime

def TruckRefill(JadwalTruk, LokasiDepot, DisMatrix):
    trukpos = list(JadwalTruk.values())[0][-1][-1]
    locDepot = LokasiDepot
    jarakkedepot = DisMatrix[(trukpos, locDepot)]
    Wtempuh = int(jarakkedepot/20)
    Wdihabiskan = list(JadwalTruk.values())[0][-1][-2] + Wtempuh
    refill = 100
    rutebaru = (locDepot, Wdihabiskan, refill)
    JadwalTruk.setdefault(i,[]).append(rutebaru)
    return JadwalTruk 


'''                          M A I N  P R O G R A M                              '''
if __name__ == '__main__' : 
#print ('titik awal vehicle :', PostofVehicle(V, N))
#print('urutan demand dari besar ke kecil :',SortingRetailerDemand(DemandRetailer_N))