import pymonetdb
import numpy as np
import time
import matplotlib.pyplot as plt


def direct_tra_mmu(db, ra_name: str, ra_os: str, arr_dtype: str):
    cursor = db.cursor()

    # Fetch two relations (tables)
    query = f'SELECT COUNT(*) FROM mmu(tra(\"{ra_name}\" by \"{ra_name}\".\"{ra_os}\") as t by t."C", \"{ra_name}\" by \"{ra_name}\".\"{ra_os}\");'
    # print(query)
    cursor.execute(query)
    m = np.array(cursor.fetchall())
    m = m.astype(f'{arr_dtype}')
    cursor.close()
    db.commit()
    return m


# Connect to MonetDB and fetch data then apply mmu
def fetch_and_calculate_tra_mmu(db, ra_name: str, ra_os: str, arr_dtype: str, os_column_index: int):
    cursor = db.cursor()

    # Fetch two relations (tables)
    cursor.execute(f'SELECT * FROM \"{ra_name}\" order by \"{ra_name}\".\"{ra_os}\" desc;')
    matrix1 = np.array(cursor.fetchall())
    matrix1 = np.delete(matrix1, os_column_index, axis=1)
    matrix1 = matrix1.astype(f'{arr_dtype}')

    db.commit()
    cursor.close()

    # Perform matrix calculations
    return np.matmul(matrix1.T, matrix1).shape[0]


def table_exists(connection, table_name):
    cursor = connection.cursor()
    query = f"SELECT COUNT(*) FROM sys.tables WHERE name = '{table_name}'"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    return result > 0


def run_mmu_experiment(relation_name: str, ordering_schema: str, data_type: str):
    direct_calculation = []
    fetch_and_calculate = []
    percentage = []
    sizes = [5000, 10000,40000,60000, 70000]
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

    db.close()
    db = pymonetdb.connect(username='monetdb', password='monetdb', hostname='localhost', database='test')
    for size in sizes:
        try:
            start_time_1 = time.time()
            fetch_and_calculate_tra_mmu(db, f'{relation_name}_{size}', ordering_schema, data_type, -1)
            end_time_1 = time.time()
            result_1 = end_time_1 - start_time_1
            fetch_and_calculate.append(result_1 * 1000)
            print(f"fetch&calculate time {result_1} for size {size}")
            start_time_2 = time.time()
            direct_tra_mmu(db, f'{relation_name}_{size}', ordering_schema, data_type)
            end_time_2 = time.time()
            result = end_time_2 - start_time_2
            direct_calculation.append(result * 1000)
            percentage.append(result / result_1)
            print(f"direct calculation time {result} for size {size}")
        except Exception as e:
            print(f"An error occurred: {e}")
            exit(9)
    db.close()
    return sizes, direct_calculation, fetch_and_calculate, percentage


def direct_tra(db, ra_name: str, ra_os: str, arr_dtype: str):
    cursor = db.cursor()

    # Fetch two relations (tables)
    query = f'SELECT COUNT(*) FROM tra(\"{ra_name}\" by \"{ra_name}\".\"{ra_os}\") as t;'
    # print(query)
    cursor.execute(query)
    m = np.array(cursor.fetchall())
    m = m.astype(f'{arr_dtype}')
    cursor.close()
    return m





if __name__ == '__main__':
    sizes, results,results_f_c, percent_result = run_mmu_experiment("mmu_test_r", "label", "float")

    fig, ax = plt.subplots(1,2,figsize=(14, 5))
    ax[0].set_title("Execution time of mmu of different relation size")
    ax[0].plot([x/1000 for x in sizes], results, label="In-database mmu calculation")
    ax[0].plot([x/1000 for x in sizes], results_f_c, label="Fetch and calculate with Numpy")

    ax[0].set_xlabel("Number of rows (*1000)")
    ax[0].set_ylabel("Execution time in milliseconds")
    ax[0].legend()
    ax[1].set_title("Performance factor on different size of relation")
    ax[1].plot([x/1000 for x in sizes], percent_result)
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_xlabel("Number of rows (*1000)")
    ax[1].set_ylabel('Performance factor')
    plt.show()
