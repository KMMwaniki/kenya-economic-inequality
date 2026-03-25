-- =====================================================
-- Kenya County Economic Inequality Analysis
-- Database Setup Script
-- =====================================================

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS counties;
DROP TABLE IF EXISTS demographics;
DROP TABLE IF EXISTS infrastructure;
DROP TABLE IF EXISTS health;
DROP TABLE IF EXISTS education;

-- Create counties table with regional classifications
CREATE TABLE counties (
    county_id INTEGER PRIMARY KEY,
    county_name TEXT NOT NULL,
    region TEXT NOT NULL,
    sub_region TEXT
);

-- Create demographics table
CREATE TABLE demographics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    county_id INTEGER,
    year INTEGER,
    population INTEGER,
    poverty_rate DECIMAL(5,2),
    unemployment_rate DECIMAL(5,2),
    gini_coefficient DECIMAL(4,3),
    FOREIGN KEY (county_id) REFERENCES counties(county_id)
);

-- Create infrastructure table
CREATE TABLE infrastructure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    county_id INTEGER,
    year INTEGER,
    road_density DECIMAL(8,2),
    electricity_access DECIMAL(5,2),
    internet_access DECIMAL(5,2),
    paved_roads_percentage DECIMAL(5,2),
    FOREIGN KEY (county_id) REFERENCES counties(county_id)
);

-- Create health table
CREATE TABLE health (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    county_id INTEGER,
    year INTEGER,
    hospital_count INTEGER,
    doctors_per_1000 DECIMAL(6,4),
    child_mortality DECIMAL(6,2),
    health_facilities_per_10000 DECIMAL(6,2),
    FOREIGN KEY (county_id) REFERENCES counties(county_id)
);

-- Create education table
CREATE TABLE education (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    county_id INTEGER,
    year INTEGER,
    literacy_rate DECIMAL(5,2),
    school_enrollment DECIMAL(5,2),
    dropout_rate DECIMAL(5,2),
    primary_completion_rate DECIMAL(5,2),
    FOREIGN KEY (county_id) REFERENCES counties(county_id)
);

