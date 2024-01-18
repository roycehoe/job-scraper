from dataclasses import dataclass

import requests

from models import MyCareersFutureResponse, Result


@dataclass
class MyCareersFutureRequestParams:
    page: int

    LIMIT: int = 100
    BASE_URL = "https://api.mycareersfuture.gov.sg"
    SEARCH_TERM: str = "software engineer"
    SESSION_ID: str = "22065856.1685672782"

    def get_request_body(self):
        return {
            "sessionId": self.SESSION_ID,
            "search": self.SEARCH_TERM,
        }


def get_my_careers_future_url(limit: int, page: int, base_url: str):
    return f"{base_url}/v2/search?limit={limit}&page={page}"


def get_my_careers_future_response(
    request_params: MyCareersFutureRequestParams,
) -> MyCareersFutureResponse:
    url = get_my_careers_future_url(
        request_params.LIMIT, request_params.page, request_params.BASE_URL
    )
    request_body = request_params.get_request_body()
    response = requests.post(url=url, data=request_body)
    return MyCareersFutureResponse(**response.json())


def scrape_my_careers_future_website() -> list[Result]:
    scraped_data: list[Result] = []
    page = 0
    while True:
        request_param = MyCareersFutureRequestParams(page=page)
        response = get_my_careers_future_response(request_param)
        if not response.results:
            return scraped_data
        scraped_data = [*scraped_data, *response.results]
        page += 1


@dataclass
class MyCareersFutureReportData:
    company_name: str
    job_title: str
    salary_min: int
    salary_max: int
    application_url: str
    position_level: str


def get_my_careers_future_report_data(r: Result) -> MyCareersFutureReportData:
    return MyCareersFutureReportData(
        company_name=r.posted_company.name,
        job_title=r.title,
        salary_min=r.salary.minimum,
        salary_max=r.salary.maximum,
        application_url=r.metadata.job_details_url,
        position_level=r.position_levels[0].position,
    )


scraped_data = scrape_my_careers_future_website()
truncated_scaped_data = list(map(get_my_careers_future_report_data, scraped_data))

from dataclass_csv import DataclassWriter

with open("test.csv", "w") as f:
    w = DataclassWriter(f, truncated_scaped_data, MyCareersFutureReportData)
    w.write()
