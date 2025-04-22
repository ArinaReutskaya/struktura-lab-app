# 📊 Struktura Lab MVP

**Struktura Lab** to aplikacja Streamlit umożliwiająca użytkownikom tworzenie dwóch portfeli inwestycyjnych i porównywanie ich wyników z wybranym benchmarkiem. Dane historyczne pobierane są z archiwum notowań GPW (od 2020 roku). 

## 🔎 Funkcje aplikacji

- ✅ Wybór instrumentów z kategorii: **akcje**, **obligacje**, **indeksy**
- ✅ Przypisywanie wag procentowych do każdego instrumentu
- ✅ Ustawienie zakresu dat oraz kwoty początkowej
- ✅ Porównanie dwóch portfeli między sobą oraz względem benchmarku
- ✅ Wizualizacja oraz metryki:  
  `CAGR`, `Volatility`, `Sharpe Ratio`, `Max Drawdown`, `Best/Worst Year`, `Correlation`
  
---

## 🚀 Jak uruchomić lokalnie?

1. Zainstaluj wymagane biblioteki:
pip install -r requirements.txt
2. Odpal aplikację:
streamlit run app.py

---

## 📁 Struktura projektu

📦 StrukturaLab
├── app.py               ← Główna aplikacja Streamlit
├── requirements.txt     ← Lista zależności
├── README.md            ← Opis projektu
└──  .gitignore           ← Ignorowane pliki (CSV)


---

## 📚 Źródło danych

Dane pochodzą z publicznego archiwum notowań GPW (www.gpw.pl). Projekt ma charakter edukacyjno-analityczny.

---

## 💡 Pomysł i wykonanie

Projekt stworzony przez Arina Reutskaya — analityczkę inwestycyjną i miłośniczkę memów 💼📉✨  

---

## 🧪 Plany na przyszłość

- Symulacje Monte Carlo 🔮  
- Random Forest do klasyfikacji portfeli 🌲  
- Generowanie raportów PDF i automatyczna wysyłka e-mail  
- Tryb premium z dodatkowymi metrykami  

---

> ⚠️ Projekt w wersji MVP — zapraszam do testów i feedbacku!

