
from unittest.mock import patch

import httpx
import server


def run_test(label, expected_code, function):
    result = function()
    actual_code = result.get("error", {}).get("code")

    assert result["success"] is False, result
    assert actual_code == expected_code, result

    print(f"PASS: {label} ({actual_code})")


def main():
    # Ensure the in-memory cache is empty.
    server._countries = None

    # Simulate a timeout.
    with patch(
        "server.httpx.get",
        side_effect=httpx.TimeoutException("Timed out")
    ):
        run_test(
            "Search timeout",
            "TIMEOUT",
            lambda: server.search_countries("Germany")
        )

    # Simulate an HTTP 503 error.
    request = httpx.Request("GET", server.DATA_URL)
    response = httpx.Response(503, request=request)

    with patch(
        "server.httpx.get",
        return_value=response
    ):
        run_test(
            "Country details HTTP error",
            "HTTP_ERROR",
            lambda: server.get_country_details("Germany")
        )

    # Simulate a network connection failure.
    with patch(
        "server.httpx.get",
        side_effect=httpx.ConnectError("Connection failed")
    ):
        run_test(
            "Network error",
            "NETWORK_ERROR",
            lambda: server.search_countries("Germany")
        )

    print("All upstream error tests passed!")


if __name__ == "__main__":
    main()
