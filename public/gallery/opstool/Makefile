%.html: %.py
	python $< | python -m sees /dev/stdin -o $@

%.json: %.py
	python $< > $@
