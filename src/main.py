import logging
import re
from collections import Counter
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL, PEP_URL
from outputs import control_output
from utils import find_tag, get_response


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, "whatsnew/")

    response = get_response(session, whats_new_url)

    soup = BeautifulSoup(response.text, "lxml")

    toctreel1 = soup.find(class_="toctree-wrapper compound").find_all(
        "li", attrs={"class": "toctree-l1"}
    )

    results = [("Ссылка на статью", "Заголовок", "Редактор, Автор")]

    for version_link in tqdm(toctreel1):
        url = urljoin(whats_new_url, version_link.a["href"])

        response = get_response(session, url)

        soup = BeautifulSoup(response.text, "lxml")

        h1 = find_tag(soup, "h1")
        dl = find_tag(soup, "dl")
        dl_text = dl.text.replace("\n", "")

        results.append([url, h1.text, dl_text])

    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)

    soup = BeautifulSoup(response.text, "lxml")

    sidebar = find_tag(soup, "div", attrs={"class": "sphinxsidebarwrapper"})
    ul_tags = sidebar.find_all("ul")

    for ul in ul_tags:
        if "All versions" in ul.text:
            a_tags = ul.find_all("a")
            break
    else:
        raise Exception("Ничего не нашлось")

    results = [("Ссылка на документацию", "Версия", "Статус")]

    pattern = r"Python (?P<version>\d\.\d+) \((?P<status>.*)\)"

    for a_tag in a_tags:
        link = a_tag["href"]
        text_match = re.search(pattern, a_tag.text)
        if text_match:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ""
        results.append([link, version, status])

    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, "download.html")

    response = get_response(session, downloads_url)

    soup = BeautifulSoup(response.text, "lxml")
    table = find_tag(soup, "table", {"class": "docutils"})

    pdf_a4_tag = find_tag(table, "a", {"href": re.compile(r".+pdf-a4\.zip$")})
    pdf_a4_link = pdf_a4_tag["href"]

    archive_url = urljoin(downloads_url, pdf_a4_link)
    response = session.get(archive_url)

    filename = archive_url.split("/")[-1]

    downloads_dir = BASE_DIR / "downloads"
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename

    with open(archive_path, "wb") as file:
        file.write(response.content)

    logging.info(f"Архив был загружен и сохранён: {archive_path}")


def get_pep_status(session, url):
    response = get_response(session, url)

    soup = BeautifulSoup(response.text, "lxml")
    return soup.find(string="Status").parent.find_next_sibling("dd").text


def pep(session):
    response = get_response(session, PEP_URL)

    soup = BeautifulSoup(response.text, "lxml")

    result = Counter()

    for tbody in tqdm(soup.find_all("tbody")[:-1]):
        different_statuses = ""

        for tr in tqdm(tbody.find_all("tr"), leave=False):
            tr_status = find_tag(tr, "td").text
            if tr_status:
                tr_status = tr_status[1:]

            tr_url = urljoin(PEP_URL, find_tag(tr, "a")["href"])

            pep_status = get_pep_status(session, tr_url)

            if pep_status not in EXPECTED_STATUS.get(tr_status):
                if different_statuses:
                    different_statuses += "\n\n"

                different_statuses += (
                    f"Несовпадающие статусы:\n{tr_url}\n"
                    f"Статус в карточке: {pep_status}\n"
                    f"Ожидаемые статусы: {EXPECTED_STATUS.get(tr_status)}"
                )
            result[pep_status] += 1
        if different_statuses:
            logging.info(different_statuses)

    return (
            [("Статус", "Количество")] +
            result.most_common() +
            [('Итого', sum(result.values()))]
    )


MODE_TO_FUNCTION = {
    "whats-new": whats_new,
    "latest-versions": latest_versions,
    "download": download,
    "pep": pep,
}


def main():
    configure_logging()
    logging.info("Парсер запущен!")

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f"Аргументы командной строки: {args}")

    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results:
        control_output(results, args)
    logging.info("Парсер завершил работу.")


if __name__ == "__main__":
    main()
