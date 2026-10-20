from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Web UI"])


@router.get("/", response_class=HTMLResponse)
def index_page():
    """
    Serve the interactive web interface.
    """
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AutoEDA & ML Report Generator</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
            <meta name="theme-color" content="#f4f5ef">
            <title>Fieldnote | CSV Analysis</title>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
        <style>
            <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap" rel="stylesheet">
                --primary: #6366f1;
                --primary-hover: #4f46e5;
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
            body {
                * { box-sizing: border-box; }
                html { scroll-behavior: smooth; }
                background-color: var(--bg);
                    margin: 0;
                    font-family: 'DM Sans', sans-serif;
                    color: var(--ink);
                display: flex;
                    background-color: var(--paper);
                    background-image: linear-gradient(rgba(36,91,67,.035) 1px, transparent 1px), linear-gradient(90deg, rgba(36,91,67,.035) 1px, transparent 1px);
                    background-size: 34px 34px;
                width: 100%;
                button, input { font: inherit; }
                button:focus-visible, input:focus-visible, a:focus-visible, .drop-zone:focus-visible { outline: 3px solid #98b94e; outline-offset: 3px; }
                .topbar {
                    height: 68px;
                    padding: 0 clamp(20px, 5vw, 76px);
                    border-bottom: 1px solid var(--line);
                    background: rgba(255,254,250,.88);
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                }
                .brand { display: flex; align-items: center; gap: 11px; font: 800 18px 'Manrope', sans-serif; letter-spacing: 0; }
                .brand-mark { width: 30px; height: 30px; border-radius: 8px; display: grid; place-items: center; background: var(--forest); color: var(--lime); }
                .top-links { display: flex; gap: 22px; align-items: center; }
                .top-links a { color: var(--muted); text-decoration: none; font-size: 13px; }
                .top-links a:hover { color: var(--forest); }
                .top-status { display: flex; align-items: center; gap: 8px; color: var(--muted); font: 11px var(--mono); text-transform: uppercase; }
                .top-status::before { content: ''; width: 7px; height: 7px; border-radius: 50%; background: #76a65d; box-shadow: 0 0 0 3px #e4eed9; }
                main { max-width: 1120px; width: calc(100% - 48px); margin: 0 auto; padding: 64px 0 52px; }
                .intro { display: grid; grid-template-columns: 1fr 250px; gap: 40px; align-items: end; margin-bottom: 32px; animation: rise .55s ease both; }
                .eyebrow { color: var(--forest); font: 11px var(--mono); letter-spacing: 0; text-transform: uppercase; }
                h1 { font: 700 clamp(36px, 5vw, 60px)/1.05 'Manrope', sans-serif; letter-spacing: 0; margin: 14px 0 12px; max-width: 650px; }
                .intro p { color: var(--muted); font-size: 16px; line-height: 1.65; margin: 0; max-width: 590px; }
                .intro-note { padding: 14px 0 2px 18px; border-left: 2px solid var(--lime); color: var(--muted); font-size: 13px; line-height: 1.55; }
                .intro-note strong { display: block; color: var(--ink); font: 600 11px var(--mono); text-transform: uppercase; margin-bottom: 6px; }
                .workspace { background: var(--panel); border: 1px solid var(--line); border-radius: 6px; box-shadow: 0 14px 42px rgba(31,54,39,.07); animation: rise .65s .08s ease both; }
                .workspace-head { min-height: 54px; padding: 0 24px; border-bottom: 1px solid var(--line); display: flex; align-items: center; justify-content: space-between; }
                .workspace-head h2 { margin: 0; font: 700 13px 'Manrope', sans-serif; }
                .step-label { color: var(--muted); font: 10px var(--mono); }
                .workspace-body { display: grid; grid-template-columns: minmax(0, 1fr) 310px; }
                .upload-column { padding: 25px; border-right: 1px solid var(--line); }
                .drop-zone { min-height: 244px; padding: 26px; border: 1px dashed #aab9a9; background-color: #f8f9f3; background-image: radial-gradient(#ced8c7 0.7px, transparent 0.7px); background-size: 13px 13px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; cursor: pointer; transition: border-color .2s, background-color .2s, transform .2s; }
                .drop-zone:hover, .drop-zone.dragover { border-color: var(--forest); background-color: #eff4e8; transform: translateY(-2px); }
                .upload-icon { width: 48px; height: 48px; display: grid; place-items: center; background: var(--forest); color: var(--lime); margin-bottom: 15px; border-radius: 50%; }
                .drop-title { font: 700 16px 'Manrope', sans-serif; margin: 0 0 5px; }
                .drop-copy { color: var(--muted); font-size: 12px; margin: 0; }
                .file-meta { min-height: 18px; margin-top: 9px; color: var(--forest); font: 11px var(--mono); overflow-wrap: anywhere; }
                .field-grid { margin-top: 23px; display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
                .field { display: flex; flex-direction: column; gap: 7px; }
                label { color: var(--muted); font: 10px var(--mono); text-transform: uppercase; }
                .field input { width: 100%; height: 42px; padding: 0 12px; border: 1px solid var(--line); border-radius: 3px; color: var(--ink); background: white; font: 12px var(--mono); }
                .field input::placeholder { color: #a2aaa2; }
                .options-column { padding: 25px 22px; background: #fbfcf7; }
                .options-title { color: var(--muted); font: 10px var(--mono); letter-spacing: 0; text-transform: uppercase; margin: 0 0 15px; }
                .option-row { display: flex; gap: 11px; padding: 13px 0; border-top: 1px solid var(--line); }
                .option-icon { color: var(--forest); flex: 0 0 20px; }
                .option-row strong { display: block; font: 600 12px 'Manrope', sans-serif; margin-bottom: 3px; }
                .option-row span { display: block; color: var(--muted); font-size: 11px; line-height: 1.45; }
                .actions { display: flex; flex-direction: column; gap: 9px; margin-top: 18px; }
                button { min-height: 45px; padding: 0 15px; border: 0; border-radius: 3px; display: flex; justify-content: center; align-items: center; gap: 9px; cursor: pointer; font-size: 12px; font-weight: 700; transition: background .18s, transform .18s; }
                button:hover:not(:disabled) { transform: translateY(-1px); }
                button:disabled { opacity: .6; cursor: wait; }
                .btn-primary { background: var(--forest); color: white; }
                .btn-primary:hover:not(:disabled) { background: var(--forest-dark); }
                .btn-secondary { background: transparent; color: var(--forest); border: 1px solid #b8c8b9; }
                .btn-secondary:hover:not(:disabled) { background: #eff4e8; }
                .spinner { width: 15px; height: 15px; border: 2px solid rgba(255,255,255,.35); border-top-color: white; border-radius: 50%; animation: spin .8s linear infinite; display: none; }
                .btn-primary.loading .spinner { display: block; }
                .notice { display: none; margin: 18px 25px 0; padding: 12px 14px; border-left: 3px solid var(--coral); background: #fff2ec; color: #713b2d; font-size: 13px; line-height: 1.5; }
                .notice.show { display: block; }
                .results { display: none; margin-top: 22px; border: 1px solid var(--line); border-radius: 6px; background: var(--panel); animation: rise .3s ease both; }
                .results.show { display: block; }
                .results-head { padding: 19px 23px; display: flex; align-items: center; justify-content: space-between; gap: 18px; border-bottom: 1px solid var(--line); }
                .results-heading { display: flex; align-items: center; gap: 11px; }
                .success-mark { width: 27px; height: 27px; border-radius: 50%; background: #e7f0d8; color: var(--forest); display: grid; place-items: center; }
                .results-heading h2 { font: 700 14px 'Manrope', sans-serif; margin: 0 0 3px; }
                .results-heading p { color: var(--muted); font: 10px var(--mono); margin: 0; }
                .download-btn { min-height: 39px; padding: 0 14px; color: white; background: var(--forest); text-decoration: none; border-radius: 3px; display: inline-flex; align-items: center; gap: 8px; font-size: 11px; font-weight: 700; white-space: nowrap; }
                .download-btn:hover { background: var(--forest-dark); }
                .stats-grid { display: grid; grid-template-columns: repeat(5, 1fr); }
                .stat { min-height: 88px; padding: 18px 20px; border-right: 1px solid var(--line); }
                .stat:last-child { border-right: 0; }
                .stat-value { display: block; color: var(--forest); font: 700 23px 'Manrope', sans-serif; overflow-wrap: anywhere; }
                .stat-label { display: block; margin-top: 5px; color: var(--muted); font: 9px var(--mono); text-transform: uppercase; }
                .footer { display: flex; justify-content: space-between; gap: 18px; margin-top: 25px; color: var(--muted); font-size: 11px; }
                .footer a { color: var(--forest); text-decoration: none; }
                .footer-links { display: flex; gap: 16px; }
                @keyframes spin { to { transform: rotate(360deg); } }
                @keyframes rise { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
                @media (max-width: 760px) {
                    main { width: calc(100% - 32px); padding-top: 40px; }
                    .intro { grid-template-columns: 1fr; gap: 16px; }
                    .intro-note { max-width: 350px; }
                    .workspace-body { grid-template-columns: 1fr; }
                    .upload-column { border-right: 0; border-bottom: 1px solid var(--line); }
                    .options-column { padding: 22px 25px; }
                    .options-list { display: grid; grid-template-columns: 1fr 1fr; gap: 0 16px; }
                    .stats-grid { grid-template-columns: repeat(2, 1fr); }
                    .stat { border-bottom: 1px solid var(--line); }
                    .stat:nth-child(2n) { border-right: 0; }
                    .stat:last-child { grid-column: 1 / -1; border-bottom: 0; }
                }
                @media (max-width: 480px) {
                    .topbar { height: 58px; padding: 0 16px; }
                    .top-links { gap: 12px; }
                    .top-links a { font-size: 11px; }
                    .top-status { display: none; }
                    main { width: calc(100% - 24px); padding-top: 32px; }
                    .upload-column { padding: 16px; }
                    .drop-zone { min-height: 210px; padding: 20px 12px; }
                    .field-grid { grid-template-columns: 1fr; gap: 12px; }
                    .options-column { padding: 20px 16px; }
                    .options-list { grid-template-columns: 1fr; }
                    .workspace-head { padding: 0 16px; }
                    .results-head { padding: 15px; align-items: flex-start; flex-direction: column; }
                    .stat { padding: 15px; }
                    .footer { flex-direction: column; }
                }
                text-align: center;
                margin-bottom: 35px;
            }
            <nav class="topbar" aria-label="Main navigation">
                <div class="brand"><span class="brand-mark" aria-hidden="true">f.</span> Fieldnote</div>
                <div class="top-links"><a href="/docs">API docs</a><a href="/health">System status</a></div>
                <div class="top-status">Ready for analysis</div>
            </nav>
            <main>
                <section class="intro">
                    <div>
                        <div class="eyebrow">DATA WORKSPACE / 01</div>
                        <h1>Make your data<br>tell its story.</h1>
                        <p>Drop in a CSV and get a clear picture of its quality, patterns, and predictive signal, packaged as a report you can share.</p>
                    </div>
                    <div class="intro-note"><strong>Private by design</strong>No account needed. Your dataset is analyzed by this service and the report is ready to download when it finishes.</div>
                </section>

                <section class="workspace" aria-labelledby="workspaceTitle">
                    <div class="workspace-head"><h2 id="workspaceTitle">Start an analysis</h2><span class="step-label">01 &nbsp; UPLOAD &nbsp; / &nbsp; 02 &nbsp; REPORT</span></div>
                    <div class="workspace-body">
                        <form id="uploadForm" class="upload-column">
                            <div class="drop-zone" id="dropZone" role="button" tabindex="0" aria-label="Choose or drop a CSV file">
                                <span class="upload-icon" aria-hidden="true"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5M4 15v4a1 1 0 001 1h14a1 1 0 001-1v-4"/></svg></span>
                                <p class="drop-title" id="fileNameDisplay">Drop your CSV file here</p>
                                <p class="drop-copy">or click to browse from your device</p>
                                <div class="file-meta" id="fileMeta">CSV format · UTF-8 recommended</div>
                                <input type="file" id="fileInput" name="file" accept=".csv,text/csv" hidden>
                            </div>
                            <div class="field-grid">
                                <div class="field"><label for="targetColumn">Target column <span>(optional)</span></label><input type="text" id="targetColumn" name="target_column" placeholder="e.g. diagnosis"></div>
                                <div class="field"><label for="idColumns">Identifier columns</label><input type="text" id="idColumns" name="id_columns" placeholder="e.g. id, record_key"></div>
                            </div>
                        </form>
                        <aside class="options-column" aria-label="Analysis details">
                            <h3 class="options-title">Included in your report</h3>
                            <div class="options-list">
                                <div class="option-row"><span class="option-icon">01</span><div><strong>Dataset profile</strong><span>Shape, types, missing values and duplicates</span></div></div>
                                <div class="option-row"><span class="option-icon">02</span><div><strong>Exploratory analysis</strong><span>Distributions, correlations and outliers</span></div></div>
                                <div class="option-row"><span class="option-icon">03</span><div><strong>ML baseline</strong><span>Classification metrics when applicable</span></div></div>
                                <div class="option-row"><span class="option-icon">04</span><div><strong>Portable PDF</strong><span>Charts and findings in one document</span></div></div>
                            </div>
                            <div class="actions">
                                <button type="submit" form="uploadForm" class="btn-primary" id="generateBtn"><span class="spinner" aria-hidden="true"></span><span id="btnText">Generate report</span><span aria-hidden="true">&#8594;</span></button>
                                <button type="button" class="btn-secondary" id="sampleBtn"><span aria-hidden="true">&#9655;</span> Try the included sample</button>
                            </div>
                        </aside>
                    </div>
                    <div class="notice" id="notice" role="alert" aria-live="polite"></div>
                </section>

                <section class="results" id="results" aria-live="polite" aria-labelledby="resultsTitle">
                    <div class="results-head">
                        <div class="results-heading"><span class="success-mark" aria-hidden="true">&#10003;</span><div><h2 id="resultsTitle">Your report is ready</h2><p id="reportName">PDF REPORT</p></div></div>
                        <a class="download-btn" id="downloadLink" href="#"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3v12m0 0l-4-4m4 4l4-4M4 17v3h16v-3"/></svg> Download PDF</a>
                    </div>
                    <div class="stats-grid" id="statsContainer"></div>
                </section>
                <footer class="footer"><span>Analysis powered by your CSV and the Fieldnote report engine.</span><div class="footer-links"><a href="/docs">API reference</a><a href="/redoc">ReDoc</a></div></footer>
            </main>
                margin-bottom: 12px;
            }
            .drop-zone p {
                font-size: 1.05rem;
                color: var(--text);
                const fileMeta = document.getElementById('fileMeta');
                margin-bottom: 6px;
            }
            .drop-zone span {
                color: var(--text-muted);
                const results = document.getElementById('results');
            .input-group {
                margin-top: 20px;
                const notice = document.getElementById('notice');
                display: grid;
                function chooseFile() { fileInput.click(); }
                dropZone.addEventListener('click', chooseFile);
                dropZone.addEventListener('keydown', (event) => {
                    if (event.key === 'Enter' || event.key === ' ') {
                        event.preventDefault();
                        chooseFile();
                    }
                });
                gap: 15px;
                dropZone.addEventListener('dragover', (event) => {
                    event.preventDefault();
                display: flex;
                });
                dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
                dropZone.addEventListener('drop', (event) => {
                    event.preventDefault();
                font-size: 0.85rem;
                    if (event.dataTransfer.files.length > 0) {
                        fileInput.files = event.dataTransfer.files;
                        showSelectedFile(fileInput.files[0]);
            input[type="text"] {
                });
                border: 1px solid var(--card-border);
                function showSelectedFile(file) {
                    fileNameDisplay.textContent = file.name;
                    fileMeta.textContent = `${(file.size / 1024).toLocaleString(undefined, { maximumFractionDigits: 1 })} KB · Ready to analyze`;
                    notice.classList.remove('show');
                }
                fileInput.addEventListener('change', () => {
                    if (fileInput.files.length) showSelectedFile(fileInput.files[0]);
                });
            }
            input[type="text"]:focus {
                    generateBtn.classList.toggle('loading', loading);
                    btnText.textContent = loading ? 'Analyzing dataset…' : 'Generate report';
            }
            .actions {
                    notice.classList.remove('show');
                }

                function showError(message) {
                    notice.textContent = message;
                    notice.classList.add('show');
                margin-top: 25px;
                display: flex;
                gap: 15px;
                    downloadLink.href = data.report_url;
                    downloadLink.setAttribute('download', data.filename || 'analysis-report.pdf');
                    document.getElementById('reportName').textContent = data.filename || 'PDF REPORT';
                font-size: 1rem;
                font-weight: 600;
                    const metricsAvailable = Number.isFinite(Number(met.accuracy));
                    const cards = [
                        ['Rows', ov.rows],
                        ['Columns', ov.columns],
                        ['Analysis type', ov.task_type],
                        ['Target column', ov.target_column],
                        ...(metricsAvailable ? [['Model accuracy', `${(Number(met.accuracy) * 100).toFixed(1)}%`]] : [])
                    ];
                    statsContainer.replaceChildren(...cards.map(([label, value]) => {
                        const card = document.createElement('div');
                        card.className = 'stat';
                        const statValue = document.createElement('span');
                        statValue.className = 'stat-value';
                        statValue.textContent = value ?? '—';
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
                        const detail = typeof data.detail === 'string' ? data.detail : 'The report could not be generated. Check the CSV and try again.';
                        throw new Error(detail);
                margin-top: 20px;
                    return data;
                }

                uploadForm.addEventListener('submit', async (event) => {
                    event.preventDefault();
                    const file = fileInput.files[0];
                    if (!file) return showError('Choose a CSV file before starting the analysis.');
                    if (!file.name.toLowerCase().endsWith('.csv')) return showError('Please choose a file with the .csv extension.');

                    const formData = new FormData();
                    formData.append('file', file);
                    const target = document.getElementById('targetColumn').value.trim();
                    const ids = document.getElementById('idColumns').value.trim();
                    if (target) formData.append('target_column', target);
                    if (ids) formData.append('id_columns', ids);
            .stat-box {
                    results.classList.remove('show');
                padding: 15px;
                border-radius: 12px;
                border: 1px solid var(--card-border);
                text-align: center;
            }
            .stat-val {
                        displayResults(await readResponse(response));
                    } catch (error) {
                        showError(error.message || 'Something went wrong while generating the report.');
                font-size: 0.8rem;
                color: var(--text-muted);
                margin-top: 4px;
                });
            .download-btn {
                sampleBtn.addEventListener('click', async () => {
                display: block;
                    results.classList.remove('show');
                text-align: center;
                padding: 14px;
                        displayResults(await readResponse(response));
                    } catch (error) {
                        showError(error.message || 'The sample report could not be generated.');
                transition: transform 0.2s;
            }
            .download-btn:hover {
                });
            }
            .spinner {
                border: 3px solid rgba(255, 255, 255, 0.1);
                border-radius: 50%;
                border-top: 3px solid #fff;
                width: 20px;
                height: 20px;
                animation: spin 1s linear infinite;
                display: none;
            }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            .links {
                text-align: center;
                margin-top: 15px;
                font-size: 0.9rem;
            }
            .links a {
                color: #a5b4fc;
                text-decoration: none;
                margin: 0 10px;
            }
            .links a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <div class="badge">⚡ FASTAPI + ML EDA AUTOMATION</div>
                <h1>CSV to Report Generator</h1>
                <p class="subtitle">Upload a dataset to instantly generate comprehensive EDA & Baseline ML PDF reports</p>
            </header>

            <div class="card">
                <form id="uploadForm">
                    <div class="drop-zone" id="dropZone">
                        <svg viewBox="0 0 24 24"><path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM14 13v4h-4v-4H7l5-5 5 5h-3z"/></svg>
                        <p id="fileNameDisplay">Click or Drag & Drop your CSV file here</p>
                        <span>Supports .csv format</span>
                        <input type="file" id="fileInput" name="file" accept=".csv" style="display: none;">
                    </div>

                    <div class="input-group">
                        <div class="input-field">
                            <label>Target Column (Optional)</label>
                            <input type="text" id="targetColumn" name="target_column" placeholder="e.g. diagnosis">
                        </div>
                        <div class="input-field">
                            <label>ID Columns to Drop (Comma-separated)</label>
                            <input type="text" id="idColumns" name="id_columns" placeholder="e.g. id">
                        </div>
                    </div>

                    <div class="actions">
                        <button type="button" class="btn-secondary" id="sampleBtn">Run Sample (Cancer_Data.csv)</button>
                        <button type="submit" class="btn-primary" id="generateBtn">
                            <div class="spinner" id="spinner"></div>
                            <span id="btnText">Generate Full PDF Report</span>
                        </button>
                    </div>
                </form>
            </div>

            <div class="card" id="statusCard">
                <h3 style="color: var(--success); display: flex; align-items: center; gap: 8px;">
                    ✓ Report Generated Successfully!
                </h3>
                <div class="stats-grid" id="statsContainer"></div>
                <a href="#" id="downloadLink" class="download-btn" target="_blank">📥 Download PDF Report</a>
            </div>

            <div class="links">
                <a href="/docs" target="_blank">📚 Swagger API Docs</a>
                <a href="/redoc" target="_blank">📖 ReDoc</a>
                <a href="/health" target="_blank">🩺 Health Status</a>
            </div>
        </div>

        <script>
            const dropZone = document.getElementById('dropZone');
            const fileInput = document.getElementById('fileInput');
            const fileNameDisplay = document.getElementById('fileNameDisplay');
            const uploadForm = document.getElementById('uploadForm');
            const generateBtn = document.getElementById('generateBtn');
            const sampleBtn = document.getElementById('sampleBtn');
            const spinner = document.getElementById('spinner');
            const btnText = document.getElementById('btnText');
            const statusCard = document.getElementById('statusCard');
            const statsContainer = document.getElementById('statsContainer');
            const downloadLink = document.getElementById('downloadLink');

            dropZone.onclick = () => fileInput.click();

            dropZone.ondragover = (e) => {
                e.preventDefault();
                dropZone.classList.add('dragover');
            };
            dropZone.ondragleave = () => dropZone.classList.remove('dragover');
            dropZone.ondrop = (e) => {
                e.preventDefault();
                dropZone.classList.remove('dragover');
                if (e.dataTransfer.files.length > 0) {
                    fileInput.files = e.dataTransfer.files;
                    fileNameDisplay.textContent = fileInput.files[0].name;
                }
            };

            fileInput.onchange = () => {
                if (fileInput.files.length > 0) {
                    fileNameDisplay.textContent = fileInput.files[0].name;
                }
            };

            function setLoading(loading) {
                spinner.style.display = loading ? 'block' : 'none';
                btnText.textContent = loading ? 'Analyzing & Compiling Report...' : 'Generate Full PDF Report';
                generateBtn.disabled = loading;
                sampleBtn.disabled = loading;
            }

            function displayResults(data) {
                statusCard.style.display = 'block';
                downloadLink.href = data.report_url;
                downloadLink.setAttribute('download', data.filename);

                const ov = data.overview || {};
                const met = data.metrics || {};

                statsContainer.innerHTML = `
                    <div class="stat-box">
                        <div class="stat-val">${ov.rows ?? '-'}</div>
                        <div class="stat-lbl">Rows</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-val">${ov.columns ?? '-'}</div>
                        <div class="stat-lbl">Columns</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-val">${ov.task_type ?? '-'}</div>
                        <div class="stat-lbl">Task</div>
                    </div>
                    ${met.accuracy ? `
                    <div class="stat-box">
                        <div class="stat-val">${(met.accuracy * 100).toFixed(1)}%</div>
                        <div class="stat-lbl">Accuracy</div>
                    </div>` : ''}
                    ${met.f1 ? `
                    <div class="stat-box">
                        <div class="stat-val">${(met.f1 * 100).toFixed(1)}%</div>
                        <div class="stat-lbl">F1 Score</div>
                    </div>` : ''}
                `;
                statusCard.scrollIntoView({ behavior: 'smooth' });
            }

            uploadForm.onsubmit = async (e) => {
                e.preventDefault();
                if (!fileInput.files.length) {
                    alert('Please select a CSV file first!');
                    return;
                }
                const formData = new FormData(uploadForm);
                setLoading(true);
                statusCard.style.display = 'none';

                try {
                    const response = await fetch('/api/generate-report', {
                        method: 'POST',
                        body: formData
                    });
                    const data = await response.json();
                    if (!response.ok) throw new Error(data.detail || 'Failed to generate report');
                    displayResults(data);
                } catch (err) {
                    alert('Error: ' + err.message);
                } finally {
                    setLoading(false);
                }
            };

            sampleBtn.onclick = async () => {
                setLoading(true);
                statusCard.style.display = 'none';
                try {
                    const response = await fetch('/api/sample-report');
                    const data = await response.json();
                    if (!response.ok) throw new Error(data.detail || 'Sample generation failed');
                    displayResults(data);
                } catch (err) {
                    alert('Error: ' + err.message);
                } finally {
                    setLoading(false);
                }
            };
        </script>
    </body>
    </html>
    """
