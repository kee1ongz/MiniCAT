class QueryRunTimeoutError(Exception):
    pass


# from custom_exceptions import QueryRunTimeoutError
# from query_run import query_run

# try:
#     query_run(ql_db_path, ql_query, bqrs_path)
# except QueryRunTimeoutError:
#     # 处理超时异常的代码
#     print("Query execution timed out")