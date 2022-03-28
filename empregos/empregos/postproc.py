import pandas as pd
import json
pd.options.mode.chained_assignment = None  # default='warn'


# treat file

def split_loc(df):

    df[["cidade", "estado"]] = df["localização"].str.split("/", expand=True)
    return df

def reduce_name(df):
    df["name"] = df["name"].str.replace("Vaga de ", "")
    df.rename(columns={"name": "vaga"}, inplace=True)
    return df

def take_category(df):

    regex = "(vaga-de-emprego-na-area-)(.*)(-em-.*)"
    df["categoria"] = df["link"].str.split("/").str[1].to_list()
    df["categoria"] = df["categoria"].str.extractall(regex)[1].unstack()
    df["categoria"] = df["categoria"].str.capitalize()
    return df

def pos_proc(filename):

    if filename.split(".")[-1]=="json":
        with open(filename, encoding="latin-1") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    if filename.split(".")[-1] == "csv":
        df = pd.read_csv(filename)
    #Filtra os registros que estão no formato certo Cidade / Estado
    df_estado = df.loc[df["localização"].str.contains("/")]
    df_estado["question"] = df_estado["localização"].str.split("/")
    df_estado["len"] = df_estado["question"].apply(lambda x: len(x))
    df_estado.sort_values("len", inplace=True)
    # Filtra os registros que tem info correta
    df_estado = df_estado.loc[df_estado.len == 2]
    df_estado.drop(["question", "len"], axis=1, inplace=True)

    df_sem_estado = df.loc[~df["localização"].str.contains("/")]
    df_sem_estado.drop("localização", axis=1, inplace=True)
    df_sem_estado.rename(columns={'salário':"localização", "empresa": "salário"}, inplace=True)
    df_sem_estado["empresa"] = ["Confidencial"]*len(df_sem_estado)

    df = pd.concat([df_estado, df_sem_estado], ignore_index=True)

    df = split_loc(df)
    df = reduce_name(df)
    df = take_category(df)

    df.to_csv("empregosBNE_tratado.csv", index=False, sep=";")