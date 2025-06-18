# Sinapsaury
# Sinapsaury Wiki

Sinapsaury is a small Flask based personal wiki application. It stores articles in a SQLite database and allows browsing them by categories and subcategories. Articles are written in Markdown and can contain terms that become tooltip links.

## Features

- **Categories** – Articles belong to categories such as *Encyklopedie*, *Příběh* and *Novinky*. From the index page you can filter articles by category.
- **Subcategories** – The *Encyklopedie* category offers subcategories like *Fauna*, *Flora*, *Technologie* and *Kodex* with further grouping for fauna (e.g. *Savci*, *Plazi*, *Draci*, *Silica*).
- **Tooltips** – Words defined in the `terms` table are automatically replaced with links that show a tooltip when hovered and lead to another article.
- **Markdown support** – Article contents are rendered from Markdown using the `markdown` package.
- **Search and article management** – You can search articles, create new ones, edit existing ones and delete them from the web interface.

## Setup

1. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Install dependencies**
   ```bash
   pip install Flask markdown
   ```
3. **Initialize the database**
   Navigate to the `moje_wiki` directory and run the database scripts:
   ```bash
   cd moje_wiki
   python init_db.py        # create the articles table
   python upgrade_db.py     # add category column
   python upgrade_db_2.py   # add subcategory column
   python upgrade_db_3.py   # add created timestamp
   python upgrade_db_4.py   # add grouping column
   python upgrade_terms.py  # create the terms table
   python insert_terms.py   # insert sample tooltip terms
   ```
   If you need a clean start later, run `python reset_db.py`.

## Running

While still inside `moje_wiki` with the virtual environment activated, launch the application:

```bash
python app.py
```

Open `http://localhost:5000` in your browser to see the wiki.
