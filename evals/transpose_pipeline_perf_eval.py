import pymonetdb
import time
import pandas as pd

def pipeline_performance_complex_query():
    db = pymonetdb.connect(username='monetdb', password='monetdb', hostname='localhost', database='test')

    cursor = db.cursor()
    query = '''SELECT 
    T1.a,
    T2.c,
    T3.sum_b,
    T4.max_d
FROM 
    (SELECT a, b FROM ra WHERE a > 10) AS T1
JOIN 
    (SELECT c, d FROM rb WHERE d < 20) AS T2 ON T1.a = T2.c
JOIN 
    (SELECT a, SUM(b) AS sum_b FROM ra GROUP BY a) AS T3 ON T1.a = T3.a
JOIN 
    (SELECT c, MAX(d) AS max_d FROM rb GROUP BY c) AS T4 ON T2.c = T4.c
WHERE 
    T1.a IN (SELECT a FROM ra WHERE b > 5)
    AND T2.c IN (SELECT c FROM rb WHERE d < 15)
ORDER BY 
    T3.sum_b DESC, 
    T4.max_d ASC;'''
    cursor.execute(query)
    cursor.close()
    db.close()


def run_transpose_pipeline_performance(n_iter: int):
    time_consumed = []
    for i in range(n_iter):
        time_start = time.time()
        pipeline_performance_complex_query()
        end_start = time.time()
        time_consumed.append(end_start - time_start)
    df = pd.DataFrame()
    df['Performance'] = pd.Series(time_consumed)
    return df


if __name__ == '__main__':
    df = run_transpose_pipeline_performance(1000)
    print(f"Total execution time {df['Performance'].sum()}")
    print(f"Average execution time {df['Performance'].mean()}")
    print(f"Maximum execution time {df['Performance'].max()}")
    print(f"Minimum execution time {df['Performance'].min()}")