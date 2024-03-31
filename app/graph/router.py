from strawberry.fastapi import GraphQLRouter

from app.settings import settings

from .base import schema

router = GraphQLRouter(schema, graphiql=True if settings.run_mode != "prod" else False)
