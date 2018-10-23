import numpy as np
from itertools import combinations
class TreeNode:
	def __init__(self, nodeName, count, nodeParent):
		self.nodeName = nodeName
		self.count = count
		self.nodeParent = nodeParent
		self.nextSimilarItem = None
		self.children = {}
	def increase_count(self):
		self.count += 1

#	def sss(self):
#		print self.nodeName,self.count
#		if (self.children!={}):
#			for child in self.children.values():
#				child.sss()
#		else:
#			print '    '
		
def createfptree(order_dataset,headpoint_table ):
	fptree=TreeNode('NULL',1,None)
	root=fptree
	for items in order_dataset:
		fptree=root
		for item in items:
			if item in fptree.children:
				fptree.children[item].increase_count()
			else:
				fptree.children[item]=TreeNode(item,1,fptree)#new node
				if headpoint_table[item]==None:
					headpoint_table[item]=fptree.children[item]
					
				else:
					point=headpoint_table[item]
					
					while(point.nextSimilarItem != None):
						point = point.nextSimilarItem#until node nextSimilarItem = None
					point.nextSimilarItem=fptree.children[item]
			fptree=	fptree.children[item]
	fptree=root
	return fptree, headpoint_table

def minefptree(fptree,headpoint_table,minSupport=3):
	for elem in headpoint_table:
		count_table={}
		curr_node=headpoint_table[elem]
		mark_node=curr_node
		while((curr_node.nodeParent.nodeName!='NULL')or(mark_node.nextSimilarItem!=None)):
			if curr_node.nodeParent.nodeName!='NULL':
				curr_node=curr_node.nodeParent
				
				count_table[curr_node.nodeName]=count_table.get(curr_node.nodeName,0)+mark_node.count
			else:
				curr_node=mark_node.nextSimilarItem
				mark_node=curr_node
		
		count_table={k:v for k,v in count_table.items() if v>=minSupport}
		if (count_table!={}):
			for table_len in range(len(count_table)):
					for pat in combinations(count_table,table_len+1):
						min=100
						for pat_elem in pat:
							print pat_elem,
							if count_table[pat_elem]<min:
								min=count_table[pat_elem]
						print elem,
						print ':',min
						
if __name__=='__main__':
	data=open('data.nitems_0.01.ntrans_0.1.tlen_3', 'r').readlines()
	dataset=[]
	r=0 #row
	for i in range(len(data)):
		current=(data[i].split())[0]
		if current!=r:
			dataset.append([])
			r=current
		dataset[int(current)-1].append((data[i].split())[2])
	print 'dataset:'
	print dataset
	#start
	minSupport=20
	freq_table={}
	for items in dataset:
		for item in items:
			freq_table[item]=freq_table.get(item,0)+1
	freq_table={k:v for k,v in freq_table.items() if v>=minSupport}#del item (<minSupport)
	order_freq_table=sorted(freq_table.items(),key=lambda (k,v):v,reverse=True)#['8':49,....]
	headpoint_table={}
	for elem in order_freq_table:
		headpoint_table[elem[0]]=None #{'0':None,'8':None,.....}
	order_dataset=dataset
	for i in range(len(order_dataset)):
		order_dataset[i]=[k[0] for k in order_freq_table if k[0] in order_dataset[i]]
	#[['8','9',...],...]

	fptree,headpoint_table=createfptree(order_dataset,headpoint_table)
	#fptree.sss()
	minefptree(fptree,headpoint_table,minSupport)
