from datetime import date
import inspect

from fastapi import UploadFile, Form, File, HTTPException
from pydantic import BaseModel, field_validator, HttpUrl

from validation import (
    validate_name,
    validate_image,
    validate_gender,
    validate_birth_date,
)


class ProfileCreateSchema(BaseModel):
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    info: str
    avatar: UploadFile

    @classmethod
    def from_form(
        cls,
        first_name: str = None,
        last_name: str = None,
        gender: str = None,
        date_of_birth: date = None,
        info: str = None,
        avatar: UploadFile = None,
    ) -> "ProfileCreateSchema":
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        if first_name is None:
            first_name = Form(...)
        if last_name is None:
            last_name = Form(...)
        if gender is None:
            gender = Form(...)
        if date_of_birth is None:
            date_of_birth = Form(...)
        if info is None:
            info = Form(...)
        if avatar is None:
            avatar = File(...)
        return cls(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date_of_birth,
            info=info,
            avatar=avatar,
        )

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, name: str) -> str:
        try:
            validate_name(name)
            return name.lower()
        except ValueError as e:
            raise HTTPException(
                status_code=422,
                detail=[
                    {
                        "type": "value_error",
                        "loc": ["first_name"],
                        "msg": str(e),
                        "input": name,
                    }
                ],
            ) from e

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, name: str) -> str:
        try:
            validate_name(name)
            return name.lower()
        except ValueError as e:
            raise HTTPException(
                status_code=422,
                detail=[
                    {
                        "type": "value_error",
                        "loc": ["last_name"],
                        "msg": str(e),
                        "input": name,
                    }
                ],
            ) from e

    @field_validator("avatar")
    @classmethod
    def validate_avatar(cls, avatar: UploadFile) -> UploadFile:
        try:
            validate_image(avatar)
            return avatar
        except ValueError as e:
            raise HTTPException(
                status_code=422,
                detail=[
                    {
                        "type": "value_error",
                        "loc": ["avatar"],
                        "msg": str(e),
                        "input": avatar.filename,
                    }
                ],
            ) from e

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, gender: str) -> str:
        try:
            validate_gender(gender)
            return gender
        except ValueError as e:
            raise HTTPException(
                status_code=422,
                detail=[
                    {
                        "type": "value_error",
                        "loc": ["gender"],
                        "msg": str(e),
                        "input": gender,
                    }
                ],
            ) from e

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, date_of_birth: date) -> date:
        try:
            validate_birth_date(date_of_birth)
            return date_of_birth
        except ValueError as e:
            raise HTTPException(
                status_code=422,
                detail=[
                    {
                        "type": "value_error",
                        "loc": ["date_of_birth"],
                        "msg": str(e),
                        "input": str(date_of_birth),
                    }
                ],
            ) from e

    @field_validator("info")
    @classmethod
    def validate_info(cls, info: str) -> str:
        cleaned_info = info.strip()
        if not cleaned_info:
            raise HTTPException(
                status_code=422,
                detail=[
                    {
                        "type": "value_error",
                        "loc": ["info"],
                        "msg": "Info field cannot be empty or contain only spaces.",
                        "input": info,
                    }
                ],
            )
        return cleaned_info


class ProfileResponseSchema(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    info: str
    avatar: HttpUrl
