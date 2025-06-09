from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import markdown
import re


# Tooltip spuštění
def replace_terms(text, definitions):
    def replacer(match):
        word = match.group(0)
        if word in definitions:
            title = definitions[word]["title"]
            url = definitions[word]["url"]
            return f'<a href="{url}" title="{title}">{word}</a>'
        return word

    pattern = r'\b(' + '|'.join(re.escape(term) for term in definitions.keys()) + r')\b'
    return re.sub(pattern, replacer, text)

app = Flask(__name__)

# Zobrazování odstavců, nadpisů...
@app.template_filter('markdown')
def markdown_filter(text):
    return markdown.markdown(text)


# Funkce pro připojení k databázi
def get_db_connection():
    conn = sqlite3.connect('wiki.db')
    conn.row_factory = sqlite3.Row
    return conn


# Tooltip
def get_term_definitions():
    conn = get_db_connection()
    rows = conn.execute('SELECT name, tooltip, url FROM terms').fetchall()
    conn.close()

    return {
        row['name']: {
            "title": row['tooltip'],
            "url": row['url']
        } for row in rows
    }


# Úvodní stránka – seznam článků
@app.route('/')
def index():
    query = request.args.get('q')
    conn = get_db_connection()

    if query:
        articles = conn.execute(
            "SELECT * FROM articles WHERE title LIKE ? OR content LIKE ?",
            (f'%{query}%', f'%{query}%')
        ).fetchall()
    else:
        articles = conn.execute('SELECT * FROM articles').fetchall()



# Nově: poslední 3 články podle času vytvoření
    latest = conn.execute(
        'SELECT * FROM articles ORDER BY created DESC LIMIT 3'
    ).fetchall()

    conn.close()
    return render_template('index.html', articles=articles, latest=latest)


# Detail článku
@app.route('/article/<int:id>')
def article(id):
    conn = get_db_connection()
    article = conn.execute('SELECT * FROM articles WHERE id = ?', (id,)).fetchone()
    conn.close()

    if article is None:
        return 'Článek nenalezen.', 404

    # Získat definice pojmů z databáze
    term_definitions = get_term_definitions()

    # Nahradit výskyty termínů v obsahu článku
    replaced_content = replace_terms(article['content'], term_definitions)

    # Vrátit stránku s upraveným obsahem
    return render_template('detail.html', article=article, content=replaced_content)



# Přidání nového článku
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        subcategory = request.form.get('subcategory') or None
        grouping = request.form.get('grouping') or None

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO articles (title, content, category, subcategory, grouping)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, content, category, subcategory, grouping))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('create.html')


# Zobrazení podkategorii
@app.route('/encyklopedie/<subcategory>')
def encyclopedia_sub(subcategory):
    conn = get_db_connection()
    articles = conn.execute('''
        SELECT * FROM articles
        WHERE category = 'Encyklopedie' AND subcategory = ?
    ''', (subcategory,)).fetchall()
    conn.close()
    return render_template('subcategory.html', articles=articles, subcategory=subcategory)


# Zobrazení podkategorii FAUNA
@app.route('/encyklopedie/fauna/<group>')
def fauna_group(group):
    conn = get_db_connection()
    articles = conn.execute('''
        SELECT * FROM articles
        WHERE category = 'Encyklopedie'
        AND subcategory = 'Fauna'
        AND grouping = ?
    ''', (group,)).fetchall()
    conn.close()
    return render_template('fauna_group.html', articles=articles, group=group)


# Editace článku
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    article = conn.execute('SELECT * FROM articles WHERE id = ?', (id,)).fetchone()

    if article is None:
        return 'Článek nenalezen.', 404

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn.execute('UPDATE articles SET title = ?, content = ? WHERE id = ?', (title, content, id))
        conn.commit()
        conn.close()

        return redirect(url_for('article', id=id))

    conn.close()
    return render_template('edit.html', article=article)


# Mazání článku
@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    article = conn.execute('SELECT * FROM articles WHERE id = ?', (id,)).fetchone()

    if article is None:
        conn.close()
        return 'Článek nenalezen.', 404

    conn.execute('DELETE FROM articles WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))


# Kategorie článků
@app.route('/category/<name>')
def category(name):
    conn = get_db_connection()
    articles = conn.execute(
        'SELECT * FROM articles WHERE category = ?',
        (name,)
    ).fetchall()
    conn.close()
    return render_template('category.html', articles=articles, category=name)


# cesta na článek pro tooltip kliknutí
@app.route('/encyklopedie/<subcategory>/<name>')
def encyclopedia_article(subcategory, name):
    conn = get_db_connection()
    article = conn.execute(
        'SELECT * FROM articles WHERE category = ? AND subcategory = ? AND title = ?',
        ('Encyklopedie', subcategory, name)
    ).fetchone()
    conn.close()

    if article is None:
        return f"Článek '{name}' v kategorii '{subcategory}' nenalezen.", 404

    # Definice a nahrazení pojmů
    term_definitions = get_term_definitions()
    content = replace_terms(article['content'], term_definitions)

    return render_template('detail.html', article=article, content=content)


# další funkce


if __name__ == '__main__':
    app.run(debug=True)