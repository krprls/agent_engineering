"""Deterministic Context Builder for WidgetWare SDR Package."""

import copy
from pathlib import Path
import yaml

from widgetware_sdr.instructions import get_system_instructions


def _get_default_config_dir() -> Path:
    """Locate default config directory relative to file or current workspace."""
    # Check relative to this source file (my-work/class-03/config)
    pkg_root = Path(__file__).resolve().parent.parent.parent
    config_dir = pkg_root / "config"
    if config_dir.exists() and config_dir.is_dir():
        return config_dir

    # Fallback to current working directory / config
    cwd_config = Path.cwd() / "config"
    if cwd_config.exists() and cwd_config.is_dir():
        return cwd_config

    return config_dir


def load_yaml_config(file_path: Path) -> dict:
    """Load and parse a YAML configuration file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty or invalid.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Required configuration file missing: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = yaml.safe_load(f)

    if not isinstance(content, dict) or not content:
        raise ValueError(f"Configuration file {file_path} is empty or invalid.")

    return content


def build_context(
    account: dict,
    objective: str,
    evidence: list[dict],
    state: dict | None = None,
    config_dir: str | Path | None = None,
) -> dict:
    """Assemble and return the 5-layer WidgetWare SDR context object.

    Args:
        account: Target account data dictionary.
        objective: Objective string for the research task.
        evidence: List of evidence dictionaries preserving provenance.
        state: Optional prior workflow state dictionary (defaults to empty dict if None).
        config_dir: Optional path to directory containing products.yaml, icp.yaml, policies.yaml.

    Returns:
        Structured context dictionary preserving 5 distinct layers.

    Raises:
        FileNotFoundError: If required YAML configuration files are not found.
        ValueError: If configuration content is missing or invalid.
    """
    if config_dir is None:
        cfg_path = _get_default_config_dir()
    else:
        cfg_path = Path(config_dir)

    products_file = cfg_path / "products.yaml"
    icp_file = cfg_path / "icp.yaml"
    policies_file = cfg_path / "policies.yaml"

    products_data = load_yaml_config(products_file)
    icp_data = load_yaml_config(icp_file)
    policies_data = load_yaml_config(policies_file)

    system_instructions = get_system_instructions()

    # Deepcopy inputs to guarantee immutability
    account_copy = copy.deepcopy(account)
    evidence_copy = copy.deepcopy(evidence)
    state_copy = copy.deepcopy(state) if state is not None else {}

    return {
        "system_instructions": system_instructions,
        "business_context": {
            "products": products_data,
            "icp": icp_data,
            "policies": policies_data,
        },
        "task_context": {
            "account": account_copy,
            "objective": objective,
        },
        "retrieved_evidence": evidence_copy,
        "state": state_copy,
    }
