# Data Source Attribution & Licensing Specification

**Project:** Poll Results Visualizer  
**Author:** Akash Das  
**Current Primary Dataset:** Stack Overflow Annual Developer Survey 2025  

---

## 1. Primary Dataset Overview
The primary survey dataset integrated into the **Poll Results Visualizer** project is the official **Stack Overflow Annual Developer Survey 2025**, published by Stack Exchange, Inc.

- **Survey Year:** 2025
- **Publisher / Rights Holder:** Stack Exchange, Inc.
- **Collection Methodology:** Opt-in, web-based survey fielded to developers and technical professionals worldwide.
- **Data Granularity:** Respondent-level, wide-format records (`ResponseId`).

---

## 2. Official Source Locations
The dataset and survey instruments originate strictly from official Stack Overflow distribution endpoints:

1. **Official Survey Portal & Results:**  
   [https://survey.stackoverflow.co/2025/](https://survey.stackoverflow.co/2025/)
2. **Official Survey Repository:**  
   [https://github.com/StackExchange/Survey](https://github.com/StackExchange/Survey)
3. **Official Archive Release Directory:**  
   [https://github.com/StackExchange/Survey/tree/main/packages/archive/2025](https://github.com/StackExchange/Survey/tree/main/packages/archive/2025)
4. **Direct Git LFS Media Endpoints:**  
   - Public Respondent Results: `https://media.githubusercontent.com/media/StackExchange/Survey/main/packages/archive/2025/results.csv`
   - Survey Question Schema: `https://media.githubusercontent.com/media/StackExchange/Survey/main/packages/archive/2025/schema.csv`

---

## 3. Data Licensing vs. Application Code Licensing

> [!IMPORTANT]
> **Distinct Dual-Licensing Architecture**:
> - **Application Source Code & Tooling:** Licensed under the [MIT License](../LICENSE), Copyright (c) 2026 Akash Das.
> - **Stack Overflow Survey Dataset:** Licensed under the [Open Database License (ODbL) v1.0](https://opendatacommons.org/licenses/odbl/1-0/) and [Database Contents License (DbCL) v1.0](https://opendatacommons.org/licenses/dbcl/1-0/), © Stack Exchange, Inc.

The survey dataset itself is **not** licensed under the project's MIT license.

### Open Database License (ODbL) 1.0 Terms
Under ODbL 1.0, you are free to:
- **Share:** Copy, distribute, and use the database.
- **Create:** Produce works (such as visualizations, dashboards, and research papers) from the database.
- **Adapt:** Modify, transform, and build upon the database.

Under the following conditions:
- **Attribution:** You must attribute any public use of the database or works produced from it.
- **Share-Alike:** If you publicly use any adapted version of this database, you must also offer that adapted database under the ODbL 1.0 license.
- **Keep Open:** If you redistribute the database, or an adapted version of it, you must use technology that does not restrict the ability of others to access or use the work (i.e. no digital rights management or closed restrictions).

### Database Contents License (DbCL) 1.0 Terms
Individual cell contents extracted from the survey responses are governed by the DbCL 1.0, waiving copyright in factual data while keeping database-level rights intact under ODbL.

---

## 4. Formal Attribution Notice
When citing, redistributing, or presenting insights derived from this dataset, cite:
```text
Stack Overflow Annual Developer Survey 2025
© Copyright 2026 Stack Exchange, Inc.
Data published under the Open Database License (ODbL) v1.0.
Individual contents published under the Database Contents License (DbCL) v1.0.
Available at: https://survey.stackoverflow.co/2025/
```

---

## 5. Download & Local Setup Instructions
If the dataset files are not already present in your local workspace:

1. Create destination directory:
   ```bash
   mkdir -p data/raw/stackoverflow_developer_survey_2025
   ```
2. Download official public files:
   - Schema:
     `curl -L -o data/raw/stackoverflow_developer_survey_2025/survey_results_schema.csv https://media.githubusercontent.com/media/StackExchange/Survey/main/packages/archive/2025/schema.csv`
   - Results:
     `curl -L -o data/raw/stackoverflow_developer_survey_2025/survey_results_public.csv https://media.githubusercontent.com/media/StackExchange/Survey/main/packages/archive/2025/results.csv`
3. Raw survey files are excluded from Git commits via `.gitignore` (`data/raw/*`) to adhere to repository size and data isolation best practices.
