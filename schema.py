import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from sqlalchemy import or_

from database import db_session, User as UserModel, Source as SourceModel, Issue as IssueModel, \
    Article as ArticleModel


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


class AtticleResult(graphene.ObjectType):
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
    sources = SQLAlchemyConnectionField(Source)
    source = graphene.Field(lambda: Source, source_id=graphene.String(), source_name=graphene.String())

    issues = SQLAlchemyConnectionField(Issue)
    issue = graphene.Field(lambda: Issue, issue_id=graphene.String(), url=graphene.String(),
                           issue_number=graphene.String())
    articles = SQLAlchemyConnectionField(Article)
    article = graphene.Field(lambda: Article, article_id=graphene.String(), article_content=graphene.String(), )

    # find_user = graphene.Field(lambda: Users, username=graphene.String())
    # all_users = SQLAlchemyConnectionField(Users)

    def resolve_issue(self, args, context, info):
        query = Issue.get_query(context)
        id = args.get("issue_id")
        url = args.get("issue_url")
        issue_number = args.get("issue_number")
        issue = query.filter(
            or_(IssueModel.object_id == id, (IssueModel.url == url), (IssueModel.issue_number == issue_number))).first()
        return issue

    def resolve_article(self, args, context, info):
        query = Article.get_query(context)
        id = args.get("article_id")
        content = args.get("article_content")
        article = query.filter(
            or_(ArticleModel.object_id == id, (ArticleModel.pre_content.like("%content%")))).first()
        return article

    def resolve_find_user(self, args, context, info):
        query = Users.get_query(context)
        username = args.get('username')
        return query.filter(UserModel.username == username).first()

    def resolve_source(self, args, context, info):
        query = Source.get_query(context)
        id = args.get('source_id')
        name = args.get('source_name')
        source = query.filter(or_(SourceModel.object_id == id, (SourceModel.name == name))).first()

        return source


class MyMutations(graphene.ObjectType):
    create_user = createUser.Field()
    change_username = changeUsername.Field()


schema = graphene.Schema(query=Query, mutation=MyMutations, types=[Source, Issue, Article])
