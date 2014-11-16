from __future__ import division
from math import log, sqrt, exp
from scipy.stats import norm
 
#Default values used for testing
s1 = 200; s2=250
mu1 = 0.10; sigma1= 0.3
mu2=0.10; sigma2= 0.2
rate=0.10; rho=0.75
t=1
 
sigma = lambda sig1=sigma1, sig2=sigma2, corr=rho: sqrt(sig1**2+sig2**2 -2*corr*sig1*sig2)
 
m_d1 = lambda stock1=s1, stock2=s2, sig1=sigma1, sig2=sigma2, years=t, corr=rho: (log(stock1/stock2)+1/2*sigma()**2*years)/(sigma()*sqrt(years))
 
m_d2 = lambda stock1=s1, stock2=s2, sig1=sigma1, sig2=sigma2, years=t, corr=rho: m_d1() -sigma()*sqrt(years)
     
m_delta1 = lambda stock1=s1, stock2=s2, sig1=sigma1, sig2=sigma2, years=t, corr=rho: norm.cdf(m_d1())
 
m_delta2 = lambda stock1=s1, stock2=s2, sig1=sigma1, sig2=sigma2, years=t, corr=rho: -norm.cdf(m_d2())
 
m_gamma11 = lambda stock1=s1, stock2=s2, sig1=sigma1, sig2=sigma2, years=t, corr=rho: norm.pdf(m_d1())/(stock1*sigma()*sqrt(years))
 
m_gamma22 = lambda stock1=s1, stock2=s2, sig1=sigma1, sig2=sigma2, years=t, corr=rho: norm.pdf(m_d2())/(stock2*sigma()*sqrt(years))
     
m_gamma12 = lambda stock1=s1, stock2=s2, sig1=sigma1, sig2=sigma2, years=t, corr=rho:-norm.pdf(m_d1())/(stock2*sigma()*sqrt(years))
         
m_theta = lambda stock1=s1, stock2=s2, sig1=sigma1, sig2=sigma2, years=t, corr=rho: -stock1*sigma()*norm.pdf(m_d1())/(2*sqrt(years))
         
m_vega1 = lambda stock1=s1, stock2=s2, sig1=sigma1, sig2=sigma2, years=t, corr=rho: stock1*sqrt(t)*norm.pdf(m_d1())*((sig1-(corr*sig2))/sigma())
      
m_vega2 = lambda stock1=s1, stock2=s2, sig1=sigma1, sig2=sigma2, years=t, corr=rho: stock1*sqrt(t)*norm.pdf(m_d1())*((sig2-(corr*sig1))/sigma()) 
 
m_correlation = lambda stock1=s1, stock2=s2, sig1=sigma1, sig2=sigma2, years=t, corr=rho: -stock1*sqrt(t)*norm.pdf(m_d1())*((sig1*sig2)/sigma()) 
         
m_margrabe = lambda stock1=s1, stock2=s2, sig1=sigma1, sig2=sigma2, years=t, corr=rho: stock1*norm.cdf(m_d1())-stock2*norm.cdf(m_d2())
 
def main():  
    print "Margrabe = "+str(m_margrabe()) + "\n"
    print "THE GREEKS \n"
    print "Delta Asset 1 = "+str(m_delta1())
    print "Delta Stock 2 = "+str(m_delta2()) +"\n"
    print "Gamma Asset 11 = "+str(m_gamma11())
    print "Gamma Stock 12 = "+str(m_gamma12())
    print "Gamma Stock 22 = "+str(m_gamma22()) + "\n"
    print "Theta = "+str(m_theta()) +"\n"
    print "Vega sigma 1 = "+str(m_vega1())
    print "Vega sigma 2 = "+str(m_vega2()) + "\n"
    print "Correlation = "+str(m_correlation()) + "\n"
    print "sigma"   
    print sigma()
    print "sig1 : " + str(sigma1) + " sig2: " +str(sigma2)    
    print "d1: " + str(m_d1())
    print m_d2()
    print str(norm.cdf(-0.647510235324)) + ' , ' + str(norm.cdf(-0.930352947799))
     
 
if __name__=='__main__':
    main()