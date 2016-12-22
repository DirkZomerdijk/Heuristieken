README.txt

FILES
chip.py
run.py
astar.py
functions.py
visualizer.py

CHIP.PY
Bevat alle aspecten van de chip, zoals de lagen, alle gates en gelegde nets:
- class Chip: bevat de hele chip, bestaande uit:
    - class Gate: elke gate
    - class Nets: elk gelegd net
    - class Layer: alle 8 layers

ASTAR.PY
Bevat het kortste pad zoek-algoritme, en de bijbehorende functies:
- next_to_gate: maakt een lijst met alle coordinaten die naast een Gate object liggen
- make_children: functie die de vrije coordinaten rondom een specifiek coordinaat zoekt.
- manhattan: berekent de kortste afstand tussen twee gates
- astar: functie die het kortste pad zoekt via 'vrije' coordinaten tussen twee Gate objecten

FUNCTIONS.PY
Bevat alle functies voor de heuristieken toegepast op dit probleem:
- sort_on_distance: sorteert de netlist op de minimale afstand tussen gate-paren, van lang naar kort.
- sort_on_connections: sorteerd de netlist op het aantal verbinden die een gate heeft, van veel naar weinig.
- remove_random_nets: verwijderd drie random nets uit de reeds geplaatste nets
- make_shorter: neemt de volledige chip nadat alle nets gelegd zijn, en gaat één voor één nets verwijderen en opnieuw leggen. Om zo de totale netlengte te verlagen.
- find_obstacles: zoekt naar Nets objecten die in de weg liggen voor een specifiek pad.
- remove_obstacle: verwijderd één van de Nets objecten die in de weg liggen voor een specifiek pad, net zo vaak tot het te leggen pad geplaats kan worden.
- run_algorithm: dit is de start van het volledige algoritme. Deze functie werkt de netlist af en roept voor elk gate-paar de A* functie aan, en past de heurtistieken (sorteren van de netlist, obstakels verwijderen) toe.

VISUALIZER.PY
Class om de volledige chip in 3D te visualiseren:
- class Visualizer

RUN.PY
Alles wat je nodig hebt om het programma te laten runnen. Wat moet je instellen:
- welke sorteer functie gebruikt wordt (regel 41)
- welke obstakel verwijder-methode gebruikt wordt (regel 40)
- welke netlist gelegd wordt (regel 17)
- of je de uitkomst wil visualiseren (regel 42)
