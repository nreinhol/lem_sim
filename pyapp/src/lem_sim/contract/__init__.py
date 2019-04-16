from .contract_handler import ContractHandler  # noqa

from pathlib import Path

PROJECT_DIR = str(Path(__file__).resolve().parents[4])
CONTRACT_DIR = PROJECT_DIR + '/dealer/build/contracts/'
