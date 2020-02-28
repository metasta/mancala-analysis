db.js: analysis.py PositionTable.py
	python3 analysis.py | sed -e 's/ //g' -e 's/{/const db = {/g' > db.js

PositionTable.py: posgen.py
	python3 posgen.py > PositionTable.py