from manage_embedding import load_index
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

async def data_querying(input_text: str):
    try:
        index = await load_index("data")
        engine = index.as_query_engine()
        response = engine.query(input_text)
        response_text = response.response
        logging.info(f"Query response: {response_text}")
        return response_text
    except Exception as e:
        logging.error(f"Error querying data: {e}")
        return f"An error occurred while querying: {e}"