-- Insert county data (all 47 counties)
INSERT INTO counties (county_id, county_name, region, sub_region) VALUES
-- Nairobi Region
(1, 'Nairobi', 'Nairobi', 'Metropolitan'),
-- Central Region
(2, 'Kiambu', 'Central', 'Greater Nairobi'),
(3, 'Muranga', 'Central', 'Central Highlands'),
(4, 'Nyeri', 'Central', 'Central Highlands'),
(5, 'Kirinyaga', 'Central', 'Central Highlands'),
(6, 'Nyandarua', 'Central', 'Central Highlands'),
-- Rift Valley Region
(7, 'Nakuru', 'Rift Valley', 'Southern Rift'),
(8, 'Uasin Gishu', 'Rift Valley', 'North Rift'),
(9, 'Trans Nzoia', 'Rift Valley', 'North Rift'),
(10, 'Baringo', 'Rift Valley', 'Northern Rift'),
(11, 'Elgeyo Marakwet', 'Rift Valley', 'Northern Rift'),
(12, 'Kericho', 'Rift Valley', 'South Rift'),
(13, 'Bomet', 'Rift Valley', 'South Rift'),
(14, 'Nandi', 'Rift Valley', 'North Rift'),
(15, 'Laikipia', 'Rift Valley', 'Northern Rift'),
(16, 'Narok', 'Rift Valley', 'Southern Rift'),
(17, 'Kajiado', 'Rift Valley', 'Southern Rift'),
(18, 'Samburu', 'Rift Valley', 'Northern Rift'),
(19, 'Turkana', 'Rift Valley', 'Northern Rift'),
(20, 'West Pokot', 'Rift Valley', 'Northern Rift'),
-- Eastern Region
(21, 'Machakos', 'Eastern', 'Lower Eastern'),
(22, 'Kitui', 'Eastern', 'Lower Eastern'),
(23, 'Makueni', 'Eastern', 'Lower Eastern'),
(24, 'Meru', 'Eastern', 'Upper Eastern'),
(25, 'Tharaka Nithi', 'Eastern', 'Upper Eastern'),
(26, 'Embu', 'Eastern', 'Upper Eastern'),
(27, 'Isiolo', 'Eastern', 'Northern Frontier'),
(28, 'Marsabit', 'Eastern', 'Northern Frontier'),
-- Western Region
(29, 'Kakamega', 'Western', 'Lake Region'),
(30, 'Bungoma', 'Western', 'Lake Region'),
(31, 'Busia', 'Western', 'Lake Region'),
(32, 'Vihiga', 'Western', 'Lake Region'),
-- Nyanza Region
(33, 'Kisumu', 'Nyanza', 'Lake Region'),
(34, 'Siaya', 'Nyanza', 'Lake Region'),
(35, 'Homa Bay', 'Nyanza', 'Lake Region'),
(36, 'Migori', 'Nyanza', 'Lake Region'),
(37, 'Kisii', 'Nyanza', 'Highlands'),
(38, 'Nyamira', 'Nyanza', 'Highlands'),
-- Coast Region
(39, 'Mombasa', 'Coast', 'Coastal Strip'),
(40, 'Kwale', 'Coast', 'Coastal Strip'),
(41, 'Kilifi', 'Coast', 'Coastal Strip'),
(42, 'Tana River', 'Coast', 'Coastal Strip'),
(43, 'Lamu', 'Coast', 'Coastal Strip'),
(44, 'Taita Taveta', 'Coast', 'Coastal Strip'),
-- North Eastern Region
(45, 'Garissa', 'North Eastern', 'Northern Frontier'),
(46, 'Wajir', 'North Eastern', 'Northern Frontier'),
(47, 'Mandera', 'North Eastern', 'Northern Frontier');

-- Insert demographic data (focusing on 2023 as reference year)
INSERT INTO demographics (county_id, year, population, poverty_rate, unemployment_rate, gini_coefficient) VALUES
-- Nairobi
(1, 2023, 4397073, 18.5, 12.3, 0.482),
-- Central counties
(2, 2023, 2419735, 22.3, 8.7, 0.423),
(3, 2023, 996922, 24.8, 9.2, 0.431),
(4, 2023, 826992, 26.1, 10.1, 0.438),
(5, 2023, 610411, 27.4, 9.8, 0.442),
(6, 2023, 664931, 32.5, 12.4, 0.456),
-- Rift Valley major counties
(7, 2023, 2162366, 28.7, 11.2, 0.445),
(8, 2023, 1186960, 27.3, 10.5, 0.441),
(9, 2023, 990341, 32.1, 13.8, 0.452),
(10, 2023, 666763, 48.3, 18.5, 0.489),
(11, 2023, 454480, 42.7, 16.2, 0.476),
(12, 2023, 901777, 35.2, 12.9, 0.458),
(13, 2023, 875689, 38.4, 14.1, 0.465),
(14, 2023, 885711, 34.6, 12.7, 0.455),
(15, 2023, 518560, 41.2, 15.8, 0.472),
(16, 2023, 1157387, 58.7, 22.3, 0.512),
(17, 2023, 1126640, 47.2, 17.9, 0.485),
(18, 2023, 310327, 65.3, 26.7, 0.534),
(19, 2023, 926976, 72.4, 31.2, 0.558),
(20, 2023, 621241, 63.8, 24.5, 0.521),
-- Eastern counties
(21, 2023, 1421629, 36.7, 13.4, 0.461),
(22, 2023, 1136187, 48.9, 18.2, 0.492),
(23, 2023, 987653, 45.6, 16.8, 0.481),
(24, 2023, 1545714, 33.4, 12.1, 0.452),
(25, 2023, 393177, 39.2, 14.5, 0.467),
(26, 2023, 608599, 34.8, 12.6, 0.457),
(27, 2023, 268002, 62.4, 23.7, 0.518),
(28, 2023, 459785, 71.6, 29.4, 0.551),
-- Western counties
(29, 2023, 1867579, 43.2, 15.6, 0.475),
(30, 2023, 1670570, 41.8, 14.9, 0.471),
(31, 2023, 893681, 46.5, 17.2, 0.484),
(32, 2023, 590013, 44.1, 16.1, 0.478),
-- Nyanza counties
(33, 2023, 1155574, 37.8, 13.7, 0.463),
(34, 2023, 842762, 52.3, 19.6, 0.498),
(35, 2023, 1131068, 54.2, 20.8, 0.503),
(36, 2023, 1046644, 48.7, 17.5, 0.488),
(37, 2023, 1266225, 42.3, 15.2, 0.473),
(38, 2023, 605576, 44.7, 16.4, 0.479),
-- Coast counties
(39, 2023, 1208333, 28.5, 14.2, 0.448),
(40, 2023, 866824, 56.8, 21.4, 0.508),
(41, 2023, 1453787, 52.6, 19.8, 0.496),
(42, 2023, 315943, 68.4, 27.3, 0.542),
(43, 2023, 143920, 54.3, 20.1, 0.501),
(44, 2023, 340671, 51.7, 18.9, 0.494),
-- North Eastern counties
(45, 2023, 841353, 69.2, 28.6, 0.548),
(46, 2023, 781263, 73.5, 32.4, 0.562),
(47, 2023, 867457, 75.8, 34.1, 0.571);

