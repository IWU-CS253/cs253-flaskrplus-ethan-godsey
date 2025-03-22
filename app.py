# -*- coding: utf-8 -*-
"""
    Flaskr Plus
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.

    Author: Ethan Godsey
"""

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, flash


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('SELECT id, title, text, category FROM entries ORDER BY id DESC')
    entries = cur.fetchall()

    lst_cats = db.execute('SELECT DISTINCT category FROM entries').fetchall()
    return render_template('show_entries.html', entries=entries, lst_cats=lst_cats)


@app.route('/add', methods=['POST'])
def add_entry():
    db = get_db()
    db.execute('insert into entries (title, text, category) values (?, ?, ?)',
               [request.form['title'], request.form['text'], request.form['category']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/show', methods=['POST'])
def show():
    db = get_db()

    # get the category selected in the dropdown
    selected = request.form.get('category', 'All')

    # if it is the All, show all posts
    if selected == 'All':
        cats = db.execute('SELECT id, title, text, category FROM entries')

    # otherwise show posts with specific category
    else:
        cats = db.execute('SELECT id, title, text, category FROM entries WHERE category = ?', (selected,))


    entries = cats.fetchall()

    # for some reason this is not passing over, I couldn't figure out why.
    # there is a working java filter in a previous version of my code
    lst_cats = db.execute('SELECT DISTINCT category FROM entries').fetchall()

    return render_template('show_entries.html', lst_cats=lst_cats, entries=entries)

@app.route('/delete', methods=['POST'])
def delete_post():
    # post the title of the entry deleted
   title = request.form["title"]
   db = get_db()

    # delete the row from the table, referencing the saved hidden attr
   db.execute('DELETE FROM entries WHERE title = ?', (title,))
   db.commit()
   return redirect(url_for('show_entries'))

@app.route('/edit', methods=['POST'])
def edit_post():
    post_id = request.form.get('id')
    title = request.form.get('title')
    category = request.form.get('category')
    text = request.form.get('text')

    return render_template("edit.html", post_id=post_id, title=title, category=category, text=text)
@app.route('/update', methods=['POST'])
def update_post():
    db = get_db()

    post_id = request.form.get('id')
    new_title = request.form.get('new_title')
    new_text = request.form.get('new_text')
    new_category = request.form.get('new_category')
    db.execute('UPDATE entries SET title = ?, text = ?, category = ? WHERE id = ?',
               (new_title, new_text, new_category, post_id))
    db.commit()

    entries = db.execute('SELECT title, text, category FROM entries ORDER BY id DESC').fetchall()

    flash("Post updated!")
    return render_template('show_entries.html', entries=entries)
