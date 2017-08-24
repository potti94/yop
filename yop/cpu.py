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


def print_line(line,i,max_dashes,nodes,up_window,var,fix,n):
	mem_perc=round(float((var/fix)*100),2)
	nb_dashes=int(((var)/fix)*max_dashes)
	dashes="|"* nb_dashes
	spaces=" "* int(max_dashes-nb_dashes)
	line="%2s [%1s]:[%s%s]%5s%%||" % (i,(nodes[i].node_state[2])[3], dashes, spaces,mem_perc)
	mvwaddstr(up_window,(i+n)%10, (i//5)*len(line)+1, line,A_BOLD)


def print_total(middel_window,total_cap,total_used,choice):
	perc=round(float((total_used/total_cap)*100),2)
	nb_dashes=int(((total_used)/total_cap)*100)
	dashes="|"*nb_dashes
	spaces=" "* int(100-nb_dashes)
	if choice =="mem":
		line="MEM: [%s%s] %5s%%" % (dashes, spaces,perc)
		mvwaddstr(middel_window,0, 0, line,A_BOLD)
	else:
		line="CPU: [%s%s] %5s%%" % (dashes, spaces,perc)
		mvwaddstr(middel_window,1, 0, line,A_BOLD)
			
	


def controle_display(page,nb_pages,temp):
	if page!=0 and page!=nb_pages:
		if temp==KEY_UP:
			page-=1
			return[page*4,page*4+4]
		if temp==KEY_DOWN:
			page+=1
			return[page*4,page*4+4]
	if page==0:
		if temp==KEY_DOWN:
			page+=1
			return[page*4,page*4+4]
	if page==nb_pages:
		if temp==KEY_UP:
			page-=1
			return[page*4,page*4+4]
				
						
			









def header(nb_nodes,nodes,up_window,middel_window,temp):
	n=0
	max_dashes=18
	i=0	
	j=1
	k=0
	page=0
	nb_pages=nb_nodes//4
	if temp==ord("m"):
		#============ memory==================
		while i<nb_nodes:
			j+=nodes[i].capability[0]
			k+=nodes[i].used[0]
		total_cap=j-1
		total_used=k
		choice=="mem"	
		print_total(middel_window,total_cap,total_used,choice)	
		
		#======================== cpu =============
		j=1
		k=0
		while i<nb_nodes:
			j+=nodes[i].capability[0]
			k+=nodes[i].used[0]
		total_cap=j-1
		total_used=k	
		choice="cpu"
		print_total(middel_window,total_cap,total_used,choice)
#==============================================================================		
			
		start,finish=control_display(page,nb_pages,temp)
		
		i=start
		while i<finish:
			line=""
			print_line(line,i,max_dashes,nodes,up_window,nodes[i].used[0],nodes[i].capability[0],n)
			j+=nodes[i].capability[0]
			k+=nodes[i].used[0]
			i+=1
			n+=1
		i=start
		n=1		
		while i<finish:
			line=""
			print_line(line,i,max_dashes,nodes,up_window,nodes[i].used[1],nodes[i].capability[1],n)
			j+=nodes[i].capability[1]
			k+=nodes[i].used[1]
			i+=1
			n+=1
			
		total_cap=j-1
		total_used=k		
	 	#print_total(middel_window,total_cap,total_used)	
		total_cap=j
		total_used=k		
	
def footer(down_window):
	init_pair(1,COLOR_WHITE,COLOR_BLUE)
	long=""
	for line in {("M :","MEMORY "),("V :","CORES "),("S :","STATES "),("I :","ID "),("Q :","QUIT")}:
		mvwaddstr(down_window,29,len(long)+1, line[0],A_BOLD)
		long=long+line[0]
		mvwaddstr(down_window,29,len(long)+1, line[1],color_pair(1)+A_REVERSE+A_BOLD)
		long=long+line[1]
		
		

class display(Thread):
    def __init__(self,key):
        Thread.__init__(self)
    
    def run(self):
        stdscr=initscr()
        start_color()
        keypad(stdscr,True)
        noecho()
        curs_set(False)   
       
        x=stdscr.getmaxyx()[1]
        y=stdscr.getmaxyx()[0]
    
        while key!=ord("q"):
            #nodes=get_cluster_nodes()
            #nb_nodes=randint(0,36)
            nb_nodes=20
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
            header(nb_nodes,nodes,up_window,middel_window,temp)
            footer(down_window)
            update_panels()
            doupdate()
        
            time.sleep(2)			

def main():
	global key
	global temp
	key=temp=109
	thread1=display(key)
	thread1.start()
	while key!=ord("q"):
		key=getch()
		if key==ord("m") or key==KEY_UP or key==KEY_DOWN or key==ord("v"):
			temp=key
	
	thread1.join()		
	endwin()
	quit()
	




if __name__=="__main__":
	main()
	