-- Insert infrastructure data
INSERT INTO infrastructure (county_id, year, road_density, electricity_access, internet_access, paved_roads_percentage) VALUES
(1, 2023, 152.3, 89.5, 78.4, 68.5),
(2, 2023, 98.7, 78.3, 62.1, 45.2),
(3, 2023, 76.4, 65.2, 48.3, 32.6),
(4, 2023, 82.1, 68.7, 52.4, 38.9),
(5, 2023, 71.3, 62.4, 44.7, 31.2),
(6, 2023, 58.9, 48.2, 32.5, 24.7),
(7, 2023, 87.5, 72.6, 56.8, 41.3),
(8, 2023, 79.2, 69.8, 52.3, 38.4),
(9, 2023, 68.4, 58.7, 41.6, 31.7),
(10, 2023, 42.7, 32.4, 18.9, 18.2),
(11, 2023, 46.3, 35.8, 21.4, 21.6),
(12, 2023, 71.8, 61.5, 44.2, 34.5),
(13, 2023, 63.2, 53.7, 37.8, 28.9),
(14, 2023, 67.9, 58.2, 40.5, 31.2),
(15, 2023, 52.4, 42.6, 27.3, 23.4),
(16, 2023, 38.7, 24.3, 12.8, 15.6),
(17, 2023, 44.2, 35.7, 19.6, 20.1),
(18, 2023, 28.6, 18.9, 8.7, 11.3),
(19, 2023, 22.4, 12.3, 5.2, 7.8),
(20, 2023, 26.8, 15.7, 7.4, 9.5),
(21, 2023, 72.5, 62.8, 45.3, 34.2),
(22, 2023, 54.7, 44.5, 28.7, 25.6),
(23, 2023, 58.3, 48.9, 32.4, 27.8),
(24, 2023, 74.6, 64.2, 47.8, 35.9),
(25, 2023, 62.8, 53.4, 38.2, 29.4),
(26, 2023, 69.2, 59.6, 42.5, 32.1),
(27, 2023, 32.5, 22.7, 11.6, 14.2),
(28, 2023, 24.7, 14.5, 6.8, 9.3),
(29, 2023, 66.4, 56.9, 40.2, 30.8),
(30, 2023, 63.8, 54.2, 37.9, 29.4),
(31, 2023, 59.2, 49.8, 33.6, 27.2),
(32, 2023, 61.5, 52.3, 36.4, 28.7),
(33, 2023, 78.4, 68.5, 53.7, 38.9),
(34, 2023, 56.7, 46.8, 31.2, 26.4),
(35, 2023, 54.2, 44.2, 28.9, 24.8),
(36, 2023, 60.8, 51.6, 35.4, 28.2),
(37, 2023, 70.3, 60.4, 44.8, 33.6),
(38, 2023, 64.9, 55.7, 39.8, 30.2),
(39, 2023, 84.6, 74.2, 59.4, 42.7),
(40, 2023, 48.5, 38.9, 24.7, 23.1),
(41, 2023, 52.7, 43.2, 28.4, 25.6),
(42, 2023, 35.8, 25.6, 14.3, 17.2),
(43, 2023, 40.2, 31.8, 18.7, 19.8),
(44, 2023, 44.6, 35.2, 21.6, 22.4),
(45, 2023, 26.3, 16.4, 8.2, 10.5),
(46, 2023, 23.8, 13.8, 6.5, 8.9),
(47, 2023, 21.5, 11.9, 5.4, 7.2);

