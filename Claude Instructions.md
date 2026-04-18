# Claude Instructions — NML Vehicle Generation

You are helping generate NML (NewGRF Meta Language) code for an OpenTTD vehicle set containing ~1,600 vehicles across four feature types: aircraft, road vehicles, ships, and trains. The vehicle specifications are defined in markdown files (`Airplanes.md`, `Road.md`, `Ships.md`, `Trains.md`) and tracked in `Checklist.md`.

## Project Structure

```
newgrf_vehicles/
├── darwin_aircraft.nml          # Reference NML file (3 aircraft)
├── Makefile                     # Build: nmlc --grf=<name>.grf <name>.nml
├── lang/english.lng             # Language strings
├── Checklist.md                 # Master vehicle index (1,607 vehicles)
├── Airplanes.md                 # Aircraft specs + refit tables
├── Road.md                      # Buses, trucks, cars + trailer specs
├── Ships.md                     # Passenger, cargo, specialised + refit tables
├── Trains.md                    # Steam/diesel/electric/EMU/DMU/metro + wagon specs
├── aircraft/                    # NML output: airliners/, airships/, helicopters/, evtol/
├── road/                        # NML output: buses/, trucks/, cars/, trailers/
├── ships/                       # NML output: passenger/, cargo/, specialised/
└── trains/                      # NML output: steam/, diesel/, electric/, emu-highspeed/,
                                 #             dmu-railcars/, metro/, wagons/
```

## NML Code Style

Follow the conventions in `darwin_aircraft.nml`:

```nml
item(FEAT_AIRCRAFT, item_boeing_747_100, 500) {
    property {
        name:                   string(STR_BOEING_747_100_NAME);
        climates_available:     bitmask(CLIMATE_TEMPERATE);
        introduction_date:      date(1969, 2, 9);
        model_life:             30;
        vehicle_life:           25;
        reliability_decay:      20;
        cost_factor:            80;
        running_cost_factor:    220;
        aircraft_type:          AIRCRAFT_TYPE_LARGE;
        acceleration:           35;
        speed:                  895 km/h;
        passenger_capacity:     452;
        mail_capacity:          50;
        loading_speed:          12;
        cargo_age_period:       340;
        refittable_cargo_classes:     bitmask(CC_PASSENGERS, CC_MAIL);
        non_refittable_cargo_classes: bitmask();
    }
}
```

- Use `item_<snake_case_name>` for item identifiers
- Use `STR_<UPPER_SNAKE_CASE>_NAME` for string identifiers
- Align property values with consistent whitespace
- Add a block comment header above each item with vehicle ID and brief description
- Group related vehicles in a single `.nml` file per subcategory

## Feature Types and Required Properties

### All Vehicle Types (Common)

| Property | Range | Notes |
|----------|-------|-------|
| `name` | string(STR_xxx) | Language string reference |
| `climates_available` | bitmask | Use `bitmask(CLIMATE_TEMPERATE)` — this set is temperate only |
| `introduction_date` | date(yyyy, m, d) | From the Year column in spec tables |
| `model_life` | 0–254 years, or `VEHICLE_NEVER_EXPIRES` | How long the model stays in the purchase list |
| `vehicle_life` | 0–255 years | Lifespan of an individual purchased vehicle |
| `reliability_decay` | 0–255 | Default 20. Higher = faster decay, more servicing needed |
| `cost_factor` | 0–255 | Multiplier to base purchase cost |
| `running_cost_factor` | 0–255 | Multiplier to base running costs |
| `loading_speed` | 0–255 | Cargo units loaded per tick interval (see below) |
| `cargo_age_period` | 0–65535 | Ticks before cargo ages one step. Default 185. Higher = slower aging = better |
| `refittable_cargo_classes` | bitmask(CC_xxx) | Cargo classes the vehicle can refit to |
| `non_refittable_cargo_classes` | bitmask(CC_xxx) | Cargo classes explicitly excluded |

### Trains (FEAT_TRAINS)

