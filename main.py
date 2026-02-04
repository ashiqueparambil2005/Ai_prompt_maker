import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
from datetime import datetime

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Ultra Studio V11 Pro",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Enhanced CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    
    .stTextArea textarea, .stTextInput input {
        border-radius: 12px;
        border: 2px solid #e0e7ff;
        padding: 12px;
        transition: all 0.3s ease;
    }
    
    .stButton button {
        border-radius: 12px;
        height: 3.5em;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] * { color: white !important; }
    
    .creator-card {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 15px;
        margin-top: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. Session State ---
if 'generated_prompts' not in st.session_state:
    st.session_state.generated_prompts = []
if 'api_calls_count' not in st.session_state:
    st.session_state.api_calls_count = 0
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'img_description' not in st.session_state:
    st.session_state.img_description = ""

# --- 4. Sidebar ---
with st.sidebar:
    st.markdown("# ⚙️ Control Panel")
    st.markdown("---")
    
    # API Key with persistence
    api_key = st.text_input(
        "🔑 Gemini API Key:", 
        value=st.session_state.api_key,
        type="password",
        help="Your API key is saved for this session"
    )
    
    if api_key:
        st.session_state.api_key = api_key
        st.success("✅ API Key Connected")
    else:
        st.warning("⚠️ API Key Required")
    
    st.markdown("---")
    
    st.markdown("### 🎨 Visual Style")
    visual_style = st.selectbox(
        "Output Style:",
        [
            "🎯 Strict Realism (Default)",
            "🎬 Cinematic Movie",
            "🎪 Disney/Pixar 3D",
            "🌃 Cyberpunk/Neon",
            "📼 Vintage Film Grain",
            "🎨 Oil Painting Art",
            "🌊 Dreamy Watercolor"
        ]
    )
    
    st.markdown("---")
    
    with st.expander("🔧 Advanced Settings"):
        max_words_per_clip = st.slider("Words per Clip:", 10, 30, 15)
        enable_auto_save = st.checkbox("Auto-save Prompts", value=True)
    
    st.markdown("---")
    
    st.markdown("### 📊 Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("API Calls", st.session_state.api_calls_count)
    with col2:
        st.metric("Prompts", len(st.session_state.generated_prompts))
    
    st.markdown("---")
    
    st.markdown("### ⚡ Quick Actions")
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.generated_prompts = []
        st.session_state.api_calls_count = 0
        st.rerun()
    
    if st.button("📥 Export All", use_container_width=True):
        if st.session_state.generated_prompts:
            export_text = "\n\n---\n\n".join(st.session_state.generated_prompts)
            st.download_button(
                "💾 Download",
                data=export_text,
                file_name=f"prompts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    st.markdown("---")
    
    # Creator Info
    st.markdown("""
    <div class="creator-card">
        <div style="text-align: center;">
            <h4 style="margin: 0 0 10px 0;">👨‍💻 Created By</h4>
            <p style="margin: 5px 0; font-weight: 600; font-size: 16px;">Ashique</p>
            <p style="margin: 5px 0; font-size: 14px; opacity: 0.9;">📧 ashiqueconnect@gmail.com</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. Setup ---
if not st.session_state.api_key:
    st.markdown("""
    <div style='text-align: center; padding: 60px 20px; background: white; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);'>
        <h1 style='color: #667eea; font-size: 3em; margin-bottom: 20px;'>✨ Ultra Studio V11 Pro</h1>
        <p style='font-size: 1.2em; color: #64748b; margin-bottom: 30px;'>
            The Ultimate AI Content Creation Platform
        </p>
        <p style='color: #f59e0b; font-size: 1.1em;'>⚠️ Please enter your Gemini API Key in the sidebar ←</p>
        <p style='color: #64748b; margin-top: 20px;'>Your API key will be saved for this session</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

try:
    genai.configure(api_key=st.session_state.api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-exp')
except Exception as e:
    st.error(f"❌ API Error: {str(e)}")
    st.info("💡 Get your API key: https://aistudio.google.com/apikey")
    st.stop()

# --- 6. Helper Functions ---
def safe_generate(prompt, show_spinner=True):
    try:
        if show_spinner:
            with st.spinner("🤖 AI is thinking..."):
                time.sleep(0.5)
                response = model.generate_content(prompt)
                st.session_state.api_calls_count += 1
                return response.text.strip()
        else:
            response = model.generate_content(prompt)
            st.session_state.api_calls_count += 1
            return response.text.strip()
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            return "⏳ Rate Limit - Wait 60 seconds"
        elif "quota" in error_msg.lower():
            return "💳 Quota Exceeded"
        else:
            return f"⚠️ Error: {error_msg}"

def analyze_image(image_file):
    try:
        img = Image.open(image_file)
        if max(img.size) > 1024:
            img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
        
        prompt = "Analyze this image for video generation. Describe: appearance, hair, clothing, age, notable features. Be concise."
        
        with st.spinner("🔍 Analyzing..."):
            response = model.generate_content([prompt, img])
            st.session_state.api_calls_count += 1
            return response.text.strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def generate_video_prompt(image_desc, dialogue, style, clip_number=1):
    style_name = style.split(" ", 1)[1] if " " in style else style
    
    prompt = f"""Create a professional AI video prompt for tools like Kling AI or Runway.

CHARACTER: {image_desc}
DIALOGUE: "{dialogue}"
STYLE: {style_name}

Include:
1. Character description and position
2. Exact dialogue to speak
3. Facial expressions matching emotion
4. Lip sync instructions
5. Camera setup and movement
6. Lighting and atmosphere
7. Style-specific elements

Make it production-ready."""
    
    result = safe_generate(prompt, show_spinner=False)
    
    if enable_auto_save and result and "Error" not in result:
        st.session_state.generated_prompts.append(f"Clip {clip_number}:\n{result}")
    
    return result

def split_dialogue(text, max_words=15):
    if not text:
        return []
    
    sentences = text.replace('!', '.').replace('?', '.').split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    
    clips = []
    current_clip = []
    current_word_count = 0
    
    for sentence in sentences:
        words = sentence.split()
        
        if len(words) > max_words:
            if current_clip:
                clips.append(" ".join(current_clip))
                current_clip = []
                current_word_count = 0
            
            for i in range(0, len(words), max_words):
                clips.append(" ".join(words[i:i+max_words]))
        else:
            if current_word_count + len(words) > max_words:
                clips.append(" ".join(current_clip))
                current_clip = [sentence]
                current_word_count = len(words)
            else:
                current_clip.append(sentence)
                current_word_count += len(words)
    
    if current_clip:
        clips.append(" ".join(current_clip))
    
    return clips

# --- 7. Main UI ---
st.markdown("""
<div style='text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 20px; margin-bottom: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.2);'>
    <h1 style='color: white; font-size: 3em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>
        ✨ Ultra Studio V11 Pro
    </h1>
    <p style='color: rgba(255,255,255,0.9); font-size: 1.2em;'>
        Professional AI Content Creation • Powered by Gemini 2.5 Flash
    </p>
</div>
""", unsafe_allow_html=True)

tab_script, tab_video, tab_image, tab_viral = st.tabs([
    "📝 Script Doctor", 
    "🎬 Video Generator", 
    "🖼️ Image Prompts",
    "🚀 Viral Manager"
])

# === TAB 1: SCRIPT DOCTOR ===
with tab_script:
    st.markdown("### ✍️ AI Script Enhancement")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📄 Input")
        raw_script = st.text_area("Your draft:", height=250, placeholder="Enter your script...")
        
        col_mode, col_length = st.columns(2)
        with col_mode:
            mode = st.selectbox("Style:", [
                "🎯 Viral Hook", "💼 Professional", "😂 Funny", 
                "🎓 Educational", "💰 Sales", "🌏 Malayalam→English", "✨ Creative"
            ])
        with col_length:
            target_length = st.selectbox("Length:", ["Keep Original", "Shorter", "Longer", "Expand"])
        
        enhance_btn = st.button("✨ Enhance", type="primary", use_container_width=True)
    
    with col2:
        st.markdown("#### ✨ Enhanced")
        
        if enhance_btn and raw_script:
            prompt = f"Rewrite in {mode} style, {target_length}:\n{raw_script}"
            result = safe_generate(prompt)
            
            if result and "Error" not in result:
                st.success("✅ Done!")
                st.text_area("Copy this:", value=result, height=250)
                
                col_o, col_n = st.columns(2)
                col_o.metric("Original", len(raw_script.split()))
                col_n.metric("Enhanced", len(result.split()))
                
                st.download_button("📥 Download", result, 
                    f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            else:
                st.error(result)

# === TAB 2: VIDEO GENERATOR ===
with tab_video:
    st.markdown("### 🎬 Video Prompt Generator")
    
    col_input, col_output = st.columns([1, 1])
    
    with col_input:
        st.markdown("#### 👤 Character")
        
        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "webp"])
        
        if uploaded_file:
            col_img, col_btn = st.columns([1, 1])
            with col_img:
                st.image(uploaded_file, use_container_width=True)
            with col_btn:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔍 Analyze", use_container_width=True):
                    analysis = analyze_image(uploaded_file)
                    if "Error" not in analysis:
                        st.session_state.img_description = analysis
                        st.success("✅ Done!")
        
        final_img_desc = st.text_area(
            "Description:",
            value=st.session_state.get('img_description', ''),
            height=150,
            placeholder="Describe character..."
        )
        
        st.markdown("---")
        st.markdown("#### 📝 Script")
        
        final_script = st.text_area("Dialogue:", height=200, placeholder="Enter script...")
        
        if final_script:
            clips = split_dialogue(final_script, max_words_per_clip)
            st.info(f"📊 Will create **{len(clips)} clips**")
        
        st.markdown("---")
        generate_btn = st.button("🚀 Generate Prompts", type="primary", use_container_width=True)
    
    with col_output:
        st.markdown("#### 🎯 Prompts")
        
        if generate_btn:
            if final_img_desc and final_script:
                clips = split_dialogue(final_script, max_words_per_clip)
                
                progress = st.progress(0)
                status = st.empty()
                
                for i, clip in enumerate(clips):
                    progress.progress((i + 1) / len(clips))
                    status.text(f"Clip {i+1}/{len(clips)}...")
                    
                    if i > 0:
                        time.sleep(1.5)
                    
                    prompt = generate_video_prompt(final_img_desc, clip, visual_style, i+1)
                    
                    with st.expander(f"🎬 Clip {i+1}", expanded=(i==0)):
                        if "Error" in prompt:
                            st.warning(prompt)
                        else:
                            st.code(prompt)
                            st.download_button("💾", prompt, f"clip_{i+1}.txt", key=f"dl{i}")
                
                status.text("✅ Complete!")
                
                if st.session_state.generated_prompts:
                    all_prompts = "\n\n---\n\n".join(st.session_state.generated_prompts)
                    st.download_button("📥 Download All", all_prompts, 
                        f"all_prompts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            else:
                st.error("⚠️ Need character & script")

# === TAB 3: IMAGE PROMPTS ===
with tab_image:
    st.markdown("### 🖼️ Image Prompt Generator")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        idea = st.text_area("Your vision:", height=200, placeholder="Describe your image...")
        
        col_a, col_b = st.columns(2)
        aspect = col_a.selectbox("Ratio:", ["1:1", "16:9", "9:16", "4:3", "21:9"])
        detail = col_b.selectbox("Detail:", ["High", "Medium", "Simple"])
        
        create_btn = st.button("✨ Create", type="primary", use_container_width=True)
    
    with col2:
        st.markdown("#### 🎨 Prompt")
        
        if create_btn and idea:
            prompt = f"Create image prompt for {visual_style}, {aspect}, {detail} detail:\n{idea}"
            result = safe_generate(prompt)
            
            if result and "Error" not in result:
                st.success("✅ Done!")
                st.code(result)
                st.download_button("💾 Download", result, 
                    f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            else:
                st.error(result)

# === TAB 4: VIRAL MANAGER ===
with tab_viral:
    st.markdown("### 🚀 Viral Strategy Generator")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        topic = st.text_input("Topic:", placeholder="What's your content about?")
        platform = st.multiselect("Platforms:", 
            ["YouTube", "Instagram", "TikTok", "Twitter", "LinkedIn", "Facebook"],
            default=["YouTube"])
        audience = st.selectbox("Audience:", 
            ["General", "Young Adults", "Professionals", "Parents", "Tech", "Entrepreneurs"])
        tone = st.selectbox("Tone:", 
            ["Exciting", "Educational", "Funny", "Inspirational", "Professional"])
        
        gen_btn = st.button("🚀 Generate", type="primary", use_container_width=True)
    
    with col2:
        st.markdown("#### 💎 Strategy")
        
        if gen_btn and topic:
            prompt = f"""Create viral strategy for:
Topic: {topic}
Platforms: {', '.join(platform)}
Audience: {audience}
Tone: {tone}

Include:
1. 5 viral titles
2. SEO description
3. 30 hashtags
4. 3 CTAs
5. Hook ideas
6. Platform tips"""
            
            result = safe_generate(prompt)
            
            if result and "Error" not in result:
                st.success("✅ Done!")
                st.markdown(result)
                st.download_button("📥 Download", result, 
                    f"viral_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            else:
                st.error(result)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 20px;'>
    <p><strong>Ultra Studio V11 Pro</strong> • Enhanced Edition</p>
    <p style='font-size: 0.9em;'>Built with ❤️ by Ashique • Powered by Gemini 2.5 Flash</p>
</div>
""", unsafe_allow_html=True)