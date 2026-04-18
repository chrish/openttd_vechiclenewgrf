#!/usr/bin/env python3
"""
Generate NML code for all vehicles from the markdown spec files.

Reads Airplanes.md, Road.md, Ships.md, Trains.md and produces:
  - NML item blocks in the appropriate subdirectory files
  - Language strings for lang/english.lng
  - Updated Checklist.md with NML column marked

Vehicle IDs start at 1000 and correspond to checklist index:
  checklist #N  →  vehicle ID  (999 + N)

The first 10 vehicles (IDs 1000–1009) were already hand-written in
aircraft/airliners/early_airliners.nml and lang/english.lng, so
this script starts from vehicle #11 (ID 1010).
"""

import re
import os
import math

# ---------------------------------------------------------------------------
#  Constants
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIRST_NEW_INDEX = 11  # start from checklist #11 (ID 1010)

# ---------------------------------------------------------------------------
#  Parsing helpers
# ---------------------------------------------------------------------------

def parse_capacity(cap_str):
    """Extract a numeric capacity from strings like '32', '21–32', '32 pax', '5 t', '0.5 t'."""
    cap_str = cap_str.strip().replace(',', '')
    # Handle ranges: take the higher value (e.g. "21–32" → 32)
    range_match = re.search(r'([\d.]+)\s*[–—-]\s*([\d.]+)', cap_str)
    if range_match:
        return float(range_match.group(2))
    # Single number
    num_match = re.search(r'([\d.]+)', cap_str)
    if num_match:
        return float(num_match.group(1))
    return 0


def parse_speed(speed_str):
    """Extract numeric speed in km/h from strings like '895 km/h', 'Mach 2.0 (2,160 km/h)'."""
    speed_str = speed_str.strip().replace(',', '')
    # Check for parenthesised km/h (for Mach speeds)
    paren_match = re.search(r'\(([\d.]+)\s*km/h\)', speed_str)
    if paren_match:
        return int(float(paren_match.group(1)))
    # Plain km/h
    kmh_match = re.search(r'([\d.]+)\s*km/h', speed_str)
    if kmh_match:
        return int(float(kmh_match.group(1)))
    # Just a number
    num_match = re.search(r'([\d.]+)', speed_str)
    if num_match:
        return int(float(num_match.group(1)))
    return 0


def parse_hp(hp_str):
    """Extract numeric horsepower from strings like '2,200 hp', '1.4 hp'."""
    hp_str = hp_str.strip().replace(',', '')
    m = re.search(r'([\d.]+)\s*hp', hp_str, re.IGNORECASE)
    if m:
        return int(float(m.group(1)))
    m = re.search(r'([\d.]+)', hp_str)
    if m:
        return int(float(m.group(1)))
    return 0


def parse_year(year_str):
    """Parse year string, returning int or 2100 for 'TBD'."""
    year_str = year_str.strip()
    if year_str == 'TBD':
        return 2100
    m = re.match(r'(\d{4})', year_str)
    if m:
        return int(m.group(1))
    return 0


def parse_cargo_age_mult(ca_str):
    """Parse cargo age multiplier like '1×', '2.5×'."""
    ca_str = ca_str.strip()
    m = re.search(r'([\d.]+)\s*[×x]', ca_str)
    if m:
        return float(m.group(1))
    return 1.0


def to_snake_case(name):
    """Convert a vehicle name to snake_case for NML identifiers."""
    # Remove quotes, parentheses, slashes
    s = name.replace('"', '').replace("'", '').replace("'", '')
    s = re.sub(r'\(.*?\)', '', s)  # remove parenthetical content
    s = s.replace('/', ' ').replace('\\', ' ')
    s = s.replace('-', ' ').replace('.', ' ').replace(',', ' ')
    s = s.replace('&', ' and ')
    s = re.sub(r'[^a-zA-Z0-9\s]', '', s)  # remove remaining specials
    s = s.strip()
    s = re.sub(r'\s+', '_', s)
    return s.lower()


def to_string_id(name):
    """Convert a vehicle name to STR_UPPER_SNAKE_CASE_NAME."""
    s = to_snake_case(name).upper()
    return f'STR_{s}_NAME'

# ---------------------------------------------------------------------------
#  Table parsing from markdown files
# ---------------------------------------------------------------------------

def parse_standard_table(filepath, sections_config):
    """
    Parse vehicle rows from a markdown file's tables.

    sections_config: list of dicts with keys:
      - header_pattern: regex to match section header
      - vtype: vehicle type label (for checklist)
      - feat: NML feature (FEAT_AIRCRAFT, etc.)
      - subdir: output subdirectory (e.g., 'aircraft/airliners')
      - cols: dict mapping logical names to column indices:
          year, name, capacity, speed, type, hp (optional), manufacturer (optional)
      - extra: dict of static extra properties to add to every vehicle in this section

    Returns list of vehicle dicts.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    vehicles = []
    current_section = None

    for line in lines:
        stripped = line.strip()

        # Check for section header changes
        for sec in sections_config:
            if re.search(sec['header_pattern'], stripped, re.IGNORECASE):
                current_section = sec
                break

        if current_section is None:
            continue
        if current_section.get('skip'):
            continue

        # Must be a table row
        if not stripped.startswith('|'):
            continue
        # Skip separator rows
        if re.match(r'^\|[\s\-|:]+\|$', stripped):
            continue

        cols_raw = stripped.split('|')[1:-1]
        cols_data = [c.strip() for c in cols_raw]

        if not cols_data:
            continue

        # Skip header rows
        if cols_data[0] in ('Year', 'Year ') or (len(cols_data) > 1 and 'Name' in cols_data[1]):
            continue

        # Skip era/section separator rows (bold markers)
        if '**' in cols_data[0]:
            continue
        if len(cols_data) > 1 and cols_data[0] == '' and '**' in (cols_data[1] if len(cols_data) > 1 else ''):
            continue

        col_map = current_section['cols']
        if len(cols_data) <= max(col_map.values()):
            continue

        year_str = cols_data[col_map['year']].replace('**', '').strip()
        name_str = cols_data[col_map['name']].replace('**', '').strip()

        if not year_str or not name_str:
            continue
        year = parse_year(year_str)
        if year == 0:
            continue

        v = {
            'name': name_str,
            'year': year,
            'vtype': current_section['vtype'],
            'feat': current_section['feat'],
            'subdir': current_section['subdir'],
            'speed': parse_speed(cols_data[col_map['speed']]) if 'speed' in col_map else 0,
            'capacity': parse_capacity(cols_data[col_map['capacity']]) if 'capacity' in col_map else 0,
            'type_desc': cols_data[col_map['type']].strip() if 'type' in col_map else '',
            'hp': parse_hp(cols_data[col_map['hp']]) if 'hp' in col_map else 0,
            'manufacturer': cols_data[col_map.get('manufacturer', 2)].strip() if 'manufacturer' in col_map else '',
        }

        # Merge static extra props
        if 'extra' in current_section:
            v.update(current_section['extra'])

        vehicles.append(v)

    return vehicles


def parse_wagon_trailer_table(filepath, sections_config):
    """
    Parse wagon/trailer tables which have format:
    | Year | Name | Capacity | Cargo Age | Loading Speed | Notes |
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    vehicles = []
    current_section = None

    for line in lines:
        stripped = line.strip()

        for sec in sections_config:
            if re.search(sec['header_pattern'], stripped, re.IGNORECASE):
                current_section = sec
                break

        if current_section is None or current_section.get('skip'):
            continue

        if not stripped.startswith('|'):
            continue
        if re.match(r'^\|[\s\-|:]+\|$', stripped):
            continue

        cols_raw = stripped.split('|')[1:-1]
        cols_data = [c.strip() for c in cols_raw]

        if not cols_data or len(cols_data) < 5:
            continue

        # Skip headers
        if cols_data[0] in ('Year', 'Year ') or 'Name' in cols_data[1]:
            continue
        if '**' in cols_data[0]:
            continue

        year = parse_year(cols_data[0])
        if year == 0:
            continue

        name_str = cols_data[1].strip()
        if not name_str:
            continue

        v = {
            'name': name_str,
            'year': year,
            'vtype': current_section['vtype'],
            'feat': current_section['feat'],
            'subdir': current_section['subdir'],
            'capacity': parse_capacity(cols_data[2]),
            'cargo_age_mult': parse_cargo_age_mult(cols_data[3]),
            'loading_speed_raw': int(re.search(r'(\d+)', cols_data[4]).group(1)) if re.search(r'(\d+)', cols_data[4]) else 5,
            'speed': 0,  # wagons/trailers inherit from tow vehicle
            'type_desc': cols_data[5].strip() if len(cols_data) > 5 else '',
            'hp': 0,
            'is_wagon': True,
        }

        if 'extra' in current_section:
            v.update(current_section['extra'])

        vehicles.append(v)

    return vehicles

