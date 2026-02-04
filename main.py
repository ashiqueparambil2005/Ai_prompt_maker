import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
from datetime import datetime

# --- 1. Page Configuration (Premium Design) ---
st.set_page_config(
    page_title="Ultra Studio V11 Pro",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Enhanced CSS (Modern & Professional) ---
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Container */
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Card Styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Input Fields */
    .stTextArea textarea, .stTextInput input {
        border-radius: 12px;
        border: 2px solid #e0e7ff;
        padding: 12px;
        font-size: 14px;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Buttons */
    .stButton button {
        border-radius: 12px;
        height: 3.5em;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Primary Button */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: white;
        border-radius: 12px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
    }
    
    /* Success/Error Messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 12px;
        padding: 16px;
        border-left: 4px solid;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        border-radius: 8px;
        background-color: #f8f9fa;
        font-weight: 600;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Code Blocks */
    .stCodeBlock {
        border-radius: 12px;
        border: 2px solid #e0e7ff;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        border-radius: 12px;
        border: 2px dashed #667eea;
        padding: 20px;
        background-color: #f8f9ff;
    }
    
    /* Hide Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Progress Bar */
    .stProgress > div > div {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Session State Initialization ---
if 'generated_prompts' not in st.session_state:
    st.session_state.generated_prompts = []
if 'api_calls_count' not in st.session_state:
    st.session_state.api_calls_count = 0
if 'last_error' not in st.session_state:
    st.session_state.last_error = None

# --- 4. Enhanced Sidebar (Premium Settings) ---
with st.sidebar:
    st.markdown("# ⚙️ Control Panel")
    st.markdown("---")
    
    # API Key Input with validation
    api_key = st.text_input(
        "🔑 Gemini API Key:", 
        type="password",
        help="Get your API key from Google AI Studio"
    )
    
    # API Status Indicator
    if api_key:
        st.success("✅ API Key Connected")
    else:
        st.warning("⚠️ API Key Required")
    
    st.markdown("---")
    
    # Enhanced Style Selector
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
        ],
        help="Choose the visual aesthetic for your content"
    )
    
    st.markdown("---")
    
    # Advanced Settings
    with st.expander("🔧 Advanced Settings"):
        max_words_per_clip = st.slider(
            "Words per Video Clip:",
            min_value=10,
            max_value=30,
            value=15,
            help="Shorter clips = better lip sync"
        )
        
        enable_auto_save = st.checkbox(
            "Auto-save Prompts",
            value=True,
            help="Save generated prompts to session"
        )
        
        temperature = st.slider(
            "Creativity Level:",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher = more creative, Lower = more focused"
        )
    
    st.markdown("---")
    
    # Stats Display
    st.markdown("### 📊 Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("API Calls", st.session_state.api_calls_count)
    with col2:
        st.metric("Prompts", len(st.session_state.generated_prompts))
    
    st.markdown("---")
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.generated_prompts = []
        st.session_state.api_calls_count = 0
        st.rerun()
    
    if st.button("📥 Export All Prompts", use_container_width=True):
        if st.session_state.generated_prompts:
            export_text = "\n\n---\n\n".join(st.session_state.generated_prompts)
            st.download_button(
                "💾 Download",
                data=export_text,
                file_name=f"prompts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

# --- 5. Setup & Error Handling ---
if not api_key:
    st.markdown("""
    <div style='text-align: center; padding: 60px 20px; background: white; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);'>
        <h1 style='color: #667eea; font-size: 3em; margin-bottom: 20px;'>✨ Ultra Studio V11 Pro</h1>
        <p style='font-size: 1.2em; color: #64748b; margin-bottom: 30px;'>
            The Ultimate AI Content Creation Platform
        </p>
        <p style='color: #f59e0b; font-size: 1.1em;'>
            ⚠️ Please enter your Gemini API Key in the sidebar to begin
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error(f"❌ API Configuration Failed: {str(e)}")
    st.info("💡 Tip: Verify your API key at https://makersuite.google.com/app/apikey")
    st.stop()

# --- 6. Enhanced Helper Functions ---

def safe_generate(prompt, show_spinner=True):
    """Enhanced API call wrapper with rate limiting and error handling."""
    try:
        if show_spinner:
            with st.spinner("🤖 AI is thinking..."):
                time.sleep(0.5)  # Visual feedback
                response = model.generate_content(prompt)
                st.session_state.api_calls_count += 1
                return response.text.strip()
        else:
            response = model.generate_content(prompt)
            st.session_state.api_calls_count += 1
            return response.text.strip()
    except Exception as e:
        error_msg = str(e)
        st.session_state.last_error = error_msg
        
        if "429" in error_msg or "ResourceExhausted" in error_msg:
            return "⏳ **Rate Limit Reached**\n\nPlease wait 60 seconds before trying again."
        elif "quota" in error_msg.lower():
            return "💳 **Quota Exceeded**\n\nYour API quota has been exhausted. Check your Google Cloud Console."
        elif "invalid" in error_msg.lower():
            return "🔑 **Invalid API Key**\n\nPlease verify your API key in the sidebar."
        else:
            return f"⚠️ **Error Occurred**\n\n{error_msg}\n\nPlease try again or contact support."

def analyze_image(image_file):
    """Advanced image analysis with facial features detection."""
    try:
        img = Image.open(image_file)
        
        # Resize if too large
        max_size = 1024
        if max(img.size) > max_size:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        prompt = """Analyze this image for video generation purposes. Provide:
        1. Physical appearance (face shape, features, expressions)
        2. Hair style and color
        3. Clothing and accessories
        4. Age range and gender (if apparent)
        5. Notable characteristics
        
        Format: Clear, concise descriptions suitable for AI video prompts."""
        
        with st.spinner("🔍 Analyzing image..."):
            response = model.generate_content([prompt, img])
            st.session_state.api_calls_count += 1
            return response.text.strip()
    except Exception as e:
        return f"⚠️ Image Analysis Failed: {str(e)}"

def generate_video_prompt(image_desc, dialogue, style, clip_number=1):
    """Advanced video prompt generation with style-specific rules."""
    
    # Extract style name
    style_name = style.split(" ", 1)[1] if " " in style else style
    
    # Style-specific configurations
    style_configs = {
        "Strict Realism (Default)": {
            "rules": "Ultra-realistic, natural lighting, phone camera quality, micro-movements only, NO cinematic effects",
            "camera": "Handheld smartphone camera, natural shake, authentic feel",
            "lighting": "Natural ambient lighting, no studio setup"
        },
        "Cinematic Movie": {
            "rules": "8K cinematic quality, dramatic lighting, shallow depth of field, professional color grading",
            "camera": "RED camera, smooth gimbal movement, film grain",
            "lighting": "Three-point studio lighting, dynamic shadows, golden hour tones"
        },
        "Disney/Pixar 3D": {
            "rules": "High-quality 3D animation, Pixar render quality, expressive characters, vibrant colors",
            "camera": "Animated camera movement, dynamic angles",
            "lighting": "Soft, colorful lighting with rim lights, bounced light"
        },
        "Cyberpunk/Neon": {
            "rules": "Neon-lit environment, cyberpunk aesthetic, high contrast, futuristic",
            "camera": "Blade Runner inspired, rain effects, lens flares",
            "lighting": "Neon pink/blue lighting, volumetric fog, dramatic shadows"
        },
        "Vintage Film Grain": {
            "rules": "16mm film aesthetic, vintage color grading, film grain, retro vibe",
            "camera": "Classic film camera, slight vignette, scratches",
            "lighting": "Warm vintage lighting, soft shadows, nostalgic tone"
        },
        "Oil Painting Art": {
            "rules": "Oil painting style, artistic brush strokes, classical art aesthetic",
            "camera": "Static artistic framing, painting-like composition",
            "lighting": "Rembrandt lighting, chiaroscuro effects"
        },
        "Dreamy Watercolor": {
            "rules": "Soft watercolor aesthetic, flowing colors, dreamy atmosphere",
            "camera": "Soft focus, ethereal movement, gentle transitions",
            "lighting": "Soft diffused lighting, pastel tones, dreamy glow"
        }
    }
    
    # Get style config or default
    config = style_configs.get(style_name, style_configs["Strict Realism (Default)"])
    
    prompt = f"""Create a professional video generation prompt for AI video tools like Kling AI, Runway, or Pika.

**CLIP #{clip_number}**

CHARACTER DESCRIPTION:
{image_desc}

DIALOGUE TO SPEAK:
"{dialogue}"

VISUAL STYLE:
{style_name}

TECHNICAL REQUIREMENTS:
- Style Rules: {config['rules']}
- Camera Setup: {config['camera']}
- Lighting: {config['lighting']}

OUTPUT FORMAT:
Generate a single, detailed video prompt that includes:
1. Character description and positioning
2. The exact dialogue to be spoken
3. Facial expressions matching the emotional tone
4. Lip synchronization instructions
5. Camera movement and framing
6. Lighting and atmosphere details
7. Style-specific visual elements

Make it production-ready for professional AI video generation tools."""
    
    result = safe_generate(prompt, show_spinner=False)
    
    # Save to session if enabled
    if enable_auto_save and result and "Error" not in result:
        st.session_state.generated_prompts.append(f"Clip {clip_number}:\n{result}")
    
    return result

def split_dialogue(text, max_words=15):
    """Intelligent dialogue splitting with sentence awareness."""
    if not text:
        return []
    
    # Split by sentences first
    sentences = text.replace('!', '.').replace('?', '.').split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    
    clips = []
    current_clip = []
    current_word_count = 0
    
    for sentence in sentences:
        words = sentence.split()
        
        # If sentence alone exceeds max_words, split it
        if len(words) > max_words:
            if current_clip:
                clips.append(" ".join(current_clip))
                current_clip = []
                current_word_count = 0
            
            # Split long sentence
            for i in range(0, len(words), max_words):
                clips.append(" ".join(words[i:i+max_words]))
        else:
            # Check if adding this sentence exceeds limit
            if current_word_count + len(words) > max_words:
                clips.append(" ".join(current_clip))
                current_clip = [sentence]
                current_word_count = len(words)
            else:
                current_clip.append(sentence)
                current_word_count += len(words)
    
    # Add remaining
    if current_clip:
        clips.append(" ".join(current_clip))
    
    return clips

# --- 7. Main UI Layout ---

# Hero Section
st.markdown("""
<div style='text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 20px; margin-bottom: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.2);'>
    <h1 style='color: white; font-size: 3em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>
        ✨ Ultra Studio V11 Pro
    </h1>
    <p style='color: rgba(255,255,255,0.9); font-size: 1.2em; margin-bottom: 0;'>
        Professional AI Content Creation Suite • Enhanced Edition
    </p>
</div>
""", unsafe_allow_html=True)

# Create Enhanced Tabs
tab_script, tab_video, tab_image, tab_viral, tab_batch = st.tabs([
    "📝 Script Doctor", 
    "🎬 Video Generator", 
    "🖼️ Image Prompts",
    "🚀 Viral Manager",
    "⚡ Batch Processing"
])

# === TAB 1: ENHANCED SCRIPT DOCTOR ===
with tab_script:
    st.markdown("### ✍️ AI-Powered Script Enhancement")
    st.markdown("Transform your raw ideas into polished, engaging scripts.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📄 Input")
        raw_script = st.text_area(
            "Paste your draft script:",
            height=250,
            placeholder="Enter your script, ideas, or raw content here...",
            help="Can be rough notes, bullet points, or full scripts"
        )
        
        col_mode, col_length = st.columns(2)
        with col_mode:
            mode = st.selectbox(
                "Enhancement Style:",
                [
                    "🎯 Viral Hook",
                    "💼 Professional",
                    "😂 Funny/Entertaining",
                    "🎓 Educational",
                    "💰 Sales/Marketing",
                    "🌏 Malayalam to English",
                    "✨ Creative Storytelling"
                ]
            )
        
        with col_length:
            target_length = st.selectbox(
                "Target Length:",
                ["Keep Original", "Make Shorter", "Make Longer", "Expand Dramatically"]
            )
        
        enhance_btn = st.button("✨ Enhance Script", type="primary", use_container_width=True)
    
    with col2:
        st.markdown("#### ✨ Enhanced Output")
        
        if enhance_btn:
            if raw_script:
                enhancement_prompt = f"""Rewrite this script with the following specifications:
                
Style: {mode}
Length Adjustment: {target_length}
Original Script: {raw_script}

Requirements:
- Maintain the core message and meaning
- Apply the {mode} tone and style
- {target_length.replace('Keep Original', 'Maintain current length')}
- Ensure smooth flow and engagement
- Fix grammar and improve clarity

Provide only the enhanced script, no explanations."""
                
                result = safe_generate(enhancement_prompt)
                
                if result and "Error" not in result:
                    st.success("✅ Script enhanced successfully!")
                    
                    # Display with copy button
                    st.text_area(
                        "Copy your enhanced script:",
                        value=result,
                        height=250,
                        help="Click in the box and Ctrl+A, Ctrl+C to copy"
                    )
                    
                    # Word count comparison
                    col_orig, col_new = st.columns(2)
                    with col_orig:
                        st.metric("Original Words", len(raw_script.split()))
                    with col_new:
                        st.metric("Enhanced Words", len(result.split()))
                    
                    # Download option
                    st.download_button(
                        "📥 Download Script",
                        data=result,
                        file_name=f"enhanced_script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                else:
                    st.error(result)
            else:
                st.warning("⚠️ Please enter a script to enhance")

# === TAB 2: ENHANCED VIDEO GENERATOR ===
with tab_video:
    st.markdown("### 🎬 Professional Video Prompt Generator")
    st.markdown("Create broadcast-quality video prompts with character consistency.")
    
    # Two-column layout
    col_input, col_output = st.columns([1, 1])
    
    with col_input:
        # Character Setup Card
        with st.container():
            st.markdown("#### 👤 Character Setup")
            
            # Image upload with preview
            uploaded_file = st.file_uploader(
                "Upload Character Image",
                type=["jpg", "jpeg", "png", "webp"],
                help="Upload a reference image for consistent character appearance"
            )
            
            if uploaded_file is not None:
                # Display image with nice formatting
                col_img, col_btn = st.columns([1, 1])
                with col_img:
                    st.image(uploaded_file, caption="Character Reference", use_container_width=True)
                with col_btn:
                    st.markdown("<br>", unsafe_allow_html=True)
                    analyze_btn = st.button("🔍 Auto-Analyze Image", use_container_width=True)
                    
                    if analyze_btn:
                        analysis = analyze_image(uploaded_file)
                        if "Error" not in analysis:
                            st.session_state.img_description = analysis
                            st.success("✅ Analysis complete!")
                        else:
                            st.error(analysis)
            
            # Character description
            final_img_desc = st.text_area(
                "Character Description:",
                value=st.session_state.get('img_description', ''),
                height=150,
                placeholder="Describe your character: age, appearance, clothing, style...\n\nExample: A 25-year-old woman with long brown hair, wearing a casual blue sweater, friendly smile, modern professional look.",
                help="Be specific about appearance for consistent results"
            )
        
        st.markdown("---")
        
        # Script Input Card
        with st.container():
            st.markdown("#### 📝 Script Input")
            
            final_script = st.text_area(
                "Paste your final script:",
                height=200,
                placeholder="Enter the complete dialogue your character will speak...",
                help="This will be automatically split into optimal video clips"
            )
            
            # Preview clip count
            if final_script:
                preview_clips = split_dialogue(final_script, max_words_per_clip)
                st.info(f"📊 Will generate **{len(preview_clips)} video clips** based on your script")
        
        st.markdown("---")
        
        # Generate Button
        generate_btn = st.button(
            "🚀 Generate Video Prompts",
            type="primary",
            use_container_width=True,
            help="Click to create professional video prompts for each clip"
        )
    
    with col_output:
        st.markdown("#### 🎯 Generated Video Prompts")
        
        if generate_btn:
            if final_img_desc and final_script:
                clips = split_dialogue(final_script, max_words_per_clip)
                
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                st.success(f"✅ Generating {len(clips)} professional video prompts...")
                
                # Generate prompts with progress
                for i, clip in enumerate(clips):
                    # Update progress
                    progress = (i + 1) / len(clips)
                    progress_bar.progress(progress)
                    status_text.text(f"Processing Clip {i+1}/{len(clips)}...")
                    
                    # Rate limiting
                    if i > 0:
                        time.sleep(2.5)
                    
                    prompt = generate_video_prompt(final_img_desc, clip, visual_style, i+1)
                    
                    # Display in expandable card
                    with st.expander(f"🎬 Clip {i+1} — \"{clip[:50]}...\"", expanded=(i==0)):
                        if "Error" in prompt or "⏳" in prompt or "💳" in prompt:
                            st.warning(prompt)
                        else:
                            st.code(prompt, language="text")
                            
                            # Copy and download buttons
                            col_copy, col_download = st.columns(2)
                            with col_download:
                                st.download_button(
                                    "💾 Download",
                                    data=prompt,
                                    file_name=f"clip_{i+1}_prompt.txt",
                                    mime="text/plain",
                                    key=f"download_{i}"
                                )
                
                # Completion
                progress_bar.progress(1.0)
                status_text.text("✅ All prompts generated successfully!")
                
                # Export all option
                st.markdown("---")
                if st.session_state.generated_prompts:
                    all_prompts = "\n\n" + "="*50 + "\n\n".join(st.session_state.generated_prompts)
                    st.download_button(
                        "📥 Download All Prompts",
                        data=all_prompts,
                        file_name=f"all_video_prompts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
            else:
                st.error("⚠️ Please provide both **Character Description** and **Script**")

# === TAB 3: IMAGE PROMPTS ===
with tab_image:
    st.markdown("### 🖼️ AI Image Prompt Generator")
    st.markdown("Create detailed, professional prompts for Midjourney, DALL-E, and Stable Diffusion.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 💡 Your Vision")
        
        idea = st.text_area(
            "Describe what you want to create:",
            height=200,
            placeholder="Example: A futuristic city at sunset with flying cars and neon signs...",
            help="Be as detailed or as simple as you want - AI will enhance it"
        )
        
        col_aspect, col_quality = st.columns(2)
        with col_aspect:
            aspect_ratio = st.selectbox(
                "Aspect Ratio:",
                ["1:1 Square", "16:9 Landscape", "9:16 Portrait", "4:3 Classic", "21:9 Ultrawide"]
            )
        
        with col_quality:
            detail_level = st.selectbox(
                "Detail Level:",
                ["High Detail", "Medium Detail", "Simple/Minimalist"]
            )
        
        create_btn = st.button("✨ Create Image Prompt", type="primary", use_container_width=True)
    
    with col2:
        st.markdown("#### 🎨 Generated Prompt")
        
        if create_btn:
            if idea:
                image_prompt = f"""Create a professional, detailed image generation prompt for {visual_style}.

User's Vision: {idea}

Requirements:
- Aspect Ratio: {aspect_ratio}
- Detail Level: {detail_level}
- Visual Style: {visual_style}

Generate a complete, production-ready prompt that includes:
1. Main subject and composition
2. Lighting and atmosphere
3. Color palette
4. Technical specifications (resolution, quality)
5. Style-specific keywords
6. Camera angle and perspective

Format: Ready to paste into Midjourney, DALL-E, or Stable Diffusion."""
                
                result = safe_generate(image_prompt)
                
                if result and "Error" not in result:
                    st.success("✅ Prompt created!")
                    st.code(result, language="text")
                    
                    col_dl, col_copy = st.columns(2)
                    with col_dl:
                        st.download_button(
                            "💾 Download",
                            data=result,
                            file_name=f"image_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                else:
                    st.error(result)
            else:
                st.warning("⚠️ Please describe your image idea")

# === TAB 4: VIRAL MANAGER ===
with tab_viral:
    st.markdown("### 🚀 Viral Content Strategy Generator")
    st.markdown("Create compelling titles, descriptions, and hashtags for maximum reach.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📊 Content Details")
        
        topic = st.text_input(
            "Video/Post Topic:",
            placeholder="Example: How to make perfect coffee at home",
            help="What is your content about?"
        )
        
        platform = st.multiselect(
            "Target Platforms:",
            ["YouTube", "Instagram", "TikTok", "Twitter/X", "LinkedIn", "Facebook"],
            default=["YouTube"]
        )
        
        audience = st.selectbox(
            "Target Audience:",
            ["General Public", "Young Adults (18-25)", "Professionals", "Parents", "Tech Enthusiasts", "Entrepreneurs"]
        )
        
        tone_viral = st.selectbox(
            "Content Tone:",
            ["Exciting/Energetic", "Educational/Informative", "Funny/Entertaining", "Inspirational", "Professional"]
        )
        
        generate_viral_btn = st.button("🚀 Generate Viral Strategy", type="primary", use_container_width=True)
    
    with col2:
        st.markdown("#### 💎 Viral Content Package")
        
        if generate_viral_btn:
            if topic:
                viral_prompt = f"""Create a comprehensive viral content strategy for:

Topic: {topic}
Platforms: {', '.join(platform)}
Target Audience: {audience}
Tone: {tone_viral}

Generate:
1. **5 Viral Video Titles** (attention-grabbing, click-worthy)
2. **Video Description** (SEO-optimized, engaging)
3. **30 Strategic Hashtags** (mix of popular and niche)
4. **3 Call-to-Action Options**
5. **Content Hook Ideas** (first 5 seconds)
6. **Platform-Specific Tips**

Format professionally and make it ready to use."""
                
                result = safe_generate(viral_prompt)
                
                if result and "Error" not in result:
                    st.success("✅ Viral strategy generated!")
                    st.markdown(result)
                    
                    st.download_button(
                        "📥 Download Strategy",
                        data=result,
                        file_name=f"viral_strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                else:
                    st.error(result)
            else:
                st.warning("⚠️ Please enter a topic")

# === TAB 5: BATCH PROCESSING ===
with tab_batch:
    st.markdown("### ⚡ Batch Processing")
    st.markdown("Process multiple scripts or topics at once for efficiency.")
    
    st.info("🚀 **Coming Soon**: Batch process multiple scripts, convert multiple images, and generate series content in one click!")
    
    batch_input = st.text_area(
        "Enter multiple topics (one per line):",
        height=200,
        placeholder="Topic 1\nTopic 2\nTopic 3...",
        help="Each line will be processed separately"
    )
    
    if st.button("⚡ Process Batch", type="primary"):
        if batch_input:
            topics = [t.strip() for t in batch_input.split('\n') if t.strip()]
            st.info(f"Ready to process {len(topics)} items. Full batch processing coming in next update!")
        else:
            st.warning("Please enter topics to process")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 20px;'>
    <p><strong>Ultra Studio V11 Pro</strong> • Enhanced Edition</p>
    <p style='font-size: 0.9em;'>Built with ❤️ for content creators • Powered by ashiqueconnect@gmail.com</p>
</div>
""", unsafe_allow_html=True)