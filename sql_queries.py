import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events";
staging_songs_table_drop = "DROP TABLE IF EXISTS  staging_events";
songplay_table_drop = "DROP TABLE IF EXISTS songplays";
user_table_drop = "DROP TABLE IF EXISTS users";
song_table_drop = "DROP TABLE IF EXISTS songs";
artist_table_drop = "DROP TABLE IF EXISTS artists";
time_table_drop = "DROP TABLE IF EXISTS time";

# CREATE TABLES

staging_events_table_create= (""" CREATE TABLE IF NOT EXISTS staging_events(
                    staging_event_id    INTEGER IDENTITY(0,1),
                    artist         VARCHAR,
                    auth           VARCHAR,
                    fistName       VARCHAR,
                    gender         VARCHAR,
                    itemInSession  INTEGER,
                    lastName       VARCHAR,
                    length         NUMERIC,   
                    level          VARCHAR,
                    location       VARCHAR,
                    method         VARCHAR,
                    page           VARCHAR,
                    registration   BIGINT,
                    sessionId      INTEGER,
                    song           VARCHAR,
                    status         INTEGER,
                    ts             BIGINT,
                    userAgent      VARCHAR,
                    userId         INTEGER
                    );
""")

staging_songs_table_create = (""" CREATE TABLE IF NOT EXISTS staging_songs(
                    staging_song_id    INTEGER IDENTITY(0,1),
                    num_songs          INTEGER,
                    artist_id          VARCHAR,
                    artist_latitude    NUMERIC,
                    artist_longitude   NUMERIC,
                    artist_location    VARCHAR,
                    artist_name        VARCHAR,
                    duration           NUMERIC,
                    song_id            VARCHAR,
                    title              VARCHAR,
                    year               INTEGER);
""")

songplay_table_create = ("""
        CREATE TABLE IF NOT EXISTS songplays(
                    songplay_id             INT IDENTITY(1,1) PRIMARY KEY, 
                    start_time              BIGINT, 
                    user_id                 INTEGER NOT NULL,
                    level                   VARCHAR,
                    song_id                 VARCHAR, 
                    artist_id               VARCHAR,
                    session_id              INTEGER NOT NULL,
                    location                VARCHAR,
                    user_agent              VARCHAR)
""");

user_table_create = ("""
            CREATE TABLE IF NOT EXISTS users(
                     user_id     INTEGER PRIMARY KEY, 
                     first_name  VARCHAR, 
                     last_name   VARCHAR,
                     gender      VARCHAR,
                     level       VARCHAR)
""");

song_table_create = ("""
            CREATE TABLE IF NOT EXISTS songs(
                    song_id    VARCHAR PRIMARY KEY, 
                    title      VARCHAR, 
                    artist_id  VARCHAR,
                    year       INTEGER, 
                    duration   BIGINT);
""");

artist_table_create = ("""
            CREATE TABLE IF NOT EXISTS artists(
                        artist_id    VARCHAR PRIMARY KEY,
                        name         VARCHAR, 
                        location     VARCHAR,
                        latitude     VARCHAR,
                        longitude    VARCHAR);
""");

time_table_create = ("""
        CREATE TABLE IF NOT EXISTS time(
                       start_time    TIMESTAMP PRIMARY KEY, 
                       hour          INTEGER,
                       day           INTEGER, 
                       week          INTEGER,
                       month         VARCHAR,
                       year          INTEGER, 
                       weekday       VARCHAR);
""");

# STAGING TABLES

staging_events_copy = ("""
                        COPY staging_events FROM {}
                        CREDENTIALS 'aws_iam_role= {}'
                        REGION 'us-west-2'
                        JSON AS {} 
            """).format(config.get('S3','LOG_DATA'),config.get('IAM_ROLE','ARN'), config.get('S3','LOG_JSONPATH'))

staging_songs_copy = ("""
                   COPY staging_songs 
                           FROM {}
                           CREDENTIALS 'aws_iam_role= {}'
                           REGION 'us-west-2'
                           JSON  AS 'auto'
                            """).format(config.get('S3','SONG_DATA'),config.get('IAM_ROLE','ARN'))
# FINAL TABLES

songplay_table_insert = ("""
                    INSERT INTO songplays( 
                        start_time,
                        user_id, 
                        level, 
                        song_id, 
                        artist_id, 
                        session_id, 
                        location, 
                        user_agent) 
                         SELECT DISTINCT  se.ts  AS start_time, 
                                   se.user_id AS user_id,
                                   se.level AS level,
                                   ss.song_id AS song_id,
                                   ss.artist_id AS artist_id,
                                   se.session_id AS session_id,
                                   se.location AS location,
                                   se.user_agent AS user_agent
                            FROM staging_events AS se
                            JOIN staging_songs AS ss
                            ON se.song = ss.title
                            AND se.artist = ss.artist_name
                            WHERE se.page = 'NextSong'
                            AND se.user_id IS NOT NULL)
""")

user_table_insert = ("""

                    INSERT INTO users(
                        user_id, 
                        first_name, 
                        last_name, 
                        gender, 
                        level)
                        SELECT userId, firstName, lastName, gender, level
                        FROM staging_events
                        WHERE userId IS NOT NULL
""")

song_table_insert = ("""
                     INSERT INTO songs(
                        song_id,
                        title, 
                        artist_id, 
                        year, 
                        duration) 
                        SELECT song_id, title, artist_id, year, duration
                        FROM staging_songs
                        WHERE song_id IS NOT NULL 
""")

artist_table_insert = ("""
                     INSERT INTO artists(
                         artist_id,
                         name, 
                         location, 
                         latitude,
                         longitude) 
                         SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
                          FROM staging_songs
                          WHERE artist_id IS NOT NULL
""")

time_table_insert = ("""
                    
                    INSERT INTO time(
                        start_time,
                        hour, 
                        day, 
                        week, 
                        month, 
                        year, 
                        weekday)
                       SELECT sp.start_time AS start_time,
                               EXTRACT(hour FROM start_time) AS hour,
                               EXTRACT(day FROM start_time) AS day,
                               EXTRACT(week FROM start_time) AS week,
                               EXTRACT(month FROM start_time) AS month,
                               EXTRACT(year FROM start_time) AS year,
                               EXTRACT(dayofweek FROM start_time)
                        FROM (SELECT TIMESTAMP 'epoch' + CAST(start_time AS BIGINT)/1000 *INTERVAL '1 second' 
                        AS start_time 
                        FROM    songplays sp)
""")


# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]

