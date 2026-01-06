from seeds.schema.result import SeedsResult
import os
from tools.logger import get_logger


logger = get_logger("SEEDS_DUMPS")


def save_seeds_result(result: SeedsResult, scenario: str):
    filepath = f"./dumps/{scenario}_seeds.json"

    if not os.path.exists("dumps"):
        os.mkdir("dumps")

    with open(filepath, "w+", encoding="utf-8") as file:
        file.write(result.model_dump_json())
        logger.info(f"Seeding result saved to file: {filepath}")



def load_seeds_result(scenario: str) -> SeedsResult:
    filepath = f"./dumps/{scenario}_seeds.json"

    with open(filepath, "r", encoding="utf-8") as file:
        result = SeedsResult.model_validate_json(file.read())
        logger.info(f"Seeding result loaded from file: {filepath}")
        return result