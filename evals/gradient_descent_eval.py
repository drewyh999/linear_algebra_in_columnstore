import pymonetdb
import numpy as np
import time
import matplotlib.pyplot as plt


def get_matrices_from_db(relation_x: str, relation_x_os: str, relation_y: str, relation_y_os: str):
    db = pymonetdb.connect(username='monetdb', password='monetdb', hostname='localhost', database='test')
    cursor = db.cursor()

    cursor.execute("SELECT feature FROM w_matrix order by feature desc;")
    res = np.array(cursor.fetchall())
    selection_string = ','.join([x[0] for x in res])

    W = np.zeros((13, 1), dtype='float')

    # Fetch columns from database in order of W's order schema
    query = f'SELECT {selection_string} FROM \"{relation_x}\" order by \"{relation_x}\".\"{relation_x_os}\" desc;'
    cursor.execute(query)
    X_matrix = np.array(cursor.fetchall())
    X_matrix = X_matrix.astype('float')

    cursor.execute(f'SELECT Density FROM \"{relation_y}\" order by \"{relation_y}\".\"{relation_y_os}\" desc;')
    Y_vector = np.array(cursor.fetchall())
    Y_vector = Y_vector.astype('float')
    db.close()
    cursor.close()
    return X_matrix, Y_vector, W


def lr(learning_rate: float, n_iter: int):
    X, Y, W = get_matrices_from_db("bodyfat", "id", "bodyfat_y", "id")
    for i in range(n_iter):
        result = W - (learning_rate / X.shape[0]) * np.matmul(X.T, (np.matmul(X, W)) - Y)
        W = result
    return W


def create_procedures():
    db = pymonetdb.connect(username='monetdb', password='monetdb', hostname='localhost', database='test')
    init_w_procedure = '''
        CREATE OR REPLACE PROCEDURE INIT_W()
        BEGIN
            UPDATE "w_matrix" SET "weight"=0;
        END;
        '''

    try:
        cursor = db.cursor()
        cursor.execute(init_w_procedure)
        cursor.close()
        db.commit()
        print(f"Initialization of weight relation procedure created")
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(9)

    lr_procedure_query = '''
        CREATE OR REPLACE PROCEDURE LR(learning_rate double, n_iter int)
        BEGIN
            DECLARE number_of_samples double;
            SELECT COUNT(*) INTO number_of_samples FROM bodyfat;
            DECLARE rowcount int;
            SET rowcount = 0;
            WHILE (rowcount < n_iter) DO
                UPDATE w_matrix
                SET "weight" = DIFF."new_weight"
                FROM (select feature, "weight" as "new_weight" from msub(
                            w_matrix by "feature",
                            (select "C", "weight" * learning_rate / number_of_samples as gradient_result from mmu(
                                tra(bodyfat by id) as x_t
                                by x_t."C",
                                msub(
                                    mmu(bodyfat by id, w_matrix by feature) by "id",
                                    bodyfat_y by id
                                    )
                                by id
                            )) as RES by RES."C"
                        )) as DIFF
                WHERE w_matrix."feature" = DIFF."feature";
                SET rowcount = rowcount + 1;
            END WHILE;
        END;
        '''
    try:
        cursor = db.cursor()
        cursor.execute(lr_procedure_query)
        cursor.close()
        db.commit()
        print(f"Linear regression procedure created")
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(9)
    db.close()


def indb_lr(learning_rate: float, n_iter: int):
    db = pymonetdb.connect(username='monetdb', password='monetdb', hostname='localhost', database='test')

    lr_query = f'''
    call init_w();
    call lr({learning_rate}, {n_iter});
    select weight from w_matrix order by feature desc;
    '''
    try:
        cursor = db.cursor()
        cursor.execute(lr_query)
        res = np.array(cursor.fetchall(), dtype='float')
        cursor.close()
        db.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(9)
    db.close()
    return res


def run_lr_experiment(learning_rate: float):
    n_iters = [10, 50, 100, 200, 300, 500, 1000]
    results_numpy = []
    results_indb = []
    for i in n_iters:
        start_time_1 = time.time()
        lr(learning_rate, i)
        end_time_1 = time.time()
        results_numpy.append((end_time_1 - start_time_1) * 1000)
        start_time_2 = time.time()
        indb_lr(learning_rate, i)
        end_time_2 = time.time()
        results_indb.append((end_time_2 - start_time_2) * 1000)
    return n_iters, results_numpy, results_indb


if __name__ == '__main__':
    learning_rate = 0.0001
    n_iter = 5
    W_pd = lr(learning_rate, n_iter)
    W_indb = indb_lr(learning_rate, n_iter)
    # Starts not to equal from decimal=14
    print(f"Assertion {np.testing.assert_array_almost_equal(W_pd, W_indb, decimal=13)}")

    n_iters, results_numpy, results_indb = run_lr_experiment(0.0000001)
    fig, ax = plt.subplots()
    ax.plot(n_iters, results_numpy, label='Numpy execution time')
    ax.plot(n_iters, results_indb, label='In database execution time')
    ax.set_xlabel("Number of iterations")
    ax.set_ylabel("Execution time (Milliseconds)")
    ax.legend()
    plt.show()
