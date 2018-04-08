import random
import uuid

from pip._vendor import requests
from pyquery import PyQuery as pq

from database import Issue, db_session, Article


class AndroidWeeklyScrapper(object):
    def scrap_response(self, source_id, source_url, issue_number):
        issue = Issue.query.filter(Issue.url == "{0}{1}".format(source_url, "issue-{0}".format(issue_number))).first()
        if issue is None:
            try:
                fetch_response = requests.get("{0}{1}".format(source_url, "issue-{0}".format(issue_number)))

                raw = pq(fetch_response.content.decode('utf-8'))

                issue_id = str(uuid.uuid4().hex)
                issue = Issue(id=issue_id, object_id=issue_id, issue_number=str(issue_number), source_id=source_id,
                              url=str(
                                  "{0}{1}".format(source_url, "issue-{0}".format(issue_number))))
                db_session.add(issue)
                db_session.commit()
                raw(".issues table").map(lambda e, table_row:
                                         AndroidWeeklyScrapper.scrap_n_save_data(self, table_row, issue_id, source_id))
            except  Exception as e:
                db_session.rollback()
                print(e)
            finally:
                db_session.close()

            return True
        else:
            return False

    def scrap_n_save_data(self, table_dom, issue_id, source_id):
        table = pq(table_dom)("tr td")
        article_id = str(uuid.uuid4().hex)
        r = lambda: random.randint(0, 255)
        try:
            if table.children("p").text() is not None and table.children(
                    ".main-url").text() is not None and table.children(
                    ".article-headline").attr("href"):
                article = Article(id=article_id, object_id=article_id,
                                  pre_content=table.children("p").text().encode('utf-8'),
                                  issue_id=issue_id, source_id=source_id,
                                  main_url=table.children(".main-url").text().encode('utf-8'),
                                  url=table.children(".article-headline").attr("href").encode('utf-8'),
                                  title=table.children(".article-headline").text().encode('utf-8'),
                                  img="http://via.placeholder.com/300x300/{0}/{1}?text={2}".format(
                                      '#%02X%02X%02X' % (r(), r(), r()), "#FFFFFF", "A").encode('utf-8'))
                db_session.add(article)
                db_session.commit()
        except Exception as e:
            db_session.rollback()
            print(e)
        finally:
            db_session.close()
