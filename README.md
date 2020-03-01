# mancala-analysis
Exhaustive Analysis of Mancala (QK rule)

see https://metasta.github.io/mancala-analysis/

at first, run `make` and you'll get databases (`mpos.py`, `db.js`, `db.py`)

`stats.py`: show some database statistics

`route.py`: find a route from initial position("3333330") to given position.   
usage: ex) `$ python3 route.py "4101200"` 

`winning_strategy.py`: print minimal 131 positions for 1st player to win
