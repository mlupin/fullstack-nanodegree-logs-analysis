#!/usr/bin/env python

import psycopg2
import datetime


def connect(database_name="news"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")


def executeQuery(query, *kw):
    db, cursor = connect()
    cursor.execute(query, *kw)
    results = [(str(row[0]), round((row[1]), 2))
               for row in cursor.fetchall()]
    db.commit()
    db.close()
    return results


def question1():

    """
    Returns a list of three most popular articles of all time
    with number of views, sorted by views in desc order.
    """
    query = """
            SELECT title, views
            FROM article_views
            ORDER BY views DESC
            LIMIT 3
            """
    results = executeQuery(query)

    for i in xrange(len(results)):
        print "%s - %d views" % (results[i][0], results[i][1])
    return results


def question2():
    """
    Returns a list of most popular authors of all time
    with number of views, sorted by views in desc order.
    """
    query = """
            SELECT name, sum(views) AS views
            FROM author_views_by_article
            GROUP BY name
            ORDER BY views DESC
            """
    results = executeQuery(query)

    for i in xrange(len(results)):
        print "%s - %d views" % (results[i][0], results[i][1])
    return results


def question3():
    """
    Returns list of days with more than 1% of requests that lead to errors
    """
    query = """
            SELECT date,
            100.0 * errors/requests as perc_errors
            FROM date_requests
            WHERE 100.0 * errors/requests > 1
            ORDER BY perc_errors DESC
            """
    results = executeQuery(query)

    for i in xrange(len(results)):
        date = datetime.datetime.strptime(results[i][0],
                                          '%Y-%m-%d').strftime("%B %d, %Y")
        print "%s - %s%% errors" % (date, results[i][1])
    return results


print "\nThree most popular articles of all time:"
question1()
print "\nList of most popular authors of all time:"
question2()
print "\nList of days with more than 1% of requests that lead to errors:"
question3()