| Property | Range | Notes |
|----------|-------|-------|
| `sprite_id` | `SPRITE_ID_NEW_TRAIN` | Required for custom graphics |
| `speed` | 0–65000 (float, speed units) | Use `km/h` suffix |
| `power` | 0–65000 hp | Use `hp` suffix |
| `weight` | 0–1279 ton | Use `ton` suffix |
| `tractive_effort_coefficient` | 0.0–1.0 | TE (kN) = coefficient × 9.8 × weight (tons) |
| `air_drag_coefficient` | 0.0–1.0 | Default ≈ 8 / max_speed_kmh |
| `running_cost_base` | `RUNNING_COST_STEAM` / `DIESEL` / `ELECTRIC` / `NONE` | Determines base cost category |
| `engine_class` | `ENGINE_CLASS_STEAM` / `DIESEL` / `ELECTRIC` / `MONORAIL` / `MAGLEV` | Affects livery, sound, visual effect |
| `track_type` | Railtypetable entry | Default: `RAIL`, `ELRL`, `MONO`, `MGLV` |
| `cargo_capacity` | 0–255 | For wagons. Pax = 4× base, mail/goods = 2× base |
| `default_cargo_type` | Cargo label | e.g. `PASS`, `COAL`, `MAIL` |
| `length` | 1–8 | 8 = full length (VEHICLE_LENGTH) |
| `dual_headed` | 0 or 1 | 1 for dual-headed engines |
| `misc_flags` | bitmask(TRAIN_FLAG_xxx) | `TILT`, `2CC`, `MU`, `AUTOREFIT` |
| `visual_effect_and_powered` | visual_effect_and_powered(...) | Steam/diesel/electric visual effects |

### Road Vehicles (FEAT_ROADVEHS)

| Property | Range | Notes |
|----------|-------|-------|
| `sprite_id` | `SPRITE_ID_NEW_ROADVEH` | Required for custom graphics |
| `speed` | 0–511 km/h | Use `km/h` suffix |
| `power` | 0–2550 hp | Use `hp` suffix |
| `weight` | 0–63.75 ton | Use `ton` suffix |
| `tractive_effort_coefficient` | 0.0–1.0 | Default 0.3 |
| `running_cost_base` | `RUNNING_COST_ROADVEH` / `DIESEL` / `NONE` | |
| `cargo_capacity` | 0–255 | Pax = 4×, mail/goods = 2× |
| `length` | 1–8 | 8 = full length |
| `misc_flags` | bitmask(ROADVEH_FLAG_xxx) | `TRAM`, `2CC`, `AUTOREFIT` |

### Ships (FEAT_SHIPS)

| Property | Range | Notes |
|----------|-------|-------|
| `sprite_id` | `SPRITE_ID_NEW_SHIP` | Required for custom graphics |
| `speed` | 0–127 km/h (0–32767 in OpenTTD 14+) | Use `km/h` suffix |
| `cargo_capacity` | 0–255 | NOT affected by cargo type (unlike other features) |
| `is_refittable` | 0 or 1 | Must be 1 for refit classes to take effect |
| `ocean_speed_fraction` | 0.0–1.0 | Speed fraction on ocean tiles (default 1.0) |
| `canal_speed_fraction` | 0.0–1.0 | Speed fraction on canal tiles (default 1.0) |
| `acceleration` | 1–255 | ~0.5 km/h per tick. Default 1 (OpenTTD 14+) |

### Aircraft (FEAT_AIRCRAFT)

| Property | Range | Notes |
|----------|-------|-------|
| `sprite_id` | `SPRITE_ID_NEW_AIRCRAFT` | Required for custom graphics |
| `speed` | 0–3280 km/h | Use `km/h` suffix |
| `aircraft_type` | `AIRCRAFT_TYPE_HELICOPTER` / `SMALL` / `LARGE` | Large = high crash rate on small airports |
| `acceleration` | 0–255 | Default aircraft use 18–50 |
| `passenger_capacity` | 0–65536 | Passenger compartment |
| `mail_capacity` | 0–255 | Mail compartment (added to pax cap when refitted to non-pax) |
| `range` | 0–2894 | Max euclidean distance between airports. 0 = unlimited |

## Useful Expressions and Formulas

### Cost Factor (0–255)

The `cost_factor` is a multiplier applied to the vehicle type's base purchase cost. Scale relative to vehicle capability:

```
For trains:      cost_factor ≈ (power_hp / 100) × era_multiplier
For road vehs:   cost_factor ≈ (capacity / 10) + (speed_kmh / 20)
For ships:       cost_factor ≈ (capacity / 50) + (speed_kmh / 5)
For aircraft:    cost_factor ≈ (pax_capacity / 20) + (speed_kmh / 100)
```

