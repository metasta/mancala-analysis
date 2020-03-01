db.py: db.js
	sed -e 's/const //g' db.js > db.py

db.js: analysis.py mpos.py
	python3 analysis.py | sed -e 's/ //g' -e 's/{/const db = {/g' > db.js

mpos.py: posgen.py
	python3 posgen.py > mpos.py