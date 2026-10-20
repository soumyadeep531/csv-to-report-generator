from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Web UI"])


@router.get("/", response_class=HTMLResponse)
def index_page():
    """
    Serve the interactive web interface.
    """
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#f4f5ef">
    <meta name="description" content="Automated Exploratory Data Analysis and Machine Learning Baseline Report Generator">
    <title>Fieldnote | CSV Analysis & ML Report Generator</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Manrope:wght@500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --paper: #f4f5ef;
            --ink: #192923;
            --muted: #68766e;
            --line: #dce2d9;
            --panel: #fffefa;
            --forest: #245b43;
            --forest-dark: #194531;
            --lime: #cfe56c;
            --coral: #c7664d;
            --mono: 'DM Mono', monospace;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        html { scroll-behavior: smooth; }

        body {
            font-family: 'DM Sans', sans-serif;
            color: var(--ink);
            background-color: var(--paper);
            background-image: 
                linear-gradient(rgba(36,91,67,0.035) 1px, transparent 1px),
                linear-gradient(90deg, rgba(36,91,67,0.035) 1px, transparent 1px);
            background-size: 34px 34px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        button, input { font: inherit; }
        button:focus-visible, input:focus-visible, a:focus-visible, .drop-zone:focus-visible {
            outline: 3px solid #98b94e;
            outline-offset: 3px;
        }

        .topbar {
            height: 68px;
            padding: 0 clamp(20px, 5vw, 76px);
            border-bottom: 1px solid var(--line);
            background: rgba(255,254,250,0.88);
            backdrop-filter: blur(8px);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 11px;
            font: 800 18px 'Manrope', sans-serif;
            color: var(--ink);
            text-decoration: none;
        }

        .brand-mark {
            width: 30px;
            height: 30px;
            border-radius: 8px;
            display: grid;
            place-items: center;
            background: var(--forest);
            color: var(--lime);
            font-weight: 800;
            font-size: 15px;
        }

        .top-links {
            display: flex;
            gap: 22px;
            align-items: center;
        }

        .top-links a {
            color: var(--muted);
            text-decoration: none;
            font-size: 13px;
            font-weight: 500;
            transition: color 0.15s;
        }

        .top-links a:hover {
            color: var(--forest);
        }

        .top-status {
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--muted);
            font: 11px var(--mono);
            text-transform: uppercase;
        }

        .top-status::before {
            content: '';
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #76a65d;
            box-shadow: 0 0 0 3px #e4eed9;
        }

        main {
            max-width: 1120px;
            width: calc(100% - 48px);
            margin: 0 auto;
            padding: 56px 0 52px;
            flex: 1;
        }

        .intro {
            display: grid;
            grid-template-columns: 1fr 280px;
            gap: 40px;
            align-items: end;
            margin-bottom: 32px;
            animation: rise 0.5s ease both;
        }

        .eyebrow {
            color: var(--forest);
            font: 11px var(--mono);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        h1 {
            font: 700 clamp(32px, 4.5vw, 54px)/1.08 'Manrope', sans-serif;
            margin: 12px 0 12px;
            max-width: 650px;
            color: var(--ink);
        }

        .intro p {
            color: var(--muted);
            font-size: 15.5px;
            line-height: 1.6;
            margin: 0;
            max-width: 590px;
        }

        .intro-note {
            padding: 14px 0 2px 18px;
            border-left: 2px solid var(--lime);
            color: var(--muted);
            font-size: 12.5px;
            line-height: 1.55;
        }

        .intro-note strong {
            display: block;
            color: var(--ink);
            font: 600 11px var(--mono);
            text-transform: uppercase;
            margin-bottom: 5px;
        }

        .workspace {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 8px;
            box-shadow: 0 14px 42px rgba(31,54,39,0.06);
            overflow: hidden;
            animation: rise 0.6s 0.08s ease both;
        }

        .workspace-head {
            min-height: 52px;
            padding: 0 24px;
            border-bottom: 1px solid var(--line);
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #fafbf6;
        }

        .workspace-head h2 {
            margin: 0;
            font: 700 13px 'Manrope', sans-serif;
            color: var(--ink);
        }

        .step-label {
            color: var(--muted);
            font: 10px var(--mono);
            letter-spacing: 0.05em;
        }

        .workspace-body {
            display: grid;
            grid-template-columns: minmax(0, 1fr) 310px;
        }

        .upload-column {
            padding: 26px;
            border-right: 1px solid var(--line);
        }

        .drop-zone {
            min-height: 220px;
            padding: 26px;
            border: 2px dashed #b8c8b9;
            border-radius: 6px;
            background-color: #f9faf4;
            background-image: radial-gradient(#ced8c7 0.8px, transparent 0.8px);
            background-size: 14px 14px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            cursor: pointer;
            transition: border-color 0.2s, background-color 0.2s, transform 0.2s;
        }

        .drop-zone:hover, .drop-zone.dragover {
            border-color: var(--forest);
            background-color: #eff5ea;
            transform: translateY(-2px);
        }

        .upload-icon {
            width: 46px;
            height: 46px;
            display: grid;
            place-items: center;
            background: var(--forest);
            color: var(--lime);
            margin-bottom: 13px;
            border-radius: 50%;
        }

        .drop-title {
            font: 700 15px 'Manrope', sans-serif;
            margin: 0 0 4px;
            color: var(--ink);
        }

        .drop-copy {
            color: var(--muted);
            font-size: 12px;
            margin: 0;
        }

        .file-meta {
            min-height: 18px;
            margin-top: 10px;
            color: var(--forest);
            font: 11px var(--mono);
            overflow-wrap: anywhere;
        }

        .field-grid {
            margin-top: 22px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 14px;
        }

        .field {
            display: flex;
            flex-direction: column;
            gap: 7px;
        }

        label {
            color: var(--muted);
            font: 10px var(--mono);
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .field input {
            width: 100%;
            height: 42px;
            padding: 0 12px;
            border: 1px solid var(--line);
            border-radius: 4px;
            color: var(--ink);
            background: white;
            font: 12px var(--mono);
            transition: border-color 0.15s;
        }

        .field input:focus {
            border-color: var(--forest);
            outline: none;
        }

        .field input::placeholder {
            color: #a2aaa2;
        }

        .options-column {
            padding: 26px 22px;
            background: #fbfcf8;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .options-title {
            color: var(--muted);
            font: 10px var(--mono);
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin: 0 0 14px;
        }

        .options-list {
            display: flex;
            flex-direction: column;
        }

        .option-row {
            display: flex;
            gap: 11px;
            padding: 11px 0;
            border-top: 1px solid var(--line);
        }

        .option-icon {
            color: var(--forest);
            font: 700 11px var(--mono);
            flex: 0 0 20px;
        }

        .option-row strong {
            display: block;
            font: 600 12px 'Manrope', sans-serif;
            margin-bottom: 2px;
            color: var(--ink);
        }

        .option-row span {
            display: block;
            color: var(--muted);
            font-size: 11px;
            line-height: 1.45;
        }

        .actions {
            display: flex;
            flex-direction: column;
            gap: 9px;
            margin-top: 20px;
        }

        button {
            min-height: 44px;
            padding: 0 15px;
            border: 0;
            border-radius: 4px;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 8px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 700;
            transition: background 0.18s, transform 0.18s, opacity 0.18s;
        }

        button:hover:not(:disabled) {
            transform: translateY(-1px);
        }

        button:disabled {
            opacity: 0.65;
            cursor: wait;
        }

        .btn-primary {
            background: var(--forest);
            color: white;
        }

        .btn-primary:hover:not(:disabled) {
            background: var(--forest-dark);
        }

        .btn-secondary {
            background: transparent;
            color: var(--forest);
            border: 1px solid #b8c8b9;
        }

        .btn-secondary:hover:not(:disabled) {
            background: #eff4e8;
        }

        .spinner {
            width: 14px;
            height: 14px;
            border: 2px solid rgba(255,255,255,0.35);
            border-top-color: white;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            display: none;
        }

        .btn-primary.loading .spinner {
            display: block;
        }

        .notice {
            display: none;
            margin: 18px 26px;
            padding: 12px 14px;
            border-left: 3px solid var(--coral);
            background: #fff2ec;
            color: #713b2d;
            font-size: 13px;
            line-height: 1.5;
            border-radius: 0 4px 4px 0;
        }

        .notice.show {
            display: block;
        }

        .results {
            display: none;
            margin-top: 24px;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--panel);
            overflow: hidden;
            animation: rise 0.3s ease both;
        }

        .results.show {
            display: block;
        }

        .results-head {
            padding: 18px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 18px;
            border-bottom: 1px solid var(--line);
            background: #fafbf6;
        }

        .results-heading {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .success-mark {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: #e4eed9;
            color: var(--forest);
            display: grid;
            place-items: center;
            font-size: 13px;
            font-weight: 800;
        }

        .results-heading h2 {
            font: 700 14px 'Manrope', sans-serif;
            margin: 0 0 2px;
            color: var(--ink);
        }

        .results-heading p {
            color: var(--muted);
            font: 10px var(--mono);
            margin: 0;
        }

        .download-btn {
            min-height: 40px;
            padding: 0 16px;
            color: white;
            background: var(--forest);
            text-decoration: none;
            border-radius: 4px;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            font-weight: 700;
            white-space: nowrap;
            transition: background 0.18s;
        }

        .download-btn:hover {
            background: var(--forest-dark);
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        }

        .stat {
            min-height: 84px;
            padding: 16px 20px;
            border-right: 1px solid var(--line);
        }

        .stat:last-child {
            border-right: 0;
        }

        .stat-value {
            display: block;
            color: var(--forest);
            font: 700 22px 'Manrope', sans-serif;
            overflow-wrap: anywhere;
        }

        .stat-label {
            display: block;
            margin-top: 4px;
            color: var(--muted);
            font: 9px var(--mono);
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 18px;
            margin-top: 28px;
            color: var(--muted);
            font-size: 12px;
        }

        .footer a {
            color: var(--forest);
            text-decoration: none;
        }

        .footer a:hover {
            text-decoration: underline;
        }

        .footer-links {
            display: flex;
            gap: 16px;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        @keyframes rise {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 760px) {
            main { width: calc(100% - 32px); padding-top: 36px; }
            .intro { grid-template-columns: 1fr; gap: 16px; }
            .intro-note { max-width: 400px; }
            .workspace-body { grid-template-columns: 1fr; }
            .upload-column { border-right: 0; border-bottom: 1px solid var(--line); }
            .options-column { padding: 22px 24px; }
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            .stat { border-bottom: 1px solid var(--line); }
        }

        @media (max-width: 480px) {
            .topbar { height: 58px; padding: 0 16px; }
            .top-links { gap: 12px; }
            .top-links a { font-size: 11px; }
            .top-status { display: none; }
            main { width: calc(100% - 24px); padding-top: 28px; }
            .upload-column { padding: 18px; }
            .drop-zone { min-height: 190px; padding: 18px 12px; }
            .field-grid { grid-template-columns: 1fr; gap: 12px; }
            .options-column { padding: 18px 16px; }
            .results-head { padding: 16px; align-items: flex-start; flex-direction: column; }
            .footer { flex-direction: column; text-align: center; }
        }
    </style>
</head>
<body>
    <nav class="topbar" aria-label="Main navigation">
        <a href="/" class="brand">
            <span class="brand-mark" aria-hidden="true">f.</span>
            Fieldnote
        </a>
        <div class="top-links">
            <a href="/docs">API Docs</a>
            <a href="/health">Health</a>
            <a href="/redoc">ReDoc</a>
        </div>
        <div class="top-status">Ready for analysis</div>
    </nav>

    <main>
        <section class="intro">
            <div>
                <div class="eyebrow">DATA WORKSPACE / 01</div>
                <h1>Make your data<br>tell its story.</h1>
                <p>Drop in a CSV and get a clear picture of its quality, distributions, and predictive signal, packaged as a downloadable PDF report.</p>
            </div>
            <div class="intro-note">
                <strong>Private by design</strong>
                No database or account required. Datasets are processed in-memory and summarized directly into portable reports.
            </div>
        </section>

        <section class="workspace" aria-labelledby="workspaceTitle">
            <div class="workspace-head">
                <h2 id="workspaceTitle">Start an analysis</h2>
                <span class="step-label">01 &nbsp; UPLOAD &nbsp; / &nbsp; 02 &nbsp; REPORT</span>
            </div>
            <div class="workspace-body">
                <form id="uploadForm" class="upload-column">
                    <div class="drop-zone" id="dropZone" role="button" tabindex="0" aria-label="Choose or drop a CSV file">
                        <span class="upload-icon" aria-hidden="true">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5M4 15v4a1 1 0 001 1h14a1 1 0 001-1v-4"/>
                            </svg>
                        </span>
                        <p class="drop-title" id="fileNameDisplay">Drop your CSV file here</p>
                        <p class="drop-copy">or click to browse from your device</p>
                        <div class="file-meta" id="fileMeta">CSV format · UTF-8 recommended</div>
                        <input type="file" id="fileInput" name="file" accept=".csv,text/csv" hidden>
                    </div>

                    <div class="field-grid">
                        <div class="field">
                            <label for="targetColumn">Target column <span>(optional)</span></label>
                            <input type="text" id="targetColumn" name="target_column" placeholder="e.g. diagnosis">
                        </div>
                        <div class="field">
                            <label for="idColumns">Identifier columns</label>
                            <input type="text" id="idColumns" name="id_columns" placeholder="e.g. id, record_key">
                        </div>
                    </div>
                </form>

                <aside class="options-column" aria-label="Analysis details">
                    <div>
                        <h3 class="options-title">Included in your report</h3>
                        <div class="options-list">
                            <div class="option-row">
                                <span class="option-icon">01</span>
                                <div><strong>Dataset profile</strong><span>Shape, types, missing values and duplicates</span></div>
                            </div>
                            <div class="option-row">
                                <span class="option-icon">02</span>
                                <div><strong>Exploratory analysis</strong><span>Distributions, correlations and PCA</span></div>
                            </div>
                            <div class="option-row">
                                <span class="option-icon">03</span>
                                <div><strong>ML baseline</strong><span>Classification metrics & feature importance</span></div>
                            </div>
                            <div class="option-row">
                                <span class="option-icon">04</span>
                                <div><strong>Portable PDF</strong><span>Full-color charts and AI executive summary</span></div>
                            </div>
                        </div>
                    </div>

                    <div class="actions">
                        <button type="submit" form="uploadForm" class="btn-primary" id="generateBtn">
                            <span class="spinner" aria-hidden="true"></span>
                            <span id="btnText">Generate report</span>
                            <span aria-hidden="true">&#8594;</span>
                        </button>
                        <button type="button" class="btn-secondary" id="sampleBtn">
                            <span aria-hidden="true">&#9655;</span> Try the included sample
                        </button>
                    </div>
                </aside>
            </div>
            <div class="notice" id="notice" role="alert" aria-live="polite"></div>
        </section>

        <section class="results" id="results" aria-live="polite" aria-labelledby="resultsTitle">
            <div class="results-head">
                <div class="results-heading">
                    <span class="success-mark" aria-hidden="true">&#10003;</span>
                    <div>
                        <h2 id="resultsTitle">Your report is ready</h2>
                        <p id="reportName">PDF REPORT</p>
                    </div>
                </div>
                <a class="download-btn" id="downloadLink" href="#" target="_blank">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 3v12m0 0l-4-4m4 4l4-4M4 17v3h16v-3"/>
                    </svg>
                    Download PDF
                </a>
            </div>
            <div class="stats-grid" id="statsContainer"></div>
        </section>

        <footer class="footer">
            <span>Analysis powered by Fieldnote Automated EDA & ML Engine.</span>
            <div class="footer-links">
                <a href="/docs">Swagger Docs</a>
                <a href="/redoc">ReDoc</a>
                <a href="/health">Health API</a>
            </div>
        </footer>
    </main>

    <script>
        const dropZone = document.getElementById('dropZone');
        const fileInput = document.getElementById('fileInput');
        const fileNameDisplay = document.getElementById('fileNameDisplay');
        const fileMeta = document.getElementById('fileMeta');
        const uploadForm = document.getElementById('uploadForm');
        const generateBtn = document.getElementById('generateBtn');
        const sampleBtn = document.getElementById('sampleBtn');
        const btnText = document.getElementById('btnText');
        const notice = document.getElementById('notice');
        const results = document.getElementById('results');
        const statsContainer = document.getElementById('statsContainer');
        const downloadLink = document.getElementById('downloadLink');
        const reportName = document.getElementById('reportName');

        function chooseFile() {
            fileInput.click();
        }

        dropZone.addEventListener('click', chooseFile);
        dropZone.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                chooseFile();
            }
        });

        dropZone.addEventListener('dragover', (event) => {
            event.preventDefault();
            dropZone.classList.add('dragover');
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('dragover');
        });

        dropZone.addEventListener('drop', (event) => {
            event.preventDefault();
            dropZone.classList.remove('dragover');
            if (event.dataTransfer.files.length > 0) {
                fileInput.files = event.dataTransfer.files;
                showSelectedFile(fileInput.files[0]);
            }
        });

        function showSelectedFile(file) {
            fileNameDisplay.textContent = file.name;
            fileMeta.textContent = `${(file.size / 1024).toLocaleString(undefined, { maximumFractionDigits: 1 })} KB · Ready to analyze`;
            notice.classList.remove('show');
        }

        fileInput.addEventListener('change', () => {
            if (fileInput.files.length) {
                showSelectedFile(fileInput.files[0]);
            }
        });

        function setLoading(loading, message = 'Analyzing dataset…') {
            generateBtn.disabled = loading;
            sampleBtn.disabled = loading;
            generateBtn.classList.toggle('loading', loading);
            btnText.textContent = loading ? message : 'Generate report';
            if (loading) {
                notice.classList.remove('show');
            }
        }

        function showError(message) {
            notice.textContent = message;
            notice.classList.add('show');
        }

        function displayResults(data) {
            const ov = data.overview || {};
            const met = data.metrics || {};

            downloadLink.href = data.report_url;
            downloadLink.setAttribute('download', data.filename || 'analysis-report.pdf');
            reportName.textContent = data.filename || 'PDF REPORT';

            const cards = [
                ['Rows', ov.rows ?? '—'],
                ['Columns', ov.columns ?? '—'],
                ['Task Type', ov.task_type ?? '—'],
                ['Target Column', ov.target_column ?? '—']
            ];

            if (met.accuracy !== undefined && met.accuracy !== null) {
                cards.push(['Model Accuracy', `${(Number(met.accuracy) * 100).toFixed(1)}%`]);
            }
            if (met.f1 !== undefined && met.f1 !== null) {
                cards.push(['F1 Score', `${(Number(met.f1) * 100).toFixed(1)}%`]);
            }

            statsContainer.replaceChildren(...cards.map(([label, value]) => {
                const card = document.createElement('div');
                card.className = 'stat';
                const statValue = document.createElement('span');
                statValue.className = 'stat-value';
                statValue.textContent = value;
                const statLabel = document.createElement('span');
                statLabel.className = 'stat-label';
                statLabel.textContent = label;
                card.append(statValue, statLabel);
                return card;
            }));

            results.classList.add('show');
            results.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }

        async function readResponse(response) {
            const data = await response.json().catch(() => ({}));
            if (!response.ok) {
                const detail = typeof data.detail === 'string' ? data.detail : 'The report could not be generated. Please check the CSV and try again.';
                throw new Error(detail);
            }
            return data;
        }

        uploadForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const file = fileInput.files[0];
            if (!file) {
                return showError('Choose a CSV file before starting the analysis.');
            }
            if (!file.name.toLowerCase().endsWith('.csv')) {
                return showError('Please select a file with the .csv extension.');
            }

            const formData = new FormData();
            formData.append('file', file);
            const target = document.getElementById('targetColumn').value.trim();
            const ids = document.getElementById('idColumns').value.trim();
            if (target) formData.append('target_column', target);
            if (ids) formData.append('id_columns', ids);

            setLoading(true, 'Analyzing dataset & compiling PDF…');
            results.classList.remove('show');

            try {
                const response = await fetch('/api/generate-report', {
                    method: 'POST',
                    body: formData
                });
                displayResults(await readResponse(response));
            } catch (error) {
                showError(error.message || 'Something went wrong while generating the report.');
            } finally {
                setLoading(false);
            }
        });

        sampleBtn.addEventListener('click', async () => {
            setLoading(true, 'Running bundled Cancer_Data.csv sample…');
            results.classList.remove('show');

            try {
                const response = await fetch('/api/sample-report');
                displayResults(await readResponse(response));
            } catch (error) {
                showError(error.message || 'The sample report could not be generated.');
            } finally {
                setLoading(false);
            }
        });
    </script>
</body>
</html>
"""
