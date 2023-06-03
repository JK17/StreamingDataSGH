# StreamingDataSGH

# Jak odpalić skrypt za pierwszym razem
1. Uruchomić dockerowy obraz z zajęć
2. uruchomić w normalnym terminalu komendy kafki 
`docker exec broker kafka-topics --bootstrap-server broker:9092 --create --topic test2`
zamiast test2 mozna dac inna nazwe tylko wtedy trzeba zmienic to w kodzie, luzik
3. Następnie w folderze notebooks utworzyć nowy folder nazwać jak się chce i tam wrzucić repo
4. Następnie w terminalu w Jupyterze (jak się kliknie Nowy launcher to tam jest do wyboru)
trzeba przejść do folderu gdzie znajdują się nasze kody i uruchomić komendę `python wysylanie_danych_temperatura.py`
wtedy dane się wysyłają
5. Aby odebrać dane z kafki przez sparka trzeba uruchomić nowy terminal w jupyterze znowu przejść do folderu z naszymi kodami i uruchomić komendę `spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 spark_odbierz_dane.py`
6. Powinien się utworzyć folder wyniki w którym są dane w formacie parquet, aby je wczytać do df, przykład jest w *try_get_parquet_please.ipynb* po prostu cały ten folder należy potraktować jak plik
7. Jeśli chcecie coś naprawić lub się zepsuło to warto usunąć ten folder i spróbować jeszcze raz

# Jak odpalić skrypt następnym razem
1. Jeśli już w kafce jest gotowy topic to wystarczy punkt 4.-6.

# Uwagi
- plik parquet traktujemy jako naszą "bazę danych"
- przy przechodzeniu przez foldery w terminalu przydają się komendy 
    - `ls` aby wyświetlić w aktulanym położeniu foldery i pliki
    - `cd <nazwa>` aby przejsc do folderu o podanej nazwie
    - `cd ..` aby przejść wyżej 
    - tab uzupełnia nazwę więc nie trzeba pisać całej nazwy jeśli jest jednoznacznie zmatchowana 