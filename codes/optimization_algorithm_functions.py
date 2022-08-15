import numpy as np
   
def fp(N, p):
    kp=p[N]
    sp=p[-2]
    sm=p[-1]
    c1=p[-3]
    c2=p[-4]
    c3=p[-5]    
    a0m=1.-c1
    a1m=c1    
    a0p=(1.-c1)*(1.-c2)
    a1p=c1+c2-2.*c1*c2
    a2p=c1*c2      
    a0q=(1.-c1)*(1.-c2)*(1.-c3)
    a1q=c1*(1.-c2)*(1.-c3)+c2*(1.-c1)*(1.-c3)+c3*(1.-c1)*(1.-c2)
    a2q=c1*c2*(1.-c3)+c1*c3*(1.-c2)+c2*c3*(1.-c1)
    a3q=c1*c2*c3                    
    ka=kp+N*sm
    kb=kp+N*sm+sp-sm
    kc=kp+N*sm+2.*(sp-sm)
    kd=kp+N*sm+3.*(sp-sm)    
    result1=kp*(a0m/ka+a1m/kb)
    result2=kp*(a0p/ka+a1p/kb+a2p/kc)
    result3=kp*(a0q/ka+a1q/kb+a2q/kc+a3q/kd)    
    result= np.where(N>0, np.where(N<2, result1, np.where(N<3, result2, result3)), 1.)
    return result


def tt(N, p, maxN=9):
    kp=p[N]
    sp=p[-2]
    sm=p[-1]   
    c1=p[-3]
    c2=p[-4]
    c3=p[-5]    
    a0m=1.-c1
    a1m=c1    
    a0p=(1.-c1)*(1.-c2)
    a1p=c1+c2-2.*c1*c2
    a2p=c1*c2      
    a0q=(1.-c1)*(1.-c2)*(1.-c3)
    a1q=c1*(1.-c2)*(1.-c3)+c2*(1.-c1)*(1.-c3)+c3*(1.-c1)*(1.-c2)
    a2q=c1*c2*(1.-c3)+c1*c3*(1.-c2)+c2*c3*(1.-c1)
    a3q=c1*c2*c3                    
    ka=kp+N*sm
    kb=kp+N*sm+sp-sm
    kc=kp+N*sm+2.*(sp-sm)
    kd=kp+N*sm+3.*(sp-sm)
    result1=a0m/ka+a1m/kb
    result2=a0p/ka+a1p/kb+a2p/kc
    result3=a0q/ka+a1q/kb+a2q/kc+a3q/kd
    return np.where(N<2, result1, np.where(N<3, result2, result3))

    
def pref(N, p):           
    kp=p[N]
    sp=p[-2]
    sm=p[-1]    
    c1=p[-3]
    c2=p[-4]
    c3=p[-5]    
    a0m=1.-c1
    a1m=c1    
    a0p=(1.-c1)*(1.-c2)
    a1p=c1+c2-2.*c1*c2
    a2p=c1*c2      
    a0q=(1.-c1)*(1.-c2)*(1.-c3)
    a1q=c1*(1.-c2)*(1.-c3)+c2*(1.-c1)*(1.-c3)+c3*(1.-c1)*(1.-c2)
    a2q=c1*c2*(1.-c3)+c1*c3*(1.-c2)+c2*c3*(1.-c1)
    a3q=c1*c2*c3                    
    ka=kp+N*sm
    kb=kp+N*sm+sp-sm
    kc=kp+N*sm+2.*(sp-sm)
    kd=kp+N*sm+3.*(sp-sm)
    result1=2*(a0m/ka**2.+a1m/kb**2.)/(a0m/ka+a1m/kb)**2.-1.
    result2=2*(a0p/ka**2.+a1p/kb**2.+a2p/kc**2.)/(a0p/ka+a1p/kb+a2p/kc)**2.-1.
    result3=2*(a0q/ka**2.+a1q/kb**2.+a2q/kc**2.+a3q/kd**2.)/(a0q/ka+a1q/kb+a2q/kc+a3q/kd)**2.-1.    
    return np.where(N<2, result1, np.where(N<3, result2, result3))

def gradient(f, x, dx):
    grad=np.zeros(len(x))
    for i in range(len(grad)):
        dp=np.zeros(len(x))
        dp[i]=dx[i]
        grad[i]=( f(x+dp)-f(x) )/dp[i]
    return grad
    
 
def lossN(Exp, Th, A, B):
    return A*(Exp[0]-Th[0])**2.+B*(Exp[1]-Th[1])**2.

def deriv(f, dx, x0):
    return (f(x0+dx)-f(x0))/dx
    
def Km(t, N, p):
    kp=p[N]
    return -deriv(np.log(S(t, N, p)))-kp    



