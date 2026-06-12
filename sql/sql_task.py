import sqlite3

conn = sqlite3.connect(':memory:')
c = conn.cursor()

c.execute('CREATE TABLE skills (name TEXT, lang TEXT, category TEXT)')
skills = [('Nick', 'C#', 'backend'), ('Nick', 'SQL', 'database'),
          ('Eva', 'Java', 'backend'), ('Vika', 'vue.js', 'frontend'),
          ('Vika', 'SQL', 'database')]
c.executemany('INSERT INTO skills VALUES (?,?,?)', skills)

c.execute('CREATE TABLE languages (name TEXT, lang TEXT)')
langs = [('Nick', 'C#'), ('Nick', 'SQL'), ('Eva', 'Rust'),
         ('Vika', 'Rust'), ('Vika', 'SQL')]
c.executemany('INSERT INTO languages VALUES (?,?)', langs)

c.execute('SELECT name FROM skills GROUP BY name HAVING COUNT(DISTINCT category) = (SELECT COUNT(DISTINCT category) FROM skills)')
r1 = c.fetchall()

c.execute('SELECT name FROM languages GROUP BY name HAVING SUM(CASE WHEN lang="SQL" THEN 1 ELSE 0 END)>0 AND COUNT(DISTINCT lang)>=2')
r2 = c.fetchall()

with open('sql_tasl.sql', 'w') as f:
    f.write(f'1 Сотрудники, которые знают хотя бы по одному языку в каждой категории\n{", ".join(x[0] for x in r1) if r1 else "нет таких"}\n\n')
    f.write(f'2 Знают SQL а также как минимум один дополнительный язык программирования\n{", ".join(x[0] for x in r2) if r2 else "нет таких"}')

conn.close()