**Era multipliers** (adjust for inflation and technology):
| Era | Multiplier |
|-----|-----------|
| Pre-1920 | 0.5–0.8 |
| 1920–1950 | 0.8–1.2 |
| 1950–1980 | 1.0–1.5 |
| 1980–2010 | 1.2–2.0 |
| 2010+ | 1.5–2.5 |
| Futuristic | 2.0–3.0 |

Clamp final result to 1–255. Use higher values for premium/luxury vehicles, lower for utility/austerity models.

### Running Cost Factor (0–255)

The `running_cost_factor` is a multiplier to the base running cost (determined by `running_cost_base` for trains/road vehicles). Running costs should reflect fuel consumption, crew, and maintenance:

```
For trains (steam):    running_cost_factor ≈ (power_hp / 30) + 20
For trains (diesel):   running_cost_factor ≈ (power_hp / 40) + 15
For trains (electric): running_cost_factor ≈ (power_hp / 50) + 10
For road vehicles:     running_cost_factor ≈ (speed_kmh / 5) + (capacity / 10) + 10
For ships:             running_cost_factor ≈ (speed_kmh × 2) + (capacity / 100) + 10
For aircraft:          running_cost_factor ≈ (speed_kmh / 10) + (pax_capacity / 5) + 50
```

Older vehicles should have proportionally higher running costs (less efficient). Clamp to 1–255.

### Loading Speed

Loading speed determines how quickly cargo is loaded/unloaded. The loading interval varies by feature:

| Feature | Tick Interval | Default loading_speed |
|---------|--------------|----------------------|
| Trains | Every 40 ticks | 5 |
| Road vehicles | Every 20 ticks | 5 |
| Ships | Every 10 ticks | 10 |
| Aircraft | Every 20 ticks | 20 |

**Scaling by era and capacity:**

```
loading_speed ≈ base × era_factor × capacity_factor

Era factors:
  Pre-1920:  0.5   (manual labour, slow cranes)
  1920–1950: 0.75  (early mechanisation)
  1950–1970: 1.0   (forklifts, conveyors)
  1970–2000: 1.5   (containerisation, jet bridges)
  2000+:     2.0   (automated systems)
  Futuristic: 3.0  (robotic handling)

Capacity factor (larger vehicles need faster loading to stay competitive):
  < 50 units:   1.0
  50–200 units:  1.25
  200–500 units: 1.5
  > 500 units:   2.0
```

Clamp to 1–255. Round to nearest integer.

### Cargo Age Period

`cargo_age_period` controls how fast cargo "spoils" (payment decreases). Default is 185 ticks (≈2.5 days). **Higher values = slower aging = better for passengers/perishables.**

```
cargo_age_period = 185 × comfort_modifier

Comfort modifiers by era:
  Pre-1920:  0.75  (rough ride, no climate control → 139)
  1920–1950: 1.0   (basic comfort → 185)
  1950–1970: 1.25  (pressurised cabins, A/C → 231)
  1970–2000: 1.5   (improved suspension, amenities → 278)
  2000+:     1.75  (premium comfort, wi-fi → 324)
  Futuristic: 2.5  (advanced life support → 463)
```

For freight-only vehicles, leave at default (185) or omit. For refrigerated/climate-controlled vehicles carrying perishables, multiply by an additional 1.25–1.5.

### Train Weight and Tractive Effort

```
weight: Use the real-world weight in tonnes from the spec table.
        For wagons, include typical loaded weight.

tractive_effort_coefficient: Fraction of weight available as pull force.
  Steam:    0.20–0.30  (typically 0.25)
  Diesel:   0.25–0.35  (typically 0.30)
  Electric: 0.25–0.35  (typically 0.30)
  Modern:   0.30–0.40  (high-adhesion bogies)

Resulting tractive effort (kN) = coefficient × 9.8 × weight_tonnes
```

### Train Power

Use the Horsepower column directly from the spec tables. NML accepts `hp` as a unit suffix:

```nml
power: 2200 hp;
```

### Speed

Always use `km/h` suffix for clarity. Take the Cruising Speed column from spec tables directly:

```nml
speed: 895 km/h;   /* aircraft */
speed: 130 km/h;   /* train */
speed: 48 km/h;    /* ship */
speed: 80 km/h;    /* road vehicle */
```

### Model Life and Vehicle Life

