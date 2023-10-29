print("Hell, Git")

def f_x(x, y):
    return y-x*x*x

def f_y(x, y):
    return -x+y*y*y

def calck_K_L(k,l,x,y,h):#считаем коэфиценты в методе Рунге Кутта
    k[0]=h*f_x(x,y)
    l[0]=h*f_y(x,y)
    k[1]=h*f_x(x+0.5*k[0], y+0.5*l[0])
    l[1]=h*f_y(x+0.5*k[0], y+0.5*l[0])
    k[2]=h*f_x(x+0.25*k[0]+0.25*k[1], y+0.25*l[0]+0.25*l[1])
    l[2]=h*f_y(x+0.25*k[0]+0.25*k[1], y+0.25*l[0]+0.25*l[1])
    k[3]=h*f_x(x-k[1]+2*k[2], y-l[1]+2*l[2])
    l[3]=h*f_y(x-k[1]+2*k[2], y-l[1]+2*l[2])
    k[4]=h*f_x(x+(7/27)*k[0]+(10/27)*k[1]+(1/27)*k[3], y+(7/27)*l[0]+(10/27)*l[1]+(1/27)*l[3])
    l[4]=h*f_y(x+(7/27)*k[0]+(10/27)*k[1]+(1/27)*k[3], y+(7/27)*l[0]+(10/27)*l[1]+(1/27)*l[3])
    k[5]=h*f_x(x+0.0448*k[0]-0.2*k[1]+0.8736*k[2]+0.0864*k[3]-0.6048*k[4], y+0.0448*l[0]-0.2*l[1]+0.8736*l[2]+0.0864*l[3]-0.6048*l[4])
    l[5]=h*f_y(x+0.0448*k[0]-0.2*k[1]+0.8736*k[2]+0.0864*k[3]-0.6048*k[4], y+0.0448*l[0]-0.2*l[1]+0.8736*l[2]+0.0864*l[3]-0.6048*l[4])

def calck_r(k):#считаем возможные отклонения
    return -(1/336)*(42.*k[0]+224.*k[2]+21.*k[3]-162.*k[4]-125.*k[5])

def chois_h(r,x,y,epsilon):#подтверждаем шаг
    M = 0.0000000001 #надо выбрать М
    return (abs(r/max(M,y,x)) > epsilon)

def horisontal_chois_h(r,x,y,h):
    epsilon_0 = 0.0000000001
    if(chois_h(r,x,y,epsilon_0)):
        return h/2
    if(chois_h(r,x,y,0.015625*epsilon_0)):
        return h
    return h*2

def chois_Last_h(h,x_last,y_last,x,y): #выбираем последний шаг(те пересечение с прямой y=0)
    while(y<0. ):
        h=h*0.9999
        x = x_last
        y = y_last
        calck_K_L(k,l,x,y,h)
        x = x +(1/6)*(k[0]+2*k[2]+k[3])
        y = y +(1/6)*(l[0]+2*l[2]+l[3])
    print( "Проверка качества; последний h и y",h,y)  
    return [h,x,y]

import matplotlib.pyplot as plt
def R_K(k,l,x,y,alf):
    x_0 = x
    r_arr=[]
    r_c=0.
    t_arr=[0]
    X_arr=[x]
    Y_arr=[y]
    t = 0
    h = 0.0001
    flg_plus = 0
    flg_y = 0
    flg_brk = 0
    while(t<alf):#альф тут пережиток прошлого, можно взять чтото большое, все равно остановимся раньше

        calck_K_L(k,l,x,y,h)
        r = calck_r(k)
        h_new = horisontal_chois_h(r,x,y,h)
        
        if(x<0): # что бы знать когда остановиться
            flg_plus = 0
        else:
            flg_plus = 1
        
        while(h_new<h):#если мы выбрали слишком плохой первый шаг
            h = h_new
            calck_K_L(k,l,x,y,h)
            r = calck_r(k)
            h_new = horisontal_chois_h(r,x,y,h)
            
        
        y_last = y
        x_last = x
        x = x +(1/6)*(k[0]+2*k[2]+k[3])
        y = y +(1/6)*(l[0]+2*l[2]+l[3])
        h = h_new
        if(y<0. and y_last>0.):# при таких y мы останавливаемся
            flg_y = 1
            print("момент когда начинаем искать последний шаг t,x =",t,x)
            print("y=",y,"предпоследний y",y_last)
        else:
            flg_y = 0
            
        if(flg_y==1 and flg_plus==1):#ищем момент остановки
            [h,x,y]=chois_Last_h(h,x_last,y_last,x,y)
            flg_brk = 1
            print("Последний (x,y) =",x,y)
        t+=h
        r_c+=r
        r_arr.append(r)
        X_arr.append(x)
        Y_arr.append(y)
        t_arr.append(t)
        #print("t=",t,"x=",x,"y=",y)
        if ( flg_brk == 1):
            break
        

    plt.plot(X_arr,Y_arr)
    plt.show()
   # plt.plot(t_arr,X_arr)
    #plt.show()
    #plt.plot(t_arr,Y_arr)
    #plt.show()
    print("что-то типо ошибки",r_c)
    return x-x_0

k = [0.,0.,0.,0.,0.,0.]
l = [0. for i in range(6)]
alf = 40
t=0.0004
x_0=0.001
y_0=0.
x=x_0
y=y_0

dx=R_K(k,l,x,y,alf)
print("Разница между начальным и конечным иксом:",dx)
