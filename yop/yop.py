#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from unicurses import *
from nodes import *
from random import *
import time
from threading import Thread



def set_nodes(nb_nodes):
	i=0
	nodes=[]
	while i<nb_nodes:
		obj_node=Nodes()
		nodes.append(obj_node)
		randomize(obj_node)
		i+=1
	return nodes	


def print_line(line,i,max_dashes,nodes,up_window,var,fix,n,page,x):
	mem_perc=round(float((var/fix)*100),2)
	nb_dashes=int(((var)/fix)*max_dashes)
	dashes="|"* nb_dashes
	spaces=" "* int(max_dashes-nb_dashes)
	if n==0:		
		line="%4s [%1s]:[%s%s]%5s%%" % (i,(nodes[i].node_state[0])[3], dashes, spaces,mem_perc)
	else:
		cover=" "
		line="%4s [%1s]:[%s%s]%5s%%" % (cover,(nodes[i].node_state[0])[3], dashes, spaces,mem_perc)
	k=5*(x//35)
	mvwaddstr(up_window,((i-page*k)*2+n)%10,((i-page*k)//5)*len(line), line,A_BOLD)

def print_total(middel_window,total_cap,total_used,choice):
	perc=round(float((total_used/total_cap)*100),2)
	init_pair(4,COLOR_WHITE, COLOR_GREEN)
	nb_dashes=int(((total_used)/total_cap)*100)
	dashes="|"*nb_dashes
	spaces=" "* int(60-nb_dashes)
	if choice ==0:
		line="MEM: [%s%s] %5s%%" % (dashes, spaces,perc)
		mvwaddstr(middel_window,0, 0, line,A_BOLD+color_pair(4))
	else:
		line="CPU: [%s%s] %5s%%" % (dashes, spaces,perc)
		mvwaddstr(middel_window,1, 0, line,A_BOLD+color_pair(4))
				






def header(nb_nodes,nodes,up_window,middel_window,page,x):
	n=0
	max_dashes=18
	i=0	
	j=1
	k=0
	choice=0
	start=0
	finish=20
	global nb_pages
	
	nb_pages=(nb_nodes//(5*(x//35)))-1
	#============ memory ==================
	while i<nb_nodes:
		j+=nodes[i].capability[0]
		k+=nodes[i].used[0]
		i+=1
	total_cap=j-1
	total_used=k
	print_total(middel_window,total_cap,total_used,choice)	
	
	#======================== cpu =============
	j=1
	k=0
	i=0
	while i<nb_nodes:
		j+=nodes[i].capability[0]
		k+=nodes[i].used[0]
		i+=1
	total_cap=j-1
	total_used=k	
	choice=1
	print_total(middel_window,total_cap,total_used,choice)
#==============================================================================		
	if page >nb_pages:
		page=nb_pages
			
	mvwaddstr(middel_window,0,100,nb_pages)		
	start=page*(5*(x//35))
	finish=page*(5*(x//35))+(5*(x//35))
	i=start
	f=finish
	
	if page==nb_pages:      #MAGIC FORMULA OF LAST PAGE DISPLAY
		max_dashes=(x-17*(1+(nb_nodes-page*(5*(x//35)))//5))//((((nb_nodes-1)-i)//5)+1)  
		
			
	while i<f and i<nb_nodes:
		line=""
		print_line(line,i,max_dashes,nodes,up_window,nodes[i].used[0],nodes[i].capability[0],n,page,x)
		j+=nodes[i].capability[0]
		k+=nodes[i].used[0]
		i+=1
	i=start
	n=1		
	while i<f and i<nb_nodes:
		line=""
		print_line(line,i,max_dashes,nodes,up_window,nodes[i].used[1],nodes[i].capability[1],n,page,x)
		j+=nodes[i].capability[1]
		k+=nodes[i].used[1]
		i+=1	
	total_cap=j-1
	total_used=k		
	total_cap=j
	total_used=k	
	
def footer(down_window,y):
	init_pair(1,COLOR_BLUE,COLOR_BLACK)
	long=""
	for line in {("h :","HELP "),("DOWN :","CHANGE NODES "),("UP :","CHANGE NODES "),("n :","NODES "),("q :","QUIT")}:
		mvwaddstr(down_window,y-14,len(long)+1, line[0],A_BOLD)
		long=long+line[0]
		mvwaddstr(down_window,y-14,len(long)+1, line[1],color_pair(1)+A_BOLD+A_REVERSE)
		long=long+line[1]
		
def limits(down_window,bordure,y,x):
	i=0
	decal=0
	init_pair(3,COLOR_BLUE,COLOR_WHITE)
	while i<16:
		mvwaddstr(down_window,0,decal+bordure[i],"|",color_pair(3)+A_BOLD+A_REVERSE)
		j=1
		while j<(5*(x//35))+1:
			mvwaddstr(down_window,j,decal+bordure[i],"|",A_BOLD)
			j+=1
		decal+=bordure[i]+1
		i+=1
			
	

def corp(down_window,nodes,nb_nodes,page,x,y):
	decal=0
	i=j=0
	bordure=[19,17,5,2,4,6,6,6,3,3,3,3,3,11,4,8,18]
	init_pair(2,COLOR_BLUE,COLOR_BLACK)
	long=""
	for line in ("ID","User","Queue","S","Node","UMEM","RMEM","NMEM","UC","RC","NC","UCO","RCO","T","P","Time+"):
		long+=line+" "*int((bordure[i]-len(line)+1))
		i+=1
	long+="Name"+" "*int(x-len(long)-4)
	mvwaddstr(down_window,0,0,long,color_pair(2)+A_REVERSE+A_BOLD)
	limits(down_window,bordure,y,x)
	nb_pages=(nb_nodes//(5*(x//35)))-1
	if page >nb_pages:
		page=nb_pages
			
	start=page*(5*(x//35))
	finish=page*(5*(x//35))+(5*(x//35))
	i=start
	f=finish
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%(5*(x//35))+1, 0, str(nodes[i].node_id[1])+"/"+str(nodes[i].node_id[0]), A_BOLD)
		i+=1

	i=start
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%(5*(x//35))+1, decal+bordure[j]+1, nodes[i].user[0], A_BOLD)
		i+=1
	decal+=bordure[j]+2
	j+=1
	i=start
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%(5*(x//35))+1, decal+bordure[j], nodes[i].queue[0], A_BOLD)
		i+=1
	decal+=bordure[j]+1	
	i=start	
	j+=1
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%(5*(x//35))+1, decal+bordure[j], (nodes[i].node_state[0])[3], A_BOLD)
		i+=1
	decal+=bordure[j]+1	
	j+=1
	i=start	
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%(5*(x//35))+1, decal+bordure[j],i, A_BOLD)
		i+=1
	decal+=bordure[j]+1	
	j+=1
	i=start	
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%(5*(x//35))+1, decal+bordure[j], nodes[i].mem[0], A_BOLD)
		mvwaddstr(down_window, i%(5*(x//35))+1, decal+bordure[j+1]+bordure[j]+1, nodes[i].mem[1], A_BOLD)
		mvwaddstr(down_window, i%(5*(x//35))+1, decal+bordure[j+2]+bordure[j+1]+bordure[j]+2, nodes[i].mem[2], A_BOLD)
		i+=1
	decal+=bordure[j]+3+bordure[j+2]+bordure[j+1]
	j+=3
	i=start	
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%(5*(x//35))+1, decal+bordure[j], nodes[i].c[0], A_BOLD)
		mvwaddstr(down_window, i%(5*(x//35))+1, decal+bordure[j+1]+bordure[j]+1, nodes[i].c[1], A_BOLD)
		mvwaddstr(down_window, i%(5*(x//35))+1, decal+bordure[j+2]+bordure[j+1]+bordure[j]+2, nodes[i].c[2], A_BOLD)
		i+=1
	decal+=bordure[j]+3+bordure[j+2]+bordure[j+1]
	j+=3
	i=start	
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%(5*(x//35))+1, decal+bordure[j], nodes[i].co[0], A_BOLD)
		mvwaddstr(down_window, i%(5*(x//35))+1, decal+bordure[j+1]+bordure[j]+1, nodes[i].co[1], A_BOLD)
		i+=1
	decal+=bordure[j]+bordure[j+1]+2	
	j+=2
	i=start	
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%(5*(x//35))+1, decal+bordure[j], nodes[i].t[0], A_BOLD)
		i+=1
	decal+=bordure[j]+1	
	j+=1
	i=start	
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%(5*(x//35))+1, decal+bordure[j], str(nodes[i].p[0])+"%", A_BOLD)
		i+=1
	decal+=bordure[j]+1	
	j+=1
	i=start	
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%(5*(x//35))+1, decal+bordure[j], nodes[i].time[0], A_BOLD)
		i+=1
	decal+=bordure[j]+1	
	j+=1
	i=start	
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%(5*(x//35))+1, decal+bordure[j], nodes[i].name[0], A_BOLD)
		i+=1
	j+=1
	mvwaddstr(down_window,y-15, 10,x//35)	




def N_limits(down_window,bordure,y,x):
	i=0
	decal=0
	while i<3:
		mvwaddstr(down_window,0,decal+bordure[i],"|",color_pair(3)+A_BOLD+A_REVERSE)
		j=1
		while j<(5*(x//35))+1:
			mvwaddstr(down_window,j,decal+bordure[i],"|",A_BOLD)
			j+=1
		decal+=bordure[i]+1
		i+=1






def N_corp(down_window,nodes,nb_nodes,page,x,y):
	decal=0
	i=j=0
	bordure=[4,19,27,25]
	init_pair(2,COLOR_BLUE,COLOR_BLACK)
	long=""
	for line in ("Node","ID","IP"):
		long+=line+" "*int((bordure[i]-len(line)+1))
		i+=1
	long+="Rack"+" "*int(x-len(long)-4)
	mvwaddstr(down_window,0,0,long,color_pair(2)+A_REVERSE+A_BOLD)
	N_limits(down_window,bordure,y,x)
	nb_pages=(nb_nodes//(5*(x//35)))-1
	if page >nb_pages:
		page=nb_pages
			
	start=page*(5*(x//35))
	finish=page*(5*(x//35))+(5*(x//35))
	i=start
	f=finish
	
	
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%(5*(x//35))+1, 0, i, A_BOLD)
		i+=1
	i=start	
	
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%(5*(x//35))+1, decal+bordure[j]+1, str(nodes[i].node_id[1])+"/"+str(nodes[i].node_id[0]), A_BOLD)
		i+=1
	decal+=bordure[j]+2
	j+=1	
	i=start
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%(5*(x//35))+1, decal+bordure[j]+1, nodes[i].http_rack[0], A_BOLD)
		i+=1
	decal+=bordure[j]+1
	j+=1
	i=start
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%(5*(x//35))+1, decal+bordure[j], nodes[i].http_rack[1], A_BOLD)
		i+=1	
	
	



def N_footer(down_window,y):
	mvwaddstr(down_window,y-14,0,"Press ESC To Return",color_pair(1)+A_BOLD+A_REVERSE)
	

	
class N_Nodes(Thread):
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
    	stdscr=initscr()
    	start_color()
    	keypad(stdscr,True)
    	noecho()
    	curs_set(False)
    	while temp!=27:
    		nodes=set_nodes(nb_nodes)
    		x=stdscr.getmaxyx()[1]
    		y=stdscr.getmaxyx()[0]
    		up_window=newwin(11,x, 0, 0)
    		up_panel=new_panel(up_window)
    		middel_window=newwin(2,x,11,0)
    		middel_panel=new_panel(middel_window)
    		down_window=newwin(y-13,x, 13, 0)
    		down_panel=new_panel(down_window)
    		header(nb_nodes,nodes,up_window,middel_window,page,x)
    		down_window=newwin(y-13,x, 13, 0)
    		down_panel=new_panel(down_window)
    		N_footer(down_window,y)
    		N_corp(down_window,nodes,nb_nodes,page,x,y)
    		update_panels()
    		doupdate()
    		time.sleep(1)
    		
	
    	


		

class display(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        stdscr=initscr()
        start_color()
        keypad(stdscr,True)
        noecho()
        curs_set(False)
        while key!=ord("q") and key!=ord("Q"):
            #nodes=get_cluster_nodes()
            #nb_nodes=randint(0,365)
            x=stdscr.getmaxyx()[1]
            y=stdscr.getmaxyx()[0]
            global temp
            global nb_nodes
            nb_nodes=20
            nodes=set_nodes(nb_nodes)
        #     ================== window decomposition ===========================
            up_window=newwin(10,x, 0, 0)
            up_panel=new_panel(up_window)
            middel_window=newwin(2,x,11,0)
            middel_panel=new_panel(middel_window)
            down_window=newwin(y-13,x, 13, 0)
            down_panel=new_panel(down_window)
        #   ===================================================================               
            header(nb_nodes,nodes,up_window,middel_window,page,x)
            footer(down_window,y)
            corp(down_window,nodes,nb_nodes,page,x,y)
            thread2=N_Nodes()
            if temp==ord("n"):
            	thread2.start()
            	thread2.join()		
            update_panels()
            doupdate()
            time.sleep(1)			

def main():
	global temp
	global key
	global page
	page=0
	temp=key=109
	thread1=display()
	thread1.start()
	while key!=ord("q") and key!=ord("Q"):
		key=getch()
		if key==ord("h") or key==KEY_UP or key==KEY_DOWN or key==ord("n")or key==27or key==ord("s"):
			temp=key
			if temp==KEY_UP or temp==KEY_DOWN:
				if page!=0 and page!=nb_pages:
					if temp==KEY_UP:			
						page-=1
					if temp==KEY_DOWN:
						page+=1
				elif page==0:
					if temp==KEY_DOWN:
						page+=1
				elif page==nb_pages:
					if temp==KEY_UP:
						page-=1
		
			
	
	thread1.join()		
	endwin()
	quit()
	




if __name__=="__main__":
	main()
	