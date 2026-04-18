#!/usr/bin/env python3
"""Parse the four vehicle markdown files and generate a master checklist."""

import re

def parse_vehicles_from_file(filepath, sections_config):
    """
    Parse a markdown file and extract vehicle rows from tables.
    
    sections_config is a list of dicts:
      { 'header_pattern': regex to match section header,
        'type': the Type label,
        'name_col': index of the name column (0-based in data cols),
        'year_col': index of the year column (0-based in data cols) }
    
    We detect sections by matching heading lines (## or bold text),
    then extract table rows within each section.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    vehicles = []
    current_type = None
    in_table = False
    col_count = 0
    
    # Build a map of section patterns
    # We'll track current section by scanning for headings or bold markers
    
    # Simple approach: scan through lines, detect section changes, parse table rows
    for line in lines:
        stripped = line.strip()
        
        # Check for section headers (## headings or --- separators with context)
        for sec in sections_config:
            if re.search(sec['header_pattern'], stripped, re.IGNORECASE):
                current_type = sec['type']
                name_col = sec.get('name_col', 1)
                year_col = sec.get('year_col', 0)
                in_table = False  # Reset table state for new section
                break
        
        if current_type is None:
            continue
            
        # Skip non-table lines
        if not stripped.startswith('|'):
            in_table = False
            continue
        
        # Skip separator lines like |---|---|
        if re.match(r'^\|[\s\-|:]+\|$', stripped):
            in_table = True
            continue
        
        # Skip header rows (contain "Year" or "Name" as headers)
        cols = [c.strip() for c in stripped.split('|')]
        # Remove empty first/last from split
        cols = [c for c in cols if c != '' or True]
        if stripped.startswith('|'):
            cols = stripped.split('|')[1:-1]  # Remove empty first and last
            cols = [c.strip() for c in cols]
        
        if not cols:
            continue
            
        # Check if this is a header row
        if cols[0] in ('Year', 'Year ') or (len(cols) > 1 and cols[1] in ('Name', 'Name / Class', 'Name / Class ')):
            in_table = True
            continue
        
        # Skip era/section separator rows (contain ** bold markers)
        if '**' in cols[0] or (len(cols) > 1 and cols[0].strip() == '' and '**' in cols[1]):
            continue
            
        # Skip rows where year column is empty or just whitespace
        if len(cols) <= max(year_col, name_col):
            continue
            
        year_str = cols[year_col].strip().replace('**', '').strip()
        name_str = cols[name_col].strip().replace('**', '').strip()
        
        if not year_str or not name_str:
            continue
            
        # Skip if year doesn't look like a year or TBD
        if not re.match(r'^\d{4}$', year_str) and year_str != 'TBD':
            continue
        
        vehicles.append({
            'name': name_str,
            'year': year_str,
            'type': current_type
        })
    
    return vehicles


def main():
    all_vehicles = []
    
    # ====== AIRPLANES ======
    airplane_sections = [
        {'header_pattern': r'## Major Airliners', 'type': 'Airplane', 'name_col': 1, 'year_col': 0},
        {'header_pattern': r'## Airships & Blimps', 'type': 'Airship', 'name_col': 1, 'year_col': 0},
        {'header_pattern': r'## Helicopters', 'type': 'Helicopter', 'name_col': 1, 'year_col': 0},
        {'header_pattern': r'## Futuristic Aircraft', 'type': 'Futuristic Aircraft', 'name_col': 1, 'year_col': 0},
        {'header_pattern': r'## Aircraft Refit', 'type': '_SKIP_', 'name_col': 1, 'year_col': 0},
    ]
    # More granular futuristic sub-types
    airplane_sections_v2 = [
        {'header_pattern': r'## Major Airliners', 'type': 'Airplane'},
        {'header_pattern': r'## Airships & Blimps', 'type': 'Airship'},
        {'header_pattern': r'## Helicopters', 'type': 'Helicopter'},
        {'header_pattern': r'\*\*Near-Future Airliners', 'type': 'Futuristic Airplane'},
        {'header_pattern': r'\*\*Supersonic & Hypersonic', 'type': 'Futuristic Airplane'},
        {'header_pattern': r'\*\*Futuristic Helicopters', 'type': 'Futuristic Helicopter'},
        {'header_pattern': r'\*\*Futuristic eVTOL', 'type': 'Futuristic eVTOL'},
        {'header_pattern': r'\*\*Futuristic Airships', 'type': 'Futuristic Airship'},
        {'header_pattern': r'## Aircraft Refit', 'type': '_SKIP_'},
        {'header_pattern': r'### General Refit', 'type': '_SKIP_'},
    ]
    
    for sec in airplane_sections_v2:
        sec.setdefault('name_col', 1)
        sec.setdefault('year_col', 0)
    
    avs = parse_vehicles_from_file('Airplanes.md', airplane_sections_v2)
    all_vehicles.extend([v for v in avs if v['type'] != '_SKIP_'])
    
    # ====== ROAD ======
    road_sections = [
        {'header_pattern': r'## Buses', 'type': 'Bus'},
        {'header_pattern': r'## Trucks', 'type': 'Truck'},
        {'header_pattern': r'## Cars', 'type': 'Car'},
        {'header_pattern': r'## Futuristic Road Vehicles', 'type': '_FUTURISTIC_ROAD_'},
        {'header_pattern': r'\*\*Near-Future Buses', 'type': 'Futuristic Bus'},
        {'header_pattern': r'\*\*Near-Future Trucks', 'type': 'Futuristic Truck'},
        {'header_pattern': r'\*\*Near-Future Cars', 'type': 'Futuristic Car'},
        {'header_pattern': r'\*\*Far-Future Road', 'type': 'Futuristic Road Vehicle'},
        {'header_pattern': r'## Truck Trailers', 'type': '_TRAILER_SECTION_'},
        {'header_pattern': r'### Passenger Trailers', 'type': 'Bus Trailer'},
        {'header_pattern': r'### Mail.*Parcel Trailers', 'type': 'Mail Trailer'},
        {'header_pattern': r'### Armoured Trailers', 'type': 'Armoured Trailer'},
        {'header_pattern': r'### Grain.*Wheat Trailers', 'type': 'Grain Trailer'},
        {'header_pattern': r'### Livestock Trailers', 'type': 'Livestock Trailer'},
        {'header_pattern': r'### Coal Trailers', 'type': 'Coal Trailer'},
        {'header_pattern': r'### Iron Ore.*Mineral Trailers', 'type': 'Ore Trailer'},
        {'header_pattern': r'### Steel.*Metal Flatbed', 'type': 'Steel Trailer'},
        {'header_pattern': r'### Oil.*Petroleum Tanker Trailers', 'type': 'Oil Tanker Trailer'},
        {'header_pattern': r'### Wood.*Timber Trailers', 'type': 'Timber Trailer'},
        {'header_pattern': r'### Goods.*General Cargo Trailers', 'type': 'Goods Trailer'},
        {'header_pattern': r'### Food.*Refrigerated Trailers', 'type': 'Food Trailer'},
        {'header_pattern': r'### Paper.*Covered Trailers', 'type': 'Paper Trailer'},
        {'header_pattern': r'### Rubber.*Fruit.*Tropical.*Trailers', 'type': 'Tropical Cargo Trailer'},
        {'header_pattern': r'### Copper.*Water.*Misc.*Trailers', 'type': 'Bulk Trailer'},
    ]
    for sec in road_sections:
        sec.setdefault('name_col', 1)
        sec.setdefault('year_col', 0)
    
    rvs = parse_vehicles_from_file('Road.md', road_sections)
    all_vehicles.extend([v for v in rvs if not v['type'].startswith('_')])
    
    # ====== SHIPS ======
    ship_sections = [
        {'header_pattern': r'## Passenger Ships & Ferries', 'type': 'Passenger Ship'},
        {'header_pattern': r'## Cargo Ships', 'type': 'Cargo Ship'},
        {'header_pattern': r'## Specialised & Smaller', 'type': 'Specialised Vessel'},
        {'header_pattern': r'## Futuristic Ships', 'type': '_FUTURISTIC_SHIP_'},
        {'header_pattern': r'\*\*Near-Future Passenger Ships', 'type': 'Futuristic Passenger Ship'},
        {'header_pattern': r'\*\*Near-Future Cargo Ships', 'type': 'Futuristic Cargo Ship'},
        {'header_pattern': r'\*\*Near-Future Specialised', 'type': 'Futuristic Specialised Vessel'},
        {'header_pattern': r'\*\*Far-Future Ships', 'type': 'Futuristic Ship'},
        {'header_pattern': r'## Ship Refit', 'type': '_SKIP_'},
        {'header_pattern': r'### General Refit', 'type': '_SKIP_'},
    ]
    for sec in ship_sections:
        sec.setdefault('name_col', 1)
        sec.setdefault('year_col', 0)
    
    svs = parse_vehicles_from_file('Ships.md', ship_sections)
    all_vehicles.extend([v for v in svs if not v['type'].startswith('_')])
    
    # ====== TRAINS ======
    train_sections = [
        {'header_pattern': r'## Steam Locomotives', 'type': 'Steam Locomotive'},
        {'header_pattern': r'## Diesel Locomotives', 'type': 'Diesel Locomotive'},
        {'header_pattern': r'## Electric Locomotives', 'type': 'Electric Locomotive'},
        {'header_pattern': r'## Electric Multiple Units & High-Speed', 'type': 'EMU / High-Speed Train'},
        {'header_pattern': r'## Diesel Multiple Units & Railcars', 'type': 'DMU / Railcar'},
        {'header_pattern': r'## Metro.*Rapid Transit', 'type': 'Metro Train'},
        {'header_pattern': r'## Futuristic Trains', 'type': '_FUTURISTIC_TRAIN_'},
        {'header_pattern': r'\*\*Near-Future Locomotives', 'type': 'Futuristic Locomotive'},
        {'header_pattern': r'\*\*Near-Future High-Speed', 'type': 'Futuristic High-Speed Train'},
        {'header_pattern': r'\*\*Near-Future Regional & Metro', 'type': 'Futuristic Regional/Metro'},
        {'header_pattern': r'\*\*Near-Future Freight Trains', 'type': 'Futuristic Freight Train'},
        {'header_pattern': r'\*\*Far-Future Trains', 'type': 'Futuristic Train'},
        {'header_pattern': r'## Wagons.*Rolling Stock', 'type': '_WAGON_SECTION_'},
        {'header_pattern': r'### Passenger Coaches', 'type': 'Passenger Coach'},
        {'header_pattern': r'### Mail Vans', 'type': 'Mail Van'},
        {'header_pattern': r'### Armoured Vans', 'type': 'Armoured Van'},
        {'header_pattern': r'### Grain.*Wheat Hoppers', 'type': 'Grain Hopper'},
        {'header_pattern': r'### Livestock Wagons', 'type': 'Livestock Wagon'},
        {'header_pattern': r'### Coal Wagons', 'type': 'Coal Wagon'},
        {'header_pattern': r'### Iron Ore Wagons', 'type': 'Iron Ore Wagon'},
        {'header_pattern': r'### Steel.*Metal Wagons', 'type': 'Steel Wagon'},
        {'header_pattern': r'### Oil.*Petroleum Tank', 'type': 'Oil Tank Wagon'},
        {'header_pattern': r'### Wood.*Timber Wagons', 'type': 'Timber Wagon'},
        {'header_pattern': r'### Goods.*General Cargo', 'type': 'Goods Van'},
        {'header_pattern': r'### Food.*Refrigerated', 'type': 'Food/Reefer Van'},
        {'header_pattern': r'### Paper.*Covered Wagons', 'type': 'Paper Wagon'},
        {'header_pattern': r'### Rubber.*Fruit.*Tropical', 'type': 'Tropical Cargo Wagon'},
        {'header_pattern': r'### Copper.*Water.*Misc', 'type': 'Bulk Wagon'},
    ]
    for sec in train_sections:
        sec.setdefault('name_col', 1)
        sec.setdefault('year_col', 0)
    
    tvs = parse_vehicles_from_file('Trains.md', train_sections)
    all_vehicles.extend([v for v in tvs if not v['type'].startswith('_')])
    
    # ====== Generate the checklist ======
    
    lines = []
    lines.append('# Vehicle Checklist')
    lines.append('')
    lines.append(f'Total vehicles: **{len(all_vehicles)}**')
    lines.append('')
    lines.append('| # | Vehicle Name | Type | Year | Graphics | NML | QA | Released |')
    lines.append('|---|---|---|---|---|---|---|---|')
    
    for idx, v in enumerate(all_vehicles, 1):
        name = v['name'].replace('|', '\\|')
        vtype = v['type']
        year = v['year']
        lines.append(f'| {idx} | {name} | {vtype} | {year} | | | | |')
    
    lines.append('')
    
    # Add summary
    lines.append('---')
    lines.append('')
    lines.append('## Summary by Type')
    lines.append('')
    lines.append('| Type | Count |')
    lines.append('|---|---|')
    
    type_counts = {}
    for v in all_vehicles:
        t = v['type']
        type_counts[t] = type_counts.get(t, 0) + 1
    
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        lines.append(f'| {t} | {c} |')
    
    lines.append(f'| **Total** | **{len(all_vehicles)}** |')
    lines.append('')
    
    with open('Checklist.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f'Generated Checklist.md with {len(all_vehicles)} vehicles')
    print(f'\nBreakdown by type:')
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f'  {t}: {c}')


if __name__ == '__main__':
    main()
