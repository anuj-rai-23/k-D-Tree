''' Code written and submitted by:
Anuj Rai (M.Tech AI)
Roll No: 2019AIM1003
for CS509 PG Software Lab Mini Project Phase-B (Range Query and deletion in KD-Tress) 
Assumptions: The points are loaded into program from the text file(.txt) named as 'DataSet.txt'. Also, every spatial data point has unique id. '''
import copy
from time import time
axis=["X","Y","Z"]

# Structure of Root Node of tree
class RootNode:
    def __init__(self,region):
        self.left=None
        self.right=None
        self.region=region

# Structure of Internal node with its field
class InternalNode: 
    def __init__(self): 
        self.left = None
        self.right = None
        self.axis=-1
        self.val=-1
        self.parent=None
        self.childtype=" "

#Structure of Leaf Node
class LeafNode:
    def __init__(self,key):
        self.val=key
        self.parent=None
        self.left=None
        self.right=None
        self.childtype=" "

#Function that return region bounded by point set i.e. max and min points in their dimensions
def region(point_set,n):
    mn=[]
    mx=[]
    for i in (1,n):
        mn.append(min(x[i] for x in point_set))
        mx.append(max(x[i] for x in point_set))
    return [mn,mx]

#Function to find if two regions overlap
def TestIntersect(Reg1,Reg2):
    l=len(Reg1[0])
    for i in range(0,l):
        if Reg1[0][i]>Reg2[1][i] or Reg1[1][i]<Reg2[0][i]:
            return False
    return True

#Function to find if region1 is inside region 2
def Inside(Reg1,Reg2):
    l=len(Reg1[0])
    for i in range(0,l):
        if Reg1[0][i]<Reg2[0][i] or Reg1[1][i]>Reg2[1][i]:
            return False
    return True

#Function that returns the axis with maximum spread along all dimensions
def stretch(point_set,n):
    mx=0
    d=0
    for i in (1,n):
        xmax=max(x[i] for x in point_set)
        xmin=min(x[i] for x in point_set)
        if xmax-xmin>mx:
            mx=xmax-xmin
            d=i;
    return d

#Function that returns split points and index of node with median point along axis of maximum spread
def median_index(point_set,n):
    sort_list=sorted(point_set, key = lambda x: x[n]) 
    l=len(sort_list)
    if l%2==1:
        k=l//2+1
    else:
        k=l//2
    p=k
    while k<l and sort_list[k-1][n]==sort_list[k][n]:
        k=k+1
    if k==l:
     k=l-1
     while k>1 and sort_list[k-1][n]==sort_list[k][n]:
       k=k-1
    return sort_list[:k],sort_list[k:],sort_list[k-1][n]
   
#Function that makes tree with the set of points according to value of alpha    
def make_tree(tree,point_set,dim,alpha):
  #print (point_set)
  axis=stretch(point_set,dim)
  a,b,c=median_index(point_set,axis)
  tree.axis=axis
  tree.val=c
  #print (a,"----",b,"\n")
  if len(a)<=alpha:
      P=LeafNode(a)
      P.childtype="L"
      tree.left=P
      tree.left.parent=tree
  else:
    A=InternalNode();
    A.childtype="L"
    tree.left=A
    make_tree(A,a,dim,alpha)
    tree.left.parent=tree
  if len(b)<=alpha:
      Q=LeafNode(b)
      Q.childtype="R"
      tree.right=Q
      tree.right.parent=tree
  else:
      B=InternalNode();
      B.childtype="R"
      tree.right=B
      make_tree(B,b,dim,alpha)
      tree.right.parent=tree

#Function that prints the information stored at given node for all kind of nodes
def detail(tree,dim):
  if isinstance(tree,RootNode):
    print ("Root "+str(axis[tree.axis-1])+"="+str(tree.val)+" Region ",tree.region)
  elif isinstance(tree,InternalNode):
    print ("Internal "+str(axis[tree.axis-1])+"="+str(tree.val)+" Child-Type "+tree.childtype)
  else:
    print( "Leaf Child-Type "+tree.childtype+" Points =",tree.val)

#Function that returns height of tree
def height(Node):
  if Node==None:
    return 0
  elif isinstance(Node,LeafNode):
    return 1
  else:
    lh=height(Node.left)
    rh=height(Node.right)
    return max(lh,rh)+1

