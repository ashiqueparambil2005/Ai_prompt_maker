import streamlit as st
import google.generativeai as genai
from google import genai as genai_client
from PIL import Image
import time
from datetime import datetime
import json
import io

# --- Page Configuration ---
st.set_page_config(
    page_title="Ultra Studio V12 Pro",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Ultra Modern CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Manrope:wght@400;500;600;700;800&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Inter', sans-serif;
    }
    
    /* === LOGIN PAGE === */
    .login-container {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    .login-box {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 32px;
        padding: 3rem 2.5rem;
        max-width: 480px;
        width: 100%;
        box-shadow: 0 30px 90px rgba(0, 0, 0, 0.2);
        animation: slideUp 0.5s ease-out;
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .login-logo {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-logo-icon {
        font-size: 4em;
        margin-bottom: 1rem;
        display: inline-block;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .login-title {
        font-size: 2.5em;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        font-family: 'Manrope', sans-serif;
    }
    
    .login-subtitle {
        color: #64748b;
        font-size: 1.1em;
        margin-bottom: 2rem;
    }
    
    /* === MAIN APP === */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .main {
        padding: 0;
        max-width: 100%;
    }
    
    /* === NAVBAR === */
    .navbar {
        background: white;
        padding: 1rem 3rem;
        box-shadow: 0 2px 20px rgba(0, 0, 0, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 1000;
        margin-bottom: 2rem;
    }
    
    .navbar-brand {
        font-size: 1.8em;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Manrope', sans-serif;
    }
    
    .navbar-stats {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.5em;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 0.85em;
        color: #64748b;
        margin-top: 0.2rem;
    }
    
    /* === HERO SECTION === */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 32px;
        padding: 4rem 3rem;
        margin: 0 3rem 3rem 3rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .hero-title {
        font-size: 3.5em;
        font-weight: 900;
        color: white;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
        font-family: 'Manrope', sans-serif;
    }
    
    .hero-subtitle {
        font-size: 1.3em;
        color: rgba(255, 255, 255, 0.95);
        margin-bottom: 2rem;
        position: relative;
        z-index: 1;
    }
    
    .hero-features {
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin-top: 2rem;
        position: relative;
        z-index: 1;
    }
    
    .hero-feature {
        color: white;
        font-size: 1.1em;
    }
    
    .hero-feature-icon {
        font-size: 2em;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    /* === TABS === */
    .stTabs {
        background: white;
        border-radius: 24px;
        padding: 2rem;
        margin: 0 3rem 3rem 3rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.08);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: #f8f9fa;
        border-radius: 16px;
        padding: 0.5rem;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px !important;
        padding: 1rem 2rem !important;
        font-weight: 600 !important;
        color: #64748b !important;
        border: none !important;
        font-size: 1.05em !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* === CARDS === */
    .feature-card {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        border: 2px solid #f1f5f9;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.15);
        border-color: #667eea;
    }
    
    /* === INPUT FIELDS === */
    .stTextArea textarea, .stTextInput input {
        border-radius: 16px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }
    
    /* === BUTTONS === */
    .stButton button {
        border-radius: 14px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.05em !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15) !important;
    }
    
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    .stButton button[kind="secondary"] {
        background: white !important;
        border: 2px solid #e2e8f0 !important;
        color: #475569 !important;
    }
    
    /* === SELECT BOXES === */
    .stSelectbox > div > div {
        border-radius: 14px !important;
        border: 2px solid #e2e8f0 !important;
    }
    
    /* === FILE UPLOADER === */
    [data-testid="stFileUploader"] {
        border-radius: 20px !important;
        border: 3px dashed #cbd5e1 !important;
        padding: 2rem !important;
        background: #f8f9fa !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #667eea !important;
        background: white !important;
    }
    
    /* === PROGRESS BAR === */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 10px !important;
    }
    
    /* === ALERTS === */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 16px !important;
        padding: 1.2rem !important;
        border-left: 4px solid !important;
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* === EXPANDER === */
    .streamlit-expanderHeader {
        border-radius: 14px !important;
        background: white !important;
        font-weight: 600 !important;
        padding: 1.2rem !important;
        border: 2px solid #e2e8f0 !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #667eea !important;
        background: #f8f9ff !important;
    }
    
    /* === LOGOUT BUTTON === */
    .logout-btn {
        background: white !important;
        border: 2px solid #fee2e2 !important;
        color: #dc2626 !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .logout-btn:hover {
        background: #fee2e2 !important;
        transform: scale(1.05);
    }
    
    /* === HIDE DEFAULTS === */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    
    /* === RESPONSIVE === */
    @media (max-width: 768px) {
        .hero-title { font-size: 2em; }
        .navbar { padding: 1rem; }
        .stTabs { margin: 0 1rem 1rem 1rem; }
        .hero-section { margin: 0 1rem 1rem 1rem; padding: 2rem 1.5rem; }
        .hero-features { flex-direction: column; gap: 1rem; }
    }
    </style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'generated_prompts' not in st.session_state:
    st.session_state.generated_prompts = []
if 'api_calls_count' not in st.session_state:
    st.session_state.api_calls_count = 0
if 'img_description' not in st.session_state:
    st.session_state.img_description = ''
if 'last_image_gen_time' not in st.session_state:
    st.session_state.last_image_gen_time = 0

# --- Helper Functions ---
def safe_generate(prompt, model):
    """Safe API call with error handling"""
    # Check if demo mode
    if model is None:
        return "🎮 **Demo Mode Active**\n\nThis is a preview of what the AI would generate. To use real AI features, please:\n1. Logout\n2. Get a free API key from ai.google.dev\n3. Login with your API key\n\n[Sample output would appear here]"
    
    try:
        response = model.generate_content(prompt)
        st.session_state.api_calls_count += 1
        return response.text.strip()
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "ResourceExhausted" in error_msg:
            return "⏳ Rate limit reached. Please wait 60 seconds."
        elif "quota" in error_msg.lower():
            return "💳 API quota exceeded."
        elif "invalid" in error_msg.lower():
            return "🔑 Invalid API key."
        else:
            return f"⚠️ Error: {error_msg}"

def analyze_image(image_file, model):
    """Analyze uploaded image"""
    # Check if demo mode
    if model is None:
        return "🎮 **Demo Mode** - Image analysis not available. Login with API key to use this feature."
    
    try:
        img = Image.open(image_file)
        if max(img.size) > 1024:
            img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
        
        prompt = """Analyze this image for AI video generation. Describe:
        1. Physical appearance (face, features, expressions)
        2. Hair (style, color, length)
        3. Clothing and accessories
        4. Age range and gender
        5. Overall style and vibe
        
        Be specific and concise for AI prompts."""
        
        response = model.generate_content([prompt, img])
        st.session_state.api_calls_count += 1
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Analysis failed: {str(e)}"

def split_dialogue(text, max_words=15):
    """Split dialogue into clips"""
    if not text:
        return []
    
    sentences = text.replace('!', '.').replace('?', '.').split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    
    clips = []
    current = []
    word_count = 0
    
    for sentence in sentences:
        words = sentence.split()
        
        if len(words) > max_words:
            if current:
                clips.append(" ".join(current))
                current = []
                word_count = 0
            
            for i in range(0, len(words), max_words):
                clips.append(" ".join(words[i:i+max_words]))
        else:
            if word_count + len(words) > max_words:
                clips.append(" ".join(current))
                current = [sentence]
                word_count = len(words)
            else:
                current.append(sentence)
                word_count += len(words)
    
    if current:
        clips.append(" ".join(current))
    
    return clips

def generate_image_ai(prompt, api_key, number_of_images=1):
    """Generate images using Imagen 4.0 model"""
    try:
        # Create client with API key
        client = genai_client.Client(api_key=api_key)
        
        # Add a small delay to avoid rate limiting
        time.sleep(2)
        
        # Generate images using Imagen 4.0
        from google.genai import types
        
        response = client.models.generate_images(
            model='imagen-4.0-generate-001',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=number_of_images,
            )
        )
        
        # Extract all generated images
        if response.generated_images and len(response.generated_images) > 0:
            images = [img.image for img in response.generated_images]
            st.session_state.api_calls_count += 1
            return images, None
        
        return None, "No images generated in response"
        
    except Exception as e:
        error_msg = str(e)
        
        # Detailed error logging for debugging
        print(f"Full error: {error_msg}")
        
        if "429" in error_msg or "ResourceExhausted" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            return None, "⏳ Rate limit. Wait 60 seconds and try again."
        elif "quota" in error_msg.lower() or "QUOTA" in error_msg:
            return None, "💳 API quota exceeded. Check your quota at ai.google.dev"
        elif "invalid" in error_msg.lower() or "API_KEY_INVALID" in error_msg:
            return None, "🔑 Invalid API key for image generation."
        elif "not found" in error_msg.lower() or "NOT_FOUND" in error_msg:
            return None, "⚠️ Model 'imagen-4.0-generate-001' not found. Make sure it's enabled for your API key."
        elif "permission" in error_msg.lower() or "PERMISSION_DENIED" in error_msg:
            return None, "🚫 No permission to use Imagen. Check API settings."
        elif "FAILED_PRECONDITION" in error_msg:
            return None, "⚠️ Imagen 4.0 not available in your region yet. Try again later."
        else:
            return None, f"⚠️ Error: {error_msg}"

# --- LOGIN PAGE ---
if not st.session_state.logged_in:
    st.markdown("""
    <div class="login-container">
        <div class="login-box">
            <div class="login-logo">
                <div class="login-logo-icon">✨</div>
                <h1 class="login-title">Ultra Studio</h1>
                <p class="login-subtitle">Professional AI Content Creation</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form in the center
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            api_key_input = st.text_input(
                "Gemini API Key",
                type="password",
                placeholder="Enter your API key...",
                help="Get your free API key from ai.google.dev"
            )
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                login_button = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
            
            if login_button:
                if api_key_input.strip():
                    with st.spinner("🔍 Validating API key..."):
                        try:
                            # Test API key with a simple request
                            genai.configure(api_key=api_key_input)
                            test_model = genai.GenerativeModel('gemini-3-flash-preview')
                            
                            # Make a minimal test request
                            response = test_model.generate_content("Hi")
                            
                            # If we got here, the API key works
                            st.session_state.logged_in = True
                            st.session_state.api_key = api_key_input
                            st.success("✅ Login successful! Redirecting...")
                            time.sleep(1.5)
                            st.rerun()
                            
                        except Exception as e:
                            error_msg = str(e)
                            if "API_KEY_INVALID" in error_msg or "invalid" in error_msg.lower():
                                st.error("❌ Invalid API key. Please verify your key from ai.google.dev")
                            elif "quota" in error_msg.lower():
                                st.error("❌ API quota exceeded. Please check your quota limits.")
                            elif "permission" in error_msg.lower():
                                st.error("❌ API key doesn't have required permissions.")
                            else:
                                st.error(f"❌ Connection failed: {error_msg}")
                            
                            st.info("💡 Make sure your API key is active at https://ai.google.dev")
                else:
                    st.warning("⚠️ Please enter your API key")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("**Don't have an API key?**")
        if st.button("🎮 Try Demo Mode", use_container_width=False, help="Explore the interface without API key"):
            st.session_state.logged_in = True
            st.session_state.api_key = "DEMO_MODE"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.expander("📖 How to get your API key", expanded=False):
            st.markdown("""
            **Quick Setup (30 seconds):**
            
            1. Visit [ai.google.dev](https://ai.google.dev)
            2. Sign in with Google account
            3. Click **"Get API Key"** in Gemini API
            4. Click **"Create API Key"**
            5. Copy your key
            6. Paste above and login
            
            **It's completely FREE!** 🎉
            """)
        
        with st.expander("❓ Troubleshooting", expanded=False):
            st.markdown("""
            **If login fails, check these:**
            
            ✅ API key is copied correctly (no extra spaces)
            
            ✅ API key is from [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
            
            ✅ Gemini API is enabled in your Google Cloud project
            
            ✅ You have internet connection
            
            ✅ Your API quota hasn't been exceeded
            
            **Still having issues?** The API key should look like:
            `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`
            """)
    
    st.stop()

# --- MAIN APPLICATION (After Login) ---

# Check if demo mode
is_demo = (st.session_state.api_key == "DEMO_MODE")

# Configure API (skip if demo mode)
if not is_demo:
    genai.configure(api_key=st.session_state.api_key)
    model = genai.GenerativeModel('gemini-3-flash-preview')
else:
    model = None
    # Show demo banner
    st.warning("🎮 **Demo Mode** - You're exploring the interface. Enter a real API key to use AI features.", icon="ℹ️")

# --- NAVBAR ---
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("""
    <div class="navbar">
        <div class="navbar-brand">✨ Ultra Studio V12 Pro</div>
        <div class="navbar-stats">
            <div class="stat-item">
                <div class="stat-value">{}</div>
                <div class="stat-label">API Calls</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{}</div>
                <div class="stat-label">Prompts</div>
            </div>
        </div>
    </div>
    """.format(st.session_state.api_calls_count, len(st.session_state.generated_prompts)), unsafe_allow_html=True)

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Logout", key="logout", help="Logout from Ultra Studio"):
        st.session_state.logged_in = False
        st.session_state.api_key = ""
        st.rerun()

# --- HERO SECTION ---
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">Transform Ideas into Reality</h1>
    <p class="hero-subtitle">Professional AI-powered content creation for videos, images, and viral content</p>
    <div class="hero-features">
        <div class="hero-feature">
            <span class="hero-feature-icon">📝</span>
            <div>Script Doctor</div>
        </div>
        <div class="hero-feature">
            <span class="hero-feature-icon">🎬</span>
            <div>Video Prompts</div>
        </div>
        <div class="hero-feature">
            <span class="hero-feature-icon">🎨</span>
            <div>AI Image Creator</div>
        </div>
        <div class="hero-feature">
            <span class="hero-feature-icon">🖼️</span>
            <div>Image Prompts</div>
        </div>
        <div class="hero-feature">
            <span class="hero-feature-icon">🚀</span>
            <div>Viral Content</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 Script Doctor",
    "🎬 Video Generator",
    "🎨 AI Image Creator",
    "🖼️ Image Prompts",
    "🚀 Viral Manager"
])

# === TAB 1: SCRIPT DOCTOR ===
with tab1:
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### 📥 Your Script")
        raw_script = st.text_area(
            "Enter your content",
            height=300,
            placeholder="Paste your script, ideas, or bullet points here...",
            key="script_input"
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            mode = st.selectbox(
                "Style",
                ["🎯 Viral Hook", "💼 Professional", "😂 Funny", "🎓 Educational", 
                 "💰 Sales", "🌏 Malayalam → English", "✨ Creative"]
            )
        
        with col_b:
            length = st.selectbox(
                "Length",
                ["Keep Original", "Make Shorter", "Make Longer", "Expand Dramatically"]
            )
        
        enhance_btn = st.button("✨ Enhance Script", type="primary", use_container_width=True, key="enhance")
    
    with col2:
        st.markdown("### ✨ Enhanced Result")
        
        if enhance_btn:
            if raw_script.strip():
                with st.spinner("🤖 Enhancing your script..."):
                    prompt = f"""Rewrite this script professionally:

Style: {mode}
Length: {length}
Input: {raw_script}

Requirements:
- Maintain core message
- Apply {mode} style
- {length}
- Professional quality
- Clear and engaging

Output enhanced script only."""
                    
                    result = safe_generate(prompt, model)
                    
                    if result and "Error" not in result:
                        st.success("✅ Script enhanced!")
                        st.text_area("Enhanced Script", value=result, height=300, key="enhanced_output")
                        
                        col_m1, col_m2 = st.columns(2)
                        with col_m1:
                            st.metric("Original Words", len(raw_script.split()))
                        with col_m2:
                            st.metric("Enhanced Words", len(result.split()))
                        
                        st.download_button(
                            "📥 Download",
                            data=result,
                            file_name=f"enhanced_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                            use_container_width=True
                        )
                    else:
                        st.error(result)
            else:
                st.warning("⚠️ Please enter content first")

# === TAB 2: VIDEO GENERATOR ===
with tab2:
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### 👤 Character Setup")
        
        uploaded_file = st.file_uploader(
            "Upload character image",
            type=["jpg", "jpeg", "png", "webp"],
            key="char_upload"
        )
        
        if uploaded_file:
            col_img, col_btn = st.columns([2, 1])
            with col_img:
                st.image(uploaded_file, use_container_width=True)
            with col_btn:
                if st.button("🔍 Analyze", use_container_width=True):
                    with st.spinner("Analyzing..."):
                        analysis = analyze_image(uploaded_file, model)
                        if "Error" not in analysis:
                            st.session_state.img_description = analysis
                            st.success("✅ Done!")
                        else:
                            st.error(analysis)
        
        img_desc = st.text_area(
            "Character description",
            value=st.session_state.img_description,
            height=150,
            placeholder="Describe the character appearance...",
            key="char_desc"
        )
        
        visual_style = st.selectbox(
            "Visual Style",
            ["🎯 Strict Realism", "🎬 Cinematic Movie", "🎪 Disney/Pixar 3D", 
             "🌃 Cyberpunk/Neon", "📼 Vintage Film", "🎨 Oil Painting"]
        )
        
        script = st.text_area(
            "Video Script",
            height=150,
            placeholder="Enter dialogue...",
            key="video_script"
        )
        
        max_words = st.slider("Words per clip", 8, 25, 15)
        
        if script:
            clips_preview = split_dialogue(script, max_words)
            st.info(f"📊 Will create {len(clips_preview)} clips")
        
        gen_btn = st.button("🚀 Generate Prompts", type="primary", use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Generated Prompts")
        
        if gen_btn:
            if img_desc.strip() and script.strip():
                clips = split_dialogue(script, max_words)
                
                progress = st.progress(0)
                st.success(f"✅ Generating {len(clips)} prompts...")
                
                for i, clip in enumerate(clips):
                    progress.progress((i + 1) / len(clips))
                    
                    style_name = visual_style.split(" ", 1)[1] if " " in visual_style else visual_style
                    
                    prompt = f"""Create professional video prompt for AI tools.

CLIP #{i+1}
CHARACTER: {img_desc}
DIALOGUE: "{clip}"
STYLE: {style_name}

Include:
- Character description
- Dialogue delivery
- Facial expressions
- Camera work
- Lighting
- Style elements

Production-ready format."""
                    
                    result = safe_generate(prompt, model)
                    
                    with st.expander(f"🎬 Clip {i+1}", expanded=(i==0)):
                        if "Error" not in result:
                            st.code(result, language="text")
                            st.download_button(
                                "💾 Download",
                                data=result,
                                file_name=f"clip_{i+1}.txt",
                                key=f"dl_{i}"
                            )
                        else:
                            st.warning(result)
                    
                    if i < len(clips) - 1:
                        time.sleep(1)
                
                st.success("✅ All prompts generated!")
            else:
                st.error("⚠️ Please provide character description and script")

# === TAB 3: AI IMAGE CREATOR ===
with tab3:
    st.markdown("### 🎨 AI Image Creator")
    
    if is_demo:
        st.info("🎮 **Demo Mode** - Image generation requires a real API key. Please login to use this feature.")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("#### 💭 Describe Your Image")
        
        image_prompt = st.text_area(
            "What do you want to create?",
            height=200,
            placeholder="Example: A cute cat wearing sunglasses sitting on a beach during sunset, photorealistic style, 4K quality",
            help="Be detailed and specific for best results",
            key="ai_image_prompt"
        )
        
        col_style, col_quality = st.columns(2)
        
        with col_style:
            art_style = st.selectbox(
                "Art Style",
                [
                    "Photorealistic",
                    "Digital Art",
                    "Oil Painting",
                    "Anime/Manga",
                    "3D Render",
                    "Watercolor",
                    "Pencil Sketch",
                    "Cyberpunk",
                    "Fantasy Art"
                ],
                key="art_style_select"
            )
        
        with col_quality:
            quality = st.selectbox(
                "Quality",
                ["Standard", "High Quality", "Ultra HD 4K"],
                index=1,
                key="quality_select"
            )
        
        # Aspect ratio
        aspect_ratio = st.selectbox(
            "Aspect Ratio",
            ["1:1 Square", "16:9 Landscape", "9:16 Portrait", "4:3 Classic", "3:2 Photo"],
            key="aspect_select"
        )
        
        # Number of images
        num_images = st.selectbox(
            "Number of Images",
            [1, 2, 3, 4],
            index=0,
            help="Generate multiple variations at once",
            key="num_images_select"
        )
        
        # Additional options
        with st.expander("⚙️ Advanced Options", expanded=False):
            mood = st.selectbox(
                "Mood/Atmosphere",
                ["Natural", "Dramatic", "Cheerful", "Dark/Moody", "Dreamy", "Vibrant"],
                key="mood_select"
            )
            
            lighting = st.selectbox(
                "Lighting",
                ["Natural", "Golden Hour", "Studio", "Neon", "Dramatic", "Soft"],
                key="lighting_select"
            )
            
            add_details = st.text_input(
                "Additional Details (optional)",
                placeholder="e.g., bokeh effect, lens flare, HDR...",
                key="add_details_input"
            )
        
        generate_img_btn = st.button(
            "🎨 Generate Image",
            type="primary",
            use_container_width=True,
            disabled=is_demo,
            key="generate_image_btn"
        )
        
        # Show cooldown timer if needed
        current_time = time.time()
        time_since_last = current_time - st.session_state.last_image_gen_time
        cooldown_time = 3  # 3 seconds cooldown
        
        if time_since_last < cooldown_time:
            remaining = int(cooldown_time - time_since_last)
            st.info(f"⏰ Please wait {remaining} seconds before generating again...")
    
    with col2:
        st.markdown("#### 🖼️ Generated Image")
        
        if generate_img_btn:
            # Check cooldown
            current_time = time.time()
            time_since_last = current_time - st.session_state.last_image_gen_time
            
            if time_since_last < 3:
                st.warning(f"⏰ Please wait {int(3 - time_since_last)} more seconds...")
            elif image_prompt.strip():
                # Build enhanced prompt
                enhanced_prompt = f"{image_prompt}"
                
                if art_style != "Photorealistic":
                    enhanced_prompt += f", {art_style} style"
                
                enhanced_prompt += f", {aspect_ratio.split()[0]} aspect ratio"
                
                if quality == "High Quality":
                    enhanced_prompt += ", high quality, detailed"
                elif quality == "Ultra HD 4K":
                    enhanced_prompt += ", ultra HD 4K, extremely detailed, professional"
                
                if mood != "Natural":
                    enhanced_prompt += f", {mood.lower()} atmosphere"
                
                if lighting != "Natural":
                    enhanced_prompt += f", {lighting.lower()} lighting"
                
                if add_details:
                    enhanced_prompt += f", {add_details}"
                
                # Show what we're generating
                with st.expander("📋 Full Prompt Being Used", expanded=False):
                    st.code(enhanced_prompt, language="text")
                
                # Generate image
                st.session_state.last_image_gen_time = time.time()
                
                with st.spinner(f"🎨 Creating {num_images} image(s)... This may take 10-30 seconds..."):
                    generated_images, error = generate_image_ai(enhanced_prompt, st.session_state.api_key, num_images)
                    
                    if generated_images:
                        st.success(f"✅ {len(generated_images)} image(s) generated successfully!")
                        
                        # Display all images
                        if len(generated_images) == 1:
                            st.image(generated_images[0], use_container_width=True, caption="Generated Image")
                            
                            # Save to bytes for download
                            img_bytes = io.BytesIO()
                            generated_images[0].save(img_bytes, format='PNG')
                            img_bytes.seek(0)
                            
                            # Download button
                            st.download_button(
                                "📥 Download Image",
                                data=img_bytes,
                                file_name=f"ai_generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                                mime="image/png",
                                use_container_width=True
                            )
                        else:
                            # Display multiple images in grid
                            cols = st.columns(2)
                            for idx, img in enumerate(generated_images):
                                with cols[idx % 2]:
                                    st.image(img, use_container_width=True, caption=f"Variation {idx + 1}")
                                    
                                    # Individual download button
                                    img_bytes = io.BytesIO()
                                    img.save(img_bytes, format='PNG')
                                    img_bytes.seek(0)
                                    
                                    st.download_button(
                                        f"📥 Download #{idx + 1}",
                                        data=img_bytes,
                                        file_name=f"ai_generated_{idx+1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                                        mime="image/png",
                                        use_container_width=True,
                                        key=f"download_{idx}"
                                    )
                        
                        # Option to regenerate
                        st.markdown("---")
                        if st.button("🔄 Generate More", use_container_width=True):
                            st.rerun()
                        
                    else:
                        st.error(f"❌ {error}")
                        
                        # Detailed troubleshooting based on error
                        if "Rate limit" in error or "quota" in error.lower():
                            st.warning("""
                            **Rate Limit Solutions:**
                            
                            ⏰ **Wait 60 seconds** and try again
                            
                            📊 Check your usage at [Google AI Studio](https://aistudio.google.com/apikey)
                            
                            💡 Free tier has limits - upgrade if needed
                            """)
                        
                        elif "not found" in error.lower() or "not available" in error.lower():
                            st.info("""
                            **Model Access Issue:**
                            
                            The `imagen-4.0-generate-001` model may not be available yet.
                            
                            ✅ Check model availability at [ai.google.dev](https://ai.google.dev)
                            
                            ✅ Make sure your API key has Imagen access enabled
                            
                            ✅ Model might be in limited preview - try again later
                            """)
                        
                        elif "permission" in error.lower():
                            st.info("""
                            **Permission Issue:**
                            
                            Your API key might not have permission for image generation.
                            
                            ✅ Visit [Google AI Studio](https://aistudio.google.com)
                            
                            ✅ Check if image generation is enabled for your project
                            
                            ✅ You may need to enable additional APIs
                            """)
                        
                        # Show raw error in expander
                        with st.expander("🔧 Technical Details"):
                            st.code(error, language="text")
            else:
                st.warning("⚠️ Please describe what you want to create")
        else:
            # Placeholder
            st.markdown("""
            <div style='background: #f8f9fa; padding: 3rem 2rem; border-radius: 14px; text-align: center;'>
                <div style='font-size: 4em; margin-bottom: 1rem;'>🎨</div>
                <p style='color: #64748b; margin: 0; font-size: 1.1em;'>
                    Describe your image and click<br>
                    <strong>Generate Image</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Example prompts
            st.markdown("---")
            st.markdown("**💡 Example Prompts:**")
            
            examples = [
                "🏔️ Mountain landscape at sunrise with clouds",
                "🤖 Futuristic robot in cyberpunk city",
                "🐱 Cute kitten playing with yarn ball",
                "🌸 Beautiful garden with cherry blossoms",
                "🚀 Spaceship traveling through galaxy"
            ]
            
            for example in examples:
                if st.button(example, key=f"ex_{example}", use_container_width=True):
                    st.session_state.ai_image_prompt = example.split(" ", 1)[1]
                    st.rerun()

# === TAB 4: IMAGE PROMPTS ===
with tab4:
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### 💭 Your Vision")
        
        idea = st.text_area(
            "Describe your image",
            height=250,
            placeholder="Example: A futuristic city at sunset...",
            key="image_idea"
        )
        
        col_ar, col_det = st.columns(2)
        with col_ar:
            aspect = st.selectbox(
                "Aspect Ratio",
                ["1:1 Square", "16:9 Landscape", "9:16 Portrait", "4:3 Classic"]
            )
        
        with col_det:
            detail = st.selectbox(
                "Detail Level",
                ["High Detail", "Medium Detail", "Simple/Minimalist"]
            )
        
        img_style = st.selectbox(
            "Visual Style",
            ["🎯 Photorealistic", "🎨 Digital Art", "🖼️ Oil Painting", "✨ Anime/Manga"]
        )
        
        create_btn = st.button("✨ Create Prompt", type="primary", use_container_width=True)
    
    with col2:
        st.markdown("### 🎨 Generated Prompt")
        
        if create_btn:
            if idea.strip():
                with st.spinner("🤖 Creating prompt..."):
                    prompt = f"""Create professional image generation prompt:

Vision: {idea}
Style: {img_style}
Aspect: {aspect}
Detail: {detail}

Include:
- Main subject
- Composition
- Lighting
- Color palette
- Technical specs
- Style keywords

Format for Midjourney/DALL-E/Stable Diffusion"""
                    
                    result = safe_generate(prompt, model)
                    
                    if result and "Error" not in result:
                        st.success("✅ Prompt created!")
                        st.code(result, language="text")
                        
                        st.download_button(
                            "📥 Download Prompt",
                            data=result,
                            file_name=f"image_prompt_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                            use_container_width=True
                        )
                    else:
                        st.error(result)
            else:
                st.warning("⚠️ Please describe your image idea")

# === TAB 5: VIRAL MANAGER ===
with tab5:
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### 📋 Content Details")
        
        topic = st.text_input(
            "Topic",
            placeholder="Example: How to make perfect coffee",
            key="viral_topic"
        )
        
        platform = st.multiselect(
            "Platforms",
            ["YouTube", "Instagram", "TikTok", "Twitter/X", "LinkedIn"],
            default=["YouTube"]
        )
        
        audience = st.selectbox(
            "Target Audience",
            ["General Public", "Young Adults (18-25)", "Professionals", 
             "Tech Enthusiasts", "Entrepreneurs"]
        )
        
        tone = st.selectbox(
            "Content Tone",
            ["Exciting/Energetic", "Educational", "Funny", "Inspirational", "Professional"]
        )
        
        viral_btn = st.button("🚀 Generate Strategy", type="primary", use_container_width=True)
    
    with col2:
        st.markdown("### 💎 Viral Package")
        
        if viral_btn:
            if topic.strip():
                with st.spinner("🤖 Creating strategy..."):
                    prompt = f"""Create viral content strategy:

Topic: {topic}
Platforms: {', '.join(platform)}
Audience: {audience}
Tone: {tone}

Generate:
1. 5 Viral Titles
2. SEO Description
3. 30 Hashtags
4. Call-to-Action options
5. Hook Ideas
6. Platform tips

Professional format."""
                    
                    result = safe_generate(prompt, model)
                    
                    if result and "Error" not in result:
                        st.success("✅ Strategy generated!")
                        st.markdown(result)
                        
                        st.download_button(
                            "📥 Download Strategy",
                            data=result,
                            file_name=f"viral_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                            use_container_width=True
                        )
                    else:
                        st.error(result)
            else:
                st.warning("⚠️ Please enter a topic")

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 2rem; background: white; border-radius: 20px; 
            margin: 0 3rem; box-shadow: 0 4px 20px rgba(0,0,0,0.08);'>
    <h3 style='color: #667eea; margin-bottom: 0.5rem; font-family: "Manrope", sans-serif;'>
        Ultra Studio V12 Pro
    </h3>
    <p style='color: #64748b; margin: 0;'>
        Professional AI Content Creation Platform
    </p>
    <p style='color: #94a3b8; font-size: 0.9em; margin-top: 0.5rem;'>
        Powered by Google Gemini AI ✨
    </p>
</div>
""", unsafe_allow_html=True)