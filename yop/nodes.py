from random import *
def randomize(a):
	a.used[0]=randint(0,a.capability[0])
	a.used[1]=randint(0,a.capability[1])
	return a.used	

class Nodes:
	def __init__(self):
		self.node_id=[1502084,0000]                    #get_node_id(self)      #host/port
		self.http_rack=["dn04.hadoop.suty-ops.com:8042","/default"]       #get_http_rack(self)    #returns a list of http addr and rack name 
		self.used=[1,1]                                                   #get_used(self)		 #used memory/ used cores	
		self.capability=[randint(1,8000),randint(1,10)]                   #get_capability(self)	 #MEMORY CAPABILITY/ number of cores	
		self.node_state=["NS_RUNNING"]                   #get_node_state(self)   #health report/ last health report time/ STATE
		self.user=["Yassine.Azzouz"]												#NS: NS_RUNNING
		self.queue=[1]
		self.mem=[9600,12000,17000]	                             #mem=[UMEM,RMEM,NMEM]
		self.c=[5,7,2]                                          # c=[UC,RC,NC]
		self.co=[7,10]                                          # co=[UCO,RCO]
		self.t=["MAPREDUCE"]
		self.p=[42]
		self.time=["8:19:32"]
		self.name=["yoping.py"]
		
							