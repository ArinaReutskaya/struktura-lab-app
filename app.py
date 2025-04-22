import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import urllib.request

st.set_page_config(page_title="Struktura Lab MVP", layout="wide")

# 📁 Wczytywanie danych
@st.cache_data
def load_data():
    csv_path = "notowania_gpw_full.csv"
    if not os.path.exists(csv_path):
        url = "https://www.dropbox.com/scl/fi/dqjun71e9a5syx2xlexrs/notowania_gpw_full.csv?rlkey=irndgl6x7i06knqsihcqtq5iz&dl=1"
        urllib.request.urlretrieve(url, csv_path)
    df = pd.read_csv(csv_path)
    df["Data"] = pd.to_datetime(df["Data"])
    return df

df = load_data()

kategorie = df["Kategoria"].dropna().unique()
tickery_per_kategoria = {
    k: df[df["Kategoria"] == k]["Nazwa"].dropna().unique().tolist()
    for k in kategorie
}

min_date = df["Data"].min().date()
max_date = df["Data"].max().date()

st.title("📈 Struktura Lab - Wybór Portfeli")

# 🔽 Formularz wejściowy
with st.form("parametry_formularza"):
    st.sidebar.header("📅 Parametry analizy")
    start_date = st.sidebar.date_input("Data początkowa", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.sidebar.date_input("Data końcowa", min_value=min_date, max_value=max_date, value=max_date)
    kwota_startowa = st.sidebar.number_input("Kwota startowa (PLN)", min_value=1000, value=10000, step=1000)

    def wybierz_portfel(numer):
        tickers = []
        wagi = {}
        total = 0
        st.subheader(f"Portfel {numer}")
        for kat in ["akcje", "obligacje", "indeksy"]:
            if kat in tickery_per_kategoria:
                selected = st.multiselect(f"{kat.capitalize()} (opcjonalnie)", tickery_per_kategoria[kat], key=f"{kat}{numer}")
                tickers.extend(selected)

        if tickers:
            st.markdown(f"### ⚖️ Wagi dla Portfela {numer}")
            for t in tickers:
                wagi[t] = st.number_input(f"Waga dla {t} (%)", min_value=0, max_value=100, value=round(100/len(tickers)), key=f"waga{numer}_{t}")
                total += wagi[t]
            st.markdown(f"**🔢 Suma wag:** {total}%")
            if total != 100:
                st.error("Suma wag musi wynosić 100%")

        return tickers, wagi, total

    col1, col2, col3 = st.columns(3)
    with col1:
        t1, w1, total1 = wybierz_portfel(1)
    with col2:
        t2, w2, total2 = wybierz_portfel(2)
    with col3:
        benchmark = st.selectbox("Benchmark", tickery_per_kategoria.get("indeksy", []))

    submitted = st.form_submit_button("📊 Analizuj")

if submitted:
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

    if t1 and total1 == 100 and t2 and total2 == 100:
        df1 = przelicz_portfel(t1, w1)
        df2 = przelicz_portfel(t2, w2)
        df_b = przelicz_portfel([benchmark], {benchmark: 100})

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

        st.subheader("🧩 Skład portfeli")
        col_pie1, col_pie2 = st.columns(2)

        with col_pie1:
            st.markdown("**📈 Portfel 1**")
            fig1, ax1 = plt.subplots()
            ax1.pie(list(w1.values()), labels=list(w1.keys()), autopct='%1.1f%%')
            ax1.axis('equal')
            st.pyplot(fig1)

        with col_pie2:
            st.markdown("**📉 Portfel 2**")
            fig2, ax2 = plt.subplots()
            ax2.pie(list(w2.values()), labels=list(w2.keys()), autopct='%1.1f%%')
            ax2.axis('equal')
            st.pyplot(fig2)
    else:
        st.warning("Upewnij się, że oba portfele mają przypisane tickery i suma wag to 100%")
