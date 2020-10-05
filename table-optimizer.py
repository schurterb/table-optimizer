#!/usr/bin/python3

"""
Created on Sat Sep 26 20:32:33 2020

@author: schurterb

"""

from random import Random
from enum import Enum
import matplotlib.pyplot as plt
from math import sqrt
import configparser
import argparse

##############################################################################
def optimize_arrangement():
    print("Begin Table Optimization")
    
    print("Loading configeration parameters")
    config = configparser.ConfigParser()
    config.read('config.ini')
    min_distance=float(config['room']['minimum_separation'])
    wall_margin=float(config['room']['wall_margin'])
    x_boundaries=[0,int(config['room']['room_length'])]
    y_boundaries=[0,int(config['room']['room_width'])]
    
    num_round_tables=int(config['tables']['number_of_round_tables'])
    round_table_radius=float(config['tables']['round_table_radius'])
    num_square_tables=int(config['tables']['number_of_square_tables'])
    square_table_radius=float(config['tables']['square_table_side_length'])/2.0
    
    num_arrangements=int(config['algorithm']['number_of_arrangements'])
    num_generations=int(config['algorithm']['number_of_generations'])
    percent_parents_from_previous_generation=float(config['algorithm']['percent_parents_from_previous_generation'])
    percent_new_arrangements_each_generation=float(config['algorithm']['percent_new_arrangements_each_generation'])
    
    
    print("Initializing Tables")
    a = arrangement(x_boundaries, y_boundaries, min_distance, wall_margin)
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
        oa[0].display(oa[1])
    
    print("End Table Optimization")

def optimize_number():
    print("Begin Table Optimization")
    
    print("Loading configeration parameters")
    config = configparser.ConfigParser()
    config.read('config.ini')
    min_distance=float(config['room']['minimum_separation'])
    wall_margin=float(config['room']['wall_margin'])
    x_boundaries=[0,int(config['room']['room_length'])]
    y_boundaries=[0,int(config['room']['room_width'])]
    
    num_round_tables=int(config['tables']['number_of_round_tables'])
    round_table_radius=float(config['tables']['round_table_radius'])
    num_square_tables=int(config['tables']['number_of_square_tables'])
    square_table_radius=float(config['tables']['square_table_side_length'])/2.0
    
    num_arrangements=int(config['algorithm']['number_of_arrangements'])
    num_generations=int(config['algorithm']['number_of_generations'])
    percent_parents_from_previous_generation=float(config['algorithm']['percent_parents_from_previous_generation'])
    percent_new_arrangements_each_generation=float(config['algorithm']['percent_new_arrangements_each_generation'])
    
    num_round_tables=num_round_tables*10
    num_square_tables=num_square_tables*10
    final_error=(num_round_tables + num_square_tables) *2
    epoch_counter=0
    while final_error > 0.0 or (num_round_tables + num_square_tables) == 0 or epoch_counter > 10000:
        print(" ** Epoch "+str(epoch_counter)+" ** ")
        print(" * "+str(num_round_tables)+" round tables")
        print(" * "+str(num_square_tables)+" square tables")
        print("Initializing Tables for epoch: "+str(epoch_counter))
        a = arrangement(x_boundaries, y_boundaries, min_distance, wall_margin)
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
        optimized_arrangements = opt.optimize(arrangements, num_generations, False)
        
        final_error=optimized_arrangements[0][1]
        print("Best result from epoch "+str(epoch_counter)+": "+str(final_error))
        if final_error > 0.0:
            if num_square_tables > 0:
                num_square_tables -= 1
            else:
                num_square_tables = int(config['tables']['number_of_square_tables'])
                num_round_tables -= 1
        
    print("Displaying final results")
    for oa in optimized_arrangements:
        oa[0].display(oa[1])
    
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
    
    def __init__(self, x_boundary=[0,100], y_boundary=[0,100], min_distance=10, margin_distance=10):
        self.rnd=Random()
        self.rnd.seed()
        self.tables=[]
        self.min_distance=min_distance
        self.x_boundary=x_boundary
        self.y_boundary=y_boundary        
        self.margin_distance = margin_distance
        
        self.x_boundary_min=self.x_boundary[0] + self.margin_distance
        self.x_boundary_max=self.x_boundary[1] - self.margin_distance
        self.y_boundary_min=self.y_boundary[0] + self.margin_distance
        self.y_boundary_max=self.y_boundary[1] - self.margin_distance
            
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
        new_arrangement = arrangement(self.x_boundary, self.y_boundary, self.min_distance, self.margin_distance)
        for table in self.tables:
            new_arrangement.tables.append(table.copy())
        return new_arrangement
    
    def display(self, error=None):
        plt.axes(xlim=self.x_boundary, ylim=self.y_boundary)
        plt.grid(True, 'major', 'both')
        for table in self.tables:
            if table.shape is Shape.circle:
                plt.gca().add_patch(self.__drawCircle(table.x, table.y, table.radius))
            elif table.shape is Shape.square:
                plt.gca().add_patch(self.__drawSquare(table.x, table.y, table.radius))
                
        if error is not None:
            plt.title("Optimized Table Arrangement - Error = "+str(error))
        else:
            plt.title("Optimized Table Arrangement")
        plt.show()
    
    def __drawSquare(self, x, y, r):
        l=r*sqrt(2)
        x=x-(l/2)
        y=y-(l/2)
        return plt.Rectangle((x, y), l, l, fc='orange',ec='orange')
        
    def __drawCircle(self, x, y, r):
        return plt.Circle((x, y), r, fc='blue',ec='blue')
        
    
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
                z = (float(pow(dx,2) + pow(dy,2)) / float(pow(m,2))) -1.0
                if z < 0:
                    e = e - z
            error += (e -1)
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
            
    def optimize(self, arrangements, num_generations, print_generations=True):
        if print_generations:
            print("Optimizing for",num_generations," generations.")
        num_arrangements=len(arrangements)
        num_parents=int(num_arrangements*self.percent_parents)
        num_new=int(num_arrangements*self.percent_new)
        for i in range(num_generations):
            if print_generations:
                print("Generation "+str(i)+":")
            results = self.testArrangements(arrangements)
            results.sort(key=lambda x:x[1])
            results = results[0:num_parents]
            if print_generations:
                print(" - Top "+str(num_parents)+" arrangements' error results")
                for r in results:
                    print("    "+str(r[1]))
            parents=[r[0] for r in results]
            if print_generations:
                print("Populating next generation...")
            arrangements = self.repopulateArrangements(parents, num_arrangements, num_new)
        return results
   
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--optimize-number', action='store_true' ,help='Optimize the number and position of the tables within the room.')
    parser.add_argument('--optimize-arrangement', action='store_true' ,help='Optimize only the position of the tables within the room.')
    args = parser.parse_args()
    if args.optimize_number:
        optimize_number()
    elif args.optimize_arrangement:
        optimize_arrangement()
    else:
        parser.print_help()
            
            
        
        
    
        
    
    
    
    
    