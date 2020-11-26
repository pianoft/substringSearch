from flask import request, redirect, url_for, render_template, flash, session, Blueprint
from flask_blog import app
from flask_blog import db
from flask_blog.models.entries import Entry
from flask_blog.views.views import login_required
from sqlalchemy.sql.expression import func
from bs4 import BeautifulSoup
import requests
import bs4

import subprocess


def runBashCommand(commands):
    subprocess.run([commands], shell=True)
    return


@app.route('/')
@login_required
def show_entries():
    global state
    entries = Entry.query.order_by(Entry.id.desc()).all()
    flash("現在表示されてる記事の数:"+str(len(entries))+"個")
    return render_template('entries/index.html', entries=entries)


setOfFileNames = set()


@app.route('/entries/stringSearch', methods=['POST', 'GET'])
@login_required
def stringSearch():
    global setOfFileNames
    entries = Entry.query.order_by(Entry.id.desc()).all()
    specifiedDesiredStrings = request.form['stringSearch'].split('、')
    fr = open("stringSearch.txt", "r")
    titlesOfFiles = fr.readlines()
    fr.close()
    newArticlesWhichWillBeListedInPage = set()
    for fileName in titlesOfFiles:
        if fileName in setOfFileNames:
            continue
        fileName = fileName[:len(fileName)-1]
        # print(fileName)
        fr2 = open(
            './rawTextsOfFiles/'+fileName, 'r')
        allTextsInArticle = fr2.read()
        fr2.close()
        remnantNumberOfSatisfactions = len(specifiedDesiredStrings)
        for eachString in specifiedDesiredStrings:
            remnantNumberOfSatisfactions += -(eachString in allTextsInArticle)
        if remnantNumberOfSatisfactions == 0:
            setOfFileNames.add(fileName)
            x1 = allTextsInArticle.find('<title>')+7
            x2 = allTextsInArticle.find('</title>')-10
            newArticlesWhichWillBeListedInPage.add(
                (fileName, allTextsInArticle[x1:x2]))
    print(specifiedDesiredStrings)
    if len(newArticlesWhichWillBeListedInPage) == 0:  # 新規の記事数が0の時このif文を書かないと検索システムが動かなくなる
        return redirect(url_for('show_entries'))

    for article in newArticlesWhichWillBeListedInPage:
        # print("http://pathtimeblog.com/archives/" +
        #       article[0][0:len(article[0])-4])
        entry = Entry(
            title="http://pathtimeblog.com/archives/" +
            article[0][0:len(article[0])-4]+".html",
            text=article[1],
        )
        db.session.add(entry)
        db.session.commit()
    return redirect(url_for('show_entries'))


@app.route('/entries/deleteAllArticles', methods=['POST', 'GET'])
@login_required
def deleteAllArticles():
    entries = Entry.query.order_by(Entry.id.desc()).all()
    for entry in entries:
        db.session.delete(entry)
        db.session.commit()
    return redirect(url_for('show_entries'))
