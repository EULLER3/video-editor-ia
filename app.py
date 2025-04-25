
import streamlit as st

st.set_page_config(page_title="Editor de Vídeo IA", page_icon="🎬")

st.title("🎬 Bem-vindo ao Editor de Vídeo com IA!")
st.write("Este é um aplicativo inicial para edição inteligente de vídeos.")

video_file = st.file_uploader("Faça upload do seu vídeo", type=["mp4", "mov", "avi"])

if video_file is not None:
    st.video(video_file)
    st.success("Vídeo carregado com sucesso!")

st.info("🚀 Versão inicial - mais funcionalidades em breve!")
