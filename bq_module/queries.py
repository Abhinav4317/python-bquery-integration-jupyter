QUERY_STORE = {
    "test_connection": """
        SELECT 
            "Connection Successful" as status, 
            CURRENT_TIMESTAMP() as server_time,
            @user_name as checked_by
    """,
    "sample_schedules_query": """
        SELECT *
        FROM `bachatt-bigquery-project.prod_db.investmentdb_schedules`
        WHERE date(updated_at) >= '2025-11-23' AND date(updated_at) <= '2025-11-25'
        LIMIT 5
    """
}

def get_query(query_name):
    return QUERY_STORE.get(query_name)