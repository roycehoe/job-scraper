from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field


class Metadata(BaseModel):
    job_post_id: str = Field(..., alias="jobPostId")
    updated_at: str = Field(..., alias="updatedAt")
    new_posting_date: str = Field(..., alias="newPostingDate")
    total_number_job_application: int = Field(..., alias="totalNumberJobApplication")
    is_posted_on_behalf: bool = Field(..., alias="isPostedOnBehalf")
    is_hide_salary: bool = Field(..., alias="isHideSalary")
    is_hide_hiring_employer_name: bool = Field(..., alias="isHideHiringEmployerName")
    job_details_url: str = Field(..., alias="jobDetailsUrl")


class PositionLevel(BaseModel):
    id: int
    position: str


class PostedCompany(BaseModel):
    uen: str
    name: str
    logo_file_name: Optional[str] = Field(..., alias="logoFileName")
    logo_upload_path: Optional[str] = Field(..., alias="logoUploadPath")


class Type(BaseModel):
    salary_type: str = Field(..., alias="salaryType")


class Salary(BaseModel):
    minimum: int
    maximum: int
    type: Type


class Skill(BaseModel):
    skill: str
    uuid: str


class Category(BaseModel):
    id: int
    category: str


class EmploymentType(BaseModel):
    id: int
    employment_type: str = Field(..., alias="employmentType")


class Status(BaseModel):
    id: str
    job_status: str = Field(..., alias="jobStatus")


class Result(BaseModel):
    metadata: Metadata
    hiring_company: Any = Field(..., alias="hiringCompany")
    address: Any
    position_levels: List[PositionLevel] = Field(..., alias="positionLevels")
    schemes: List
    posted_company: PostedCompany = Field(..., alias="postedCompany")
    salary: Salary
    skills: List[Skill]
    categories: List[Category]
    employment_types: List[EmploymentType] = Field(..., alias="employmentTypes")
    shift_pattern: Any = Field(..., alias="shiftPattern")
    uuid: str
    title: str
    status: Status
    score: Optional[float] = None


class MyCareersFutureResponse(BaseModel):
    _links: Any
    search_ranking_id: Optional[str] = Field(None, alias="searchRankingId")
    results: Optional[List[Result]] = None
    total: Optional[int] = None
    count_without_filters: Optional[int] = Field(None, alias="countWithoutFilters")
