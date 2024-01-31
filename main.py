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


def get_my_careers_future_url(base_url: str, limit: int, page: int):
    return f"{base_url}/v2/search?limit={limit}&page={page}"


def get_my_careers_future_response(
    request_params: MyCareersFutureRequestParams,
) -> MyCareersFutureResponse:
    url = get_my_careers_future_url(
        request_params.BASE_URL, request_params.LIMIT, request_params.page
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


INELIGIBLE_POSITIONS = {"Senior Executive", "Senior Management", "Manager"}


def is_relevant_my_careers_future_report_data(
    report_data: MyCareersFutureReportData, ineligible_positions=INELIGIBLE_POSITIONS
) -> bool:
    if report_data.salary_min > 5000:
        return False
    if report_data.salary_max < 6500:
        return False
    if report_data.position_level in ineligible_positions:
        return False
    return True


scraped_data = scrape_my_careers_future_website()
my_careers_future_report_data = [
    get_my_careers_future_report_data(data)
    for data in scraped_data
    if is_relevant_my_careers_future_report_data(
        get_my_careers_future_report_data(data)
    )
]

from dataclass_csv import DataclassWriter

with open("test.csv", "w") as f:
    w = DataclassWriter(f, my_careers_future_report_data, MyCareersFutureReportData)
    w.write()
