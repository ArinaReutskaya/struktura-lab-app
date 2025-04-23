📊 Struktura Lab – Analiza portfeli inwestycyjnych na GPW

  Struktura Lab to aplikacja Streamlit umożliwiająca użytkownikom tworzenie dwóch portfeli inwestycyjnych i porównywanie ich wyników z wybranym benchmarkiem. Dane historyczne pobierane są z archiwum notowań GPW (od 2020 roku). 

🔎 Funkcje aplikacji

✅ Intuicyjny wybór instrumentów z kategorii: akcje, obligacje, indeksy  
✅ Możliwość zbudowania dwóch portfeli inwestycyjnych  
✅ Przypisywanie wag procentowych do każdego instrumentu (walidacja sumy wag = 100%)  
✅ Wybór zakresu dat analizy i kwoty początkowej  
✅ Wybór benchmarku z listy indeksów  
✅ Porównanie portfeli względem siebie i względem benchmarku  
✅ Wizualizacje i wykresy wartości portfeli  
✅ Obliczanie kluczowych metryk:
  `CAGR`, `Volatility`, `Sharpe Ratio`, `Max Drawdown`, `Best/Worst Year`, `Correlation`
  
---

📤 Aplikacja domyślnie korzysta z plików:

-> tickery.csv – lekki plik startowy z listą dostępnych instrumentów

-> notowania_gpw_full.csv – pełny plik z danymi dziennymi (umieszczony lokalnie)

Dane można pobrać z Dropbox: https://www.dropbox.com/scl/fi/dqjun71e9a5syx2xlexrs/notowania_gpw_full.csv?rlkey=irndgl6x7i06knqsihcqtq5iz&dl=1
  
---

🚀 Jak uruchomić lokalnie?

1. Zainstaluj wymagane biblioteki: pip install -r requirements.txt
2. Pobierz tickery.csv oraz notowania_gpw_full.csv
3. Odpal aplikację: streamlit run app.py

---

📁 Struktura projektu

📦 StrukturaLab
├── app.py                    ← Główna aplikacja Streamlit
├── requirements.txt          ← Lista zależności
├── README.md                 ← Opis projektu
├── notowania_gpw_full. csv   ← Baza danych (CSV) 
└── tickery.csv               ← Lista tickerów z notowań GPW (CSV)

---

📚 Źródło danych

Dane pochodzą z publicznego archiwum notowań GPW (www.gpw.pl). Projekt ma charakter edukacyjno-analityczny. 

---

💡 Pomysł i wykonanie

Projekt stworzony przez Arina Reutskaya — analityczkę inwestycyjną i miłośniczkę memów 💼📉✨  

---

🔮 Plany na przyszłość
📅 Uzupełnienie danych o lata 2005–2019 z archiwum GPW
📈 Dodanie analizy wpływu dywidend i systematycznych dopłat do portfela
📊 Obliczanie dodatkowych wskaźników:

Monthly returns, Annual returns, Drawdowns, Alpha / Beta / R²

📤 Eksport wyników do PDF lub CSV
📧 Opcjonalna wysyłka e-mail z raportem


---

⚠️ Projekt w wersji MVP — zapraszam do testów i feedbacku!

