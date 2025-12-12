

-- 2) Property damage (manufacture of parts and accessories for motor vehicles)
CREATE TABLE IF NOT EXISTS property_damage_index (
    year INTEGER PRIMARY KEY,
    small_car REAL,
    big_car REAL,
    two_wheeler REAL,
    ordinary_bus REAL,
    deluxe_bus REAL,
    lcv REAL,
    hcv REAL,
    mcv REAL
);

INSERT INTO property_damage_index VALUES
(2019, 113.2,113.2,113.2,113.2,113.2,113.2,113.2,113.2),
(2020, 115.5,115.5,115.5,115.5,115.5,115.5,115.5,115.5),
(2021, 120.6,120.6,120.6,120.6,120.6,120.6,120.6,120.6),
(2022, 128.5,128.5,128.5,128.5,128.5,128.5,128.5,128.5),
(2023, 128.2,128.2,128.2,128.2,128.2,128.2,128.2,128.2),
(2024, 129.0,129.0,129.0,129.0,129.0,129.0,129.0,129.0);



-- 4) Fuel, Engine oil, Other oil, Grease cost indices (note: values are indices; original units in source: petrol/diesel/engine oil are per-litre and grease per-kg)
CREATE TABLE IF NOT EXISTS fuel_and_oil_index (
    year INTEGER PRIMARY KEY,
    petrol REAL,   -- per-litre index
    diesel REAL,   -- per-litre index
    engine_oil REAL, -- per-litre index
    other_oil REAL,  -- per-litre index
    grease REAL      -- per-kg index
);

INSERT INTO fuel_and_oil_index VALUES
(2019, 85.4, 94.4, 131.2, 92.5, 92.5),
(2020, 74.2, 79.4, 134.0, 78.1, 78.1),
(2021, 109.9, 114.7, 157.8, 113.8, 113.8),
(2022, 159.8, 183.5, 174.7, 168.2, 168.2),
(2023, 158.9, 174.2, 188.0, 160.1, 160.1),
(2024, 154.3, 167.4, 190.2, 156.8, 156.8);

-- 5) Tyre cost index (tyre cost for each vehicle type)
CREATE TABLE IF NOT EXISTS tyre_cost_index (
    year INTEGER PRIMARY KEY,
    small_car REAL,
    big_car REAL,
    two_wheeler REAL,
    ordinary_bus REAL,
    deluxe_bus REAL,
    lcv REAL,
    hcv REAL,
    mcv REAL
);

INSERT INTO tyre_cost_index VALUES
(2019, 99.2, 99.2, 104.0, 97.5, 97.5, 97.5, 97.5, 97.5),
(2020, 98.7, 98.7, 102.0, 96.1, 96.1, 96.1, 96.1, 96.1),
(2021, 102.8,102.8,105.9,103.2,103.2,103.2,103.2,103.2),
(2022, 109.9,109.9,116.4,110.5,110.5,110.5,110.5,110.5),
(2023, 111.5,111.5,119.8,114.4,114.4,114.4,114.4,114.4),
(2024, 111.5,111.5,117.9,114.1,114.1,114.1,114.1,114.1);

-- 6) Spare part new price index (manufacture of parts and accessories for motor vehicles)
CREATE TABLE IF NOT EXISTS spare_part_index (
    year INTEGER PRIMARY KEY,
    small_car REAL,
    big_car REAL,
    two_wheeler REAL,
    ordinary_bus REAL,
    deluxe_bus REAL,
    lcv REAL,
    hcv REAL,
    mcv REAL
);

INSERT INTO spare_part_index VALUES
(2019,113.2,113.2,113.2,113.2,113.2,113.2,113.2,113.2),
(2020,115.5,115.5,115.5,115.5,115.5,115.5,115.5,115.5),
(2021,120.6,120.6,120.6,120.6,120.6,120.6,120.6,120.6),
(2022,128.5,128.5,128.5,128.5,128.5,128.5,128.5,128.5),
(2023,128.2,128.2,128.2,128.2,128.2,128.2,128.2,128.2),
(2024,129.0,129.0,129.0,129.0,129.0,129.0,129.0,129.0);

-- 7) Fixed and depreciation cost index (manufacture of motor vehicles, trailers and semi-trailers)
CREATE TABLE IF NOT EXISTS fixed_depreciation_index (
    year INTEGER PRIMARY KEY,
    small_car REAL,
    big_car REAL,
    two_wheeler REAL,
    ordinary_bus REAL,
    deluxe_bus REAL,
    lcv REAL,
    hcv REAL,
    mcv REAL
);

INSERT INTO fixed_depreciation_index VALUES
(2019,113.8,113.8,113.8,113.8,113.8,113.8,113.8,113.8),
(2020,116.9,116.9,116.9,116.9,116.9,116.9,116.9,116.9),
(2021,121.1,121.1,121.1,121.1,121.1,121.1,121.1,121.1),
(2022,127.1,127.1,127.1,127.1,127.1,127.1,127.1,127.1),
(2023,128.0,128.0,128.0,128.0,128.0,128.0,128.0,128.0),
(2024,129.6,129.6,129.6,129.6,129.6,129.6,129.6,129.6);

-- 8) Commodity holding cost (FUEL & POWER) - same values across vehicle types in the source
CREATE TABLE IF NOT EXISTS commodity_holding_cost_index (
    year INTEGER PRIMARY KEY,
    small_car REAL,
    big_car REAL,
    two_wheeler REAL,
    ordinary_bus REAL,
    deluxe_bus REAL,
    lcv REAL,
    hcv REAL,
    mcv REAL
);

INSERT INTO commodity_holding_cost_index VALUES
(2019,101.7,101.7,101.7,101.7,101.7,101.7,101.7,101.7),
(2020,93.3,93.3,93.3,93.3,93.3,93.3,93.3,93.3),
(2021,116.1,116.1,116.1,116.1,116.1,116.1,116.1,116.1),
(2022,155.2,155.2,155.2,155.2,155.2,155.2,155.2,155.2),
(2023,152.7,152.7,152.7,152.7,152.7,152.7,152.7,152.7),
(2024,150.4,150.4,150.4,150.4,150.4,150.4,150.4,150.4);

-- 9) Passenger and Crew cost (years with passenger and crew cost indices)
CREATE TABLE IF NOT EXISTS passenger_crew_cost_index (
    year INTEGER PRIMARY KEY,
    passenger_cost REAL,
    crew_cost REAL
);

INSERT INTO passenger_crew_cost_index VALUES
(2019, 138.58, 118.07),
(2020, 147.91, 131.77),
(2021, 155.33, 145.91),
(2022, 166.94, 159.05),
(2023, 176.38, 160.28),
(2024, 184.27, 164.18);


