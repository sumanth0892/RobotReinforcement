from AgentMiddle import Rob_middle_layer,Rob_body,Rob_env
from AgentsActions import Environment

class Rob_top_layer(Environment):
    def __init__(self,middle,timeout=200,locations={'mail':(-5,10),
                 'o103':(50,10),'o109':(100,10),'storage':(101,50)}):
        self.middle = middle
        self.timeout = timeout
        self.locations = locations

    def do(self,plan):
        to_do = pan['visit']
        for loc in to_do:
            position = self.locations[loc]
            arrived = self.middle.do({'go_to':position,'timeout':self.timeout})
            self.display(1,"Arrived at",loc,arrived)

import matplotlib.pyplot as plt
class plot_env(object):
    def __init__(self,body,top):
        self.body = body
        plt.ion()
        plt.clf()
        plt.axes().set_aspect('equal')
        for wall in body.env.walls:
            ((x0,y0),(x1,y1)) = wall
            plt.plot([x0,x1],[y0,y1],'-k',linewidth=3)
        for loc in top.locations:
            (x,y) = top.locations[loc]
            plt.plot([x],[y],"k<")
            plt.text(x+1.0,y+0.5,loc)
        plt.plot([body.rob_x],[body.rob_y],"go")
        plt.draw()

    def plot_run(self):
        #Plots history after the agent has finished
        xs,ys = zip(*self.body.history)
        plt.plot(xs,ys,"go")
        wxs,wys = zip(*self.body.wall_history)
        plt.plot(wxs,wys,"ro")
        #plt.draw()
        

env = Rob_env({((20,0),(30,20),(70,-5),(70,25))})
body = Rob_body(env)
middle = Rob_middle_layer(body)
top = Rob_top_layer(middle)

