def gen_seeds():
    import uuid
    from database import db_session, Source
    Source
    source_arr = [{
        "base_url": "http://androidweekly.net/issues/",
        "name": "Android Weekly",
        "tag": "android"
    }]
    for s in source_arr:
        print("Generating Source.......\n\n\n")
        source_id = str(uuid.uuid4().hex)

        source = Source(id=source_id, object_id=source_id, img="http://via.placeholder.com/350x150/ffffff?text=A",
                        base_url=str(s["base_url"]), tag=str(s["tag"]),
                        name=str(s["name"]))
        db_session.add(source)
        db_session.commit()
        # for isue in range(1, 50):
        #     print("Generating Issue........\n\n")
        #     issue_id = str(uuid.uuid4().hex)
        #     issue = Issue(id=issue_id, object_id=issue_id, issue_number=str(isue), source_id=source.object_id,
        #                   url="http://randomweekly.com/issue/" + str(isue))
        #     db_session.add(issue)
        #     db_session.commit()
        #
        #     for art in range(1, 20):
        #         from database import Article
        #         print("Generating Article.......\n")
        #         article_id = str(uuid.uuid4().hex)
        #         article = Article(id=article_id, object_id=article_id,
        #                           pre_content="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
        #                           issue_id=issue.object_id, source_id=source_id,
        #                           url="http://randomweekly.com/issue/" + str(isue) + "/" + str(art),
        #                           img="http://via.placeholder.com/100x100/f96c30/FFFFFF?text=A")
        #         db_session.add(article)
        #         db_session.commit()

    pass
