import streamlit as st
import yt_dlp
import os

# Webpagina configuratie
st.set_page_config(page_title="Universal Audio Ripper", page_icon="🎵")
st.title("🎵 Universal Audio Ripper")
st.write("Plak een videolink (Facebook, VOORLOPIG GEEN YOUTUBE, TikTok, Instagram, etc.) om de audio als MP3 te downloaden.")

# Input veld voor de URL
video_url = st.text_input("Video of Audio URL:", placeholder="Plak je link hier...")

if video_url:
    st.info("De media wordt verwerkt... Een moment geduld aub.")
    
    # We gebruiken een vaste naam om "File name too long" errors van websites te voorkomen
    output_filename = "downloaded_audio"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_filename}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'extractor_args': {
            'youtube': {
                # We dwingen mobiele clients af, deze omzeilen de 403 blokkade vaak zonder extra pakketten
                'player_client': ['android', 'ios', 'mweb'] 
            }
        }

    }
    
    try:
        # Download en converteer de audio van de ingevoerde site
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        mp3_file = f"{output_filename}.mp3"
        
        # Controleer of het bestand succesvol is aangemaakt
        if os.path.exists(mp3_file):
            with open(mp3_file, "rb") as file:
                st.success("Audio succesvol geript!")
                # De downloadknop op de webpagina
                st.download_button(
                    label="Download MP3",
                    data=file,
                    file_name="audio_download.mp3",
                    mime="audio/mp3"
                )
            
            # Netjes opruimen op de server
            os.remove(mp3_file)
            
    except Exception as e:
        st.error(f"Er ging iets mis: {str(e)}")
        error_details = traceback.format_exc()
        st.error("meer zelfs, ik zou eggen, er ging iets mis")
        st.code(error_details, language="text")
        st.warning("Tip: Controleer of de video openbaar is en de link klopt.")
