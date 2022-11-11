import text_preprocessing
import sqlite3

conn = sqlite3.connect("words.db")

c = conn.cursor()

c.execute("""DROP TABLE IF EXISTS words""")
c.execute("""DROP TABLE IF EXISTS pos""")
c.execute("""DROP TABLE IF EXISTS inflections""")

c.execute(
    """CREATE TABLE IF NOT EXISTS words (
 			word_id integer primary key,
			pos_type varchar(50),
 			spelling varchar(50))
 	"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS pos (
 			pos_type varchar(50))

 	"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS inflections (
 			word_id integer,
 			inflected_form varchar(50),
 			FOREIGN KEY (word_id) REFERENCES words(word_id))
	"""
)


conn.commit()

# define part of speech tags set 

pos = set([v[0] for v in text_preprocessing.lemma_info.values() if v[0] is not None])

for i in pos:
    c.execute("INSERT INTO pos VALUES (?)", (i,))
    conn.commit()

i = 1
for k, v in text_preprocessing.lemma_info.items():
    c.execute("INSERT INTO words VALUES (?, ?, ?)", (i, v[0], k))
    for inf in v[1]:
        c.execute("INSERT INTO inflections VALUES (?, ?)", (i, inf))
    i += 1
    conn.commit()

conn.close()
