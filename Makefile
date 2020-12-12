USER := $(shell whoami)

all: transfer transferd

init-feather:
	@mdutil -i off /Volumes/CIRCUITPY
	@pushd /Volumes/CIRCUITPY && \
	rm -rf {fseventsd,Trashes} && \
	mkdir .fseventsd && \
	touch .fseventsd/no_log .metadata_never_index .Trashes && \
	cd -;

scppi:
	@scp pi/sms_listener ${USER}@c3:/projects/roomba_supervisor/
	@scp pi/button_listener ${USER}@c3:/projects/roomba_supervisor/

scpdpi:
	@scp -r ${USER}@c3:/projects/roomba_supervisor/  /pi/

services:
	@scp pi/*.service ${USER}@c3:/etc/systemd/system

transfer:
	cp -X ./roomba/code.py /Volumes/CIRCUITPY

transferd:
	@cp -rX lib ./roomba/Volumes/CIRCUITPY

user:
	@echo ${USER}
