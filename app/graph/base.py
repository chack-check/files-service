import strawberry
from strawberry.file_uploads import Upload

from app.factories import FileFactory
from app.files.dependencies import use_files_service, use_s3_connection
from app.files.schemas import ConvertionOptions, SystemFiletypes
from app.graph.types import ConvertionOptionsEnum, SystemFiletypesEnum, UploadedFile


@strawberry.type
class Query:
    @strawberry.field
    def ping(self) -> str:
        return "pong"


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def publishFiles(self, files: list[Upload],
                           system_filetype: SystemFiletypesEnum,
                           compress: bool = True,
                           convert_to: ConvertionOptionsEnum | None = None) -> list[UploadedFile]:
        s3_connection = use_s3_connection()
        files_service = use_files_service(s3_connection)
        saved_files = []
        for file in files:
            saved_file = await files_service.save_file(
                file,
                SystemFiletypes(system_filetype.value),
                ConvertionOptions(convert_to.value) if convert_to else None,
                compress,
            )
            saved_files.append(saved_file)

        return [FileFactory.saved_file_to_schema(file) for file in saved_files]


schema = strawberry.Schema(Query, Mutation)
