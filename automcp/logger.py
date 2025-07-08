import logging

logging.getLogger("openai._base_client").disabled = True
logging.getLogger("httpcore.http11").disabled = True
logging.getLogger("httpcore.connection").disabled = True
logging.getLogger("httpx").disabled = True


def setup_logging(name: str):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(name)
