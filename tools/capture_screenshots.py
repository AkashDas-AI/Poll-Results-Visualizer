"""Automated Screenshot Capture Tool for Poll Results Visualizer.

Captures pixel-perfect Full HD screenshots of all dashboard pages in Dark Mode,
plus side-by-side Dark vs Light theme comparison.

Conforms strictly to docs/SCREENSHOT_GUIDE.md:
- Viewport: 1920x1080 (16:9 Full HD)
- Format: PNG with Pillow lossless optimization (< 400 KB per asset)
- Handles scrollable inner containers for complex dashboard views

Usage:
    python tools/capture_screenshots.py
"""

import subprocess
import time
import urllib.request
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT_DARK = 8550
PORT_LIGHT = 8551
OUTPUT_DIR = Path("images")
OUTPUT_DIR.mkdir(exist_ok=True)

VIEWPORT = {"width": 1920, "height": 1080}

TARGETS = [
    {
        "url": f"http://localhost:{PORT_DARK}",
        "filename": "dashboard_overview.png",
        "description": "Figure 1: Executive Dashboard Landing Page",
        "wait_selector": "div[data-testid='stMetric']",
        "scroll_y": 0,
    },
    {
        "url": f"http://localhost:{PORT_DARK}/Overview",
        "filename": "page1_overview_demographics.png",
        "description": "Figure 2: Overview Page (Funnel & Demographics)",
        "wait_selector": ".js-plotly-plot",
        "scroll_y": 280,
    },
    {
        "url": f"http://localhost:{PORT_DARK}/Response_Analysis",
        "filename": "response_analysis.png",
        "description": "Figure 3: Response Analysis (Tech Adoption & Gaps)",
        "wait_selector": ".js-plotly-plot",
        "scroll_y": 250,
    },
    {
        "url": f"http://localhost:{PORT_DARK}/Segment_Comparison",
        "filename": "segment_comparison.png",
        "description": "Figure 4: Segment Comparison (Role Boxplots & Remote Work)",
        "wait_selector": ".js-plotly-plot",
        "scroll_y": 550,
    },
    {
        "url": f"http://localhost:{PORT_DARK}/Data_Quality",
        "filename": "data_quality.png",
        "description": "Figure 5: Data Quality (Missingness Ranking & Audit)",
        "wait_selector": ".js-plotly-plot",
        "scroll_y": 450,
    },
]


def wait_for_server(url: str, max_seconds: int = 45) -> bool:
    """Poll health endpoint until HTTP 200 OK."""
    for i in range(max_seconds):
        try:
            with urllib.request.urlopen(f"{url}/_stcore/health", timeout=1) as resp:
                if resp.status == 200:
                    print(f"Server at {url} ready in {i + 1}s!")
                    return True
        except Exception:
            time.sleep(1)
    return False


def capture_all_screenshots():
    """Execute automated screenshot generation pipeline."""
    # 1. Start Dark Theme Server
    st_dark_cmd = [
        r".venv\Scripts\python.exe", "-m", "streamlit", "run",
        "app/streamlit_app.py",
        "--server.port", str(PORT_DARK),
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false",
    ]
    print(f"Starting Dark Streamlit instance on port {PORT_DARK}...")
    proc_dark = subprocess.Popen(st_dark_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 2. Start Light Theme Server
    st_light_cmd = [
        r".venv\Scripts\python.exe", "-m", "streamlit", "run",
        "app/streamlit_app.py",
        "--server.port", str(PORT_LIGHT),
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false",
        "--theme.base", "light",
        "--theme.primaryColor", "#3B82F6",
        "--theme.backgroundColor", "#FFFFFF",
        "--theme.secondaryBackgroundColor", "#F8FAFC",
        "--theme.textColor", "#1E293B",
    ]
    print(f"Starting Light Streamlit instance on port {PORT_LIGHT}...")
    proc_light = subprocess.Popen(st_light_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        if not wait_for_server(f"http://localhost:{PORT_DARK}"):
            raise RuntimeError("Dark Streamlit instance failed to start.")
        if not wait_for_server(f"http://localhost:{PORT_LIGHT}"):
            raise RuntimeError("Light Streamlit instance failed to start.")

        time.sleep(3)

        with sync_playwright() as p:
            browser = p.chromium.launch(
                executable_path=CHROME_PATH,
                headless=True,
                args=["--hide-scrollbars", "--disable-gpu", "--no-sandbox"],
            )

            # Dark theme captures
            dark_context = browser.new_context(
                viewport=VIEWPORT,
                device_scale_factor=1,
                color_scheme="dark",
            )
            page = dark_context.new_page()

            for target in TARGETS:
                print(f"Capturing {target['description']}...")
                page.goto(target["url"], wait_until="networkidle", timeout=60000)

                try:
                    page.wait_for_selector(target["wait_selector"], timeout=20000)
                except Exception as e:
                    print(f"Selector wait warning for {target['filename']}: {e}")

                if target.get("scroll_y", 0) > 0:
                    page.evaluate(f"""() => {{
                        const el = document.querySelector('section[data-testid="stMain"]')
                            || document.querySelector('.main')
                            || document.documentElement;
                        el.scrollTop = {target['scroll_y']};
                    }}""")
                    time.sleep(1.0)

                time.sleep(3.0)
                out_path = OUTPUT_DIR / target["filename"]
                page.screenshot(path=str(out_path), full_page=False)

                # Lossless optimize with Pillow
                im = Image.open(out_path)
                im.save(out_path, optimize=True)
                size_kb = out_path.stat().st_size // 1024
                print(f"Saved: {out_path} ({size_kb} KB, {im.size[0]}x{im.size[1]})")

            # Capture Light Mode for comparison
            print("Capturing Light Mode instance for Response Analysis...")
            light_context = browser.new_context(
                viewport=VIEWPORT,
                device_scale_factor=1,
                color_scheme="light",
            )
            light_page = light_context.new_page()
            light_page.goto(
                f"http://localhost:{PORT_LIGHT}/Response_Analysis",
                wait_until="networkidle",
                timeout=60000
            )
            try:
                light_page.wait_for_selector(".js-plotly-plot", timeout=20000)
            except Exception:
                pass
            light_page.evaluate("""() => {
                const el = document.querySelector('section[data-testid="stMain"]')
                    || document.querySelector('.main')
                    || document.documentElement;
                el.scrollTop = 250;
            }""")
            time.sleep(3.0)
            light_temp_path = OUTPUT_DIR / "temp_light.png"
            light_page.screenshot(path=str(light_temp_path), full_page=False)

            # Build Theme Comparison composite
            dark_im = Image.open(OUTPUT_DIR / "response_analysis.png")
            light_im = Image.open(light_temp_path)

            half_w = 960
            h = 1080
            dark_crop = dark_im.crop((0, 0, half_w, h))
            light_crop = light_im.crop((half_w, 0, 1920, h))

            comp_im = Image.new("RGB", (1920, 1080))
            comp_im.paste(dark_crop, (0, 0))
            comp_im.paste(light_crop, (half_w, 0))

            theme_comp_path = OUTPUT_DIR / "theme_comparison.png"
            comp_im.save(theme_comp_path, optimize=True)
            print(f"Saved Theme Comparison: {theme_comp_path} ({theme_comp_path.stat().st_size // 1024} KB)")

            if light_temp_path.exists():
                light_temp_path.unlink()

            browser.close()
            print("Capture pipeline finished successfully.")

    finally:
        proc_dark.terminate()
        proc_dark.wait()
        proc_light.terminate()
        proc_light.wait()
        print("Both Streamlit instances terminated.")


if __name__ == "__main__":
    capture_all_screenshots()
