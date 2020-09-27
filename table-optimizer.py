#!/home/user/anaconda3/bin/python3

"""
Created on Sat Sep 26 20:32:33 2020

@author: schurterb

"""

from random import Random
from enum import Enum
import matplotlib.pyplot as plt

##############################################################################
def main():    
    min_distance=10
    x_boundaries=[0,100]
    y_boundaries=[0,60]
    
    num_round_tables=15
    round_table_radius=4
    num_square_tables=3
    square_table_radius=2
    
    num_arrangements=500
    num_generations=300
    percent_parents_from_previous_generation=0.1
    percent_new_arrangements_each_generation=0.3
        
    print("Begin Table Optimization")
    
    print("Initializing Tables")
    a = arrangement(min_distance, x_boundaries, y_boundaries)
    for j in range(num_round_tables):
        a.tables.append(table(Shape.circle, round_table_radius))
    for j in range(num_square_tables):
        a.tables.append(table(Shape.square, square_table_radius))
    arrangements = []
    for i in range(num_arrangements):
        a.initializeTables(a.tables)
        arrangements.append(a.copy())
                    
    print("Initializing Optimizer")
    opt = optimizer(percent_parents_from_previous_generation, 
                    percent_new_arrangements_each_generation)
    
    print("Running Optimizer")
    optimized_arrangements = opt.optimize(arrangements, num_generations)
    
    print("Displaying final results")
    for oa in optimized_arrangements:
        oa[0].display()
    
    print("End Table Optimization")

##############################################################################

class Shape(Enum):
    circle = 1
    square = 2

class table:       
    def __init__(self, shape=Shape.circle, r=3):
        self.shape=shape
        self.radius=r
        self.x=0
        self.y=0
    
    def copy(self):
        new_table = table(self.shape, self.radius)
        new_table.x = self.x
        new_table.y = self.y
        return new_table
    
class arrangement:
    
    def __init__(self, min_distance=10, x_boundary=[0,100], y_boundary=[0,100]):
        self.rnd=Random()
        self.rnd.seed()
        self.tables=[]
        self.min_distance=min_distance
        self.x_boundary=x_boundary
        self.y_boundary=y_boundary
        
        half_min_distance = self.min_distance / 2
        self.x_boundary_min=self.x_boundary[0] + half_min_distance
        self.x_boundary_max=self.x_boundary[1] - half_min_distance
        self.y_boundary_min=self.y_boundary[0] + half_min_distance
        self.y_boundary_max=self.y_boundary[1] - half_min_distance
            
    def initializeTables(self, new_tables):
        self.tables=new_tables
        for table in self.tables:
            table.x = self.rnd.uniform(self.x_boundary_min, self.x_boundary_max)
            table.y = self.rnd.uniform(self.y_boundary_min, self.y_boundary_max)
            
    def mutateTables(self, percentage=0.2, max_change=5):
        max_change = float(max_change)
        for table in self.tables:
            if self.rnd.random() <= percentage:
                new_x = table.x + (((self.rnd.random() * 2.0) - 1.0) * max_change)
                if new_x < self.x_boundary_max and new_x > self.x_boundary_min:
                    table.x = new_x
                new_y = table.y + (((self.rnd.random() * 2.0) - 1.0) * max_change)
                if new_y < self.y_boundary_max and new_y > self.y_boundary_min:
                    table.y = new_y
    
    def copy(self):
        new_arrangement = arrangement(self.min_distance, self.x_boundary, self.y_boundary)
        for table in self.tables:
            new_arrangement.tables.append(table.copy())
        return new_arrangement
    
    def display(self):
        
        round_x=[]
        round_y=[]
        round_r=[]
        square_x=[]
        square_y=[]
        square_r=[]
        scale_factor=5.2
        for table in self.tables:
            if table.shape is Shape.circle:
                round_x.append(table.x)
                round_y.append(table.y)
                round_r.append(pow(table.radius,scale_factor))
            elif table.shape is Shape.square:
                square_x.append(table.x)
                square_y.append(table.y)
                square_r.append(pow(table.radius,scale_factor))
        
        fig, axs = plt.subplots()
        axs.set(xlim=self.x_boundary, ylim=self.y_boundary)
        axs.scatter(round_x, round_y, s=round_r, marker='o', c='b')
        axs.scatter(square_x, square_y, s=square_r, marker='s', c='b')
        plt.show()
        return fig, axs
        
    
class optimizer:
    
    def __init__(self, percent_parents=0.1, percent_new=0.2):
        self.percent_parents=percent_parents
        self.percent_new=percent_new

    def calculateError(self, arrangement):
        error=0
        for i in arrangement.tables:
            e = 0
            for j in arrangement.tables:
                dx = i.x - j.x
                dy = i.y - j.y
                m = i.radius + arrangement.min_distance + j.radius
                z = ( (pow(dx,2) + pow(dy,2)) / pow(m,2) ) -1
                if z < 0:
                    e = e - z
            error += e
        return error
        
    def testArrangements(self, arrangements):
        results = []
        for arrangement in arrangements:
            error = self.calculateError(arrangement)
            results.append((arrangement, error))            
        return results
    
    def repopulateArrangements(self, parents, offspring_count, num_new):
        new_arrangements = []
        for parent in parents:
            new_arrangements.append(parent.copy())
        for i in range(0, num_new):
            new_arrangement = parents[0].copy()
            new_arrangement.initializeTables(new_arrangement.tables)
            new_arrangements.append(new_arrangement)
        counter=0
        for i in range(0, offspring_count):
            child = parents[counter].copy()
            child.mutateTables()
            new_arrangements.append(child)            
            counter += 1
            if counter >= len(parents):
                counter = 0
        return new_arrangements
            
    def optimize(self, arrangements, num_generations):
        print("Optimizing for",num_generations," generations.")
        num_arrangements=len(arrangements)
        num_parents=int(num_arrangements*self.percent_parents)
        num_new=int(num_arrangements*self.percent_new)
        for i in range(num_generations):
            print("Generation "+str(i)+":")
            results = self.testArrangements(arrangements)
            results.sort(key=lambda x:x[1])
            results = results[0:num_parents]
            print(" - Top "+str(num_parents)+" arrangements' error results")
            for r in results:
                print("    "+str(r[1]))
            parents=[r[0] for r in results]
            print("Populating next generation...")
            arrangements = self.repopulateArrangements(parents, num_arrangements, num_new)
        return results
   
if __name__ == "__main__":
    main()
        
            
            
        
        
    
        
    
    
    
    
    