```
model_life: How long the vehicle type stays in the purchase menu.
  Short-lived models:  15–20 years
  Standard models:     20–30 years
  Long-lived classics: 30–50 years
  Iconic vehicles:     VEHICLE_NEVER_EXPIRES (use sparingly)

vehicle_life: How long an individual purchased vehicle lasts.
  Early era:     15–20 years
  Mid era:       20–30 years
  Modern era:    25–35 years
  Futuristic:    30–50 years

Rule of thumb: vehicle_life ≈ model_life + 5 years
```

### Reliability Decay

```
reliability_decay: Rate of reliability decrease. Default 20.
  Very reliable:   10–15  (quality engineering, e.g. Japanese trains)
  Standard:        18–22  (most vehicles)
  Unreliable:      25–35  (experimental/prototype vehicles)
  Very unreliable: 35–50  (futuristic prototypes, early pioneers)
```

## Cargo Classes Reference

| Constant | Cargo Types |
|----------|------------|
| `CC_PASSENGERS` | Passengers |
| `CC_MAIL` | Mail |
| `CC_EXPRESS` | Valuables, gold, diamonds |
| `CC_ARMOURED` | Valuables, gold, diamonds (armoured) |
| `CC_BULK` | Coal, ore, grain, sand |
| `CC_PIECE_GOODS` | Goods, food, livestock, steel |
| `CC_LIQUID` | Oil, water |
| `CC_REFRIGERATED` | Food, fruit |
| `CC_HAZARDOUS` | Oil, chemicals |
| `CC_COVERED` | Food, goods, grain (covered transport) |
| `CC_OVERSIZED` | Wood, steel, vehicles |
| `CC_POWDERIZED` | Cement, ore dust |
| `CC_NON_POURABLE` | Goods, livestock, vehicles |

### Typical Refit Configurations

**Passenger vehicle:**
```nml
refittable_cargo_classes:     bitmask(CC_PASSENGERS, CC_MAIL);
non_refittable_cargo_classes: bitmask();
```

**General freight (trains/ships):**
```nml
refittable_cargo_classes:     bitmask(CC_BULK, CC_PIECE_GOODS, CC_COVERED, CC_LIQUID);
non_refittable_cargo_classes: bitmask(CC_PASSENGERS);
```

**Tanker:**
```nml
refittable_cargo_classes:     bitmask(CC_LIQUID);
non_refittable_cargo_classes: bitmask(CC_PASSENGERS, CC_BULK);
```

**Refrigerated:**
```nml
refittable_cargo_classes:     bitmask(CC_REFRIGERATED, CC_PIECE_GOODS);
non_refittable_cargo_classes: bitmask(CC_BULK, CC_LIQUID);
```

## Language File Format

Add entries to `lang/english.lng`:

```
STR_BOEING_747_100_NAME    :Boeing 747-100
STR_DC3_NAME               :Douglas DC-3
STR_MALLARD_NAME           :LNER A4 Mallard
```

Use the exact vehicle name from the spec tables. Pad with spaces for alignment.

## Workflow

1. Pick a vehicle from `Checklist.md`
2. Look up its specs in the corresponding markdown file (year, capacity, speed, type)
3. Look up its refit properties if a refit table exists for that vehicle or a similar era vehicle
4. Calculate properties using the formulas above
5. Generate the NML item block following the code style
6. Add the language string to `lang/english.lng`
7. Place the NML file in the appropriate subdirectory
8. Mark the NML column in `Checklist.md` with ✅

## Prompt Template

When asking Claude to generate NML for a vehicle, provide:

```
Generate NML code for the following vehicle:

Name: Boeing 747-100
Feature: FEAT_AIRCRAFT
Year: 1969
Speed: 895 km/h
Capacity: 452 passengers
Mail: 50
Type: AIRCRAFT_TYPE_LARGE
Aircraft type: Wide-body jet

Use the formulas from "Claude Instructions.md" to calculate cost_factor,
running_cost_factor, loading_speed, and cargo_age_period. Place in aircraft/airliners/.
```

## NML Reference

- NML Vehicle Properties: https://newgrf-specs.tt-wiki.net/wiki/NML:Vehicles
- NML Block Syntax: https://newgrf-specs.tt-wiki.net/wiki/NML:Block_syntax
- NML Expressions & Units: https://newgrf-specs.tt-wiki.net/wiki/NML:Units
- NML Cargo Classes: https://newgrf-specs.tt-wiki.net/wiki/NML:Cargos
