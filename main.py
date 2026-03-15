# main.py - KIMI K2.5 COMPLETO - TODO EN UNO
# API KEY INCLUIDA: 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

import streamlit as st
from openai import OpenAI
import time
import json
import base64
import zipfile
import io
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

st.set_page_config(
    page_title="🏆 KIMI K2.5 PREMIUM",
    page_icon="🚀",
    layout="centered"
)

# ============================================================================
# ÍCONO DE KIMI AI
# ============================================================================

KIMI_ICON_SVG = '''<svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="50" cy="50" r="45" fill="url(#paint0_linear)"/>
<path d="M30 35H70V45H30V35Z" fill="white"/>
<path d="M30 55H60V65H30V55Z" fill="white"/>
<path d="M40 45H60V55H40V45Z" fill="white"/>
<defs>
<linearGradient id="paint0_linear" x1="5" y1="5" x2="95" y2="95" gradientUnits="userSpaceOnUse">
<stop stop-color="#667EEA"/>
<stop offset="1" stop-color="#764BA2"/>
</linearGradient>
</defs>
</svg>'''

KIMI_ICON_BASE64 = base64.b64encode(KIMI_ICON_SVG.encode()).decode()

# ============================================================================
# CSS PERSONALIZADO
# ============================================================================

st.markdown(f"""
<style>
    .main-header {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }}
    .kimi-icon {{
        display: inline-block;
        width: 48px;
        height: 48px;
        background: url('data:image/svg+xml;base64,{KIMI_ICON_BASE64}') no-repeat;
        background-size: contain;
        margin-right: 10px;
        vertical-align: middle;
        animation: float 3s ease-in-out infinite;
    }}
    @keyframes float {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-5px); }}
        100% {{ transform: translateY(0px); }}
    }}
    .stButton > button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 30px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        border: none;
        width: 100%;
        margin: 0.5rem 0;
    }}
    .stButton > button:hover {{
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(102,126,234,0.4);
    }}
    .stTextInput > div > div > input {{
        border-radius: 30px;
        padding: 0.5rem 1rem;
    }}
    div[data-testid="stChatInput"] textarea {{
        border-radius: 30px;
        padding: 0.5rem 1rem;
    }}
    .footer {{
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        margin-top: 2rem;
        font-size: 0.8rem;
    }}
    .generator-box {{
        background: linear-gradient(135deg, #f6f9fc 0%, #e9f2f9 100%);
        padding: 1.5rem;
        border-radius: 20px;
        border: 2px solid #667eea;
        margin: 1rem 0;
    }}
    .success-box {{
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }}
    .info-box {{
        background: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #17a2b8;
        margin: 1rem 0;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# TU API KEY DE NVIDIA
# ============================================================================

NVIDIA_API_KEY = "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"

# ============================================================================
# CLASE PARA CHAT CON KIMI
# ============================================================================

class KimiChat:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=NVIDIA_API_KEY
        )
        self.model = "moonshotai/kimi-k2-instruct-0905"
        self.total_queries = 0
    
    def chat(self, message, temperature=0.7):
        self.total_queries += 1
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": message}],
                temperature=temperature,
                max_tokens=1024
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

# ============================================================================
# CLASE PARA GENERAR ZIP
# ============================================================================

class ZipGenerator:
    def generar_zip_basico(self):
        """Genera ZIP básico para ejecutar en PC"""
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            zip_file.writestr('kimi_app.py', f'''# Kimi K2.5 - App Básica
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Kimi K2.5", page_icon="🚀")
st.title("🚀 Kimi K2.5")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="{NVIDIA_API_KEY}"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Escribe aquí..."):
    st.session_state.messages.append({{"role": "user", "content": prompt}})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        response = st.empty()
        full = ""
        completion = client.chat.completions.create(
            model="moonshotai/kimi-k2-instruct-0905",
            messages=[{{"role": m["role"], "content": m["content"]}} for m in st.session_state.messages[-6:]],
            stream=True
        )
        for chunk in completion:
            if chunk.choices[0].delta.content:
                full += chunk.choices[0].delta.content
                response.markdown(full + "▌")
            time.sleep(0.01)
        response.markdown(full)
        st.session_state.messages.append({{"role": "assistant", "content": full}})
''')
            zip_file.writestr('requirements.txt', 'streamlit==1.28.1\nopenai==1.6.1\n')
            zip_file.writestr('README.txt', 'KIMI K2.5 BÁSICO\nPara ejecutar: streamlit run kimi_app.py')
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    
    def generar_zip_completo(self):
        """Genera ZIP completo para compilar APK"""
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            # main.py
            zip_file.writestr('main.py', f'''# Kimi K2.5 - App Completa
import streamlit as st
from openai import OpenAI
import time

st.set_page_config(page_title="Kimi K2.5", page_icon="🚀", layout="centered")
st.title("🚀 Kimi K2.5 Premium")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="{NVIDIA_API_KEY}"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Escribe tu mensaje..."):
    st.session_state.messages.append({{"role": "user", "content": prompt}})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        response = st.empty()
        full = ""
        completion = client.chat.completions.create(
            model="moonshotai/kimi-k2-instruct-0905",
            messages=[{{"role": m["role"], "content": m["content"]}} for m in st.session_state.messages[-6:]],
            stream=True
        )
        for chunk in completion:
            if chunk.choices[0].delta.content:
                full += chunk.choices[0].delta.content
                response.markdown(full + "▌")
            time.sleep(0.01)
        response.markdown(full)
        st.session_state.messages.append({{"role": "assistant", "content": full}})
''')
            # requirements.txt
            zip_file.writestr('requirements.txt', 'streamlit==1.28.1\nopenai==1.6.1\nrequests==2.31.0\nPillow==10.1.0\n')
            # buildozer.spec
            zip_file.writestr('buildozer.spec', '''[app]
title = Kimi AI Premium
package.name = kimiapp
package.domain = com.kimiapp.android
version = 1.0.0
requirements = python3,streamlit,openai,requests,Pillow
orientation = portrait
android.permissions = INTERNET
android.api = 30
android.minapi = 21
android.targetapi = 30
android.ndk = 23b

[buildozer]
log_level = 2
warn_on_root = 1
''')
            # README
            zip_file.writestr('README.txt', f'''KIMI K2.5 PREMIUM - APK GENERATOR

INSTRUCCIONES:
1. pip install buildozer cython
2. buildozer -v android debug
3. El APK estará en bin/

API Key: {NVIDIA_API_KEY}
''')
        zip_buffer.seek(0)
        return zip_buffer.getvalue()

# ============================================================================
# INICIALIZACIÓN DE SESIÓN
# ============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "kimi" not in st.session_state:
    st.session_state.kimi = KimiChat()
    
if "zip_gen" not in st.session_state:
    st.session_state.zip_gen = ZipGenerator()

# ============================================================================
# HEADER
# ============================================================================

st.markdown(f"""
<div class="main-header">
    <div style="display: flex; align-items: center; justify-content: center;">
        <div class="kimi-icon"></div>
        <h1 style="font-size: 2rem;">KIMI K2.5 PREMIUM</h1>
    </div>
    <p style="margin-top: 0.5rem;">Chat + Generador de ZIP/APK • API Key incluida</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# PESTAÑAS
# ============================================================================

tab1, tab2, tab3 = st.tabs(["💬 CHAT", "📦 GENERAR ZIP", "📱 GENERAR APK"])

# ============================================================================
# PESTAÑA 1: CHAT
# ============================================================================

with tab1:
    # Mostrar mensajes
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Input del usuario
    if prompt := st.chat_input("Escribe tu mensaje aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = st.session_state.kimi.chat(prompt)
                st.write(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Estadísticas
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Consultas realizadas", st.session_state.kimi.total_queries)
    with col2:
        st.metric("Mensajes en chat", len(st.session_state.messages))

# ============================================================================
# PESTAÑA 2: GENERADOR ZIP
# ============================================================================

with tab2:
    st.markdown("""
    <div class="generator-box">
        <h3>📦 GENERADOR DE ARCHIVOS ZIP</h3>
        <p>Selecciona el tipo de ZIP que necesitas:</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 ZIP BÁSICO")
        st.markdown("Para ejecutar en PC (código simple)")
        if st.button("📥 GENERAR BÁSICO", key="btn_basic", use_container_width=True):
            with st.spinner("Generando ZIP básico..."):
                zip_data = st.session_state.zip_gen.generar_zip_basico()
                st.download_button(
                    label="⬇️ DESCARGAR KIMI_BASIC.ZIP",
                    data=zip_data,
                    file_name=f"kimi_basic_{datetime.now().strftime('%Y%m%d')}.zip",
                    mime="application/zip",
                    use_container_width=True
                )
    
    with col2:
        st.markdown("### 📦 ZIP COMPLETO")
        st.markdown("Para compilar APK (con todo incluido)")
        if st.button("📥 GENERAR COMPLETO", key="btn_complete", use_container_width=True):
            with st.spinner("Generando ZIP completo..."):
                zip_data = st.session_state.zip_gen.generar_zip_completo()
                st.download_button(
                    label="⬇️ DESCARGAR KIMI_FULL.ZIP",
                    data=zip_data,
                    file_name=f"kimi_full_{datetime.now().strftime('%Y%m%d')}.zip",
                    mime="application/zip",
                    use_container_width=True
                )
    
    with st.expander("📂 VER CONTENIDO DEL ZIP COMPLETO"):
        st.code("""
kimi_full.zip/
├── main.py              # App principal
├── requirements.txt     # Dependencias
├── buildozer.spec       # Configuración Android
└── README.txt           # Instrucciones
        """)

# ============================================================================
# PESTAÑA 3: GENERADOR APK
# ============================================================================

with tab3:
    st.markdown("""
    <div class="generator-box">
        <h3>📱 GENERADOR DE APK</h3>
        <p>Instrucciones para compilar tu APK desde Android</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>📋 INSTRUCCIONES PASO A PASO:</strong>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    **1️⃣ PRIMERO: Genera el ZIP completo**
    - Ve a la pestaña "GENERAR ZIP"
    - Haz clic en "GENERAR COMPLETO"
    - Descarga el archivo ZIP
    
    **2️⃣ SEGUNDO: Prepara Termux**
    ```bash
    pkg update && pkg upgrade -y
    pkg install -y python python-pip git nano openjdk-17 gradle
    pip install buildozer cython
    ```
    
    **3️⃣ TERCERO: Descomprime y compila**
    ```bash
    # Descomprimir el ZIP
    unzip kimi_full_*.zip -d ~/kimi-app
    cd ~/kimi-app
    
    # Compilar APK (20-30 minutos)
    buildozer -v android debug
    ```
    
    **4️⃣ CUARTO: Instala el APK**
    ```bash
    # El APK estará en:
    ls -la bin/
    
    # Copiar a Descargas
    cp bin/*.apk /storage/emulated/0/Download/
    ```
    """)
    
    st.markdown("""
    <div class="success-box">
        <strong>✅ IMPORTANTE:</strong> Tu API key ya está incluida en el código
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📋 COPIAR COMANDOS", use_container_width=True):
        st.code("""
pkg update && pkg upgrade -y
pkg install -y python python-pip git nano openjdk-17 gradle
pip install buildozer cython
cd ~/kimi-app
buildozer -v android debug
cp bin/*.apk /storage/emulated/0/Download/
        """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown(f"""
<div class="footer">
    <p><strong>KIMI K2.5 PREMIUM</strong> • Chat + ZIP + APK • Todo en uno</p>
    <p style="font-size:0.7rem;">API Key incluida: {NVIDIA_API_KEY[:20]}... | Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
</div>
""", unsafe_allow_html=True)
