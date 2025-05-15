import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance
import io

# Configurações da página
st.set_page_config(
    page_title="Visualizador de imagens",
    layout="wide"
)

# Função para visualizar a imagem
def mostrar_imagem(file, caption = "", use_container_width = False):
    if hasattr(file, "type") and file.type.startswith("image/"):
        st.image(file, caption=caption, clamp=True, use_container_width=use_container_width)
    elif isinstance(file, Image.Image):
        st.image(file, caption=caption, clamp=True, use_container_width=use_container_width)
    else:
        st.error("Tipo de arquivo não suportado")

# Função para exportar imagem
def exportar_imagem(image, format: str):
    buf = None
    buf = io.BytesIO()
    image.save(buf, format= "JPEG" if format.upper() == "JPG" else format.upper())
    st.download_button(
        label=f"Exportar imagem em {format.upper()}",
        data=buf.getvalue(),
        file_name=f"imagem_modificada.{format.lower()}",
        mime=f"image/{format.lower()}",
        use_container_width=True
    )

st.header("Visualizador de Imagens")

# Upload da imagem
file = st.file_uploader("Faça o upload de uma imagem")

if file is None:
    st.warning("Faça o upload de uma imagem!", icon="⚠️")
    st.info("Tipos de arquivos suportados: PNG ou JPG", icon="ℹ️")
else:
    img = Image.open(file)
    
    btn1, btn2, btn3, btn4, btn5, btn6 = st.columns(6)
    origin_img, custom_img = st.columns(2)
    
    # Botão de resetar imagem
    if st.button("Resetar imagem modificada", use_container_width=True):
        st.session_state.modified_img = img.copy()

    # Visualização da imagem original
    with origin_img:
        mostrar_imagem(file, caption="Imagem original", use_container_width=True)

    # Modifica a imagem na sessão local, permitindo visualizar a imagem com filtro em tempo real
    if "modified_img" not in st.session_state:
        st.session_state.modified_img = img.copy()
        
    # Criações dos botões de filtro
    with btn1: # Escala de cinza
        if st.button("Escala de cinza", key="btn_gray_scale", use_container_width=True):
            st.session_state.modified_img = st.session_state.modified_img.convert("L").convert("RGB")
    with btn2: # Inversão de cores
        if st.button("Inversão de cores", key="btn_color_inversion", use_container_width=True):
            st.session_state.modified_img = Image.eval(st.session_state.modified_img, lambda x: 255 - x)
    with btn3: # Aumento de contrase
        if st.button("Aumento de contraste", key="btn_contrast", use_container_width=True):
            enhancer = ImageEnhance.Contrast(st.session_state.modified_img)
            st.session_state.modified_img = enhancer.enhance(2.0)
    with btn4: # Desfoque
        if st.button("Desfoque (blur)", key="btn_blur", use_container_width=True):
            st.session_state.modified_img = st.session_state.modified_img.filter(ImageFilter.BLUR)
    with btn5: # Nitidez
        if st.button("Nitidez (sharpen)", key="btn_sharpen", use_container_width=True):
            st.session_state.modified_img = st.session_state.modified_img.filter(ImageFilter.SHARPEN)
    with btn6: # Detecção de bordas
        if st.button("Detecção de bordas", key="btn_border", use_container_width=True):
            st.session_state.modified_img = st.session_state.modified_img.filter(ImageFilter.FIND_EDGES)

    # Visualizar a imagem modificada
    with custom_img:
        mostrar_imagem(st.session_state.modified_img, caption="Imagem modificada", use_container_width=True)
    
    rotate_button, resize_button = st.columns(2)
    
    # Botão de rotacionar imagem
    with rotate_button:
        if st.button("Rotacionar imagem", icon="🔄", use_container_width=True):
            st.session_state.modified_img = st.session_state.modified_img.rotate(90, expand=True)

    # Botão de redimensionar imagem
    with resize_button:
        st.write("Redimensionar imagem")
        width = st.number_input("Nova largura", min_value=1, value=256, key="resize_width")
        height = st.number_input("Nova altura", min_value=1, value=256, key="resize_height")
        if st.button("Aplicar Redimensionamento", key="apply_resize"):
            st.session_state.modified_img = st.session_state.modified_img.resize((int(width), int(height)))
    
    st.divider()
    
    # Seção de exportar imagens, permitindo exportar a imagem em PNG ou JPG
    st.header("Exportar imagem modificada")
    
    export_png_button, export_jpg_button = st.columns(2)
    with export_png_button: exportar_imagem(st.session_state.modified_img, "PNG")
    with export_jpg_button: exportar_imagem(st.session_state.modified_img, "JPG")
