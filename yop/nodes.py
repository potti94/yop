from random import *
def randomize(a):
	a.used[0]=randint(0,a.capability[0])
	a.used[1]=randint(0,a.capability[1])
	return a.used	

class Nodes:
	def __init__(self):
		self.node_id=["dn04.hadoop.suty-ops.com",0000]                    #get_node_id(self)      #host/port
		self.http_rack=["dn04.hadoop.suty-ops.com:8042","/default"]       #get_http_rack(self)    #returns a list of http addr and rack name 
		self.used=[1,1]                                                   #get_used(self)		 #used memory/ used cores	
		self.capability=[randint(1,8000),randint(1,10)]                   #get_capability(self)	 #MEMORY CAPABILITY/ number of cores	
		self.node_state=["",1502059470684,"NS_RUNNING"]                   #get_node_state(self)   #health report/ last health report time/ STATE
																												#NS: NS_RUNNING
		
							