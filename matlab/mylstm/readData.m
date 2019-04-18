clc
clear
load C:\Users\Anzhi\Desktop\price.txt
price=reshape(price',1,[]);
dayOf123=31+29+31;
dayOf1234=dayOf123+30;
priceTrain=price(1:dayOf123*24);
priceTest=price(dayOf123*24+1:dayOf1234*24);