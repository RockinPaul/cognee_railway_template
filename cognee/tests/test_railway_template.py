import json
from pathlib import Path


def load_template() -> dict:
    template_path = Path(__file__).resolve().parents[2] / "railway-template.json"
    return json.loads(template_path.read_text())


def test_railway_template_includes_cognee_mcp_service() -> None:
    template = load_template()

    services = {service["name"]: service for service in template["services"]}

    assert "cognee-mcp" in services


def test_cognee_mcp_service_targets_api_mode() -> None:
    template = load_template()

    services = {service["name"]: service for service in template["services"]}
    mcp_service = services["cognee-mcp"]

    assert mcp_service["build"]["dockerfilePath"] == "Dockerfile.mcp"
    assert mcp_service["deploy"]["healthcheckPath"] == "/health"
    assert mcp_service["variables"]["TRANSPORT_MODE"]["default"] == "http"
    assert (
        mcp_service["variables"]["API_URL"]["default"]
        == "http://${{cognee-api.RAILWAY_PRIVATE_DOMAIN}}"
    )
