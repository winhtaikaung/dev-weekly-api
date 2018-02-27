def gen_seeds():
    import uuid
    from database import db_session, Source, Issue
    Source

    source_id = str(uuid.uuid4().hex)
    issue_id = str(uuid.uuid4().hex)

    source = Source(id=source_id, object_id=source_id, img="http://via.placeholder.com/350x150/ffffff?text=A",
                    name="Yangon Weekly")
    db_session.add(source)
    db_session.commit()

    issue = Issue(id=issue_id, object_id=issue_id, source_id=source.object_id, url="http://randomweekly.com")
    db_session.add(issue)
    db_session.commit()

    for art in range(0, 10):
        from database import Article

        article_id = str(uuid.uuid4().hex)
        article = Article(id=article_id, object_id=article_id,
                          issue_id=issue.object_id, source_id=source_id, url="http://randomweekly.com/issue/1/1",
                          img="http://via.placeholder.com/50x50?text=A")
        db_session.add(article)
        db_session.commit()

    pass
