from mmu_perf_evals import direct_tra, table_exists
import pymonetdb
import time
import matplotlib.pyplot as plt

def run_tra_experiment(relation_name: str, ordering_schema: str, data_type: str):
    direct_calculation = []
    sizes = [5000, 10000 ,70000, 80000, 90000, 100000, 110000]
    # First create the table from original relation
    db = pymonetdb.connect(username='monetdb', password='monetdb', hostname='localhost', database='test')

    for size in sizes:
        # Fetch two relations (tables)
        size_relation_name = f'{relation_name}_{size}'
        if not table_exists(db, size_relation_name):
            try:
                cursor = db.cursor()
                query = f'CREATE TABLE "{size_relation_name}" as select * from "{relation_name}" limit {size};'
                cursor.execute(query)
                cursor.close()
                db.commit()
                print(f"Table created for {size_relation_name}")
            except Exception as e:
                print(f"An error occurred: {e}")
                exit(9)
        else:
            print(f"table already created for {size_relation_name}")

    for size in sizes:
        start_time_1 = time.time()
        direct_tra(db, f'{relation_name}_{size}', ordering_schema, data_type)
        end_time_1 = time.time()
        result = end_time_1 - start_time_1
        direct_calculation.append(result * 1000)
        print(f'Transposition time of {relation_name}_{size} is {end_time_1 - start_time_1}')
    db.close()
    return sizes, direct_calculation

if __name__ == '__main__':
    sizes, res = run_tra_experiment("mmu_test_r", "label", "float")
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(sizes, res)
    plt.show()