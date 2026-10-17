
LOAD DATA LOCAL INFILE
'smartphone-data-intelligence/data/processed/smartphones_cleaned.csv'
INTO TABLE smartphones
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    brand_name,
    model,
    price,
    @avg_rating,
    `5G_or_not`,
    processor_brand,
    num_cores,
    processor_speed,
    battery_capacity,
    fast_charging_available,
    @fast_charging,
    ram_capacity,
    internal_memory,
    screen_size,
    refresh_rate,
    num_rear_cameras,
    os,
    primary_camera_rear,
    primary_camera_front,
    extended_memory_available,
    resolution_height,
    resolution_width
)
SET
    avg_rating = NULLIF(@avg_rating, ''),
    fast_charging = NULLIF(@fast_charging, '');
