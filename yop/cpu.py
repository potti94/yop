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


def print_line(line,i,max_dashes,nodes,up_window,var,fix,n,page):
	mem_perc=round(float((var/fix)*100),2)
	nb_dashes=int(((var)/fix)*max_dashes)
	dashes="|"* nb_dashes
	spaces=" "* int(max_dashes-nb_dashes)
	if n==0:		
		line="%4s [%1s]:[%s%s]%5s%%" % (i,(nodes[i].node_state[0])[3], dashes, spaces,mem_perc)
	else:
		cover=" "
		line="%4s [%1s]:[%s%s]%5s%%" % (cover,(nodes[i].node_state[0])[3], dashes, spaces,mem_perc)
		
	mvwaddstr(up_window,((i-page*20)*2+n)%10,((i-page*20)//5)*len(line)+1, line,A_BOLD)

def print_total(middel_window,total_cap,total_used,choice):
	perc=round(float((total_used/total_cap)*100),2)
	nb_dashes=int(((total_used)/total_cap)*100)
	dashes="|"*nb_dashes
	spaces=" "* int(60-nb_dashes)
	if choice ==0:
		line="MEM: [%s%s] %5s%%" % (dashes, spaces,perc)
		mvwaddstr(middel_window,0, 0, line,A_BOLD)
	else:
		line="CPU: [%s%s] %5s%%" % (dashes, spaces,perc)
		mvwaddstr(middel_window,1, 0, line,A_BOLD)
				






def header(nb_nodes,nodes,up_window,middel_window,page):
	n=0
	max_dashes=18
	i=0	
	j=1
	k=0
	choice=0
	start=0
	finish=20
	global nb_pages
	
	nb_pages=nb_nodes//20
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
			
	start=page*20
	finish=page*20+20
	i=start
	f=finish
	while i<f and i<nb_nodes:
		line=""
		print_line(line,i,max_dashes,nodes,up_window,nodes[i].used[0],nodes[i].capability[0],n,page)
		j+=nodes[i].capability[0]
		k+=nodes[i].used[0]
		i+=1
	i=start
	n=1		
	while i<f and i<nb_nodes:
		line=""
		print_line(line,i,max_dashes,nodes,up_window,nodes[i].used[1],nodes[i].capability[1],n,page)
		j+=nodes[i].capability[1]
		k+=nodes[i].used[1]
		i+=1	
	total_cap=j-1
	total_used=k		
	total_cap=j
	total_used=k	
	
def footer(down_window,y):
	init_pair(1,COLOR_WHITE,COLOR_BLUE)
	long=""
	for line in {("h :","HELP "),("DOWN :","CHANGE NODES "),("UP :","CHANGE NODES "),("n :","NODES "),("q :","QUIT")}:
		mvwaddstr(down_window,y-13,len(long)+1, line[0],A_BOLD)
		long=long+line[0]
		mvwaddstr(down_window,y-13,len(long)+1, line[1],color_pair(1)+A_REVERSE+A_BOLD)
		long=long+line[1]
		
def limits(down_window,decal,y):
	i=1
	init_pair(3,COLOR_WHITE,COLOR_BLUE)
	while i<17:
		mvwaddstr(down_window,0,i*int(decal)-1,"|",color_pair(3))
		j=1
		while j<y-13:
			mvwaddstr(down_window,j,i*int(decal)-1,"|")
			j+=1
		i+=1	
	

def corp(down_window,nodes,nb_nodes,page,x,y):
	decal=round(x/17)
	i=j=0
	init_pair(2,COLOR_BLACK,COLOR_BLUE)
	long=""
	for line in {"Node","User","Queue","S","ID","UMEM","RMEM","NMEM","UC","RC","NC","UCO","RCO","T","P","Time+"}:
		long+=line+" "*int((decal-len(line)))
	long+="Name"+" "*int(x-len(long)-4)
	mvwaddstr(down_window,0,0,long,color_pair(2)+A_BLINK)
	limits(down_window,decal,y)
	nb_pages=nb_nodes//20
	if page >nb_pages:
		page=nb_pages
			
	start=page*20
	finish=page*20+20
	i=start
	f=finish
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%20+1, j*int(decal), nodes[i].user[0], A_BOLD)
		i+=1
	j+=1
	i=start
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%20+1, j*int(decal), nodes[i].queue[0], A_BOLD)
		i+=1
	i=start	
	j+=1
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%20+1, j*int(decal), (nodes[i].node_state[0])[3], A_BOLD)
		i+=1
	j+=1
	i=start	
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%20+1, j*int(decal),i, A_BOLD)
		i+=1
	j+=1
	i=start	
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%20+1, j*int(decal), nodes[i].mem[0], A_BOLD)
		mvwaddstr(down_window, i%20+1, (j+1)*int(decal), nodes[i].mem[1], A_BOLD)
		mvwaddstr(down_window, i%20+1, (j+2)*int(decal), nodes[i].mem[2], A_BOLD)
		i+=1
	j+=3
	i=start	
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%20+1, j*int(decal), nodes[i].c[0], A_BOLD)
		mvwaddstr(down_window, i%20+1, (j+1)*int(decal), nodes[i].c[1], A_BOLD)
		mvwaddstr(down_window, i%20+1, (j+2)*int(decal), nodes[i].c[2], A_BOLD)
		i+=1
	j+=3
	i=start	
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%20+1, j*int(decal), nodes[i].co[0], A_BOLD)
		mvwaddstr(down_window, i%20+1, (j+1)*int(decal), nodes[i].co[1], A_BOLD)
		i+=1
	j+=2
	i=start	
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%20+1, j*int(decal), nodes[i].t[0], A_BOLD)
		i+=1
	j+=1
	i=start	
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%20+1, j*int(decal), str(nodes[i].p[0])+"%", A_BOLD)
		i+=1
	j+=1
	i=start	
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%20+1, j*int(decal), nodes[i].time[0], A_BOLD)
		i+=1
	j+=1
	i=start	
	while i<f and i<nb_nodes:
		mvwaddstr(down_window, i%20+1, j*int(decal), nodes[i].name[0], A_BOLD)
		i+=1
	j+=1
	





		

class display(Thread):
    def __init__(self,key):
        Thread.__init__(self)
    
    def run(self):
        stdscr=initscr()
        start_color()
        keypad(stdscr,True)
        noecho()
        curs_set(False)
        while key!=ord("q"):
            #nodes=get_cluster_nodes()
            #nb_nodes=randint(0,365)
            x=stdscr.getmaxyx()[1]
            y=stdscr.getmaxyx()[0]
            nb_nodes=210
            nodes=set_nodes(nb_nodes)
        #     ================== window decomposition ===========================
            up_window=newwin(10,x, 0, 0)
            up_panel=new_panel(up_window)
            up_pad=newpad(10,x)
            middel_window=newwin(2,x,10,0)
            middel_panel=new_panel(middel_window)
            down_window=newwin(y-12,x, 12, 0)
            down_panel=new_panel(down_window)
        #   ===================================================================               
            header(nb_nodes,nodes,up_window,middel_window,page)
            footer(down_window,y)
            corp(down_window,nodes,nb_nodes,page,x,y)
            update_panels()
            doupdate()
            time.sleep(1)			

def main():
	global temp
	global key
	global page
	page=0
	temp=key=109
	
	thread1=display(temp)
	thread1.start()
	while key!=ord("q"):
		temp=109
		key=getch()
		if key==ord("h") or key==KEY_UP or key==KEY_DOWN or key==ord("n"):
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
	