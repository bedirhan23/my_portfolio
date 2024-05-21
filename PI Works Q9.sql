
SELECT
    device_type,
    REGEXP_SUBSTR(
        REGEXP_SUBSTR(stats_access_link, '<url>(.*)</url>'),
        '[a-zA-Z0-9_\\.]+\\.([a-zA-Z0-9_\\.]+)+', 
        1,
        1, 
        'i'
    ) AS extracted_url
FROM
    new_table_name;
