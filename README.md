# Logs Analysis

### Requirements

This project includes a [Vagrant](https://www.vagrantup.com/) virtual environment and [VirtualBox](https://www.virtualbox.org/). To use it, install VirtualBox and (Vagrant), and follow the project installation steps bellow.

### Installation

1. Clone the project repository and connect to the virtual machine
```
$ git clone https://github.com/mlupin/fullstack-nanodegree-logs-analysis.git
$ cd fullstack-nanodegree-logs-analysis
$ vagrant up
$ vagrant ssh
$ cd /vagrant
```
2. Download the data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). Unzip this file after downloading it. The file inside is called *newsdata.sql*. Put this file into the vagrant directory, which is shared with the virtual machine. Setup and load the data.
```
ubuntu@ubuntu-xenial:~$ cd /vagrant
ubuntu@ubuntu-xenial:/vagrant$ psql -d news -f newsdata.sql
```
3. Connect to the database and create views. To create views use the code provided under the 'Create Views' section.
```sh
ubuntu@ubuntu-xenial:/vagrant$ psql -d news
```
4. Run the code print results
```sh
ubuntu@ubuntu-xenial:/vagrant$ python newsdata.py
```

### Create Views
This project has 5 different views.
```
                List of relations
 Schema |          Name           | Type | Owner  
--------+-------------------------+------+--------
 public | article_views           | view | ubuntu
 public | articles_by_author      | view | ubuntu
 public | author_views_by_article | view | ubuntu
 public | date_requests           | view | ubuntu
 public | path_views              | view | ubuntu
```

1. *path_views* returns a list of paths and the number of times each path was visited in descending order.
```
CREATE VIEW path_views AS
	SELECT path,
		COUNT(CASE WHEN status LIKE '%200 OK%' THEN 1 END) AS views
	FROM log
	GROUP BY log.path
	ORDER BY views DESC;
```
2. *article_views* returns a list of article titles and the number of times each article was viewed in descending order.
```
CREATE VIEW article_views AS
	SELECT articles.title,
		COUNT(CASE WHEN log.status LIKE '%200 OK%' THEN 1 END) AS views
	FROM articles LEFT JOIN log
	ON log.path LIKE '%' || articles.slug || '%'
	GROUP BY articles.title
	ORDER BY views DESC;
```
3. *author_views_by_article* returns a list of article titles, article author, and the number of times each article was viewed.
```
CREATE VIEW author_views_by_article AS
	SELECT article_views.title,
		name,
		views
	FROM article_views JOIN articles_by_author
	ON article_views.title = articles_by_author.title;
```
4. *articles_by_author* returns a list of article titles and authors.
```
CREATE VIEW articles_by_author AS
	SELECT title,
		name
	FROM articles JOIN authors
	ON articles.author = authors.id;
```
5.  *date_requests* returns a list of dates, number of successful request, number of unsuccessful requests, and total number of requests.
```
CREATE VIEW  date_requests AS
	SELECT time::timestamp::date AS date,
		COUNT(CASE WHEN status LIKE '%200 OK%' THEN 1 END) AS views,
		COUNT(CASE WHEN status LIKE '%404 NOT FOUND%' THEN 1 END) AS errors,
		COUNT(method) AS requests
	FROM log
	GROUP BY date
	ORDER BY date;

```
### Results
```
ubuntu@ubuntu-xenial:/vagrant$ python newsdata.py 

Three most popular articles of all time:
Candidate is jerk, alleges rival - 338647 views
Bears love berries, alleges bear - 253801 views
Bad things gone, say good people - 170098 views

List of most popular authors of all time:
Ursula La Multa - 507594 views
Rudolf von Treppenwitz - 423457 views
Anonymous Contributor - 170098 views
Markoff Chaney - 84557 views

List of days with more than 1% of requests that lead to errors:
July 17, 2016 - 2.26% errors
```