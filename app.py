import moviepy.editor as mp
import speech_recognition as sr
import spacy
import streamlit as st

# Função para cortar o vídeo de acordo com os intervalos
def cut_video(video_path, cuts, platform='youtube'):
    video = mp.VideoFileClip(video_path)
    clips = [video.subclip(start, end) for start, end in cuts]
    edited_video = mp.concatenate_videoclips(clips)

    # Ajustar o formato dependendo da plataforma
    if platform == 'youtube':
        edited_video = edited_video.resize(height=1920, width=1080)
    elif platform == 'instagram':
        edited_video = edited_video.resize(height=1080, width=1080)
    elif platform == 'podcast':
        edited_video = edited_video.resize(height=720, width=1280)

    # Salvar o vídeo editado
    edited_video_path = "edited_video.mp4"
    edited_video.write_videofile(edited_video_path)
    
    return edited_video_path

# Função para gerar legendas automáticas
def generate_subtitles(video_path):
    recognizer = sr.Recognizer()
    audio_clip = mp.VideoFileClip(video_path).audio
    audio_clip.write_audiofile("audio.wav")

    with sr.AudioFile("audio.wav") as source:
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
    
    return text

# Função para gerar tags automáticas usando spaCy
def generate_tags(description):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(description)
    tags = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "GPE", "PRODUCT"]]
    return tags

# Função principal para a interface Streamlit
def main():
    st.title("Editor de Vídeo Automático")
    
    uploaded_file = st.file_uploader("Carregar vídeo", type=["mp4", "mov", "avi"])
    if uploaded_file is not None:
        video_path = "uploaded_video.mp4"
        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())

        st.subheader("Defina os Intervalos de Corte (em segundos)")
        cuts_input = st.text_area("Intervalos de corte (exemplo: [(0,10), (20,30)])", "[[0,10], [20,30]]")
        cuts = eval(cuts_input)

        platform = st.selectbox("Escolha a plataforma", ["youtube", "instagram", "podcast"])

        if st.button("Processar vídeo"):
            edited_video_path = cut_video(video_path, cuts, platform)
            subtitles = generate_subtitles(edited_video_path)
            tags = generate_tags(subtitles)

            st.subheader("Legendas Geradas")
            st.write(subtitles)

            st.subheader("Tags Geradas")
            st.write(tags)
            
            st.video(edited_video_path)
            st.success(f"Vídeo processado com sucesso! Salvo como {edited_video_path}")

if __name__ == "__main__":
    main()
