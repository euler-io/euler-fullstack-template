from api.detail_config import start_up as detail_config_start_up
from api.sample import start_up as sample_start_up
from api.search_config import start_up as search_config_start_up
from start_client import start
from config.utils import get_admin_auth_header
import logging
import time


def wait_cluster_available():
    auth_header = get_admin_auth_header()
    wait_elasticsearch(interval=5000, headers=auth_header)
    es_client = start()
    es_client.cluster.health(
        headers=auth_header,
        wait_for_status='green',
        request_timeout=60)


def wait_elasticsearch(interval=2000,
                       max_retries=30,
                       params=None,
                       headers=None):
    attempts = 0
    while attempts < max_retries:
        try:
            es_client = start()
            resp = es_client.info(params=params, headers=headers)
            logging.info("Connected to elasticsearch.")
            return resp
        except:
            logging.warn(
                f"Could not connect to Elasticsearch. Retry will occur in {interval}ms.")
            attempts += 1
            time.sleep(interval/1000)
        finally:
            es_client.close()
    raise Exception("Could not connect to Elasticsearch.")


def start_app():
    wait_cluster_available()

    detail_config_start_up()
    search_config_start_up()
    sample_start_up()


def main():
    logging.info("Running start up sequence.")
    start_app()


if __name__ == "__main__":
    main()
