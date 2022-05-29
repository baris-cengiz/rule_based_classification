import pandas as pd

persona = pd.read_csv("persona.csv")
df = persona.copy()

df.info()
df["SOURCE"].unique()
df.groupby("COUNTRY")["PRICE"].mean()
df.groupby("SOURCE")["PRICE"].mean()

df.groupby(["COUNTRY", "SOURCE"])["PRICE"].mean()

agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).aggregate({"PRICE": "mean"})
agg_df.reset_index(inplace=True)
agg_df.sort_values(by="PRICE", ascending=False, inplace=True)
agg_df.head()


def age_cat(age):
    # "qcut" function could've been used. I wanted to write my own func.
    if age <= 18:
        return "0_18"
    elif age <= 23:
        return "19_23"
    elif age <= 30:
        return "24_30"
    elif age <= 40:
        return "31_40"
    else:
        return "41_66"


agg_df["age_cat"] = agg_df["AGE"].apply(age_cat)
agg_df.head()

agg_df["PERSONA"] = agg_df["COUNTRY"] + "_" + agg_df["SOURCE"] + "_" + agg_df["SEX"] + "_" + agg_df["age_cat"]
# join() could've been used.
persona_df = agg_df.groupby("PERSONA").aggregate({"PRICE": "mean"})
persona_df.reset_index(inplace=True)
persona_df.sort_values(by="PRICE", ascending=False, inplace=True)
persona_df["PERSONA"] = persona_df["PERSONA"].str.upper()
persona_df.head()


persona_df["SEGMENT"] = pd.qcut(persona_df["PRICE"], 4, labels=["D", "C", "B", "A"])
persona_df.head()
persona_df.groupby("SEGMENT").agg({"PRICE": ["mean", "max", "sum"]})


def pred_price(df, country, source, sex, age):
    new_user = (country + "_" + source + "_" + sex + "_" + age_cat(age)).upper()
    return df[df["PERSONA"] == new_user][["SEGMENT", "PRICE"]]


pred_price(persona_df, "TUR", "ANDROID", "FEMALE", 33)
pred_price(persona_df, "FRA", "IOS", "FEMALE", 35)
