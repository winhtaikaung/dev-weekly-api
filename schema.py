import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from sqlalchemy import or_

from database import db_session, User as UserModel, Source as SourceModel, Issues as IssueModel, \
    Articles as ArticleModel


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
    articles = SQLAlchemyConnectionField(Article)
    find_user = graphene.Field(lambda: Users, username=graphene.String())
    all_users = SQLAlchemyConnectionField(Users)

    def resolve_find_user(self, args, context, info):
        query = Users.get_query(context)
        username = args.get('username')
        # you can also use and_ with filter() eg: filter(and_(param1, param2)).first()
        return query.filter(UserModel.username == username).first()

    def resolve_source(self, args, context, info):
        query = Source.get_query(context)
        id = args.get('source_id')
        name = args.get('source_name')
        # you can also use and_ with filter() eg: filter(and_(param1, param2)).first()
        return query.filter(or_(SourceModel.object_id == id, (SourceModel.name == name))).first()


class MyMutations(graphene.ObjectType):
    create_user = createUser.Field()
    change_username = changeUsername.Field()


schema = graphene.Schema(query=Query, mutation=MyMutations, types=[Users])
