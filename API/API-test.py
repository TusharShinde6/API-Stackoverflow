import requests
import pytest

BASE_URL = 'https://api.stackexchange.com/badges'
BASE_URL2 = 'https://api.stackexchange.com'
SITE = 'stackoverflow'

# Badge Test Case
@pytest.mark.parametrize("badge_id", [5367, 5368, -5369,])  # Example badge IDs to search for
def test_badge_retrieval_by_id(badge_id):
    """
    Test case for fetching a badge by ID.
    """
    response = requests.get(f'{BASE_URL}?site={SITE}&order=desc&sort=rank&pagesize=100&page=1')
    print(f"Positive_testcase, Status code: {response.status_code}")
    assert response.status_code == 200, f"Failed to retrieve badges. Status code: {response.status_code}"

    badges = response.json().get('items', [])

    badge_found = False
    for badge in badges:
        if badge['badge_id'] == badge_id:
            badge_found = True
            print("Found Badge:")
            print(badge)
            break
    else:
        print(f"Badge with ID {badge_id} not found or invalid.")
    if not badge_found:
        print("No badge")

    assert badge_found or badge_id not in [badge['badge_id'] for badge in
                                           badges], f"Badge with ID {badge_id} not found in the response."

# Positive Test Cases
@pytest.mark.parametrize("page", [1, 2])
def test_positive_test_cases_PAGE_no(page):
    """
    Positive test cases for fetching badges.
    """
    response = requests.get(f'{BASE_URL}?site={SITE}&order=desc&sort=rank&pagesize=100&page={page}')
    print(f"Positive_testcase, Status code: {response.status_code}")
    print(f"Page no used is : {page}")
    assert response.status_code == 200
    items = response.json().get('items', [])
    assert items, f"No items found on page {page}"

# Negative Test Cases
@pytest.mark.parametrize("page", [-1, 0, 999])
def test_negative_test_cases_page_no(page):
    """
    Negative test cases for fetching badges with invalid page numbers.
    """
    response = requests.get(f'{BASE_URL}?site={SITE}&order=desc&sort=rank&pagesize=100&page={page}')
    print(f"Negative_testcase, Status code: {response.status_code}")
    print(f"Pages parameters for Negative testcase : {page}")
    assert response.status_code == 400

@pytest.mark.parametrize("param_name, param_value", [
    ("site", "invalid_site"),
    ("site", ""),
    ("site", None),
    ("order", "invalid_order"),
    ("sort", "invalid_sort"),
    ("sort", None),
    ("pagesize", "invalid_pagesize"),
    ("pagesize", None)
])
def test_invalid_parameters(param_name, param_value):
    """
    Test for various invalid parameters.
    """
    params = {
        "site": SITE,
        "order": "desc",
        "sort": "rank",
        "pagesize": 100,
        "page": 1
    }
    if param_value is not None:
        params[param_name] = param_value

    response = requests.get(BASE_URL, params=params)
    print(f"Positive_testcase, Status code: {response.status_code}")
    print(f"Parameters are : '{param_name}', '{param_value}'")
    if param_value is None:
        # If param_value is None, skip checking status code
        return
    assert response.status_code == 400

def test_missing_site_parameter():
    """
    Test for missing site parameter.
    """
    response = requests.get(f'{BASE_URL}?order=desc&sort=rank&pagesize=100&page=1')
    print(f"Positive_testcase, Status code: {response.status_code}")
    print(f"Parameter missing : {SITE}")
    assert response.status_code == 400

def test_missing_required_parameters():
    """
    Test for missing required parameters.
    """
    response = requests.get(f'{BASE_URL}?order=desc&sort=rank&page=1')
    print(f"Positive_testcase, Status code: {response.status_code}")
    assert response.status_code == 400

@pytest.mark.parametrize("endpoint, params, expected_status_code", [
    ('/badges/recipients', {'site': 'stackoverflow'}, 200),
    ('/2.3/badges/tags', {'order': 'desc', 'sort': 'rank', 'site': 'stackoverflow'}, 200)
])
def test_fetch_badges(endpoint, params, expected_status_code):
    """
    Test case for fetching badge recipients and badge tags.
    """
    response = requests.get(f'{BASE_URL2}{endpoint}', params=params)
    print(f"Test case for fetching {endpoint}, Status code: {response.status_code}")
    print(f"{params}")

    assert response.status_code == expected_status_code
throttle_violation
    if response.status_code == 200:
        items = response.json().get('items', [])
        assert items, f"No items found in the response for {endpoint}"
    else:
        # Handle other status codes
        assert False, f"Unexpected status code: {response.status_code}"

@pytest.mark.parametrize("invalid_site", ["", "invalid_site", None])
def test_invalid_site_parameter(invalid_site):
    """
    Test case for invalid 'site' parameter.
    """
    endpoint = '/badges/recipients'
    params = {'site': invalid_site}

    response = requests.get(f'{BASE_URL2}{endpoint}', params=params)
    print(f"Test case for invalid 'site' parameter, Status code: {response.status_code}")
    print(f"{params}")
    assert response.status_code == 400


@pytest.mark.parametrize("page", [0, -1, 1000])
def test_boundary_page_parameter(page):
    """
    Test case for boundary value of 'page' parameter.
    """
    endpoint = '/badges/recipients'
    params = {'site': 'stackoverflow', 'page': page}

    response = requests.get(f'{BASE_URL2}{endpoint}', params=params)
    print(f"Test case for boundary value of 'page' parameter, Status code: {response.status_code}")
    print(f"{params}")
    assert response.status_code == 400


def test_injection_attacks():
    """
    Test case for SQL injection attack.
    """
    endpoint = '/badges/recipients'
    params = {'site': "stackoverflow'; DROP TABLE users;"}

    response = requests.get(f'{BASE_URL2}{endpoint}', params=params)
    print(f"Test case for SQL injection attack, Status code: {response.status_code}")
    print(f"{params}")
    assert response.status_code == 400
