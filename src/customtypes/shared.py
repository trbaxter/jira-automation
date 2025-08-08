from typing import Any, Type

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

JIRA_DATETIME_REGEX = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.000\+\d{4}$'


class NonEmptyStr(str):
    @classmethod
    def __get_pydantic_core_schema__(
            cls: Type['NonEmptyStr'],
            _source: Any,
            _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.str_schema(strip_whitespace=True, min_length=1)


class JiraDatetimeStr(str):
    @classmethod
    def __get_pydantic_core_schema__(
            cls: Type['JiraDatetimeStr'],
            _source: Any,
            _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.str_schema(pattern=JIRA_DATETIME_REGEX)