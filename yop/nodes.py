from random import *
def randomize(a):
	a.used[0]=randint(0,a.capability[0])
	a.used[1]=randint(0,a.capability[1])
	return a.used	

class Nodes:
	def __init__(self):
		self.node_id=[150208452197,8042]                                #get_node_id(self)      #host/port
		self.http_rack=["dn04.hadoop.suty-ops.com","/default"]       #get_http_rack(self)    #returns a list of http addr and rack name 
		self.used=[1,1]                                                   #get_used(self)		 #used memory/ used cores	
		self.capability=[randint(1,8000),randint(1,10)]                          #get_capability(self)	 #MEMORY CAPABILITY/ number of cores	
		self.node_state=["NS_RUNNING"]                                   #get_node_state(self)   #health report/ last health report time/ STATE
		self.user=["Yassine.mcha7em"]												#NS: NS_RUNNING
		self.queue=[randint(1,10)]
		self.mem=[randint(1,100000),randint(1,100000),randint(1,100000)]	        #mem=[UMEM,RMEM,NMEM]
		self.c=[randint(1,10),randint(1,10),randint(1,10)]                           # c=[UC,RC,NC]
		self.co=[randint(1,10),randint(1,10)]                                          # co=[UCO,RCO]
		self.t=["MAPREDUCE"]
		self.p=[randint(1,100)]
		self.time=["8:19:32"]
		self.name=["yoping.jar"]
		
							