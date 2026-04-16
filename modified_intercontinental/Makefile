# Makefile for Modified Intercontinental Airport NewGRF

NML      := ../.venv/bin/nmlc
SRC      := modified_intercontinental.nml
GRF      := modified_intercontinental.grf

OTTD_NEWGRF_DIR := $(HOME)/Documents/OpenTTD/newgrf

.PHONY: all install clean

all: $(GRF)

$(GRF): $(SRC) lang/english.lng
	$(NML) --grf=$(GRF) $(SRC)

install: $(GRF)
	install -d "$(OTTD_NEWGRF_DIR)"
	install -m 644 $(GRF) "$(OTTD_NEWGRF_DIR)/"
	@echo "Installed $(GRF) to $(OTTD_NEWGRF_DIR)"

clean:
	rm -f $(GRF) *.nfo *.cache *.cacheindex