# ---------------------------------------------------------------------------
#  Section configs for each markdown file
# ---------------------------------------------------------------------------

def get_airplane_sections():
    base_cols = {'year': 0, 'name': 1, 'manufacturer': 2, 'capacity': 3, 'speed': 4, 'type': 5}

    return [
        {'header_pattern': r'## Major Airliners', 'vtype': 'Airplane',
         'feat': 'FEAT_AIRCRAFT', 'subdir': 'aircraft/airliners', 'cols': base_cols},
        {'header_pattern': r'## Airships & Blimps', 'vtype': 'Airship',
         'feat': 'FEAT_AIRCRAFT', 'subdir': 'aircraft/airships', 'cols': base_cols},
        {'header_pattern': r'## Helicopters', 'vtype': 'Helicopter',
         'feat': 'FEAT_AIRCRAFT', 'subdir': 'aircraft/helicopters', 'cols': base_cols},
        {'header_pattern': r'## Futuristic Aircraft', 'vtype': 'Futuristic Aircraft',
         'feat': 'FEAT_AIRCRAFT', 'subdir': 'aircraft/airliners', 'cols': base_cols, 'skip': True},
        # Futuristic sub-sections:
        {'header_pattern': r'\*\*Near-Future Airliners', 'vtype': 'Futuristic Airplane',
         'feat': 'FEAT_AIRCRAFT', 'subdir': 'aircraft/airliners', 'cols': base_cols},
        {'header_pattern': r'\*\*Supersonic & Hypersonic', 'vtype': 'Futuristic Airplane',
         'feat': 'FEAT_AIRCRAFT', 'subdir': 'aircraft/airliners', 'cols': base_cols},
        {'header_pattern': r'\*\*Futuristic Helicopters', 'vtype': 'Futuristic Helicopter',
         'feat': 'FEAT_AIRCRAFT', 'subdir': 'aircraft/helicopters', 'cols': base_cols},
        {'header_pattern': r'\*\*Futuristic eVTOL', 'vtype': 'Futuristic eVTOL',
         'feat': 'FEAT_AIRCRAFT', 'subdir': 'aircraft/evtol', 'cols': base_cols},
        {'header_pattern': r'\*\*Futuristic Airships', 'vtype': 'Futuristic Airship',
         'feat': 'FEAT_AIRCRAFT', 'subdir': 'aircraft/airships', 'cols': base_cols},
        # Stop parsing at refit tables
        {'header_pattern': r'## Aircraft Refit', 'skip': True, 'vtype': '_SKIP_',
         'feat': '', 'subdir': '', 'cols': base_cols},
    ]


