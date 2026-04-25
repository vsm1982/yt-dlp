import streamlit as st
import yt_dlp
import os
import tempfile
import glob

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YT Downloader",
    page_icon="▶",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Mono', monospace;
}

.stApp {
    background-color: #0d0d0d;
    color: #f0f0f0;
}

h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
    color: #ff3c3c !important;
    line-height: 1.1 !important;
    margin-bottom: 0 !important;
}

.subtitle {
    color: #666;
    font-size: 0.78rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
}

/* Input field */
.stTextInput > div > div > input {
    background-color: #1a1a1a !important;
    border: 1px solid #333 !important;
    border-radius: 2px !important;
    color: #f0f0f0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 0.75rem 1rem !important;
    caret-color: #ff3c3c;
}
.stTextInput > div > div > input:focus {
    border-color: #ff3c3c !important;
    box-shadow: 0 0 0 2px rgba(255,60,60,0.15) !important;
}
.stTextInput label {
    color: #888 !important;
    font-size: 0.75rem !important;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* Buttons */
.stButton > button {
    background-color: #ff3c3c !important;
    color: #0d0d0d !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 1px;
    text-transform: uppercase;
    border: none !important;
    border-radius: 2px !important;
    padding: 0.6rem 1.8rem !important;
    width: 100%;
    transition: background 0.2s, transform 0.1s;
}
.stButton > button:hover {
    background-color: #ff6060 !important;
    transform: translateY(-1px);
}
.stButton > button:active {
    transform: translateY(0px);
}

/* Download button */
.stDownloadButton > button {
    background-color: #0d0d0d !important;
    color: #ff3c3c !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 1px;
    border: 1px solid #ff3c3c !important;
    border-radius: 2px !important;
    padding: 0.6rem 1.8rem !important;
    width: 100%;
    transition: background 0.2s;
}
.stDownloadButton > button:hover {
    background-color: rgba(255,60,60,0.1) !important;
}

/* Progress / status */
.stProgress > div > div > div {
    background-color: #ff3c3c !important;
}

/* Alerts */
.stAlert {
    border-radius: 2px !important;
    font-size: 0.85rem !important;
}

/* Divider line */
.divider {
    border: none;
    border-top: 1px solid #222;
    margin: 1.5rem 0;
}

/* Thumbnail */
.thumb-container {
    border: 1px solid #222;
    border-radius: 2px;
    overflow: hidden;
    margin-bottom: 1rem;
}

/* Video info card */
.info-card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-left: 3px solid #ff3c3c;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
    border-radius: 0 2px 2px 0;
    font-size: 0.82rem;
    line-height: 1.7;
    color: #ccc;
}
.info-card strong {
    color: #f0f0f0;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("<h1>YT DOWNLOADER</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">vídeo · áudio · até 720p</p>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "file_bytes" not in st.session_state:
    st.session_state.file_bytes = None
if "file_name" not in st.session_state:
    st.session_state.file_name = None
if "video_info" not in st.session_state:
    st.session_state.video_info = None

# ── Input ─────────────────────────────────────────────────────────────────────
url = st.text_input("URL do vídeo", placeholder="https://www.youtube.com/watch?v=...")

col1, col2 = st.columns([3, 1])
with col1:
    fetch_btn = st.button("🔍 Buscar informações", use_container_width=True)
with col2:
    pass

# ── Fetch info ────────────────────────────────────────────────────────────────
if fetch_btn:
    if not url.strip():
        st.warning("Por favor, insira uma URL.")
    else:
        with st.spinner("Buscando informações do vídeo..."):
            try:
                ydl_opts = {"quiet": True, "no_warnings": True, "skip_download": True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    st.session_state.video_info = {
                        "title": info.get("title", "N/A"),
                        "channel": info.get("uploader", "N/A"),
                        "duration": info.get("duration_string", "N/A"),
                        "thumbnail": info.get("thumbnail", ""),
                        "url": url,
                    }
                    st.session_state.file_bytes = None
                    st.session_state.file_name = None
            except Exception as e:
                st.error(f"Erro ao buscar informações: {e}")

# ── Show info ─────────────────────────────────────────────────────────────────
if st.session_state.video_info:
    info = st.session_state.video_info

    if info["thumbnail"]:
        st.markdown('<div class="thumb-container">', unsafe_allow_html=True)
        st.image(info["thumbnail"], use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-card">
        <strong>Título:</strong> {info['title']}<br>
        <strong>Canal:</strong> {info['channel']}<br>
        <strong>Duração:</strong> {info['duration']}
    </div>
    """, unsafe_allow_html=True)

    dl_btn = st.button("⬇ Baixar vídeo (até 720p)", use_container_width=True)

    if dl_btn:
        progress_bar = st.progress(0, text="Iniciando download…")
        status_text = st.empty()

        def progress_hook(d):
            if d["status"] == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
                downloaded = d.get("downloaded_bytes", 0)
                if total:
                    pct = int(downloaded / total * 90)
                    speed = d.get("_speed_str", "")
                    eta = d.get("_eta_str", "")
                    progress_bar.progress(pct, text=f"Baixando… {pct}%  |  {speed}  |  ETA {eta}")
            elif d["status"] == "finished":
                progress_bar.progress(95, text="Processando arquivo…")

        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts = {
                "format": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best[height<=720]/best",
                "outtmpl": os.path.join(tmpdir, "%(title)s.%(ext)s"),
                "merge_output_format": "mp4",
                "progress_hooks": [progress_hook],
                "quiet": True,
                "no_warnings": True,
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([info["url"]])

                files = glob.glob(os.path.join(tmpdir, "*"))
                if not files:
                    raise FileNotFoundError("Nenhum arquivo foi gerado.")

                out_file = files[0]
                with open(out_file, "rb") as f:
                    st.session_state.file_bytes = f.read()
                st.session_state.file_name = os.path.basename(out_file)

                progress_bar.progress(100, text="Concluído!")
                status_text.success("✅ Download concluído! Clique no botão abaixo para salvar.")

            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"Erro durante o download: {e}")

# ── Download button ───────────────────────────────────────────────────────────
if st.session_state.file_bytes and st.session_state.file_name:
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.download_button(
        label=f"💾 Salvar  —  {st.session_state.file_name}",
        data=st.session_state.file_bytes,
        file_name=st.session_state.file_name,
        mime="video/mp4",
        use_container_width=True,
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown(
    '<p style="color:#444; font-size:0.72rem; text-align:center; letter-spacing:1px;">'
    'POWERED BY YT-DLP · USO PESSOAL APENAS</p>',
    unsafe_allow_html=True,
)
