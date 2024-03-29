# Clearing Montréal of snow
The goal of this project is to solve a chinese postman problem and to calculate a path 
to clear the snow in Montréal.

Detailed explanation of how it's done :[HERE](./README_LOGIC.md)

## Theory:
The theoric part of the solution without any library needed in requirement.txt
```
python -m unittest theory/Tests/*.py
```

## Real:
The pratical part of the solution using osmnx, networkx, pandas and numpy, plotly

First set up a virtual environment
```
pip install -r requirements.txt
```

To launch the solution please launch demo.py and specify --city and --country
```
Example: python demo.py --city Kremlin-Bicetre --country France
```

Or for Montreal use the different borough for example Hampstead:
python demo.py --city Hampstead --country Canada

If no arguments are given, the default borough is Hampstead

It should open an **interactive map** and print the **statistics** for this city
and country
The order of roads to follow in order to clear the snow is written in the file
output.txt

## Interactive map:
![Interactive map](image/InteractiveMapExemple.png)
