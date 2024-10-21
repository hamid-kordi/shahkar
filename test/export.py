import pandas as pd
from sqlalchemy import create_engine


"""
    This script connects to a PostgreSQL database,
    fetches 1 million rows at a time from the shahkar_user_userprofile table
    using SQL queries with LIMIT and OFFSET, and saves each chunk to separate
    CSV files (output_i.csv). It loops 11 times, updating the OFFSET 
    to retrieve the next set of rows, and prints the progress (i).

"""


engine = create_engine("postgresql://username:1234@127.0.0.1:5433/postgres")
for i in range(11):
    query = f"SELECT * FROM shahkar_user_userprofile LIMIT 1000000 OFFSET {i*1000000}"
    df = pd.read_sql(query, engine)
    df.to_csv(f"output_{i}.csv", index=False)
    print(f"i=={i}")
