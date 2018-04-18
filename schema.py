import calendar
import datetime

import graphene
from flask import render_template
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from pip._vendor import requests
from pyquery import PyQuery as pq
from readability import Document
from sqlalchemy import or_

from database import db_session, User as UserModel, Source as SourceModel, Issue as IssueModel, \
    Article as ArticleModel, gen_offset_from_page, generate_meta
from readingtime import ReadingTime


class Users(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node,)


class Source(SQLAlchemyObjectType):
    class Meta:
        model = SourceModel
        interfaces = (relay.Node,)


class Issue(SQLAlchemyObjectType):
    class Meta:
        model = IssueModel
        interfaces = (relay.Node,)


class Article(SQLAlchemyObjectType):
    class Meta:
        model = ArticleModel
        interfaces = (relay.Node,)


class MetaObject(graphene.ObjectType):
    total_pages = graphene.Int()
    current = graphene.Int()
    prev_page = graphene.Int()
    next_page = graphene.Int()


class SourceResult(graphene.ObjectType):
    meta = graphene.Field(MetaObject)
    data = graphene.List(of_type=Source)


class IssueResult(graphene.ObjectType):
    meta = graphene.Field(MetaObject)
    data = graphene.List(of_type=Issue)


class ArticleResult(graphene.ObjectType):
    meta = graphene.Field(MetaObject)
    data = graphene.List(of_type=Article)


# Used to Create New User
class createUser(graphene.Mutation):
    class Input:
        name = graphene.String()
        email = graphene.String()
        username = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(Users)

    @classmethod
    def mutate(cls, _, args, context, info):
        user = UserModel(name=args.get('name'), email=args.get('email'), username=args.get('username'))
        db_session.add(user)
        db_session.commit()
        ok = True
        return createUser(user=user, ok=ok)


