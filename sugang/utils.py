import requests
from bs4 import BeautifulSoup
import pickle
from datetime import datetime

from django.conf import settings


def login_and_save_session():
    login_url = "https://hisnet.handong.edu/login/_login.php"
    payload = {
        "part": "",
        "f_name": "",
        "agree": "",
        "Language": "Korean",
        "id_1": settings.USERNAME,
        "password_1": settings.PASSWORD,
        "x": "16",
        "y": "24"
    }

    session = requests.Session()
    login_response = session.post(login_url, data=payload)

    # 요청 성공 여부 확인
    if login_response.status_code == 200:
        print(f"{datetime.now()}: 로그인 성공")
        # 세션 쿠키를 파일에 저장
        with open("session_cookies.pkl", "wb") as f:
            pickle.dump(session.cookies, f)
        print(f"{datetime.now()}: 세션 쿠키 저장 완료")
        settings.SESSION_EXIST = True
    else:
        print(f"{datetime.now()}: 로그인 실패")


def get_hisnet_info(year, semester, course_code, section: str):
    session = requests.Session()

    if not settings.SESSION_EXIST:
        login_and_save_session()

    # 저장된 세션 쿠키 불러오기
    with open("session_cookies.pkl", "rb") as f:
        session.cookies.update(pickle.load(f))
    print("세션 쿠키 로드 완료")

    # 보호된 페이지 URL
    protected_url = f"https://hisnet.handong.edu/for_student/course/PLES430M.php?hak_year={year}&hak_term={semester}&hakbu=%C0%FC%C3%BC&isugbn=%C0%FC%C3%BC&injung=%C0%FC%C3%BC&prof_name=&gwamok=&gwamok_code={course_code}&ksearch=search"

    # 보호된 페이지 접근
    protected_response = session.get(protected_url)

    # 요청 성공 여부 확인
    if protected_response.status_code != 200:
        print("보호된 페이지 접근 실패")

    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(protected_response.content, 'html.parser')

    tr_elements = soup.select("#att_list > tr")
    # print("tr_elements cnt:", len(tr_elements))
    header_keys = [td.get_text(strip=True) for td in tr_elements[0].find_all('td')]

    td_elements = None

    for tr in tr_elements:
        td_elements = tr.find_all('td')
        if len(td_elements) > 2 and td_elements[1].get_text(strip=True) == section:
            break
        else:
            td_elements = None

    if td_elements is None:
        return None

    data = {
        header_keys[1]: td_elements[1].get_text(strip=True),
        header_keys[2]: td_elements[2].get_text(strip=True),
        header_keys[4]: td_elements[4].get_text(strip=True),
        header_keys[5]: td_elements[5].get_text(strip=True),
        header_keys[6]: td_elements[6].get_text(strip=True),
        header_keys[7]: td_elements[7].get_text(strip=True),

        header_keys[8]: td_elements[8].get_text(strip=True),
        # header_keys[9]: td_elements[9].get_text(strip=True),
        header_keys[10]: td_elements[10].get_text(strip=True),
        header_keys[11]: td_elements[11].get_text(strip=True),
    }

    return data