def get_road_sections():
    base_cols = {'year': 0, 'name': 1, 'manufacturer': 2, 'capacity': 3, 'speed': 4, 'type': 5}

    return [
        {'header_pattern': r'## Buses', 'vtype': 'Bus',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/buses', 'cols': base_cols},
        {'header_pattern': r'## Trucks', 'vtype': 'Truck',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/trucks', 'cols': base_cols},
        {'header_pattern': r'## Cars', 'vtype': 'Car',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/cars', 'cols': base_cols},
        # Futuristic Road -- skip the umbrella header
        {'header_pattern': r'## Futuristic Road Vehicles', 'vtype': '_SKIP_',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/buses', 'cols': base_cols, 'skip': True},
        {'header_pattern': r'\*\*Near-Future Buses', 'vtype': 'Futuristic Bus',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/buses', 'cols': base_cols},
        {'header_pattern': r'\*\*Near-Future Trucks', 'vtype': 'Futuristic Truck',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/trucks', 'cols': base_cols},
        {'header_pattern': r'\*\*Near-Future Cars', 'vtype': 'Futuristic Car',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/cars', 'cols': base_cols},
        {'header_pattern': r'\*\*Far-Future Road', 'vtype': 'Futuristic Road Vehicle',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/buses', 'cols': base_cols},
        # Trailer section marker -- skip
        {'header_pattern': r'## Truck Trailers', 'vtype': '_SKIP_',
         'feat': '', 'subdir': '', 'cols': base_cols, 'skip': True},
    ]


def get_road_trailer_sections():
    """Trailer tables use: Year | Name | Capacity | Cargo Age | Loading Speed | Notes"""
    return [
        {'header_pattern': r'### Passenger Trailers', 'vtype': 'Bus Trailer',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/trailers',
         'extra': {'default_cargo': 'PASS', 'cargo_classes': 'bitmask(CC_PASSENGERS)'}},
        {'header_pattern': r'### Mail.*Parcel Trailers', 'vtype': 'Mail Trailer',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/trailers',
         'extra': {'default_cargo': 'MAIL', 'cargo_classes': 'bitmask(CC_MAIL)'}},
        {'header_pattern': r'### Armoured Trailers', 'vtype': 'Armoured Trailer',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/trailers',
         'extra': {'default_cargo': 'VALU', 'cargo_classes': 'bitmask(CC_ARMOURED, CC_EXPRESS)'}},
        {'header_pattern': r'### Grain.*Wheat Trailers', 'vtype': 'Grain Trailer',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/trailers',
         'extra': {'default_cargo': 'GRAI', 'cargo_classes': 'bitmask(CC_BULK, CC_COVERED)'}},
        {'header_pattern': r'### Livestock Trailers', 'vtype': 'Livestock Trailer',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/trailers',
         'extra': {'default_cargo': 'LVST', 'cargo_classes': 'bitmask(CC_PIECE_GOODS)'}},
        {'header_pattern': r'### Coal Trailers', 'vtype': 'Coal Trailer',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/trailers',
         'extra': {'default_cargo': 'COAL', 'cargo_classes': 'bitmask(CC_BULK)'}},
        {'header_pattern': r'### Iron Ore.*Mineral Trailers', 'vtype': 'Ore Trailer',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/trailers',
         'extra': {'default_cargo': 'IORE', 'cargo_classes': 'bitmask(CC_BULK)'}},
        {'header_pattern': r'### Steel.*Metal Flatbed', 'vtype': 'Steel Trailer',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/trailers',
         'extra': {'default_cargo': 'STEL', 'cargo_classes': 'bitmask(CC_PIECE_GOODS, CC_OVERSIZED)'}},
        {'header_pattern': r'### Oil.*Petroleum Tanker', 'vtype': 'Oil Tanker Trailer',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/trailers',
         'extra': {'default_cargo': 'OIL_', 'cargo_classes': 'bitmask(CC_LIQUID)'}},
        {'header_pattern': r'### Wood.*Timber Trailers', 'vtype': 'Timber Trailer',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/trailers',
         'extra': {'default_cargo': 'WOOD', 'cargo_classes': 'bitmask(CC_PIECE_GOODS, CC_OVERSIZED)'}},
        {'header_pattern': r'### Goods.*General Cargo', 'vtype': 'Goods Trailer',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/trailers',
         'extra': {'default_cargo': 'GOOD', 'cargo_classes': 'bitmask(CC_PIECE_GOODS, CC_COVERED, CC_EXPRESS)'}},
        {'header_pattern': r'### Food.*Refrigerated', 'vtype': 'Food Trailer',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/trailers',
         'extra': {'default_cargo': 'FOOD', 'cargo_classes': 'bitmask(CC_REFRIGERATED, CC_PIECE_GOODS)'}},
        {'header_pattern': r'### Paper.*Covered Trailers', 'vtype': 'Paper Trailer',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/trailers',
         'extra': {'default_cargo': 'PAPR', 'cargo_classes': 'bitmask(CC_PIECE_GOODS, CC_COVERED)'}},
        {'header_pattern': r'### Rubber.*Fruit.*Tropical', 'vtype': 'Tropical Cargo Trailer',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/trailers',
         'extra': {'default_cargo': 'FRUT', 'cargo_classes': 'bitmask(CC_REFRIGERATED, CC_PIECE_GOODS)'}},
        {'header_pattern': r'### Copper.*Water.*Misc', 'vtype': 'Bulk Trailer',
         'feat': 'FEAT_ROADVEHS', 'subdir': 'road/trailers',
         'extra': {'default_cargo': 'CORE', 'cargo_classes': 'bitmask(CC_BULK, CC_LIQUID)'}},
    ]


def get_ship_sections():
    base_cols = {'year': 0, 'name': 1, 'manufacturer': 2, 'capacity': 3, 'speed': 4, 'type': 5}

    return [
        {'header_pattern': r'## Passenger Ships & Ferries', 'vtype': 'Passenger Ship',
         'feat': 'FEAT_SHIPS', 'subdir': 'ships/passenger', 'cols': base_cols},
        {'header_pattern': r'## Cargo Ships', 'vtype': 'Cargo Ship',
         'feat': 'FEAT_SHIPS', 'subdir': 'ships/cargo', 'cols': base_cols},
        {'header_pattern': r'## Specialised & Smaller', 'vtype': 'Specialised Vessel',
         'feat': 'FEAT_SHIPS', 'subdir': 'ships/specialised', 'cols': base_cols},
        # Futuristic umbrella -- skip
        {'header_pattern': r'## Futuristic Ships', 'vtype': '_SKIP_',
         'feat': 'FEAT_SHIPS', 'subdir': 'ships/passenger', 'cols': base_cols, 'skip': True},
        {'header_pattern': r'\*\*Near-Future Passenger Ships', 'vtype': 'Futuristic Passenger Ship',
         'feat': 'FEAT_SHIPS', 'subdir': 'ships/passenger', 'cols': base_cols},
        {'header_pattern': r'\*\*Near-Future Cargo Ships', 'vtype': 'Futuristic Cargo Ship',
         'feat': 'FEAT_SHIPS', 'subdir': 'ships/cargo', 'cols': base_cols},
        {'header_pattern': r'\*\*Near-Future Specialised', 'vtype': 'Futuristic Specialised Vessel',
         'feat': 'FEAT_SHIPS', 'subdir': 'ships/specialised', 'cols': base_cols},
        {'header_pattern': r'\*\*Far-Future Ships', 'vtype': 'Futuristic Ship',
         'feat': 'FEAT_SHIPS', 'subdir': 'ships/passenger', 'cols': base_cols},
        # Stop at refit tables
        {'header_pattern': r'## Ship Refit', 'skip': True, 'vtype': '_SKIP_',
         'feat': '', 'subdir': '', 'cols': base_cols},
    ]


def get_train_sections():
    # Trains have an extra HP column
    train_cols = {'year': 0, 'name': 1, 'manufacturer': 2, 'capacity': 3, 'hp': 4, 'speed': 5, 'type': 6}

    return [
        {'header_pattern': r'## Steam Locomotives', 'vtype': 'Steam Locomotive',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/steam', 'cols': train_cols,
         'extra': {'engine_class': 'ENGINE_CLASS_STEAM', 'running_cost_base': 'RUNNING_COST_STEAM', 'track_type': 'RAIL'}},
        {'header_pattern': r'## Diesel Locomotives', 'vtype': 'Diesel Locomotive',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/diesel', 'cols': train_cols,
         'extra': {'engine_class': 'ENGINE_CLASS_DIESEL', 'running_cost_base': 'RUNNING_COST_DIESEL', 'track_type': 'RAIL'}},
        {'header_pattern': r'## Electric Locomotives', 'vtype': 'Electric Locomotive',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/electric', 'cols': train_cols,
         'extra': {'engine_class': 'ENGINE_CLASS_ELECTRIC', 'running_cost_base': 'RUNNING_COST_ELECTRIC', 'track_type': 'ELRL'}},
        {'header_pattern': r'## Electric Multiple Units & High-Speed', 'vtype': 'EMU / High-Speed Train',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/emu-highspeed', 'cols': train_cols,
         'extra': {'engine_class': 'ENGINE_CLASS_ELECTRIC', 'running_cost_base': 'RUNNING_COST_ELECTRIC', 'track_type': 'ELRL'}},
        {'header_pattern': r'## Diesel Multiple Units & Railcars', 'vtype': 'DMU / Railcar',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/dmu-railcars', 'cols': train_cols,
         'extra': {'engine_class': 'ENGINE_CLASS_DIESEL', 'running_cost_base': 'RUNNING_COST_DIESEL', 'track_type': 'RAIL'}},
        {'header_pattern': r'## Metro.*Rapid Transit', 'vtype': 'Metro Train',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/metro', 'cols': train_cols,
         'extra': {'engine_class': 'ENGINE_CLASS_ELECTRIC', 'running_cost_base': 'RUNNING_COST_ELECTRIC', 'track_type': 'ELRL'}},
        # Futuristic umbrella -- skip
        {'header_pattern': r'## Futuristic Trains', 'vtype': '_SKIP_',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/steam', 'cols': train_cols, 'skip': True},
        {'header_pattern': r'\*\*Near-Future Locomotives', 'vtype': 'Futuristic Locomotive',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/electric', 'cols': train_cols,
         'extra': {'engine_class': 'ENGINE_CLASS_ELECTRIC', 'running_cost_base': 'RUNNING_COST_ELECTRIC', 'track_type': 'ELRL'}},
        {'header_pattern': r'\*\*Near-Future High-Speed', 'vtype': 'Futuristic High-Speed Train',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/emu-highspeed', 'cols': train_cols,
         'extra': {'engine_class': 'ENGINE_CLASS_ELECTRIC', 'running_cost_base': 'RUNNING_COST_ELECTRIC', 'track_type': 'ELRL'}},
        {'header_pattern': r'\*\*Near-Future Regional & Metro', 'vtype': 'Futuristic Regional/Metro',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/metro', 'cols': train_cols,
         'extra': {'engine_class': 'ENGINE_CLASS_ELECTRIC', 'running_cost_base': 'RUNNING_COST_ELECTRIC', 'track_type': 'ELRL'}},
        {'header_pattern': r'\*\*Near-Future Freight', 'vtype': 'Futuristic Freight Train',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/electric', 'cols': train_cols,
         'extra': {'engine_class': 'ENGINE_CLASS_ELECTRIC', 'running_cost_base': 'RUNNING_COST_ELECTRIC', 'track_type': 'ELRL'}},
        {'header_pattern': r'\*\*Far-Future Trains', 'vtype': 'Futuristic Train',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/electric', 'cols': train_cols,
         'extra': {'engine_class': 'ENGINE_CLASS_ELECTRIC', 'running_cost_base': 'RUNNING_COST_ELECTRIC', 'track_type': 'MGLV'}},
        # Wagons umbrella -- skip (parsed separately)
        {'header_pattern': r'## Wagons', 'vtype': '_SKIP_',
         'feat': '', 'subdir': '', 'cols': train_cols, 'skip': True},
    ]


def get_train_wagon_sections():
    return [
        {'header_pattern': r'### Passenger Coaches', 'vtype': 'Passenger Coach',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/wagons',
         'extra': {'default_cargo': 'PASS', 'cargo_classes': 'bitmask(CC_PASSENGERS)',
                   'engine_class': 'ENGINE_CLASS_STEAM', 'running_cost_base': 'RUNNING_COST_NONE', 'track_type': 'RAIL'}},
        {'header_pattern': r'### Mail Vans', 'vtype': 'Mail Van',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/wagons',
         'extra': {'default_cargo': 'MAIL', 'cargo_classes': 'bitmask(CC_MAIL)',
                   'engine_class': 'ENGINE_CLASS_STEAM', 'running_cost_base': 'RUNNING_COST_NONE', 'track_type': 'RAIL'}},
        {'header_pattern': r'### Armoured Vans', 'vtype': 'Armoured Van',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/wagons',
         'extra': {'default_cargo': 'VALU', 'cargo_classes': 'bitmask(CC_ARMOURED, CC_EXPRESS)',
                   'engine_class': 'ENGINE_CLASS_STEAM', 'running_cost_base': 'RUNNING_COST_NONE', 'track_type': 'RAIL'}},
        {'header_pattern': r'### Grain.*Wheat Hoppers', 'vtype': 'Grain Hopper',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/wagons',
         'extra': {'default_cargo': 'GRAI', 'cargo_classes': 'bitmask(CC_BULK, CC_COVERED)',
                   'engine_class': 'ENGINE_CLASS_STEAM', 'running_cost_base': 'RUNNING_COST_NONE', 'track_type': 'RAIL'}},
        {'header_pattern': r'### Livestock Wagons', 'vtype': 'Livestock Wagon',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/wagons',
         'extra': {'default_cargo': 'LVST', 'cargo_classes': 'bitmask(CC_PIECE_GOODS)',
                   'engine_class': 'ENGINE_CLASS_STEAM', 'running_cost_base': 'RUNNING_COST_NONE', 'track_type': 'RAIL'}},
        {'header_pattern': r'### Coal Wagons', 'vtype': 'Coal Wagon',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/wagons',
         'extra': {'default_cargo': 'COAL', 'cargo_classes': 'bitmask(CC_BULK)',
                   'engine_class': 'ENGINE_CLASS_STEAM', 'running_cost_base': 'RUNNING_COST_NONE', 'track_type': 'RAIL'}},
        {'header_pattern': r'### Iron Ore Wagons', 'vtype': 'Iron Ore Wagon',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/wagons',
         'extra': {'default_cargo': 'IORE', 'cargo_classes': 'bitmask(CC_BULK)',
                   'engine_class': 'ENGINE_CLASS_STEAM', 'running_cost_base': 'RUNNING_COST_NONE', 'track_type': 'RAIL'}},
        {'header_pattern': r'### Steel.*Metal Wagons', 'vtype': 'Steel Wagon',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/wagons',
         'extra': {'default_cargo': 'STEL', 'cargo_classes': 'bitmask(CC_PIECE_GOODS, CC_OVERSIZED)',
                   'engine_class': 'ENGINE_CLASS_STEAM', 'running_cost_base': 'RUNNING_COST_NONE', 'track_type': 'RAIL'}},
        {'header_pattern': r'### Oil.*Petroleum Tank', 'vtype': 'Oil Tank Wagon',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/wagons',
         'extra': {'default_cargo': 'OIL_', 'cargo_classes': 'bitmask(CC_LIQUID)',
                   'engine_class': 'ENGINE_CLASS_STEAM', 'running_cost_base': 'RUNNING_COST_NONE', 'track_type': 'RAIL'}},
        {'header_pattern': r'### Wood.*Timber Wagons', 'vtype': 'Timber Wagon',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/wagons',
         'extra': {'default_cargo': 'WOOD', 'cargo_classes': 'bitmask(CC_PIECE_GOODS, CC_OVERSIZED)',
                   'engine_class': 'ENGINE_CLASS_STEAM', 'running_cost_base': 'RUNNING_COST_NONE', 'track_type': 'RAIL'}},
        {'header_pattern': r'### Goods.*General Cargo', 'vtype': 'Goods Van',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/wagons',
         'extra': {'default_cargo': 'GOOD', 'cargo_classes': 'bitmask(CC_PIECE_GOODS, CC_COVERED, CC_EXPRESS)',
                   'engine_class': 'ENGINE_CLASS_STEAM', 'running_cost_base': 'RUNNING_COST_NONE', 'track_type': 'RAIL'}},
        {'header_pattern': r'### Food.*Refrigerated', 'vtype': 'Food/Reefer Van',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/wagons',
         'extra': {'default_cargo': 'FOOD', 'cargo_classes': 'bitmask(CC_REFRIGERATED, CC_PIECE_GOODS)',
                   'engine_class': 'ENGINE_CLASS_STEAM', 'running_cost_base': 'RUNNING_COST_NONE', 'track_type': 'RAIL'}},
        {'header_pattern': r'### Paper.*Covered Wagons', 'vtype': 'Paper Wagon',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/wagons',
         'extra': {'default_cargo': 'PAPR', 'cargo_classes': 'bitmask(CC_PIECE_GOODS, CC_COVERED)',
                   'engine_class': 'ENGINE_CLASS_STEAM', 'running_cost_base': 'RUNNING_COST_NONE', 'track_type': 'RAIL'}},
        {'header_pattern': r'### Rubber.*Fruit.*Tropical', 'vtype': 'Tropical Cargo Wagon',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/wagons',
         'extra': {'default_cargo': 'FRUT', 'cargo_classes': 'bitmask(CC_REFRIGERATED, CC_PIECE_GOODS)',
                   'engine_class': 'ENGINE_CLASS_STEAM', 'running_cost_base': 'RUNNING_COST_NONE', 'track_type': 'RAIL'}},
        {'header_pattern': r'### Copper.*Water.*Misc', 'vtype': 'Bulk Wagon',
         'feat': 'FEAT_TRAINS', 'subdir': 'trains/wagons',
         'extra': {'default_cargo': 'CORE', 'cargo_classes': 'bitmask(CC_BULK, CC_LIQUID)',
                   'engine_class': 'ENGINE_CLASS_STEAM', 'running_cost_base': 'RUNNING_COST_NONE', 'track_type': 'RAIL'}},
    ]


# ---------------------------------------------------------------------------
#  Property calculation
# ---------------------------------------------------------------------------

def get_era(year):
    if year < 1920:
        return 'pre1920'
    elif year < 1950:
        return '1920_1950'
    elif year < 1970:
        return '1950_1970'
    elif year < 2000:
        return '1970_2000'
    elif year < 2030:
        return '2000_plus'
    else:
        return 'futuristic'


ERA_COST_MULT = {
    'pre1920': 0.6, '1920_1950': 1.0, '1950_1970': 1.25,
    '1970_2000': 1.5, '2000_plus': 2.0, 'futuristic': 2.5,
}

ERA_COMFORT = {
    'pre1920': 0.75, '1920_1950': 1.0, '1950_1970': 1.25,
    '1970_2000': 1.5, '2000_plus': 1.75, 'futuristic': 2.5,
}

ERA_LOADING = {
    'pre1920': 0.5, '1920_1950': 0.75, '1950_1970': 1.0,
    '1970_2000': 1.5, '2000_plus': 2.0, 'futuristic': 3.0,
}

ERA_MODEL_LIFE = {
    'pre1920': 15, '1920_1950': 20, '1950_1970': 25,
    '1970_2000': 28, '2000_plus': 25, 'futuristic': 30,
}

ERA_VEHICLE_LIFE = {
    'pre1920': 15, '1920_1950': 22, '1950_1970': 27,
    '1970_2000': 30, '2000_plus': 30, 'futuristic': 40,
}

ERA_RELIABILITY = {
    'pre1920': 32, '1920_1950': 25, '1950_1970': 20,
    '1970_2000': 18, '2000_plus': 16, 'futuristic': 14,
}


def clamp(v, lo, hi):
    return max(lo, min(hi, int(round(v))))


def calc_aircraft_props(v):
    """Calculate NML properties for an aircraft."""
    year = v['year']
    era = get_era(year)
    cap = max(1, int(v['capacity']))
    speed = max(10, v['speed'])

    # Determine aircraft_type
    type_desc = v.get('type_desc', '').lower()
    vtype = v.get('vtype', '')
    if 'helicopter' in type_desc or 'helicopter' in vtype.lower():
        aircraft_type = 'AIRCRAFT_TYPE_HELICOPTER'
    elif ('widebody' in type_desc or 'quad' in type_desc or 'double-deck' in type_desc
          or 'ultra-widebody' in type_desc or cap > 200):
        aircraft_type = 'AIRCRAFT_TYPE_LARGE'
    else:
        aircraft_type = 'AIRCRAFT_TYPE_SMALL'

    # Cost factor: (pax/20) + (speed/100), with era mult
    cost_raw = (cap / 20.0) + (speed / 100.0)
    cost_factor = clamp(cost_raw * ERA_COST_MULT[era], 1, 255)

    # Running cost: (speed/10) + (pax/5) + 50
    run_raw = (speed / 10.0) + (cap / 5.0) + 50
    # Older aircraft are less efficient
    if era == 'pre1920':
        run_raw *= 1.3
    elif era == '1920_1950':
        run_raw *= 1.15
    running_cost_factor = clamp(run_raw, 1, 255)

    # Mail capacity: roughly (pax / 5), min 1
    mail_cap = clamp(cap / 5.0, 1, 255)

    # Loading speed: base 20, scaled by era and capacity
    cap_factor = 1.0
    if cap >= 500:
        cap_factor = 2.0
    elif cap >= 200:
        cap_factor = 1.5
    elif cap >= 50:
        cap_factor = 1.25
    loading_speed = clamp(20 * ERA_LOADING[era] * cap_factor * 0.15, 1, 255)

    # Cargo age period
    cargo_age = clamp(185 * ERA_COMFORT[era], 100, 1200)

    # Acceleration
    if aircraft_type == 'AIRCRAFT_TYPE_HELICOPTER':
        accel = clamp(25 + (speed / 50), 18, 55)
    elif aircraft_type == 'AIRCRAFT_TYPE_LARGE':
        accel = clamp(18 + (speed / 100), 18, 50)
    else:
        accel = clamp(20 + (speed / 80), 18, 50)

    return {
        'aircraft_type': aircraft_type,
        'cost_factor': cost_factor,
        'running_cost_factor': running_cost_factor,
        'passenger_capacity': cap,
        'mail_capacity': mail_cap,
        'loading_speed': loading_speed,
        'cargo_age_period': cargo_age,
        'acceleration': accel,
        'model_life': ERA_MODEL_LIFE[era],
        'vehicle_life': ERA_VEHICLE_LIFE[era],
        'reliability_decay': ERA_RELIABILITY[era],
        'speed': speed,
        'refit_classes': 'bitmask(CC_PASSENGERS, CC_MAIL)',
        'non_refit_classes': 'bitmask()',
    }


def calc_road_props(v):
    """Calculate NML properties for a road vehicle (bus/truck/car)."""
    year = v['year']
    era = get_era(year)
    cap = max(1, int(v['capacity']))
    speed = max(5, v['speed'])
    vtype = v.get('vtype', '')

    is_bus = 'bus' in vtype.lower() or 'trailer' in vtype.lower() and 'pax' in v.get('default_cargo', '').lower()
    is_truck = 'truck' in vtype.lower()
    is_car = 'car' in vtype.lower()

    # Cost factor: (cap/10) + (speed/20)
    cost_raw = (cap / 10.0) + (speed / 20.0)
    cost_factor = clamp(cost_raw * ERA_COST_MULT[era], 1, 255)

    # Running cost: (speed/5) + (cap/10) + 10
    run_raw = (speed / 5.0) + (cap / 10.0) + 10
    running_cost_factor = clamp(run_raw, 1, 255)

    # Loading speed
    cap_factor = 1.0
    if cap >= 200:
        cap_factor = 1.5
    elif cap >= 50:
        cap_factor = 1.25
    loading_speed = clamp(5 * ERA_LOADING[era] * cap_factor, 1, 255)

    # Cargo age
    cargo_age = clamp(185 * ERA_COMFORT[era], 100, 1200)

    # Cargo classes
    if is_bus or is_car:
        refit = 'bitmask(CC_PASSENGERS, CC_MAIL)'
        non_refit = 'bitmask()'
    else:
        refit = 'bitmask(CC_PIECE_GOODS, CC_BULK, CC_COVERED, CC_LIQUID)'
        non_refit = 'bitmask(CC_PASSENGERS)'

    return {
        'cost_factor': cost_factor,
        'running_cost_factor': running_cost_factor,
        'cargo_capacity': cap,
        'loading_speed': loading_speed,
        'cargo_age_period': cargo_age,
        'speed': speed,
        'model_life': ERA_MODEL_LIFE[era],
        'vehicle_life': ERA_VEHICLE_LIFE[era],
        'reliability_decay': ERA_RELIABILITY[era],
        'refit_classes': refit,
        'non_refit_classes': non_refit,
    }


def calc_ship_props(v):
    """Calculate NML properties for a ship."""
    year = v['year']
    era = get_era(year)
    cap = max(1, int(v['capacity']))
    speed = max(5, v['speed'])
    vtype = v.get('vtype', '').lower()

    is_passenger = 'passenger' in vtype or 'ferry' in vtype
    is_cargo = 'cargo' in vtype

    # Cost factor: (cap/50) + (speed/5)
    cost_raw = (cap / 50.0) + (speed / 5.0)
    cost_factor = clamp(cost_raw * ERA_COST_MULT[era], 1, 255)

    # Running cost: (speed*2) + (cap/100) + 10
    run_raw = (speed * 2.0) + (cap / 100.0) + 10
    running_cost_factor = clamp(run_raw, 1, 255)

    # Loading speed
    cap_factor = 1.0
    if cap >= 500:
        cap_factor = 2.0
    elif cap >= 200:
        cap_factor = 1.5
    elif cap >= 50:
        cap_factor = 1.25
    loading_speed = clamp(10 * ERA_LOADING[era] * cap_factor, 1, 255)

    # Cargo age
    cargo_age = clamp(185 * ERA_COMFORT[era], 100, 1200)

    # Refit
    if is_passenger:
        refit = 'bitmask(CC_PASSENGERS, CC_MAIL)'
        non_refit = 'bitmask()'
    else:
        refit = 'bitmask(CC_BULK, CC_PIECE_GOODS, CC_COVERED, CC_LIQUID)'
        non_refit = 'bitmask(CC_PASSENGERS)'

    return {
        'cost_factor': cost_factor,
        'running_cost_factor': running_cost_factor,
        'cargo_capacity': cap,
        'loading_speed': loading_speed,
        'cargo_age_period': cargo_age,
        'speed': speed,
        'model_life': ERA_MODEL_LIFE[era],
        'vehicle_life': ERA_VEHICLE_LIFE[era],
        'reliability_decay': ERA_RELIABILITY[era],
        'refit_classes': refit,
        'non_refit_classes': non_refit,
        'is_passenger': is_passenger,
    }


def calc_train_props(v):
    """Calculate NML properties for a train engine."""
    year = v['year']
    era = get_era(year)
    hp = max(1, v.get('hp', 100))
    speed = max(5, v['speed'])
    engine_class = v.get('engine_class', 'ENGINE_CLASS_DIESEL')

    # Cost factor: (power/100) * era_mult
    cost_raw = hp / 100.0
    cost_factor = clamp(cost_raw * ERA_COST_MULT[era], 1, 255)

    # Running cost depends on engine type
    if 'STEAM' in engine_class:
        run_raw = (hp / 30.0) + 20
    elif 'DIESEL' in engine_class:
        run_raw = (hp / 40.0) + 15
    else:
        run_raw = (hp / 50.0) + 10
    running_cost_factor = clamp(run_raw, 1, 255)

    # Loading speed
    loading_speed = clamp(5 * ERA_LOADING[era], 1, 255)

    # Cargo age
    cargo_age = clamp(185 * ERA_COMFORT[era], 100, 1200)

    # Weight estimate based on era and power
    if 'STEAM' in engine_class:
        weight = clamp(hp * 0.06 + 30, 20, 500)
    elif 'DIESEL' in engine_class:
        weight = clamp(hp * 0.04 + 40, 30, 400)
    else:
        weight = clamp(hp * 0.03 + 30, 20, 350)

    # Tractive effort
    if 'STEAM' in engine_class:
        te_coeff = 0.25
    elif era in ('2000_plus', 'futuristic'):
        te_coeff = 0.35
    else:
        te_coeff = 0.30

    return {
        'cost_factor': cost_factor,
        'running_cost_factor': running_cost_factor,
        'power': hp,
        'speed': speed,
        'weight': weight,
        'tractive_effort_coefficient': te_coeff,
        'loading_speed': loading_speed,
        'cargo_age_period': cargo_age,
        'model_life': ERA_MODEL_LIFE[era],
        'vehicle_life': ERA_VEHICLE_LIFE[era],
        'reliability_decay': ERA_RELIABILITY[era],
        'engine_class': engine_class,
        'running_cost_base': v.get('running_cost_base', 'RUNNING_COST_DIESEL'),
        'track_type': v.get('track_type', 'RAIL'),
    }


def calc_wagon_props(v):
    """Calculate NML properties for a wagon or trailer."""
    year = v['year']
    era = get_era(year)
    cap = max(1, int(v['capacity']))
    cargo_age_mult = v.get('cargo_age_mult', 1.0)
    loading_speed_raw = v.get('loading_speed_raw', 5)

    # Cargo age: base 185 × multiplier from table
    cargo_age = clamp(185 * cargo_age_mult, 100, 1200)

    # Cost for wagons is low
    cost_factor = clamp(cap / 5.0, 1, 40)
    running_cost_factor = clamp(cap / 10.0 + 2, 1, 30)

    return {
        'cost_factor': cost_factor,
        'running_cost_factor': running_cost_factor,
        'cargo_capacity': cap,
        'loading_speed': loading_speed_raw,
        'cargo_age_period': cargo_age,
        'model_life': ERA_MODEL_LIFE[era],
        'vehicle_life': ERA_VEHICLE_LIFE[era],
        'reliability_decay': ERA_RELIABILITY[era],
        'default_cargo': v.get('default_cargo', 'GOOD'),
        'cargo_classes': v.get('cargo_classes', 'bitmask(CC_PIECE_GOODS)'),
    }


# ---------------------------------------------------------------------------
#  NML generation
# ---------------------------------------------------------------------------

def gen_aircraft_nml(v, idx, props):
    vid = 999 + idx
    snake = to_snake_case(v['name'])
    strid = to_string_id(v['name'])
    speed = props['speed']

    lines = []
    lines.append(f'/* {"─" * 66} */')
    lines.append(f'/*  #{idx}  {v["name"]} ({v["year"]}){"":>{60 - len(v["name"]) - len(str(v["year"])) - len(str(idx))}}*/')
    lines.append(f'/*  {v.get("type_desc", "")[:64]:<66} */')
    lines.append(f'/* {"─" * 66} */')
    lines.append('')
    lines.append(f'item(FEAT_AIRCRAFT, item_{snake}, {vid}) {{')
    lines.append(f'    property {{')
    lines.append(f'        name:                           string({strid});')
    lines.append(f'        climates_available:             bitmask(CLIMATE_TEMPERATE);')
    lines.append(f'        introduction_date:              date({v["year"]}, 1, 1);')
    lines.append(f'        model_life:                     {props["model_life"]};')
    lines.append(f'        vehicle_life:                   {props["vehicle_life"]};')
    lines.append(f'        reliability_decay:              {props["reliability_decay"]};')
    lines.append(f'        cost_factor:                    {props["cost_factor"]};')
    lines.append(f'        running_cost_factor:            {props["running_cost_factor"]};')
    lines.append(f'        aircraft_type:                  {props["aircraft_type"]};')
    lines.append(f'        acceleration:                   {props["acceleration"]};')
    lines.append(f'        speed:                          {speed} km/h;')
    lines.append(f'        passenger_capacity:             {props["passenger_capacity"]};')
    lines.append(f'        mail_capacity:                  {props["mail_capacity"]};')
    lines.append(f'        loading_speed:                  {props["loading_speed"]};')
    lines.append(f'        cargo_age_period:               {props["cargo_age_period"]};')
    lines.append(f'        refittable_cargo_classes:       {props["refit_classes"]};')
    lines.append(f'        non_refittable_cargo_classes:   {props["non_refit_classes"]};')
    lines.append(f'    }}')
    lines.append(f'}}')
    return '\n'.join(lines)


def gen_road_nml(v, idx, props):
    vid = 999 + idx
    snake = to_snake_case(v['name'])
    strid = to_string_id(v['name'])
    speed = props['speed']
    vtype_lower = v.get('vtype', '').lower()

    lines = []
    lines.append(f'/* {"─" * 66} */')
    lines.append(f'/*  #{idx}  {v["name"]} ({v["year"]}){"":>{60 - len(v["name"]) - len(str(v["year"])) - len(str(idx))}}*/')
    lines.append(f'/*  {v.get("type_desc", "")[:64]:<66} */')
    lines.append(f'/* {"─" * 66} */')
    lines.append('')
    lines.append(f'item(FEAT_ROADVEHS, item_{snake}, {vid}) {{')
    lines.append(f'    property {{')
    lines.append(f'        name:                           string({strid});')
    lines.append(f'        climates_available:             bitmask(CLIMATE_TEMPERATE);')
    lines.append(f'        introduction_date:              date({v["year"]}, 1, 1);')
    lines.append(f'        model_life:                     {props["model_life"]};')
    lines.append(f'        vehicle_life:                   {props["vehicle_life"]};')
    lines.append(f'        reliability_decay:              {props["reliability_decay"]};')
    lines.append(f'        cost_factor:                    {props["cost_factor"]};')
    lines.append(f'        running_cost_factor:            {props["running_cost_factor"]};')
    lines.append(f'        speed:                          {speed} km/h;')
    lines.append(f'        cargo_capacity:                 {props["cargo_capacity"]};')
    lines.append(f'        loading_speed:                  {props["loading_speed"]};')
    lines.append(f'        cargo_age_period:               {props["cargo_age_period"]};')
    lines.append(f'        refittable_cargo_classes:       {props["refit_classes"]};')
    lines.append(f'        non_refittable_cargo_classes:   {props["non_refit_classes"]};')
    lines.append(f'    }}')
    lines.append(f'}}')
    return '\n'.join(lines)


def gen_ship_nml(v, idx, props):
    vid = 999 + idx
    snake = to_snake_case(v['name'])
    strid = to_string_id(v['name'])
    speed = props['speed']

    lines = []
    lines.append(f'/* {"─" * 66} */')
    lines.append(f'/*  #{idx}  {v["name"]} ({v["year"]}){"":>{60 - len(v["name"]) - len(str(v["year"])) - len(str(idx))}}*/')
    lines.append(f'/*  {v.get("type_desc", "")[:64]:<66} */')
    lines.append(f'/* {"─" * 66} */')
    lines.append('')
    lines.append(f'item(FEAT_SHIPS, item_{snake}, {vid}) {{')
    lines.append(f'    property {{')
    lines.append(f'        name:                           string({strid});')
    lines.append(f'        climates_available:             bitmask(CLIMATE_TEMPERATE);')
    lines.append(f'        introduction_date:              date({v["year"]}, 1, 1);')
    lines.append(f'        model_life:                     {props["model_life"]};')
    lines.append(f'        vehicle_life:                   {props["vehicle_life"]};')
    lines.append(f'        reliability_decay:              {props["reliability_decay"]};')
    lines.append(f'        cost_factor:                    {props["cost_factor"]};')
    lines.append(f'        running_cost_factor:            {props["running_cost_factor"]};')
    lines.append(f'        speed:                          {speed} km/h;')
    lines.append(f'        cargo_capacity:                 {props["cargo_capacity"]};')
    lines.append(f'        loading_speed:                  {props["loading_speed"]};')
    lines.append(f'        cargo_age_period:               {props["cargo_age_period"]};')
    if props.get('is_passenger'):
        lines.append(f'        is_refittable:                  1;')
    else:
        lines.append(f'        is_refittable:                  1;')
    lines.append(f'        refittable_cargo_classes:       {props["refit_classes"]};')
    lines.append(f'        non_refittable_cargo_classes:   {props["non_refit_classes"]};')
    lines.append(f'    }}')
    lines.append(f'}}')
    return '\n'.join(lines)


def gen_train_nml(v, idx, props):
    vid = 999 + idx
    snake = to_snake_case(v['name'])
    strid = to_string_id(v['name'])
    speed = props['speed']

    lines = []
    lines.append(f'/* {"─" * 66} */')
    lines.append(f'/*  #{idx}  {v["name"]} ({v["year"]}){"":>{60 - len(v["name"]) - len(str(v["year"])) - len(str(idx))}}*/')
    lines.append(f'/*  {v.get("type_desc", "")[:64]:<66} */')
    lines.append(f'/* {"─" * 66} */')
    lines.append('')
    lines.append(f'item(FEAT_TRAINS, item_{snake}, {vid}) {{')
    lines.append(f'    property {{')
    lines.append(f'        name:                           string({strid});')
    lines.append(f'        climates_available:             bitmask(CLIMATE_TEMPERATE);')
    lines.append(f'        introduction_date:              date({v["year"]}, 1, 1);')
    lines.append(f'        model_life:                     {props["model_life"]};')
    lines.append(f'        vehicle_life:                   {props["vehicle_life"]};')
    lines.append(f'        reliability_decay:              {props["reliability_decay"]};')
    lines.append(f'        cost_factor:                    {props["cost_factor"]};')
    lines.append(f'        running_cost_factor:            {props["running_cost_factor"]};')
    lines.append(f'        running_cost_base:              {props["running_cost_base"]};')
    lines.append(f'        engine_class:                   {props["engine_class"]};')
    lines.append(f'        track_type:                     {props["track_type"]};')
    lines.append(f'        speed:                          {speed} km/h;')
    lines.append(f'        power:                          {props["power"]} hp;')
    lines.append(f'        weight:                         {props["weight"]} ton;')
    lines.append(f'        tractive_effort_coefficient:    {props["tractive_effort_coefficient"]:.2f};')
    lines.append(f'        loading_speed:                  {props["loading_speed"]};')
    lines.append(f'        cargo_age_period:               {props["cargo_age_period"]};')
    lines.append(f'    }}')
    lines.append(f'}}')
    return '\n'.join(lines)


def gen_wagon_nml(v, idx, props, feat):
    vid = 999 + idx
    snake = to_snake_case(v['name'])
    strid = to_string_id(v['name'])

    lines = []
    lines.append(f'/* {"─" * 66} */')
    lines.append(f'/*  #{idx}  {v["name"]} ({v["year"]}){"":>{60 - len(v["name"]) - len(str(v["year"])) - len(str(idx))}}*/')
    lines.append(f'/*  {v.get("type_desc", "")[:64]:<66} */')
    lines.append(f'/* {"─" * 66} */')
    lines.append('')
    lines.append(f'item({feat}, item_{snake}, {vid}) {{')
    lines.append(f'    property {{')
    lines.append(f'        name:                           string({strid});')
    lines.append(f'        climates_available:             bitmask(CLIMATE_TEMPERATE);')
    lines.append(f'        introduction_date:              date({v["year"]}, 1, 1);')
    lines.append(f'        model_life:                     {props["model_life"]};')
    lines.append(f'        vehicle_life:                   {props["vehicle_life"]};')
    lines.append(f'        reliability_decay:              {props["reliability_decay"]};')
    lines.append(f'        cost_factor:                    {props["cost_factor"]};')
    lines.append(f'        running_cost_factor:            {props["running_cost_factor"]};')
    lines.append(f'        cargo_capacity:                 {props["cargo_capacity"]};')
    lines.append(f'        loading_speed:                  {props["loading_speed"]};')
    lines.append(f'        cargo_age_period:               {props["cargo_age_period"]};')
    lines.append(f'        refittable_cargo_classes:       {props["cargo_classes"]};')
    lines.append(f'        non_refittable_cargo_classes:   bitmask();')
    if feat == 'FEAT_TRAINS':
        ec = v.get('engine_class', 'ENGINE_CLASS_STEAM')
        rcb = v.get('running_cost_base', 'RUNNING_COST_NONE')
        tt = v.get('track_type', 'RAIL')
        lines.append(f'        track_type:                     {tt};')
    lines.append(f'    }}')
    lines.append(f'}}')
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
#  File output helpers
# ---------------------------------------------------------------------------

def subdir_to_filename(subdir):
    """Map subdir like 'aircraft/airliners' to a single NML filename."""
    parts = subdir.split('/')
    if len(parts) >= 2:
        return parts[-1] + '.nml'
    return parts[0] + '.nml'


def write_nml_files(vehicles_by_subdir):
    """Write NML files, one per subdirectory."""
    for subdir, entries in sorted(vehicles_by_subdir.items()):
        dirpath = os.path.join(BASE_DIR, subdir)
        os.makedirs(dirpath, exist_ok=True)

        fname = subdir_to_filename(subdir)
        filepath = os.path.join(dirpath, fname)

        # Check for existing file (e.g. early_airliners.nml)
        # Our generated file uses the subdirectory name, won't conflict

        file_header = f'/**\n * {fname}\n *\n * Auto-generated NML vehicle definitions.\n * Vehicles from the master checklist.\n */\n\n'

        content = file_header + '\n\n'.join(entries) + '\n'

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f'  Wrote {filepath} ({len(entries)} vehicles)')


def write_lang_strings(lang_entries):
    """Append new language strings to english.lng."""
    lng_path = os.path.join(BASE_DIR, 'lang', 'english.lng')

    # Read existing content to avoid duplicates
    with open(lng_path, 'r', encoding='utf-8') as f:
        existing = f.read()

    new_entries = []
    for strid, display_name in lang_entries:
        if strid not in existing:
            # Pad for alignment (40 chars for the ID)
            padded = f'{strid:<40} :{display_name}'
            new_entries.append(padded)

    if new_entries:
        with open(lng_path, 'a', encoding='utf-8') as f:
            f.write('\n# Auto-generated vehicle names\n')
            f.write('\n'.join(new_entries))
            f.write('\n')

    print(f'  Added {len(new_entries)} new strings to english.lng')


def update_checklist(all_vehicles_ordered):
    """Re-read Checklist.md, mark NML column with ✅ for all processed vehicles."""
    checklist_path = os.path.join(BASE_DIR, 'Checklist.md')

    with open(checklist_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Build a set of checklist indices we've processed
    processed = set()
    for v in all_vehicles_ordered:
        processed.add(v['checklist_idx'])

    new_lines = []
    for line in lines:
        # Match checklist table rows: | N | Name | Type | Year | Graphics | NML | QA | Released |
        m = re.match(r'^(\|\s*(\d+)\s*\|.*?\|.*?\|.*?\|)(.*?)(\|)(.*?)(\|.*?\|.*?\|)\s*$', line)
        if m:
            idx = int(m.group(2))
            if idx in processed:
                # Ensure NML column has ✅
                prefix = m.group(1)
                gfx_col = m.group(3)
                sep = m.group(4)
                nml_col = m.group(5)
                suffix = m.group(6)

                if '✅' not in nml_col:
                    nml_col = ' ✅ '

                line = f'{prefix}{gfx_col}{sep}{nml_col}{suffix}\n'

        new_lines.append(line)

    with open(checklist_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f'  Updated Checklist.md — {len(processed)} vehicles marked')


# ---------------------------------------------------------------------------
#  Main
# ---------------------------------------------------------------------------

def main():
    print('=== NML Vehicle Generator ===\n')

    # ── Parse all source files ──
    print('Parsing Airplanes.md...')
    airplanes = parse_standard_table(
        os.path.join(BASE_DIR, 'Airplanes.md'),
        get_airplane_sections()
    )
    print(f'  Found {len(airplanes)} aircraft')

    print('Parsing Road.md (vehicles)...')
    road_vehs = parse_standard_table(
        os.path.join(BASE_DIR, 'Road.md'),
        get_road_sections()
    )
    print(f'  Found {len(road_vehs)} road vehicles')

    print('Parsing Road.md (trailers)...')
    road_trailers = parse_wagon_trailer_table(
        os.path.join(BASE_DIR, 'Road.md'),
        get_road_trailer_sections()
    )
    print(f'  Found {len(road_trailers)} road trailers')

    print('Parsing Ships.md...')
    ships = parse_standard_table(
        os.path.join(BASE_DIR, 'Ships.md'),
        get_ship_sections()
    )
    print(f'  Found {len(ships)} ships')

    print('Parsing Trains.md (engines)...')
    trains = parse_standard_table(
        os.path.join(BASE_DIR, 'Trains.md'),
        get_train_sections()
    )
    print(f'  Found {len(trains)} train engines')

    print('Parsing Trains.md (wagons)...')
    train_wagons = parse_wagon_trailer_table(
        os.path.join(BASE_DIR, 'Trains.md'),
        get_train_wagon_sections()
    )
    print(f'  Found {len(train_wagons)} train wagons')

    # ── Build ordered vehicle list matching checklist order ──
    # The checklist order is: airplanes, road_vehs, road_trailers, ships, trains, train_wagons
    all_vehicles = []
    all_vehicles.extend(airplanes)
    all_vehicles.extend(road_vehs)
    all_vehicles.extend(road_trailers)
    all_vehicles.extend(ships)
    all_vehicles.extend(trains)
    all_vehicles.extend(train_wagons)

    print(f'\nTotal parsed: {len(all_vehicles)} vehicles')

    # Assign checklist indices (1-based)
    for i, v in enumerate(all_vehicles, 1):
        v['checklist_idx'] = i

    # ── Generate NML and language strings ──
    vehicles_by_subdir = {}
    lang_entries = []
    count = 0

    for v in all_vehicles:
        idx = v['checklist_idx']

        # Skip first 10 (already hand-written)
        if idx < FIRST_NEW_INDEX:
            continue

        feat = v['feat']
        is_wagon = v.get('is_wagon', False)

        # Calculate properties
        if is_wagon:
            props = calc_wagon_props(v)
            nml_code = gen_wagon_nml(v, idx, props, feat)
        elif feat == 'FEAT_AIRCRAFT':
            props = calc_aircraft_props(v)
            nml_code = gen_aircraft_nml(v, idx, props)
        elif feat == 'FEAT_ROADVEHS':
            props = calc_road_props(v)
            nml_code = gen_road_nml(v, idx, props)
        elif feat == 'FEAT_SHIPS':
            props = calc_ship_props(v)
            nml_code = gen_ship_nml(v, idx, props)
        elif feat == 'FEAT_TRAINS':
            props = calc_train_props(v)
            nml_code = gen_train_nml(v, idx, props)
        else:
            continue

        subdir = v['subdir']
        if subdir not in vehicles_by_subdir:
            vehicles_by_subdir[subdir] = []
        vehicles_by_subdir[subdir].append(nml_code)

        # Language entry
        strid = to_string_id(v['name'])
        lang_entries.append((strid, v['name']))

        count += 1

    print(f'\nGenerated NML for {count} vehicles (skipping first {FIRST_NEW_INDEX - 1})')

    # ── Write files ──
    print('\nWriting NML files...')
    write_nml_files(vehicles_by_subdir)

    print('\nWriting language strings...')
    write_lang_strings(lang_entries)

    print('\nUpdating Checklist.md...')
    update_checklist(all_vehicles[FIRST_NEW_INDEX - 1:])

    print('\nDone!')


if __name__ == '__main__':
    main()
