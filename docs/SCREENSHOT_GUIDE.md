# Screenshot Guide: Poll Results Visualizer

**Project Name:** Poll Results Visualizer  
**Author:** Akash Das  
**Current Milestone:** Phase 8 - Final Project Polish, GitHub Preparation and Publication  
**Primary Dataset:** Stack Overflow Annual Developer Survey 2025  
**Target Asset Directory:** `images/`  
**Standard Resolutions:** Full HD ($1920 \times 1080$) / 2K ($2560 \times 1440$)  
**Default Theme:** Professional Dark Theme (Enterprise Business Intelligence)  

---

## 1. Purpose and Scope

This guide establishes the official visual documentation standards for the **Poll Results Visualizer** project. High-quality visual assets are critical for recruiter evaluation, GitHub portfolio presentation, technical documentation, and conference demonstrations.

All screenshots stored in the `images/` directory must conform to the specifications outlined below to ensure consistent typography, correct aspect ratios, optimal color contrast, and fast web asset loading.

```
+-----------------------------------------------------------------------------------+
|                        VISUAL ASSET PIPELINE & STANDARDS                          |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [Streamlit Dashboard]                                                            |
|          |                                                                        |
|          v                                                                        |
|  [Capture Protocol]   --->  Viewport: 1920x1080 (16:9), DPR: 1.0 or 2.0           |
|          |                  Format: 24/32-bit PNG (Lossless)                      |
|          v                                                                        |
|  [Quality Review]     --->  Dark Theme Contrast Check (#0E1117 / #3B82F6)          |
|          |                  Data Label Legibility & Transparent Canvas            |
|          v                                                                        |
|  [Optimization]       --->  Lossless Compression (< 400 KB per asset)             |
|          |                                                                        |
|          v                                                                        |
|  [Repository Asset]   --->  Committed to images/ with Relative Markdown Links     |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Design System and Visual Specifications

### 2.1. Enterprise BI Dark Theme (Default)
The dashboard defaults to an enterprise Business Intelligence dark palette engineered for high data density and low optical fatigue:

| UI Element | Color Hex | Visual Role |
|---|---|---|
| **Main App Background** | `#0E1117` | Clean, dark background for dashboard content |
| **Sidebar Background** | `#161B26` | Elevated dark navy for navigation and filters |
| **Metric Card Surface** | `#1C2433` | KPI card container background (`stMetric`) |
| **Primary Text** | `#F1F5F9` | Titles, section headers, metric values |
| **Secondary Text** | `#A0AEC0` | Captions, axis titles, helper labels, table headers |
| **Primary Accent** | `#3B82F6` | Primary action buttons, active tab indicators, primary bar traces |
| **Positive Indicator** | `#22C55E` | Positive metric deltas, desired tech adoption traces |
| **Warning / Hybrid** | `#F59E0B` | In-person and hybrid comparison markers, cautionary badges |
| **Borders & Dividers** | `#30394A` | Card outlines, table borders, horizontal dividers |

### 2.2. Dual-Theme Adaptability (Light Mode Alternative)
While Dark Mode is the flagship recruiter-facing theme, the application features an enterprise Light Mode managed via `app/components/theme.py`:
- **Interactive Toggle:** Rendered in the sidebar via `st.sidebar.radio` (`theme_mode_selector`), storing title-case strings `"Dark"` and `"Light"` in `st.session_state["theme_mode"]` with persistence across page navigation.
- **Enterprise Light Palette:** Main background `#F8FAFC`, sidebar `#F1F5F9`, card surface `#FFFFFF`, primary typography `#0F172A` (Slate-900), and borders `#CBD5E1`.
- **Plotly Dual-Theming:** All 10 shared chart generators and 4 page-level figures route through `apply_chart_theme`, dynamically toggling between `plotly_dark` and `plotly_white` templates with adapted gridlines (`rgba(0, 0, 0, 0.08)`), tooltips, and transparent backgrounds (`chart_paper` and `chart_bg` as `"rgba(0, 0, 0, 0)"`).

---

## 3. Capture Standards and Technical Requirements

Maintainers capturing or updating dashboard screenshots must adhere to the following technical rules:

1. **Resolution & Aspect Ratio:**
   - Standard: **$1920 \times 1080$ pixels (16:9 Full HD)**.
   - High-DPI / Retina: **$2560 \times 1440$ pixels** or **$3840 \times 2160$ pixels** (downsampled to Full HD for web optimization).
   - Strict 16:9 or full-content scroll aspect ratios; avoid arbitrary or cropped window dimensions.

