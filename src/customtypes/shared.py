from typing import Any, Type

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

JIRA_DATETIME_REGEX = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.000\+\d{4}$'


class PositiveInt(int):
    @classmethod
    def __get_pydantic_core_schema__(
            cls: Type['PositiveInt'],
            _source: Any,
            _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.int_schema(gt=0)


class NonNegativeInt(int):
    @classmethod
    def __get_pydantic_core_schema__(
            cls: Type['NonNegativeInt'],
            _source: Any,
            _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.int_schema(ge=0)


class SafeStr(str):
    @classmethod
    def __get_pydantic_core_schema__(
            cls: Type['SafeStr'],
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