import subprocess
import requests
import os
from bs4 import BeautifulSoup
import concurrent.futures

def get_csrf_token(session, url):
    response = session.get(url, proxies={"http": None, "https": None})
    csrf_token = session.cookies.get('csrftoken')
    if not csrf_token:
        soup = BeautifulSoup(response.text, "html.parser")
        token_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        if token_input:
            csrf_token = token_input['value']
    return csrf_token

def run_sqlmap(url, post_data=None, headers=None):
    print(f"\nTesting URL: {url}")
    command = [
        "sqlmap",
        "-u", url,
        "--batch",
        "--level=3",
        "--risk=3",
        "--threads=5",
        "--smart",
        "--timeout=10",
        "--random-agent",
    ]

    if post_data:
        command.extend(["--data", post_data])
    if headers:
        header_str = "\r\n".join(f"{k}: {v}" for k, v in headers.items())
        command.extend(["--headers", header_str])

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    vulnerability_found = False

    for line in process.stdout:
        print(line, end='')
        if "is vulnerable" in line.lower():
            vulnerability_found = True

    process.wait()
    if vulnerability_found:
        print(f"!!! Vulnerability detected in {url} !!!\n")
        return False
    return True

def main():
    login_url = "http://localhost:8000/login/"
    assets_url = "http://localhost:8000/assets/?search=test"
    customers_url = "http://localhost:8000/customers/?search=test"

    username = os.environ.get("SQLMAP_TEST_USERNAME", "sqlmaptestuser")
    password = os.environ.get("SQLMAP_TEST_PASSWORD", "StrongPassword123")

    session = requests.Session()
    csrf_token = get_csrf_token(session, login_url)
    if not csrf_token:
        print("Failed to get CSRF token, cannot test login properly.")
        exit(1)

    post_data_template = "username={username}&password={password}&csrfmiddlewaretoken={csrf_token}"
    post_data = post_data_template.format(username=username, password=password, csrf_token=csrf_token)

    headers = {
        "Cookie": f"csrftoken={csrf_token}",
        "Referer": login_url,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Run tests concurrently for speed
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        futures.append(executor.submit(run_sqlmap, login_url, post_data, headers))
        futures.append(executor.submit(run_sqlmap, assets_url))
        futures.append(executor.submit(run_sqlmap, customers_url))

        results = [f.result() for f in futures]

    if all(results):
        print("\nNo SQL injection vulnerabilities found on any tested URLs.")
        exit(0)
    else:
        print("\nSQL injection vulnerabilities detected!")
        exit(1)

if __name__ == "__main__":
    main()
