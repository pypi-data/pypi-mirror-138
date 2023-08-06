def query_build(query):
    # pylint: disable=R0912
    """Build query for data backend"""

    my_query = ""

    # pylint: disable=R1702
    for i in query:
        if len(i["attributes"]) != 0:
            if i != query[0]:
                my_query += f' {(i["op"]).lower()} '
            my_query += " ("
            for query_line in i["attributes"]:
                value = query_line["value"]
                if query_line["op"] == "EXCLUDE" or query_line["op"] == "EXCLUDED":
                    if isinstance(value, bool):
                        if value:
                            my_query += f" {query_line['id']} != 0 and "
                        else:
                            my_query += f" {query_line['id']} != 1 and "
                    else:
                        my_query += f" {query_line['id']} == 0 and "
                else:
                    if isinstance(value, list):
                        # pylint: disable=C0301
                        my_query += f"{query_line['id']} >= {value[0]} and {query_line['id']} <= {value[1]} and "
                    elif isinstance(value, bool):
                        my_query += f"{query_line['id']} == 1 and "
                    elif value == "True":
                        my_query += f"{query_line['id']} == 1 and "
                    elif isinstance(value, str):
                        my_query += f"""{query_line['id']} == '{query_line["value"]}' and """
            my_query = my_query[:-5]
            my_query += ") "
    return my_query