-- Insert health data
INSERT INTO health (county_id, year, hospital_count, doctors_per_1000, child_mortality, health_facilities_per_10000) VALUES
(1, 2023, 187, 0.48, 38.2, 4.2),
(2, 2023, 86, 0.32, 45.6, 3.5),
(3, 2023, 42, 0.24, 52.3, 2.8),
(4, 2023, 48, 0.26, 49.8, 3.1),
(5, 2023, 32, 0.21, 54.2, 2.6),
(6, 2023, 28, 0.18, 62.4, 2.2),
(7, 2023, 78, 0.29, 51.7, 3.2),
(8, 2023, 52, 0.25, 53.4, 2.9),
(9, 2023, 44, 0.22, 58.9, 2.5),
(10, 2023, 23, 0.14, 74.3, 1.8),
(11, 2023, 19, 0.12, 78.6, 1.6),
(12, 2023, 42, 0.23, 56.2, 2.7),
(13, 2023, 37, 0.20, 60.8, 2.4),
(14, 2023, 39, 0.21, 59.4, 2.5),
(15, 2023, 28, 0.16, 67.5, 2.0),
(16, 2023, 34, 0.12, 82.7, 1.7),
(17, 2023, 41, 0.18, 71.4, 2.1),
(18, 2023, 12, 0.08, 96.2, 1.2),
(19, 2023, 18, 0.07, 112.5, 1.1),
(20, 2023, 15, 0.09, 104.8, 1.3),
(21, 2023, 64, 0.27, 48.6, 3.0),
(22, 2023, 52, 0.20, 63.4, 2.4),
(23, 2023, 48, 0.22, 60.2, 2.6),
(24, 2023, 68, 0.28, 47.8, 3.2),
(25, 2023, 31, 0.23, 55.6, 2.5),
(26, 2023, 37, 0.24, 52.3, 2.7),
(27, 2023, 14, 0.11, 88.5, 1.4),
(28, 2023, 19, 0.09, 98.7, 1.3),
(29, 2023, 84, 0.26, 56.4, 2.8),
(30, 2023, 72, 0.24, 58.7, 2.6),
(31, 2023, 48, 0.21, 64.2, 2.3),
(32, 2023, 34, 0.22, 61.5, 2.4),
(33, 2023, 66, 0.31, 49.3, 3.3),
(34, 2023, 52, 0.19, 72.6, 2.2),
(35, 2023, 58, 0.18, 78.4, 2.1),
(36, 2023, 49, 0.20, 67.8, 2.3),
(37, 2023, 62, 0.25, 54.7, 2.9),
(38, 2023, 36, 0.22, 59.2, 2.5),
(39, 2023, 71, 0.35, 44.3, 3.6),
(40, 2023, 44, 0.16, 76.8, 2.0),
(41, 2023, 67, 0.19, 73.5, 2.2),
(42, 2023, 18, 0.10, 92.4, 1.4),
(43, 2023, 12, 0.12, 84.7, 1.6),
(44, 2023, 24, 0.14, 79.2, 1.8),
(45, 2023, 28, 0.09, 98.3, 1.3),
(46, 2023, 24, 0.07, 108.6, 1.1),
(47, 2023, 22, 0.06, 115.7, 1.0);

