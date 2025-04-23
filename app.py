import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 📄 Konfiguracja strony
st.set_page_config(page_title="Struktura Lab MVP", layout="wide")

# 📁 Wczytaj lekki plik z tickerami
@st.cache_data
def load_tickery():
    df_tickery = pd.read_csv("tickery.csv")
    tickery_per_kategoria = {
        k: df_tickery[df_tickery["Kategoria"] == k]["Nazwa"].dropna().unique().tolist()
        for k in df_tickery["Kategoria"].dropna().unique()
    }
    indeksy = df_tickery[df_tickery["Kategoria"] == "indeksy"]["Nazwa"].dropna().unique().tolist()
    return tickery_per_kategoria, indeksy

tickery_per_kategoria, indeksy = load_tickery()

# Zakres dat
min_date = pd.to_datetime("2020-01-01").date()
max_date = pd.to_datetime("today").date()

# 🎯 Tytuł
st.title("📈 Struktura Lab – Wybór Portfeli")

# 📋 Parametry analizy
with st.sidebar:
    st.header("📅 Parametry analizy")
    start_date = st.date_input("Data początkowa", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input("Data końcowa", min_value=min_date, max_value=max_date, value=max_date)
    kwota_startowa = st.number_input("Kwota startowa (PLN)", min_value=1000, value=10000, step=1000)

# 🧩 Interfejs portfeli
col1, col2, col3 = st.columns(3)

def wybierz_portfel(numer):
    with st.container():
        st.subheader(f"Portfel {numer}")
        tickers = []
        for kat in ["akcje", "obligacje", "indeksy"]:
            if kat in tickery_per_kategoria:
                selected = st.multiselect(f"{kat.capitalize()} (opcjonalnie)", tickery_per_kategoria[kat], key=f"{kat}{numer}")
                tickers.extend(selected)
        wagi = {}
        total = 0
        if tickers:
            st.markdown(f"### ⚖️ Wagi dla Portfela {numer}")
            for t in tickers:
                wagi[t] = st.number_input(f"Waga dla {t} (%)", min_value=0, max_value=100, value=round(100/len(tickers)), key=f"waga{numer}_{t}")
                total += wagi[t]
            st.markdown(f"**🔢 Suma wag:** {total}%")
            if total != 100:
                st.error("Suma wag musi wynosić 100%")
        return tickers, wagi, total

t1, w1, total1 = wybierz_portfel(1)
t2, w2, total2 = wybierz_portfel(2)

with col3:
    st.subheader("Benchmark")
    benchmark = st.selectbox("Wybierz indeks", indeksy)

# 📊 Analiza
if st.button("📊 Analizuj"):

    @st.cache_data
    def load_notowania():
        path = r"C:\Users\DELL\Desktop\Praca magisterska\Struktura Lab\notowania_gpw_full.csv"
        df = pd.read_csv(path)
        df["Data"] = pd.to_datetime(df["Data"])
        return df

    df = load_notowania()

    def przelicz_portfel(tickery, wagi):
        df_portfel = df[df["Nazwa"].isin(tickery)].copy()
        df_portfel = df_portfel[df_portfel["Data"].between(str(start_date), str(end_date))]
        df_portfel = df_portfel.sort_values("Data")

        grouped = df_portfel.groupby(["Data", "Nazwa"]).first().reset_index()
        pivot = grouped.pivot(index="Data", columns="Nazwa", values="Kurs zamknięcia")
        pivot = pivot.ffill()

        base_prices = pivot.iloc[0]
        scaled = pivot / base_prices
        for t in scaled.columns:
            scaled[t] = scaled[t] * wagi[t] / 100
        result = scaled.sum(axis=1) * kwota_startowa
        return result.reset_index().rename(columns={0: "Wartość"})

    def przelicz_benchmark(ticker):
        df_b = df[df["Nazwa"] == ticker].copy()
        df_b = df_b[df_b["Data"].between(str(start_date), str(end_date))]
        df_b = df_b.sort_values("Data")
        grouped = df_b.groupby("Data").first().reset_index()
        grouped["Wartość"] = grouped["Kurs zamknięcia"] / grouped["Kurs zamknięcia"].iloc[0] * kwota_startowa
        return grouped[["Data", "Wartość"]]

    if t1 and total1 == 100 and t2 and total2 == 100:
        df1 = przelicz_portfel(t1, w1)
        df2 = przelicz_portfel(t2, w2)
        df_b = przelicz_benchmark(benchmark)

        r1 = df1.set_index("Data")["Wartość"].pct_change().dropna()
        r2 = df2.set_index("Data")["Wartość"].pct_change().dropna()
        r_b = df_b.set_index("Data")["Wartość"].pct_change().dropna()

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df1["Data"], df1["Wartość"], label="Portfel 1")
        ax.plot(df2["Data"], df2["Wartość"], label="Portfel 2")
        ax.plot(df_b["Data"], df_b["Wartość"], label="Benchmark", linestyle="--", color="gray")
        ax.set_title("📊 Porównanie Portfeli i Benchmarku")
        ax.set_ylabel("Wartość (PLN)")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        st.subheader("📊 Metryki porównawcze")

        def metryki(zwroty, ref):
            annual = zwroty.mean() * 252
            std = zwroty.std() * np.sqrt(252)
            sharpe = annual / std if std != 0 else 0
            drawdown = (1 + zwroty).cumprod().cummax() - (1 + zwroty).cumprod()
            max_dd = drawdown.max()
            zwroty.index = pd.to_datetime(zwroty.index)
            years = (1 + zwroty).resample("Y").prod() - 1
            best = years.max()
            worst = years.min()
            common_index = zwroty.index.intersection(ref.index)
            zwroty_aligned = zwroty.loc[common_index]
            ref_aligned = ref.loc[common_index]
            corr = np.corrcoef(zwroty_aligned, ref_aligned)[0, 1] if len(common_index) > 1 else np.nan
            return [annual, std, sharpe, -max_dd, best, worst, corr]

        df_met = pd.DataFrame(index=["CAGR", "Volatility", "Sharpe Ratio", "Max Drawdown", "Best Year", "Worst Year", "Correlation"],
                              columns=["Portfel 1", "Portfel 2", "Benchmark"])
        df_met["Portfel 1"] = metryki(r1, r_b)
        df_met["Portfel 2"] = metryki(r2, r_b)
        df_met["Benchmark"] = metryki(r_b, r_b)
        st.dataframe(df_met.style.format("{:.2%}"))
    else:
        st.warning("⚠️ Upewnij się, że oba portfele mają przypisane tickery i suma wag to 100%")

