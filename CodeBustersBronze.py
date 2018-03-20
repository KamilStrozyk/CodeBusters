from random import randint
import sys
import math
#==========GENEROWANIE WIAODMOSCI==============
def GenerateMessage(a):
    s=""
    for i in a:
        s+=str(i)
    
    return s
#===========SPRAWDZANIE ZASIEGU================    
def GhostRange(x,y):
    Range=math.sqrt( (x[1]-y[1])**2 +(x[2]-y[2])**2)
    #if Range<=1760:
    if Range>=900 and Range<=1760:    
        return 1
    elif Range>=1760 and Range<=2200:
        return 2
    elif Range<=900:
        return 3
    return 0
def StunRange(x,y):
    Range=math.sqrt( (x[1]-y[1])**2 +(x[2]-y[2])**2)
    if  Range<=1760:
        return True
    return False    
def PointRange(x,y):
    Range=math.sqrt( (x[0]-y[0])**2 +(x[1]-y[1])**2)
    if  Range<=10:
        return True
    return False    




#==============================================    
targetPoint=[]

#==========CHODZENIE===========================
def MOVE(my_team_id,z):
  
      
    points=[]
    if my_team_id==0:
        points=[(800,8200),(15200,8200),(15200,800),(8000,4500)]
    else:    
        points=[(2000,2000),(800,7200),(15200,800),(8000,4500)]
        
    
    return points[z]
#=============================================   
      
def OptimalGhost(ghosts,x):
    global LowHp
    global busters_per_player
    global tourcount
    op=(-1,1200000,1200000,41,41)
    Op=op
    
    for g in ghosts:
        
    
        if g[4]<op[4] and GhostRange(g,x)!=0:
            op=g
            
          


    if Op==op or (op[4]>30 and tourcount<150):
        return -1
    return op
    

        
# Send your busters out into the fog to trap ghosts and bring them home!
LowHp=[]
busters_per_player = int(input())  # the amount of busters you control
ghost_count = int(input())  # the amount of ghosts on the map
my_team_id = int(input())  # if this is 0, your base is on the top left of the map, if it is one, on the bottom right
#============ROZPOZNAWANIE BAZY===============
BaseCoord=[] #koordynaty bazy w formacie x,y
if my_team_id==0:
    BaseCoord.append(0)
    BaseCoord.append(0)
else:
    BaseCoord.append(16000)
    BaseCoord.append(9000)
#==============================================
# game loop
#lista duchow
z=0
#=========INICJALIZACJA COOLDUWNU STUNTU=======
stuncount=[]
busting=[]
for j in range(busters_per_player):
    if len(stuncount)<=busters_per_player:
        stuncount.append(0)
        busting.append(0)
   # targetPoint.append(MOVE(randint(0,8)))    
    #targetPoint.append(MOVE(randint(0,9)))  
    #targetPoint.append((14000,4500))
    z=randint(0,9)
    targetPoint.append(RandomMOVE(z))
#===============================================     
def RemoveFromBusting(i):
    for j in range(len(busting)):
        if busting[j]==i:
            busting[j]=0
def RemoveDuplicates(LowHp):
    temp=[]
    for i in LowHp:
        if i not in temp:
            temp.append(i)
    
    return temp