2. **Browser Environment:**
   - Recommended engines: Google Chrome, Chromium, or Brave.
   - Browser Zoom Level: Exactly **100%** (verify with `Ctrl + 0`).
   - Clean Viewport: No browser bookmarks bar, no extensions icons, no scrollbars obscuring chart legends.
   - Hide Mouse Cursor: Ensure the cursor is placed outside the capture canvas or hidden via automation scripts.

3. **File Format & Asset Budgets:**
   - File Extension: `.png` (Portable Network Graphics).
   - Color Depth: 24-bit TrueColor or 32-bit RGBA.
   - File Size Budget: **$\le 400\text{ KB}$ per image** post-compression. Never commit uncompressed 5+ MB raw PNG captures.

4. **Rendering State:**
   - Wait for Streamlit loading runners ("Running...") to terminate completely before capture.
   - Ensure Plotly WebGL/SVG animations have settled (minimum 2.0-second delay post-render).

---

## 4. Official Screenshot Inventory and Specifications

The project maintains 5 primary production screenshots corresponding to the visual walkthrough in [README.md](file:///d:/Projects/Data%20Science/Poll%20Results%20Visualizer/README.md#5-dashboard-overview-and-screenshots):

```
images/
|-- .gitkeep                          # Directory tracker
|-- dashboard_overview.png            # Figure 1: Executive Home Landing Portal
|-- page1_overview_demographics.png   # Figure 2: Sample Flow Funnel & Demographics
|-- response_analysis.png             # Figure 3: Technology Adoption & Paired Gaps
|-- segment_comparison.png            # Figure 4: Cross-Cohort Boxplots & Remote Work
|-- data_quality.png                  # Figure 5: Missingness Ranking & Audit Trail
`-- theme_comparison.png              # Figure 6: Dual Dark / Light Mode Showcase (Optional)
```

---

### 4.1. Figure 1: Executive Home Landing Portal
- **Target File:** `images/dashboard_overview.png`
- **Application Route:** `http://localhost:8501/` (`app/streamlit_app.py`)
- **Required Viewport:** Top section of the landing page down through the telemetry grid.
- **Key Visual Elements:**
  - Application title: **Poll Results Visualizer** with subtitle badge.
  - Survey Methodology Notice banner explaining the unweighted opt-in convenience sample.
  - Top 4 KPI Metric Cards:
    - `Total Records: 49,191`
    - `Total Cleaned Sample: 49,009` (with `-182` filter indicator)
    - `Countries Represented: 177`
    - `Target Questions: 8`
  - Navigation overview cards detailing the 4 analytical sub-pages.
- **Hover/State Requirement:** Hover over the first metric card (`Total Records`) to showcase the active `#3B82F6` border highlight and box shadow transition.

---

### 4.2. Figure 2: Demographics & Fieldwork Inventory
- **Target File:** `images/page1_overview_demographics.png`
- **Application Route:** `http://localhost:8501/1_Overview` (`app/pages/1_Overview.py`)
- **Required Viewport:** Full view of the survey inventory and demographic distribution section.
- **Key Visual Elements:**
  - **Sample Flow Funnel Chart:** Visualizing the 4 attrition stages:
    - Raw Extract ($49,191$) $\to$ Official Qualified Base ($49,009$) $\to$ Valid Compensation ($23,947$) $\to$ Complete Econometric Cases ($22,769$).
  - **Question Completeness Table:** Displaying question text, $N_{\text{answered}}$ valid counts, completeness %, and missingness counts.
  - **Age and Experience Charts:** Side-by-side Plotly bar charts depicting natural age distribution (`#3B82F6`) and professional coding experience (`#22C55E`).
- **Notice Check:** Verify the cross-sectional notice is visible: *"Daily fieldwork velocity tracking is disabled to avoid fabricating artificial temporal trends in single-wave cross-sectional data."*

---

### 4.3. Figure 3: Technology Adoption & Preference Gaps
- **Target File:** `images/response_analysis.png`
- **Application Route:** `http://localhost:8501/2_Response_Analysis` (`app/pages/2_Response_Analysis.py`)
- **Required Viewport:** Technology Adoption sub-tab within Response Analysis.
- **Key Visual Elements:**
  - **Dual-Percentage Horizontal Bar Chart:** Language adoption comparing % of respondents ($N=48,341$) versus % of total selections.
  - **Paired Technology Comparison Chart:** Grouped bar chart comparing Current Technologies (`#3B82F6`) versus Desired Technologies (`#22C55E`) for top languages (JavaScript, Python, TypeScript, SQL, Rust, Go).
  - **Stated Preference Gap Table ($N=27,079$):** Tabular display reporting Net Desire Gap (e.g. Rust $+18.4\%$, Go $+12.2\%$, PHP $-14.1\%$).
- **Visual Hygiene Check:** Ensure no white rectangular bounding boxes appear behind Plotly trace legends; legend text must contrast clearly against the `#0E1117` background.

---

### 4.4. Figure 4: Segment Comparison & Remote Work Dynamics
- **Target File:** `images/segment_comparison.png`
- **Application Route:** `http://localhost:8501/3_Segment_Comparison` (`app/pages/3_Segment_Comparison.py`)
- **Required Viewport:** Mid-page view highlighting compensation distributions and econometric models.
- **Key Visual Elements:**
  - **Compensation Distribution Box Plots:** Median, IQR, and whisker ranges across developer roles (Engineering Manager, DevOps, Cloud Engineer, Backend, Frontend).
  - **Remote Work Salary Box Plots:** Side-by-side distribution comparison of Remote (`#3B82F6`), Hybrid (`#F59E0B`), and In-Person (`#22C55E`).
  - **Econometric Wage Attenuation Callout:** Model C Mincer regression summary displaying how the raw remote salary premium ($+88.6\%$) attenuates to $+30.65\%$ ($\hat{\beta} = +0.267353, t = 11.517$) after controlling for geographic country and professional experience.

---

### 4.5. Figure 5: Data Quality & Methodological Audit
- **Target File:** `images/data_quality.png`
- **Application Route:** `http://localhost:8501/4_Data_Quality` (`app/pages/4_Data_Quality.py`)
- **Required Viewport:** Complete view of the missing data auditing section.
- **Key Visual Elements:**
  - **Survey Item Missingness Ranking Bar Chart:** Horizontal bars displaying missingness percentage across all survey items sorted descending.
  - **Audited $6 \times 2$ RemoteWork Contingency Table:** Reconciled table against `MainBranch` showing Answered ($33,780$), Missing ($15,411$), and Total ($49,191$).
  - **Statistical Test Badge:** Chi-Square result display ($\chi^2 = 5,333.84, df = 5, p < 10^{-300}$, Cramér's $V = 0.3293$) confirming non-MCAR missingness.
  - **On-Demand CSV Export Component:** `st.download_button` for exporting cleaned filtered records.

---

### 4.6. Figure 6: Dual-Theme Comparison Showcase (Optional)
- **Target File:** `images/theme_comparison.png`
- **Composition:** Split-screen or dual-panel composite showing the identical technology adoption chart rendered in Dark Mode (left) and Light Mode (right).
- **Purpose:** Demonstrates theme independence, responsive Plotly canvas transparency, and adherence to accessibility standards.

---

## 5. Manual Capture Workflow (Step-by-Step)

Maintainers capturing screenshots manually using modern desktop browsers should follow these exact steps:

### Step 1: Launch Application Locally
```bash
# Terminal inside project root
python run.py
```
Open Chrome or Brave and navigate to `http://localhost:8501`.

### Step 2: Open Chrome DevTools Device Emulation
1. Press `F12` (or `Ctrl + Shift + I`) to open Developer Tools.
2. Press `Ctrl + Shift + M` to toggle the **Device Toolbar**.
3. In the top bar, set:
   - **Dimensions:** Responsive $\to$ `1920` width $\times$ `1080` height.
   - **Zoom:** `100%`.
   - **Device Pixel Ratio (DPR):** `1.0` (standard) or `2.0` (retina).

### Step 3: Configure Dashboard View
1. Collapse the Streamlit left navigation sidebar if necessary, or keep it neatly expanded if capturing full-page layout.
2. Scroll to position the target charts and KPI cards symmetrically within the viewport.
3. Allow 2 seconds for Plotly rendering and font anti-aliasing to complete.

### Step 4: Capture Viewport Screenshot
1. Press `Ctrl + Shift + P` inside Chrome DevTools to open the Command Palette.
2. Type: `Capture screenshot` (captures exact $1920 \times 1080$ viewport) or `Capture full size screenshot` (for entire scrolling page).
3. Save the captured PNG into the `images/` directory with the designated canonical filename.

---

## 6. Automated Headless Capture Script (Playwright)

For deterministic, automated, pixel-perfect screenshot generation, maintainers can run this standalone Python script using [Playwright](https://playwright.dev/python/):

```python
"""Automated Dashboard Screenshot Capture Script for Poll Results Visualizer.

Captures pixel-perfect Full HD screenshots of all 4 dashboard pages in Dark Mode.

Requirements:
    pip install playwright
    playwright install chromium
"""

import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:8501"
OUTPUT_DIR = Path("images")
OUTPUT_DIR.mkdir(exist_ok=True)

VIEWPORT = {"width": 1920, "height": 1080}

CAPTURE_TARGETS = [
    {
        "url": f"{BASE_URL}",
        "filename": "dashboard_overview.png",
        "description": "Executive Home Landing Portal",
        "wait_selector": "div[data-testid='stMetric']",
    },
    {
        "url": f"{BASE_URL}/1_Overview",
        "filename": "page1_overview_demographics.png",
        "description": "Demographics and Funnel",
        "wait_selector": "div[data-testid='stDataFrame']",
    },
    {
        "url": f"{BASE_URL}/2_Response_Analysis",
        "filename": "response_analysis.png",
        "description": "Technology Adoption and Preference Gaps",
        "wait_selector": ".js-plotly-plot",
    },
    {
        "url": f"{BASE_URL}/3_Segment_Comparison",
        "filename": "segment_comparison.png",
        "description": "Role Compensation and Remote Work",
        "wait_selector": ".js-plotly-plot",
    },
    {
        "url": f"{BASE_URL}/4_Data_Quality",
        "filename": "data_quality.png",
        "description": "Missingness and Nonresponse Audit",
        "wait_selector": "div[data-testid='stDataFrame']",
    },
]


def capture_all_screenshots():
    print("Launching Chromium in headless mode...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport=VIEWPORT,
            device_scale_factor=1,
            color_scheme="dark",
        )
        page = context.new_page()

        for target in CAPTURE_TARGETS:
            print(f"Capturing {target['description']} -> {target['filename']}...")
            page.goto(target["url"], wait_until="networkidle")
            page.wait_for_selector(target["wait_selector"], timeout=15000)

            # Settle Plotly SVG animations
            time.sleep(2.0)

            out_path = OUTPUT_DIR / target["filename"]
            page.screenshot(path=str(out_path), full_page=False)
            print(f"Saved: {out_path} ({out_path.stat().st_size // 1024} KB)")

        browser.close()
    print("All screenshots successfully captured.")


if __name__ == "__main__":
    capture_all_screenshots()
```

---

## 7. Post-Processing and Image Optimization

To ensure fast repository cloning and rapid loading on GitHub, optimize all generated PNG files before staging them in git:

### CLI Optimization with `oxipng` or `pngquant`
```bash
# Lossless optimization with oxipng
oxipng -o 4 -strip all images/*.png

# Or lossy high-quality optimization with pngquant
pngquant --quality=85-95 --ext .png --force images/*.png
```

### Free Web Optimization
Maintainers without CLI image tools can utilize:
- [TinyPNG](https://tinypng.com/) (browser-based lossless compression)
- [Squoosh](https://squoosh.app/) (Google Chrome Labs image optimization engine)

**Verification:** Confirm that every PNG file in `images/` is strictly under **400 KB**.

---

## 8. Embedding Screenshots in Markdown

When embedding visual assets in `README.md`, reports, or portfolio documentation, use relative file paths and descriptive alt text:

```markdown
<!-- Executive Dashboard Landing Portal -->
![Dashboard Overview](images/dashboard_overview.png)
*Figure 1: Executive Dashboard Landing Page showing global survey telemetry and high-level KPIs.*

<!-- Technology Adoption and Preference Gaps -->
![Response Analysis](images/response_analysis.png)
*Figure 2: Response Analysis page featuring dual-denominator technology adoption and paired current-versus-desired preference gaps.*

<!-- Segment Comparison and Remote Work Dynamics -->
![Segment Comparison](images/segment_comparison.png)
*Figure 3: Segment Comparison page displaying cross-cohort salary distributions, quadratic experience gradients, and remote wage attenuation.*

<!-- Data Quality and Nonresponse Mechanism Audit -->
![Data Quality](images/data_quality.png)
*Figure 4: Data Quality page illustrating survey missingness rankings and the RemoteWork nonresponse audit.*
```

---

## 9. Maintainer Review Checklist

Before committing new or updated screenshot assets to the repository:
- [ ] Viewport resolution is strictly $1920 \times 1080$ (16:9 Full HD) or higher.
- [ ] Dark theme is active by default with `#0E1117` background and `#F1F5F9` text.
- [ ] No browser scrollbars, address bars, or developer tool overlays are visible.
- [ ] Mouse cursor is hidden or positioned out of the chart canvas.
- [ ] All Plotly data labels, legends, and axis titles are sharp, anti-aliased, and fully legible.
- [ ] Numbers displayed in screenshots strictly match canonical Phase 5/6 statistical findings ($49,191$ raw, $49,009$ official, $177$ countries, $78.5\%$ AI adoption).
- [ ] Image file size is optimized to $\le 400\text{ KB}$ per file.
- [ ] Relative links in `README.md` point accurately to `images/<filename>.png`.
