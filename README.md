# table-optimizer
A genetic algorithm for the optimization of socially distant table locations during the Covid-19 pandemic.

This optimizer can be run from a terminal or command prompt with the following command:
```
python3 table-optimizer.py [FLAGS]
```
It accepts one of two flags:

* --optimize-arrangement  Optimizes the positioning of tables within a room, 
                            as defined in the config file.
* --optimize-number       Optimizes the number of tables within the room,
                            as well as their positioning.
                            
When searching for the optimum of the 'number_of_round_tables' and 'number_of_square_tables'
parameters are used as the maximum values for those fields.

### Configuration

The table optimizer algorithm can be configured via the config.ini.  The purpose
of each of the parameters in the config file is listed below.  For users not 
familiar with evolutionary or genetic algorithms, it is recommened to leave the
'[algorithm]' section as is.

The '[room]' section defines the size and properties of the room in which
the tables will be positioned.
```
[room]             
minimum_separation // The minimum allowed distance between tables (in feet)
wall_margin = 6    // The minimum distance between a table and the wall (in feet)
room_length = 83   // The length of the room (in feet)
room_width = 60    // The width of the room (in feet)
```

The '[tables]' section defines the tables that should be placed in the room.
Currently, only round and square tables are supported.
```
[tables]
number_of_round_tables    // The number of circular tables
round_table_radius        // The radius of each circular table
number_of_square_tables   // The number of square tables
square_table_side_length  // The length of one side of each square table
```

The '[algorithm]' configures the algorithm itself.
```
[algorithm]               
number_of_arrangements   // The population of each generation
number_of_generations
percent_parents_from_previous_generation 
percent_new_arrangements_each_generation 
number_of_epochs         // Used only when finding the optimum number of tables
```

### Setup

Matplotlib is the only required package not normally included with python3.  It
can easily be installed by running the following command.
```
python3 -m pip install matplotlib
```