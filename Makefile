all: transfer transferd

init:
	mdutil -i off /Volumes/CIRCUITPY
	cd /Volumes/CIRCUITPY
	rm -rf {fseventsd,Trashes}
	mkdir .fseventsd
	touch .fseventsd/no_log .metadata_never_index .Trashes
	cd -

transfer:
	cp -X code.py /Volumes/CIRCUITPY

transferd:
	cp -rX lib /Volumes/CIRCUITPY