tourcount=0    
while True:
    tourcount+=2 
 
    e=[]
    support=[]
    ghosts=[]
    entities = int(input())  # the number of busters and ghosts visible to you
    for i in range(entities):
        # entity_id: buster id or ghost id
        # y: position of this buster / ghost
        # entity_type: the team id if it is a buster, -1 if it is a ghost.
        # state: For busters: 0=idle, 1=carrying a ghost.
        # value: For busters: Ghost id being carried. For ghosts: number of busters attempting to trap this ghost.
        entity_id, x, y, entity_type, state, value = [int(j) for j in input().split()]
        e.append((entity_id, x, y, entity_type, state, value))
        if entity_type == -1:
            ghosts.append((entity_id, x, y, entity_type, state, value))
            if state<30:
                LowHp.append(entity_id)
       # print("Debug messages...",ghosts, file=sys.stderr) 
            
    action=[]#akcje dla kazdego dude'a



        
    for j in range(busters_per_player):
        if stuncount[j]>0:
            stuncount[j]-=1
        if len(action)<=busters_per_player:
           # A=randint(7,8)
            #targetPoint[j]=MOVE(A)  
            action.append(GenerateMessage(("MOVE ",targetPoint[j][0]," ",targetPoint[j][1])))
            
        else:
                action[j]=GenerateMessage(("MOVE ",targetPoint[j][0]," ",targetPoint[j][1]))
               
            
        #if stuncount[j]>0:
         #   stuncount[j]-=1
    LowHp=RemoveDuplicates(LowHp)
    

       
    for y in e:
        if y[3]==-1 and y[4]==0:
            while y[0] in LowHp:
                LowHp.remove(y[0])

        
    for x in e:               
        for y in e: 
        
            if x!=y and stuncount[x[0]%busters_per_player]==0  and x[3]==my_team_id and x[4]==0 and y[3]!=my_team_id and y[3]>=0 and StunRange(x,y)==True and y[5]<=0: 
                action[x[0]%busters_per_player]=GenerateMessage(("STUN ",y[0]))
                stuncount[x[0]%busters_per_player]=21
                busting[x[0]%busters_per_player]=0
         #   elif (x!=y and y[3]==-1 and x[3]==my_team_id and x[4]==0 and y[4]<35  and GhostRange(x,y)==1) : 
         #      action[x[0]%busters_per_player]=GenerateMessage(("BUST ",y[0]))
         #       busting[x[0]%busters_per_player]=y[0]
        #   elif (x!=y and y[3]==-1 and x[3]==my_team_id and x[4]==0 and y[4]>=35 and GhostRange(x,y)==1) : 
        #        action[x[0]%busters_per_player]=GenerateMessage(("BUST ",y[0]))
        #        #busting[x[0]%busters_per_player]=y[0]    
            elif  (x!=y and busting[x[0]%busters_per_player]!=0 and y[0]==busting[x[0]%busters_per_player]and GhostRange(x,y)==1):
               action[x[0]%busters_per_player]=GenerateMessage(("BUST ", busting[x[0]%busters_per_player]))
       #        
        #    elif x!=y and y[3]==-1 and x[3]==my_team_id and x[4]==0 and y[0] and GhostRange(x,y)==2:     
        #       action[x[0]%busters_per_player]=GenerateMessage(("MOVE ",y[1]," ",y[2])) 
        #        busting[x[0]%busters_per_player]=0
        #       support=["xd",y[1],y[2]]
       #
         #   elif x!=y and y[3]!=my_team_id and x[3]==my_team_id and y[4]==1 and y[4]<=35 and y[0] and GhostRange(x,y)==2:     
        #       action[x[0]%busters_per_player]=GenerateMessage(("MOVE ",y[1]," ",y[2])) 
        #        busting[x[0]%busters_per_player]=0
        #    elif x!=y and y[3]==-1 and x[3]==my_team_id and y[4]==1 and y[0] and GhostRange(x,y)==2:     
         #       action[x[0]%busters_per_player]=GenerateMessage(("MOVE ",y[1]," ",y[2])) 
         #       busting[x[0]%busters_per_player]=0    
        if x[4]==1 and x[3]==my_team_id and x[1]==BaseCoord[0] and x[2]==BaseCoord[1]:
            action[x[0]%busters_per_player]=GenerateMessage(("RELEASE"))
            busting[x[0]%busters_per_player]=0
        elif x[4]==1 and x[3]==my_team_id:
            action[x[0]%busters_per_player]=GenerateMessage(("MOVE ",BaseCoord[0]," ",BaseCoord[1]))
            RemoveFromBusting(busting[x[0]%busters_per_player])
            busting[x[0]%busters_per_player]=0
        elif  x[3]==my_team_id and PointRange((x[1],x[2]),(targetPoint[x[0]%busters_per_player][0],targetPoint[x[0]%busters_per_player][1])): #x[1]==targetPoint[x[0]%busters_per_player][0]  and x[2]==targetPoint[x[0]%busters_per_player][1]  :
          #  print("Debug messages...",x[0],x[1],x[2], file=sys.stderr) 
            
            if busters_per_player==4:
                z=randint(0,3)
             #  print("Debug messages...",z, file=sys.stderr) 
                targetPoint[x[0]%busters_per_player]=MOVE(my_team_id,z)
                busting[x[0]%busters_per_player]=0
            else:
                #targetPoint[x[0]%busters_per_player]=RandomMOVE(z)
                z=randint(0,3)
             #   print("Debug messages...",z, file=sys.stderr) 
                targetPoint[x[0]%busters_per_player]=MOVE(my_team_id,z)
                busting[x[0]%busters_per_player]=0
                
                
        if x[3]==my_team_id and x[4]!=1:
            y=OptimalGhost(ghosts,x)
            print("Debug messages...",x[0],y, file=sys.stderr)
            if y!=-1:
                if GhostRange(x,y)==1:
                    action[x[0]%busters_per_player]=GenerateMessage(("BUST ",y[0]))
                    busting[x[0]%busters_per_player]=y[0]
                elif GhostRange(x,y)==2:
                    action[x[0]%busters_per_player]=GenerateMessage(("MOVE ",y[1]," ",y[2])) 
                    busting[x[0]%busters_per_player]=0             
               # elif GhostRange(x,op)==3:            
         
#===============WYKONYWANIE AKCJI===========
    print("Debug messages...",LowHp, file=sys.stderr) 
    for i in range(busters_per_player):        
        print(action[i])



#============================================================================    



        