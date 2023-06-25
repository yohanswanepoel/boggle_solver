# Boggle solver in Python

## Tech used
* Mostly plain python
* SQL Lite (started with DuckDB but for this use case SQL lite was faster)
* Different optimisations took it from 30 seconds at the start down to just over a second on test board

## Create DB
```bash
sqlite3 Words.db
```

## Import CSV
* Import CSV into temporary table
* created optimised search indexes this speeds it up alot (30% faster than having a single columnt with a like only query)

```sql
.import wordlist_header.csv words

CREATE TABLE word_indexed AS 
    select 
        substr(word,1,3) as word3, 
        substr(word,1,4) as word4,
        substr(word,1,5) as word5,
        substr(word,1,6) as word6,   
        word 
    from words;


create index index_words_3 on word_indexed(word3);
create index index_words_4 on word_indexed(word4);
create index index_words_5 on word_indexed(word5);
create index index_words_6 on word_indexed(word6);
create index index_words_all on word_indexed(word);

drop table words; 

.quit 
```

