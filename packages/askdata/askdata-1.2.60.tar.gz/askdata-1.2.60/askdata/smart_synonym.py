import logging
import os
import requests
import yaml
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

root_dir = os.path.abspath(os.path.dirname(__file__))
yaml_path = os.path.join(root_dir, '../askdata/askdata_config/base_url.yaml')
with open(yaml_path, 'r') as file:
    url_list = yaml.load(file, Loader=yaml.FullLoader)


def suggest_synonyms(word, lang=None, already_added=None):

    if lang is None:
        lang = "en"
        print("Using English language as default!")

    if already_added is None:
        already_added = []

    # Google Pod
    headers = {
        "Content-Type": "application/json"
    }

    s = requests.Session()
    s.keep_alive = False
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))

    url = url_list['BASE_URL_SMART_SYNONYM_DEV']

    data = {
        "word": word,
        "lang": lang,
        "already_added ": already_added
    }

    r = s.post(url=url, headers=headers, json=data)
    r.raise_for_status()

    try:
        dict_response = r.json()
        synonyms = dict_response['synonyms']
        business_name = dict_response['business_name']
        return synonyms, business_name
    except Exception as e:
        logging.error(str(e))