-- Insert education data
INSERT INTO education (county_id, year, literacy_rate, school_enrollment, dropout_rate, primary_completion_rate) VALUES
(1, 2023, 92.4, 94.2, 6.8, 91.5),
(2, 2023, 88.7, 91.5, 8.2, 88.3),
(3, 2023, 85.2, 88.4, 9.6, 85.7),
(4, 2023, 86.4, 89.2, 9.1, 86.9),
(5, 2023, 84.3, 87.6, 10.2, 84.5),
(6, 2023, 78.6, 82.3, 12.8, 79.2),
(7, 2023, 84.7, 87.9, 9.8, 85.1),
(8, 2023, 85.3, 88.6, 9.4, 85.8),
(9, 2023, 81.2, 84.7, 11.2, 82.3),
(10, 2023, 68.4, 72.5, 18.7, 67.8),
(11, 2023, 71.2, 75.8, 16.4, 71.2),
(12, 2023, 79.5, 83.2, 12.5, 80.4),
(13, 2023, 76.8, 80.4, 13.9, 77.6),
(14, 2023, 78.2, 81.7, 13.2, 79.1),
(15, 2023, 73.5, 77.2, 15.8, 74.3),
(16, 2023, 62.3, 65.8, 24.3, 60.5),
(17, 2023, 68.7, 72.4, 19.2, 66.8),
(18, 2023, 54.2, 58.7, 31.6, 52.3),
(19, 2023, 48.7, 52.3, 38.4, 46.7),
(20, 2023, 52.4, 56.8, 34.2, 50.2),
(21, 2023, 82.6, 86.3, 11.4, 83.7),
(22, 2023, 74.8, 78.9, 15.2, 75.6),
(23, 2023, 76.3, 80.2, 14.3, 77.2),
(24, 2023, 83.4, 87.1, 10.8, 84.3),
(25, 2023, 79.7, 83.6, 12.7, 80.9),
(26, 2023, 81.5, 85.4, 11.6, 82.8),
(27, 2023, 58.7, 63.2, 28.4, 56.7),
(28, 2023, 52.3, 56.9, 35.7, 50.3),
(29, 2023, 77.4, 81.3, 13.6, 78.4),
(30, 2023, 78.2, 82.1, 12.9, 79.2),
(31, 2023, 74.5, 78.6, 15.4, 75.3),
(32, 2023, 75.8, 79.9, 14.7, 76.8),
(33, 2023, 85.6, 88.9, 9.3, 86.4),
(34, 2023, 72.3, 76.4, 16.8, 73.2),
(35, 2023, 70.8, 74.9, 17.9, 71.5),
(36, 2023, 74.2, 78.3, 15.6, 75.1),
(37, 2023, 80.3, 84.2, 12.2, 81.5),
(38, 2023, 78.9, 82.7, 13.4, 79.8),
(39, 2023, 87.3, 90.4, 8.5, 88.7),
(40, 2023, 69.5, 73.6, 18.3, 70.2),
(41, 2023, 71.2, 75.3, 17.2, 72.1),
(42, 2023, 61.4, 65.7, 26.7, 59.8),
(43, 2023, 67.8, 71.9, 19.8, 66.5),
(44, 2023, 72.4, 76.5, 16.3, 73.4),
(45, 2023, 55.6, 59.8, 33.2, 53.4),
(46, 2023, 51.3, 55.7, 38.9, 49.2),
(47, 2023, 48.5, 52.6, 41.3, 46.5);