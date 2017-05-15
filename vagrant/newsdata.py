import psycopg2
import datetime

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=news")


def executeQuery(query, *kw):
    db = connect()
    db_cursor = db.cursor()
    db_cursor.execute(query, *kw)
    db.commit()
    db.close()


def question1():

    """
    Returns a list of three most popular articles of all time
    with number of views, sorted by views in desc order.
    """
    db = connect()
    db_cursor = db.cursor()
    query = "SELECT title, views FROM article_views ORDER BY views DESC LIMIT 3"
    db_cursor.execute(query)
    results = [(str(row[0]), int(row[1]))
               for row in db_cursor.fetchall()]
    db.commit()
    db.close()

    for i in xrange(len(results)):
        print "%s - %d views" % (results[i][0], results[i][1])
    return results


def question2():
    """
    Returns a list of most popular authors of all time
    with number of views, sorted by views in desc order.
    """
    db = connect()
    db_cursor = db.cursor()
    query = "SELECT name, sum(views) AS views FROM author_views_by_article GROUP BY name ORDER BY views DESC"
    db_cursor.execute(query)
    results = [(str(row[0]), int(row[1]))
               for row in db_cursor.fetchall()]
    db.commit()
    db.close()

    for i in xrange(len(results)):
        print "%s - %d views" % (results[i][0], results[i][1])
    return results


def question3():
    """
    Returns list of days with more than 1% of requests that lead to errors
    """
    db = connect()
    db_cursor = db.cursor()
    query = "SELECT date, 100.0 * errors/requests as perc_errors FROM date_requests WHERE 100.0 * errors/requests > 1 ORDER BY perc_errors DESC"
    db_cursor.execute(query)
    results = [(str(row[0]), round((row[1]), 2))
               for row in db_cursor.fetchall()]
    db.commit()
    db.close()

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
