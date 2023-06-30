{
    'schema': 'raw',
    'table': 'country_weekly_chart',
    'sqls' : {
        'test_sql' : """
            SELECT 
                $1 AS rank, 
                $2 AS track_id, 
                $3 AS artist_names, 
                $4 AS track_name, 
                $5 AS peak_rank, 
                $6 AS previous_rank, 
                $7 AS weeks_on_chart, 
                $8 AS streams, 
                $9 AS country_code, 
                $10 AS chart_date
            FROM @raw.transformed_data_stage_csv/spotify/chart/{date}/{target_file_pattern};
    """ ,
        'load_sql' : """
                        BEGIN;

                            CREATE TEMPORARY TABLE temp_table AS 
                            SELECT 
                                $1 AS rank, 
                                $2 AS track_id, 
                                $3 AS artist_names, 
                                $4 AS track_name, 
                                $5 AS peak_rank, 
                                $6 AS previous_rank, 
                                $7 AS weeks_on_chart, 
                                $8 AS streams, 
                                $9 AS country_code, 
                                $10 AS chart_date
                            FROM @{schema}.transformed_data_stage_csv/spotify/chart/{date}/{target_file_pattern};
                            
                            DELETE FROM {schema}.{table} 
                            WHERE chart_date = '{date}';

                            INSERT INTO {schema}.{table} 
                            SELECT t.* 
                            FROM temp_table t;

                        COMMIT;
                    """
    }
         
}