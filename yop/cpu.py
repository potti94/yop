#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

from unicurses import *
from color import *
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


def print_line(line,i,max_dashes,nodes,up_window,var,fix):
	mem_perc=round(float((var/fix)*100),2)
	nb_dashes=int(((var)/fix)*max_dashes)
	dashes="|"* nb_dashes
	spaces=" "* int(max_dashes-nb_dashes)
	line=" NODE%2s [%s%s] %5s%%" % (i, dashes, spaces,mem_perc)
	mvwaddstr(up_window,i%9+1, (i//9)*len(line)+1, line,A_BOLD)


def print_total(up_window,total_cap,total_used):
	perc=round(float((total_used/total_cap)*100),2)
	nb_dashes=int(((total_used)/total_cap)*100)
	dashes="|"*nb_dashes
	spaces=" "* int(100-nb_dashes)
	line="TOTAL MEM: [%s%s] %5s%%" % (dashes, spaces,perc)
	mvwaddstr(up_window,10, 0, line,A_BOLD)
	



def header(nb_nodes,nodes,up_window,temp):
	if nb_nodes<=10:
		max_dashes=50
	elif 10<nb_nodes<=18:
		max_dashes=40
	elif 18<nb_nodes<=27:
		max_dashes=30
	else:
		max_dashes=18
	i=0	
	j=1
	k=0
	if temp==ord("m"):
		mvwaddstr(up_window,0, 20, "====== MEMORY ======", A_BOLD)
		while i<nb_nodes:
			line=""
			print_line(line,i,max_dashes,nodes,up_window,nodes[i].used[0],nodes[i].capability[0])
			j+=nodes[i].capability[0]
			k+=nodes[i].used[0]
			i+=1	
		total_cap=j
		total_used=k		
		print_total(up_window,total_cap,total_used)	
	elif temp==ord("v"):
		mvwaddstr(up_window,0, 20, "====== CORES ======", A_BOLD)		
		while i<nb_nodes:
			line=""
			print_line(line,i,max_dashes,nodes,up_window,nodes[i].used[1],nodes[i].capability[1])
			j+=nodes[i].capability[1]
			k+=nodes[i].used[1]
			i+=1
		total_cap=j-1
		total_used=k		
		print_total(up_window,total_cap,total_used)	
	elif temp==ord("s"):
		mvwaddstr(up_window,0, 20, "====== STATES ======", A_BOLD)		
		while i<nb_nodes:
			line=""
			line="NODE%2s: %10s "% (i,nodes[i].node_state[2])
			mvwaddstr(up_window,i%9+1, (i//9)*len(line)+1, line,A_BOLD)
			i+=1 		
	elif temp==ord("i"):
		mvwaddstr(up_window,0, 20, "====== ID ======", A_BOLD)		
		while i<nb_nodes:
			line=""
			line="NODE%2s: %20s,%8s "% (i,nodes[i].http_rack[0],nodes[i].http_rack[1])
			mvwaddstr(up_window,i%9+1, (i//9)*len(line)+1, line,A_BOLD)
			i+=1	
	
def footer(down_window):
	init_pair(1,COLOR_WHITE,COLOR_BLUE)
	long=""
	for line in {("M :","MEMORY "),("V :","CORES "),("S :","STATES "),("I :","ID "),("Q :","QUIT")}:
		mvwaddstr(down_window,30,len(long)+1, line[0],A_BOLD)
		long=long+line[0]
		mvwaddstr(down_window,30,len(long)+1, line[1],color_pair(1)+A_REVERSE+A_BOLD)
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
    
        while True:
            #nodes=get_cluster_nodes()
            nb_nodes=randint(0,36)
            #nb_nodes=28
            nodes=set_nodes(nb_nodes)
        #     ================== window decomposition ===========================s
            up_window=newwin(11,143, 0, 0)
            up_panel=new_panel(up_window)
            nodelay(up_window, 1)
            down_window=newwin(42-11,143, 11, 0)
            down_panel=new_panel(down_window)
            nodelay(down_window, 1)
        #   ===================================================================                
            header(nb_nodes,nodes,up_window,temp)
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
		if key==ord("m") or key==ord("v") or key==ord("s") or key==ord("i"):
			temp=key
			
	endwin()
	quit()
	




if __name__=="__main__":
	main()
	