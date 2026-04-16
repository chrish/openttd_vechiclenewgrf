# Makefile for darwin_aircraft NewGRF
#
# Usage:
#   make          — compile the GRF
#   make install  — copy the GRF to the OpenTTD newgrf folder (macOS default path)
#   make clean    — remove generated files

NML      := .venv/bin/nmlc
SRC      := darwin_aircraft.nml
GRF      := darwin_aircraft.grf
NFO      := darwin_aircraft.nfo

# macOS default OpenTTD newgrf directory; adjust if yours differs
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
	rm -f $(GRF) $(NFO) *.nfo *.cache *.cacheindex
