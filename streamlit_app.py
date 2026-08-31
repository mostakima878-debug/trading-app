import streamlit as st
import os
import time
import yt_dlp
from moviepy.editor import VideoFileClip, vfx

# पेज की सेटिंग
st.set_page_config(
    page_title="Ultimate AI Video & Audio Studio",
    page_icon="🔥",
    layout="wide"
)

st.title("🔥 Ultimate AI Video & Audio Studio (All-in-One)")
st.markdown("---")

# --- स्टेप 1: वीडियो यूआरएल इनपुट ---
st.subheader("🔗 स्टेप 1: वीडियो का लिंक डालें")
video_url = st.text_input("यहाँ Instagram Reel या YouTube वीडियो का लिंक पेस्ट करें:")

# --- स्टेप 2: वीडियो डाउनलोड करने का सेक्शन ---
st.markdown("---")
st.subheader("📥 स्टेप 2: वीडियो डाउनलोड करें")

if st.button("असली वीडियो डाउनलोड करें 🚀"):
    if video_url:
        st.info("🔄 वीडियो डाउनलोड हो रही है, कृपया थोड़ा इंतज़ार करें...")
        try:
            ydl_opts = {
                'format': 'mp4',
                'outtmpl': 'downloaded_video.mp4',
                'quiet': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            
            st.success("✅ वीडियो सफलतापूर्वक डाउनलोड हो गई!")
            if os.path.exists("downloaded_video.mp4"):
                st.video("downloaded_video.mp4")
        except Exception as e:
            st.error(f"डाउनलोड करने में एरर आया: {e}")
    else:
        st.warning("कृपया पहले कोई वैध (Valid) लिंक तो डाल मेरे भाई!")

# --- स्टेप 3: वीडियो से आवाज़ (Voice) अलग करना और AI इफ़ेक्ट डालना ---
st.markdown("---")
st.subheader("🎨 स्टेप 3: AI इफ़ेक्ट और वॉइस (Audio) प्रोसेसिंग")

effect_choice = st.selectbox(
    "आप वीडियो पर कौन सा इफ़ेक्ट लगाना चाहते हैं?",
    ["कार्टून स्टाइल (Colorize & Boost)", "सिनेमैटिक लुक (Cinematic Dark)", "ब्लैक एंड व्हाइट (Black & White)", "स्पीड फ़ास्ट (Fast Motion)"]
)

if st.button("प्रोसेसिंग शुरू करें (AI Effect & Audio Split) 🎬"):
    if os.path.exists("downloaded_video.mp4"):
        st.info("🔄 वीडियो पर AI इफ़ेक्ट लगाया जा रहा है और आवाज़ अलग की जा रही है...")
        
        try:
            # MoviePy का इस्तेमाल करके वीडियो लोड करना
            clip = VideoFileClip("downloaded_video.mp4")
            
            # 1. ऑडियो (Voice) अलग करना
            if clip.audio is not None:
                clip.audio.write_audiofile("extracted_voice.mp3", logger=None)
                st.success("🎵 वीडियो की आवाज़ (Voice) सफलतापूर्वक अलग कर ली गई है!")
            
            # 2. इफ़ेक्ट के हिसाब से वीडियो बदलना
            processed_clip = clip
            if "कार्टून" in effect_choice:
                processed_clip = clip.fx(vfx.colorx, 1.3) # रंग चमकाना ताकि कार्टून जैसा वाइब आए
            elif "सिनेमैटिक" in effect_choice:
                processed_clip = clip.fx(vfx.lum_contrast, lum=0, contrast=1.4, threshold=128)
            elif "ब्लैक एंड व्हाइट" in effect_choice:
                processed_clip = clip.fx(vfx.blackwhite)
            elif "स्पीड फ़ास्ट" in effect_choice:
                processed_clip = clip.fx(vfx.speedx, 1.5)
            
            # फाइनल प्रोसेस्ड वीडियो सेव करना
            processed_clip.write_videofile("final_ai_video.mp4", codec="libx264", audio_codec="aac", logger=None)
            
            st.success("✨ बधाई हो भाई! वीडियो और ऑडियो दोनों सफलतापर्वक तैयार हो चुके हैं!")
            
            # वीडियो दिखाना
            st.markdown("### 📺 फाइनल AI वीडियो:")
            st.video("final_ai_video.mp4")
            
            # डाउनलोड बटन (वीडियो)
            with open("final_ai_video.mp4", "rb") as fv:
                st.download_button(
                    label="📥 फाइनल AI वीडियो डाउनलोड करें (.mp4)",
                    data=fv,
                    file_name="final_ai_video.mp4",
                    mime="video/mp4"
                )
            
            # डाउनलोड बटन (अलग की गई आवाज़/Voice)
            if os.path.exists("extracted_voice.mp3"):
                with open("extracted_voice.mp3", "rb") as fa:
                    st.download_button(
                        label="🎵 अलग की गई आवाज़ (Voice) डाउनलोड करें (.mp3)",
                        data=fa,
                        file_name="extracted_voice.mp3",
                        mime="audio/mp3"
                    )
                    
            clip.close()
            processed_clip.close()
            
        except Exception as e:
            st.error(f"प्रोसेसिंग के दौरान एरर आया: {e}")
    else:
        st.warning("कृपया पहले स्टेप 2 से वीडियो डाउनलोड करें भाई!")





