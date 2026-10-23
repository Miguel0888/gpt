import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

NAVIGATION_HREFS = (
    "./index.html",
    "./asyncapi.html",
    "./hooks.html",
    "./results.html",
    "./specification.html",
)


class QuietRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format_string, *args):
        return


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def start_site_server(site_directory):
    handler = partial(QuietRequestHandler, directory=str(site_directory))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def wait_for_asyncapi_render(page):
    page.wait_for_function(
        """() => {
            const root = document.querySelector("#asyncapi");
            const text = root ? root.innerText : "";
            return text.includes("ChatGPT Web Streams")
                && text.includes("/backend-api/f/conversation");
        }""",
        timeout=45000,
    )


def verify_page_content(page, page_path):
    if page_path == "/asyncapi.html":
        wait_for_asyncapi_render(page)
        return

    if page_path == "/index.html":
        page.locator(".swagger-ui .info .title").wait_for(timeout=45000)
        title = page.locator(".swagger-ui .info .title").inner_text()
        require("ChatGPT Web API" in title, "Swagger UI did not render the OpenAPI title.")
        return

    heading = page.locator("main.content h1")
    heading.wait_for(timeout=15000)
    require(bool(heading.inner_text().strip()), "Generated documentation page has no visible heading: " + page_path)


def verify_navigation(page, base_url):
    for href in NAVIGATION_HREFS:
        page.goto(base_url + "/asyncapi.html", wait_until="domcontentloaded")
        link = page.locator('nav[aria-label="Dokumentation"] a[href="' + href + '"]')
        require(link.count() == 1, "Navigation link is missing: " + href)
        link.click()
        page_path = "/" + href.removeprefix("./")
        page.wait_for_url(base_url + page_path, timeout=15000)
        verify_page_content(page, page_path)


def verify_source_documents(page, base_url):
    for relative_path in ("openapi.yaml", "asyncapi.yaml", "asyncapi.bundle.yaml"):
        response = page.request.get(base_url + "/" + relative_path)
        require(
            response.status == 200,
            "Documentation resource returned HTTP " + str(response.status) + ": " + relative_path,
        )


def main():
    parser = argparse.ArgumentParser(description="Run browser smoke tests against the built documentation site.")
    parser.add_argument("--site-dir", default="_site", help="Directory containing the built static site.")
    arguments = parser.parse_args()

    site_directory = Path(arguments.site_dir).resolve()
    require(site_directory.is_dir(), "Built site directory does not exist: " + str(site_directory))
    require((site_directory / "asyncapi.html").is_file(), "Built site is missing asyncapi.html.")
    require((site_directory / "asyncapi.bundle.yaml").is_file(), "Built site is missing asyncapi.bundle.yaml.")

    server, thread = start_site_server(site_directory)
    base_url = "http://127.0.0.1:" + str(server.server_address[1])
    browser_errors = []

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.on("pageerror", lambda error: browser_errors.append(str(error)))

            response = page.goto(base_url + "/asyncapi.html", wait_until="domcontentloaded")
            require(response is not None and response.status == 200, "AsyncAPI page did not return HTTP 200.")
            verify_source_documents(page, base_url)
            wait_for_asyncapi_render(page)
            verify_navigation(page, base_url)

            require(not browser_errors, "Browser JavaScript errors: " + "; ".join(browser_errors))
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    print("Chromium smoke test passed: AsyncAPI rendered, Swagger UI rendered, and navigation links worked.")


if __name__ == "__main__":
    main()
