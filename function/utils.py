import os
import pandas as pd

from function.classes import F


def get_angle(fn):
    return float(fn[len("position"):].replace(".txt", ""))


def loadxy_from_folder(data_folder):
    files = sorted(os.listdir(data_folder), key=lambda fn: get_angle(fn))
    #print(files)

    xs, ys = [], []
    for f in files:
        df = pd.read_csv(os.path.join(data_folder, f), sep='\t')
        angle = get_angle(f)
        total_flux = int(df["Flux(W/m2)"].sum())
        
        xs.append(angle)
        ys.append(total_flux)
    return xs, ys


def loadF_from_folder(data_folder) -> F:
    xs, ys = loadxy_from_folder(data_folder)
    return F(xs, ys)
