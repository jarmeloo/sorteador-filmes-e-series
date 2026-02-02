import streamlit as st
import random
from biblioteca import catalogo, gerar_link

# -------------------------------
# Configuração da página
# -------------------------------
st.set_page_config(
    page_title="Disney+ Random Picker",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Disney+ Random Picker")
st.write("Indeciso sobre o que assistir? Deixa a sorte escolher por você! 👇")

# -------------------------------
# Estado da aplicação
# -------------------------------
if "recomendados" not in st.session_state:
    st.session_state.recomendados = []

# -------------------------------
# Escolha do tipo e categoria
# -------------------------------
tipo = st.radio(
    "O que você quer assistir hoje?",
    options=list(catalogo.keys())
)

categoria = st.selectbox(
    "Escolha a categoria:",
    list(catalogo[tipo].keys())
)

# -------------------------------
# Função de Sorteio
# -------------------------------
def realizar_sorteio(lista_completa, lista_atual=None):
    # Se já houver recomendados, tenta sortear títulos diferentes
    if lista_atual:
        restantes = [t for t in lista_completa if t not in lista_atual]
        # Se não houver mais novos, sorteia da lista completa mesmo
        fonte = restantes if restantes else lista_completa
    else:
        fonte = lista_completa
        
    return random.sample(fonte, min(5, len(fonte)))

# -------------------------------
# Botões de Ação
# -------------------------------
col_sorteio, col_refazer = st.columns(2)

with col_sorteio:
    if st.button("🎲 Sortear títulos", use_container_width=True):
        st.session_state.recomendados = realizar_sorteio(catalogo[tipo][categoria])

with col_refazer:
    # Só mostra o botão de refazer se já houver algo sorteado
    if st.session_state.recomendados:
        if st.button("🔄 Sortear novos títulos", use_container_width=True):
            st.session_state.recomendados = realizar_sorteio(
                catalogo[tipo][categoria], 
                st.session_state.recomendados
            )

st.divider()

# -------------------------------
# Mostrar recomendações
# -------------------------------
if st.session_state.recomendados:
    st.subheader(f"Recomendações de {tipo} – {categoria}")

    for titulo in st.session_state.recomendados:
        col_tit, col_btn = st.columns([3, 1])
        
        with col_tit:
            st.write(f"🎥 **{titulo}**")
        
        with col_btn:
            link = gerar_link(titulo)
            if link:
                # O link_button resolve o problema de abrir no navegador do usuário
                st.link_button("▶ Assistir", link)
            else:

                st.caption("Link indisponível")

