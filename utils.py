import os
import pandas as pd

from function.utils import loadF_from_folder

from solver.gl import max_irradiance_steps
from solver.utils import get_f
from solver.k_modal import general_solution


def export_to_df(test_folder: str, df_name: str, substeps_range: tuple[int, int]=None):
    f = loadF_from_folder(test_folder)
    if range is not None:
        # reduce f to an appropiate range
        ns = f.get_sub_steps(*substeps_range)
        f = get_f(ns)

    return export_to_df_fromF(f, df_name)


def export_to_df_fromF(f, df_name: str):
    max_m = len(f)
    gl_solutions = []
    km_solutions = []

    for m in range(1, max_m+1):
    # for m in range(1, 3):
        # compute gl solution
        gl_len = int(f.omega/m)
        max_irr_steps = max_irradiance_steps(f, gl_len)
        max_f = get_f(max_irr_steps)
        gl_solutions.append(max_f.get_irradiance()*m)
        # get the general solution
        km_gain, _ = general_solution(f, m)
        km_solutions.append(km_gain)
    df = pd.DataFrame(data=zip(gl_solutions, km_solutions), columns=['gl_solution', 'km_solution'])
    df.to_csv(df_name, index=False)

    return df


def get_percentual_decrease(df_folder: str, percent_indexes: list[int]=[1, 0.9, 0.75, 0.5, 0.25]):
    for test in os.listdir(df_folder):
        tfolder = os.path.join(df_folder, test)
        if os.path.isdir(tfolder):
            ldf = 0
            dfs = []
            for dpath in os.listdir(tfolder):
                df = pd.read_csv(os.path.join(tfolder, dpath))
                ldf = len(df)
                dfs.append(df)
            
            df = sum(dfs)/ldf
            indexes = [int(i*ldf)-1 for i in percent_indexes]
            full_solution = df.loc[ldf-1, "km_solution"]
            print(full_solution)

            solutions = df.loc[indexes, :]/full_solution

            print("---------- Case {0} -----".format(dpath))
            print(solutions)


if __name__ == '__main__':
    get_percentual_decrease("exp_results")