#Function that prints nodes at given level
def PrintLevel(Node , level,dim): 
    if level == 1 : 
        detail(Node,dim)
    elif level > 1 : 
        if Node.left!=None:
          PrintLevel(Node.left , level-1,dim) 
        if Node.right!=None:
          PrintLevel(Node.right , level-1,dim) 

#Function to visualise the tree according to levels
def Visualize(root,dim): 
    h = height(root) 
    for i in range(1, h+1): 
        print ("Level ",i)
        PrintLevel(root, i,dim)
        print("\n")
#Function to return common area between two regions. Returns none if they donot intersect
def common_area(Reg1,Reg2):
    Reg3=[[],[]]
    l=len(Reg1[0])
    for i in range(0,l):
        Reg3[1].append(min(Reg1[1][i],Reg2[1][i]))
        Reg3[0].append(max(Reg1[0][i],Reg2[0][i]))
    for i in range(0,l):
        if Reg3[0][i]>Reg3[1][i]:
            return None
    return Reg3

#Function that returns Found if any point is present in given leaf node
def leaf_search(tree,pnt):
  P=copy.deepcopy(tree.val)
  #print (detail(P))
  for j in P:
    del j[0]
  for j in P:
    if j==pnt:
      return "Found"
  return "Not Found"

#Function that tells if a given point lies inside a region bounded by given points     
def PointInside(a,b):
  for l1,l2 in zip(a,b[0]):
    if l1<l2:
      return "No"
  for l1,l2 in zip(a,b[1]):
    if l1>l2:
      return "No"
  return "Yes"

#Function to implement naive range query
def NaiveRangeQuery(point_set,Region):
    P=copy.deepcopy(point_set)
    ind=[]
    cnt=-1
    for j in P:
        del j[0]
    for j in P:
        cnt=cnt+1
        if PointInside(j,Region)=="Yes":
            ind.append(cnt)
    return ind

#Function to search if given point is present in the KD-tree
def search_tree(tree,pnt,regn):
  if PointInside(pnt,regn)=="No":
    return "Not Found"
  reg=copy.deepcopy(regn)
  if isinstance(tree,RootNode) or isinstance(tree,InternalNode):
    if(pnt[tree.axis-1]<=tree.val):
      reg[1][tree.axis-1]=tree.val
      if isinstance(tree.left,LeafNode) and  PointInside(pnt,reg)=="Yes":
        return leaf_search(tree.left,pnt)
      else:
        return search_tree(tree.left,pnt,reg)
    else:
      reg[0][tree.axis-1]=tree.val
      if isinstance(tree.right,LeafNode) and  PointInside(pnt,reg)=="Yes":
        return leaf_search(tree.right,pnt)
      else:
        return search_tree(tree.right,pnt,reg)

#Function that inserts a point(ID,coordinates) in a tree
def insert_record(tree,pnt,alpha):
  if isinstance(tree,RootNode) :
    if PointInside(pnt,tree.region)=="No":
      for i in range(1,len(pnt)):
        tree.region[0][i-1]=min(pnt[i],tree.region[0][i-1])
        tree.region[1][i-1]=max(pnt[i],tree.region[1][i-1])
    if(pnt[tree.axis]<=tree.val):
      insert_record(tree.left,pnt,alpha) 
    else:
      insert_record(tree.right,pnt,alpha) 
  
  elif isinstance(tree,InternalNode):
    if(pnt[tree.axis]<=tree.val):
          insert_record(tree.left,pnt,alpha)
    else :
        insert_record(tree.right,pnt,alpha)
  else:
    k=tree.val
    tree.val.append(pnt)
    if len(k)>alpha:
      R=InternalNode()
      if tree.childtype=="L":
        tree.parent.left=R
        R.childtype="L"
      else:
        tree.parent.right=R
        R.childtype="L"
      R.parent=tree.parent
      make_tree(R,tree.val,2,alpha)
     
#Function that loads a list of points from a text file
def load_points():
  fil=open("DataSet.txt","r+")
  n=fil.readlines()
  points=[]
  for i in n:
    points.append(list(map(int,i.split())))
  fil.close()
  return points

#Function to delete from leaf node
def delete_from_leaf(tree,pnt):
  P=copy.deepcopy(tree.val)
  #print (detail(P))
  flag=0
  for j in P:
    del j[0]
  cnt=-1
  for j in P:
    cnt=cnt+1
    if j==pnt:
      flag=1
      tree.val.pop(cnt)
      if len(tree.val)==0:
        if tree.childtype=="L":
          if tree.parent.childtype=="L":
            tree.parent.parent.left=tree.parent.right
            tree.parent.right.childtype="L"
          else:
            tree.parent.parent.right=tree.parent.right
        else:
          if tree.parent.childtype=="L":
            tree.parent.parent.left=tree.parent.left
          else:
            tree.parent.parent.right=tree.parent.left
            tree.parent.left.childtype="R"
      break
  if flag==0:
    print("Not Found")
  else:
    print("Deleted point ",pnt)

