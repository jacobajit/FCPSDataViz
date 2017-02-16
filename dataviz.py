
from lxml import html
import requests
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

independent="Percentage Asian Students"
dependent="Average SAT Score"

#'tbody' needed to be removed from the xpath because the browser auto-generates it
#text() is self-explanatory
independentxpath='//*[@id="report_R51141047879770178"]/tbody/tr[3]/td[7]'.replace('/tbody','') +'/text()'
#last() can be used instead of an index, makes scraping slightly more reliable
dependentxpath='//*[@id="report_R88620341367212807"]/tr[last()]/td[8]'.replace('/tbody','') +'/text()'

independentdatacategoryid=13
dependentdatacategoryid=5

#automated a process to get array of school codes from html selection element
#originally used ints here, but leading zeros cause Python 2 to interpret as octals
schoolCodes=['140','410','250','120','500',"090",'180','270','400',"020",'160',"060","070","030",'220', "050",'390','420','320','100','200','150','240','130']

i=0
dependentList=[]
independentList=[]
print (dependent+" vs. "+independent)
while i<len(schoolCodes):

	pageurl="http://schoolprofiles.fcps.edu/schlprfl/f?p=108:"+str(dependentdatacategoryid)+ ":::NO::P0_CURRENT_SCHOOL_ID,P0_EDSL:"+schoolCodes[i]+",0"
	page = requests.get(pageurl)
	tree = html.fromstring(page.content)
	dependentVar=tree.xpath(dependentxpath)
	dependentList.append(float(dependentVar[0]))
	
	pageurl="http://schoolprofiles.fcps.edu/schlprfl/f?p=108:"+str(independentdatacategoryid)+ ":::NO::P0_CURRENT_SCHOOL_ID,P0_EDSL:"+schoolCodes[i]+",0"
	page = requests.get(pageurl)
	tree = html.fromstring(page.content)
	independentVar=tree.xpath(independentxpath) 
	independentList.append(float(independentVar[0].replace(',','')))
	
	print '{0} {1}'.format(independentVar, dependentVar)
	i+=1

print(dependentList)
print(independentList)

slope, intercept, r_value, p_value, std_err = stats.linregress(independentList,dependentList)
print(r_value)

m, b = np.polyfit(independentList, dependentList, 1)
x=np.array(independentList)
plt.plot(x, m*x + b, '-') #using a numpy array fixes graphing issue here
plt.scatter(independentList, dependentList)
plt.xlabel(independent)
plt.ylabel(dependent)
plt.annotate("R = "+str(r_value), xy=(0.05, 0.95), xycoords='axes fraction')
plt.show()

