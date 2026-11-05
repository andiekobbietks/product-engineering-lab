"""Headless browser smoke test for the built Sand3D assembly gallery."""
import argparse
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path



def main():
    from playwright.sync_api import sync_playwright

    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, default=Path("site"))
    site = parser.parse_args().site.resolve()
    gallery = site / "experiments" / "assembly-explorer.html"
    if not gallery.is_file():
        raise SystemExit(f"Built gallery not found under {site}")

    server = ThreadingHTTPServer(
        ("127.0.0.1", 0),
        partial(SimpleHTTPRequestHandler, directory=str(site)),
    )
    threading.Thread(target=server.serve_forever, daemon=True).start()
    errors = []
    browser = None
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--enable-webgl",
                    "--ignore-gpu-blocklist",
                    "--use-gl=angle",
                    "--use-angle=swiftshader",
                    "--enable-unsafe-swiftshader",
                ],
            )
            page = browser.new_page(viewport={"width": 1440, "height": 1000})
            page.on("pageerror", lambda error: errors.append(str(error)))
            url = f"http://127.0.0.1:{server.server_port}/experiments/assembly-explorer.html"
            response = page.goto(url, wait_until="domcontentloaded", timeout=30000)
            if response is None or response.status != 200:
                raise AssertionError("Gallery page did not return HTTP 200")

            page.wait_for_function(
                "() => document.querySelector('#engineStatus')?.textContent.includes('Sand3D')",
                timeout=90000,
            )
            page.wait_for_function(
                "() => document.querySelectorAll('#componentList button').length === 7",
                timeout=15000,
            )
            page.locator("#componentList button").nth(6).click()
            selected_name = page.locator("#partTitle").inner_text()
            if selected_name != "Roller end features":
                raise AssertionError(f"Component selection did not update the inspector: {selected_name}")
            page.locator("#jointRange").evaluate(
                "(el) => { el.value = '45'; el.dispatchEvent(new Event('input', {bubbles: true})); }"
            )
            joint_value = page.locator("#jointValue").inner_text()
            if joint_value != "45°":
                raise AssertionError(f"Joint slider did not update articulation value: {joint_value}")

            state = page.evaluate("""() => ({
                status: document.querySelector('#engineStatus')?.textContent,
                components: document.querySelectorAll('#componentList button').length,
                jointDisabled: document.querySelector('#jointRange')?.disabled,
                playDisabled: document.querySelector('#playJoint')?.disabled,
                canvasWidth: document.querySelector('#viewport')?.width,
                canvasHeight: document.querySelector('#viewport')?.height,
                fatal: document.querySelector('#fatalError')?.textContent
            })""")
            if state["jointDisabled"] or state["playDisabled"]:
                raise AssertionError(f"Native Sand3D joint controls are disabled: {state}")
            if state["canvasWidth"] < 100 or state["canvasHeight"] < 100:
                raise AssertionError(f"3D canvas has no usable drawing size: {state}")
            if state["fatal"]:
                raise AssertionError(f"Gallery reported a fatal error: {state['fatal']}")
            if errors:
                raise AssertionError("Browser runtime errors: " + " | ".join(errors))
            gl_context = page.evaluate("""() => {
                const canvas = document.querySelector('#viewport');
                const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
                return gl ? gl.getParameter(gl.VERSION) : null;
            }""")
            if not gl_context:
                raise AssertionError("3D canvas has no working WebGL context")
            print("Sand3D browser gallery smoke test passed:", state, "WebGL:", gl_context)
            browser.close()
            browser = None
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
