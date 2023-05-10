import pandas as pd

from function.utils import loadF_from_folder

from solver.gl import max_irradiance_steps
from solver.utils import get_f
from solver.k_modal import general_solution


def export_to_df(test_folder: str, df_name: str):
    f = loadF_from_folder(test_folder)

    max_m = len(f)
    gl_solutions = []
    km_solutions = []

    for m in range(1, max_m+1):
    # for m in range(1, 3):
        # compute gl solution
        gl_len = int(f.omega/m)
        max_irr_steps = max_irradiance_steps(f, gl_len)
        max_f = get_f(max_irr_steps)
        gl_solutions.append(max_f.get_irradiance())
        # get the general solution
        km_gain, _ = general_solution(f, m)
        km_solutions.append(km_gain)
    df = pd.DataFrame(data=zip(gl_solutions, km_solutions), columns=['gl_solution', 'km_solution'])
    df.to_csv(df_name, index=False)

    return df
