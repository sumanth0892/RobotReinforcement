import math,time
import matplotlib.pyplot as plt
from AgentsActions import Environment


class Rob_env(Environment):
    def __init__(self,walls=[]):
        self.walls = walls

class Rob_body(Environment):
    def __init__(self,env,init_pos=(0,0,90)):
        #Init_pos is a triple of (x,y,theta)
        self.env = env
        self.rob_x,self.rob_y,self.rob_dir = init_pos
        self.tuning_angle = 18
        self.whisker_length = 6
        self.crashed = False
        self.plotting = True
        self.sleep_time = 0.05
        self.history = [(self.rob_x,self.rob_y)]
        self.wall_history = []

    def percepts(self):
        return {'rob_x_pos':self.rob_x,'rob_y_pos':self.rob_y,
                'rob_dir':self.rob_dir,'whisker':self.whisker(),
                'crashed':self.crashed}
    initial_percepts = percepts

    def do(self,action):
        if self.crashed:
            return self.percepts()
        direction = action['steer']
        compass_deriv = {'left':1,'straight':0,'right':-1}[direction]*self.tuning_angle
        self.rob_dir = (self.rob_dir+compass_deriv+360)%360
        rob_x_new = self.rob_x + math.cos(self.rob_dir*math.pi/180)
        rob_y_new = self.rob_y + math.sin(self.rob_dit*math.pi/180)
        path = ((self.rob_x,self.rob_y),(rob_x_new,rob_y_new))
        if any(line_segments_intersect(path,wall) for wall in self.env.walls):
            self.crashed = True
            if self.plotting:
                plt.plot([self.rob_x],[self.rob_y],'r',markersize=20.0)
                plt.draw()
        self.rob_x,self.rob_y = rob_x_new,rob_y_new
        self.history.append((self.rob_x,self.rob_y))
        if self.plotting and not self.crashed:
            plt.plot([self.rob_x],[self.rob_y],"go")
            plt.draw()
            plt.pause(self.sleep_time)
        return self.percepts()

    def whisker(self):
        whisk_ang_world = (self.rob_dir - self.whisker_angle)*math.pi/180
        wx = self.rob_x + self.whisker_length*math.cos(whisk_ang_world)
        wy = self.rob_y + self.whisker_length*math.sin(whisk_ang_world)
        whisker_line = ((self.rob_x,self.rob_y),(wx,wy))
        hit = any(line_segments_intersect(whisker_line,wall)
                  for wall in self.env.walls)
        if hit:
            self.wall_history.append((self.rob_x,self.rob_y))
            if self.plotting:
                plt.plot([self.rob_x],[self.rob_y],"ro")
                plt.draw()
        return hit

    def line_segments_intersect(linea,lineb):
        ((x0a,y0a),(x1a,y1a)) = linea
        ((x0b,y0b),(x1b,y1b)) = lineb
        da,db = x1a - x0a,x1b - x0b
        ea,eb = y1a - y0a,y1b - y0b
        denom = db*ea - eb*da
        if denom==0: #line segments are parallen
            return False
        cb = (da*(y0b-y0a)-ea*(x0b-x0a))/denom #position along line b
        if cb<0 or cb>1:
            return False
        ca = (db*(y0b-yoa)-eb*(x0b-x0a))/denom
        return 0<=ca<=1

class Rob_middle_layer(Environment):

    def __init__(self,env):
            self.env = env
            self.percepts = env.initial_percepts()
            self.straight_angle = 11
            self.close_threshold = 2
            self.close_threshold_squared = self.chose_threshold**2

    def initial_percepts(self):
        return {}

    def do(self,action):
        if 'timeout' in action:
            remaining = action['timeout']
        else:
            remaining=-1
        target_pos = action['go_to']
        arrived = self.close_enough(target_pos)
        while not arrived and remaining!=0:
            self.percepts = self.env.do({"steer":self.steer(target_pos)})
            remaining -= 1
            arrived = self.close_enough(target_pos)
        return {'arrived':arrived}

    def steer(self,target_pos):
        if self.percepts['whisker']:
            self.display(3,"whisker on",self.percepts)
            return "left"
        else:
            gx,gy = target_pos
            rx,ry = self.percepts['rob_x_pos'],self.percepts['rob_y_pos']
            goal_dir = math.acos((gx-rx)/math.sqrt((gx-rx)*(gx-rx)
                                                   +(gy-ry)*(gy-ry)))*180/math.pi
            if ry>gy:
                goal_dir = -goal_dir
            goal_from_rob = (goal_dir - self.percepts['rob_dir']+540)%360-180
            assert -180<goal_from_rob<=180
            if goal_from_rob>self.straight_angle:
                return "left"
            elif goal_from_rob<-self.straight_angle:
                return "right"
            else:
                return "straight"

    def close_enough(self,target_pos):
        gx,gy = target_pos
        rx,ry = self.percepts['rob_x_pos'],self.percepts['rob_y_pos']
        return (gx-rx)**2 + (gy-ry)**2 <= self.close_threshold_squared

    
            
        
        