# Used to Change Username with Email
class changeUsername(graphene.Mutation):
    class Input:
        username = graphene.String()
        email = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(Users)

    @classmethod
    def mutate(cls, _, args, context, info):
        query = Users.get_query(context)
        email = args.get('email')
        username = args.get('username')
        user = query.filter(UserModel.email == email).first()
        user.username = username
        db_session.commit()
        ok = True

        return changeUsername(user=user, ok=ok)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # user = SQLAlchemyConnectionField(Users)

    sources = graphene.Field(lambda: SourceResult, limit=graphene.Int(), page=graphene.Int())
    source = graphene.Field(lambda: Source, source_id=graphene.String(), source_name=graphene.String())

    def resolve_sources(self, args, context, info):
        limit = args.get("limit")
        page = args.get("page")
        all_issue = Source.get_query(context).all()
        result = Source.get_query(context).limit(limit).offset(gen_offset_from_page(page, limit))
        meta_obj = generate_meta(limit, page, all_issue)
        return IssueResult(data=result,
                           meta=MetaObject(total_pages=meta_obj["total_page"], current=meta_obj["current"],
                                           prev_page=meta_obj["prev_page"], next_page=meta_obj["next_page"]))

    def resolve_source(self, args, context, info):
        query = Source.get_query(context)
        id = args.get('source_id')
        name = args.get('source_name')
        source = query.filter(or_(SourceModel.object_id == id, (SourceModel.name == name))).first()

        return source

    # issues = SQLAlchemyConnectionField(Issue)
    issues = graphene.Field(lambda: IssueResult, limit=graphene.Int(), page=graphene.Int(), source_id=graphene.String())
    issue = graphene.Field(lambda: Issue, issue_id=graphene.String(), url=graphene.String(),
                           issue_number=graphene.String())

    def resolve_issues(self, args, context, info):
        limit = args.get("limit")
        page = args.get("page")
        source_id = args.get("source_id")
        all_issue = Issue.get_query(context).filter(IssueModel.source_id == source_id).all()
        result = Issue.get_query(context).filter(IssueModel.source_id == source_id).limit(limit).offset(
            gen_offset_from_page(page, limit))
        meta_obj = generate_meta(limit, page, all_issue)
        return IssueResult(data=result,
                           meta=MetaObject(total_pages=meta_obj["total_page"], current=meta_obj["current"],
                                           prev_page=meta_obj["prev_page"], next_page=meta_obj["next_page"]))

    def resolve_issue(self, args, context, info):
        query = Issue.get_query(context)
        id = args.get("issue_id")
        url = args.get("issue_url")
        issue_number = args.get("issue_number")
        issue = query.filter(
            or_(IssueModel.object_id == id, (IssueModel.url == url),
                (IssueModel.issue_number == issue_number))).first()
        return issue

    article = graphene.Field(lambda: Article, article_id=graphene.String(), article_content=graphene.String())
    articles = graphene.Field(lambda: ArticleResult, limit=graphene.Int(), page=graphene.Int(),
                              issue_id=graphene.String())

    def resolve_articles(self, args, context, info):
        limit = args.get("limit")
        page = args.get("page")
        issue_id = args.get("issue_id")
        all_issue = Article.get_query(context).filter(ArticleModel.issue_id == issue_id).all()
        result = Article.get_query(context).filter(ArticleModel.issue_id == issue_id).limit(limit).offset(
            gen_offset_from_page(page, limit))
        meta_obj = generate_meta(limit, page, all_issue)
        return ArticleResult(data=result,
                             meta=MetaObject(total_pages=meta_obj["total_page"], current=meta_obj["current"],
                                             prev_page=meta_obj["prev_page"], next_page=meta_obj["next_page"]))

    def resolve_article(self, args, context, info):
        query = Article.get_query(context)
        id = args.get("article_id")
        title = args.get("article_content")
        article = query.filter(
            or_(ArticleModel.object_id == id, (ArticleModel.title.like("%title%")))).first()

        try:
            if article.article_view_content is not None:
                # TIME based DB content cache with cache expire of 1 day
                if calendar.timegm(datetime.datetime.utcnow().utctimetuple()) - article.updated_date > 86400:
                    response = requests.get(
                        article.url)
                    doc = Document(response.text)
                    texts = pq(response.text)('body p').text()
                    article.article_view_content = str(
                        render_template('body_template.html', article_content=doc.summary(True),
                                        title=str(doc.short_title()),
                                        article=str(doc.title()),
                                        read_time=str(ReadingTime().estimate(texts, True)),
                                        base_url=article.main_url, article_url=article.url)).replace("\"", "'") \
                        .replace("\n", "").replace("\t", "").replace("$", "&#36;").encode(
                        'utf-8')
                    article.updated_date = int(calendar.timegm(datetime.datetime.utcnow().utctimetuple()))
                    db_session.commit()
                else:
                    pass
            else:
                response = requests.get(
                    article.url)
                doc = Document(response.text)
                texts = pq(response.text)('body p').text()

                article.article_view_content = str(
                    render_template('body_template.html', article_content=doc.summary(True),
                                    title=str(doc.short_title()),
                                    article=str(doc.title()),
                                    read_time=str(ReadingTime().estimate(texts, True)),
                                    base_url=article.main_url, article_url=article.url)) \
                    .replace("\"", "'").replace("\n", "").replace("\t", "").replace("$", "&#36;").encode('utf-8')
                article.updated_date = int(calendar.timegm(datetime.datetime.utcnow().utctimetuple()))
                db_session.commit()
        except Exception as e:
            print(e)
            db_session.rollback()

        return article

    # find_user = graphene.Field(lambda: Users, username=graphene.String())
    # all_users = SQLAlchemyConnectionField(Users)

    def resolve_find_user(self, args, context, info):
        query = Users.get_query(context)
        username = args.get('username')
        return query.filter(UserModel.username == username).first()


class MyMutations(graphene.ObjectType):
    create_user = createUser.Field()
    change_username = changeUsername.Field()


schema = graphene.Schema(query=Query, types=[Source, Issue, Article])