#Function to delete a node
def delete_point(tree,pnt,regn):
  if PointInside(pnt,regn)=="No":
    return "Not Found"
  reg=copy.deepcopy(regn)
  if isinstance(tree,RootNode) or isinstance(tree,InternalNode):
    if(pnt[tree.axis-1]<=tree.val):
      reg[1][tree.axis-1]=tree.val
      if isinstance(tree.left,LeafNode) and  PointInside(pnt,reg)=="Yes":
        return delete_from_leaf(tree.left,pnt)
      else:
        return delete_point(tree.left,pnt,reg)
    else:
      reg[0][tree.axis-1]=tree.val
      if isinstance(tree.right,LeafNode) and  PointInside(pnt,reg)=="Yes":
        return delete_from_leaf(tree.right,pnt)
      else:
        return delete_point(tree.right,pnt,reg)

#Function that inserts a given point in already built tree
def insertion(kd_tree,alpha,dim):
  pnt =  list(map(int, input("Enter point ").split()) )
  insert_record(kd_tree,pnt,alpha)
  #Visualize(kd_tree,dim)

#Function that searches for a point in tree
def point_search(kd_tree):
  pnt =  list(map(int, input("Enter point for search: ").split()) )
  print(search_tree(kd_tree,pnt,kd_tree.region))

#Function for deletion
def deletion(kd_tree):
  pnt =  list(map(int, input("Enter point ").split()) )
  delete_point(kd_tree,pnt,kd_tree.region)

#Function to insert points in output list of range query
def push_all(tree,stk,Reg):
  if isinstance(tree,LeafNode):
    k=copy.deepcopy(tree.val)
    for i in NaiveRangeQuery(k,Reg):
      stk.append(tree.val[i])
  else:
    if tree.left!=None:
      push_all(tree.left,stk,Reg)
    if tree.right!=None:
      push_all(tree.right,stk,Reg)

#Fucntion for range query
def range_query(stk,tree,Reg1,Reg2):
  if TestIntersect(Reg1,Reg2):
      if Inside(Reg1,Reg2):
        push_all(tree,stk,Reg2)
      elif isinstance(tree,LeafNode):
        push_all(tree,stk,Reg2)
      else:
        Reg3=copy.deepcopy(Reg1)
        Reg4=copy.deepcopy(Reg1)
        Reg3[1][tree.axis-1]=tree.val
        Reg4[0][tree.axis-1]=tree.val
        if tree.left!=None:
          range_query(stk,tree.left,Reg3,Reg2)
        if tree.right!=None:
          range_query(stk,tree.right,Reg4,Reg2)

#Function to execute range query
def exec_range_query(kd_tree):
  Reg=[]
  pnt =  list(map(int, input("Enter minima of region ").split()) )
  Reg.append(pnt)
  pnt =  list(map(int, input("Enter maxima of region ").split()) )
  Reg.append(pnt)
  stk=[]
  #t1=time()
  range_query(stk,kd_tree,kd_tree.region,Reg)
  if len(stk)>0:
    print (stk)
  else:
    print ("No point found")
  #t2=time()
  #R.append(t2-t1)
  
#Driver function for all the operations: Bulk loading, point search and insertion
def main():
  points=load_points()
  dimension=len(points[0])-1
  alpha=int(input("Enter alpha : "))
  Reg=region(points,dimension)
  kd_tree=RootNode(Reg);
  make_tree(kd_tree,points,dimension,alpha)
  print ("KD-tree Bulk-Loading complete")
  ip=1
  while ip!=6:
    ip=int(input("\n 1.Visualize \n 2.Search\n 3.Insertion of point\n 4.Delete\n 5.Range Query\n 6.Exit\n"))
    if ip==1:
      Visualize(kd_tree, dimension)
    elif ip==3:
      insertion(kd_tree,alpha,dimension)
    elif ip==2:
      point_search(kd_tree)
    elif ip==4:
      deletion(kd_tree)
    elif ip==5:
      exec_range_query(kd_tree)

if __name__== "__main__":
  main()
