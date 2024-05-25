import streamlit as st

def img():
    st.image(fases.get((st.session_state.tentativas)))

st.title('Jogo da Forca do Amor')
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] > .main {
            background-color: #006d77; /* Petróleo */
            background-image: linear-gradient(90deg, #006d77 0%, #83c5be 55%, #edf6f9 100%); /* Verde água */
        }
    </style>
    """, unsafe_allow_html=True)

def reset_game():
    st.session_state.clear()  # Limpa todo o estado da sessão
    st.experimental_rerun()

frases_possiveis = ['NAMORA COMIGO?', 'TE AMO MUITO', 'CASA COMIGO?', 'VOCÊ É LINDA', 'VOCÊ ME COMPLETA']
frase = st.selectbox("Escolha uma frase para jogar", frases_possiveis, key='frase_selecionada')

input_letra = st.text_input("Digite uma letra 👇", key="input_letra").upper()
fases = {
    7: "1.png",
    6: "2.png",
    5: "3.png",
    4: "4.png",
    3: "5.png",
    2: "6.png",
    1: "7.png",
    0: "0.png"
}

if 'tentativas' not in st.session_state:
    st.session_state.tentativas = 7
    st.session_state.letras_adivinhadas = []
    st.session_state.palavras_em_lista = []
    img()
    st.session_state.frase_completa = '_' * len(frase)

def jogar():
    if len(input_letra) == 1 and input_letra.isalpha():
        if input_letra in st.session_state.letras_adivinhadas:
            st.error(f"Você já adivinhou a letra {input_letra}")
        elif input_letra not in frase:
            st.error(f"{input_letra} não está na palavra.")
            st.session_state.tentativas -= 1
            st.session_state.letras_adivinhadas.append(input_letra)
        else:
            st.success(f"Parabéns, {input_letra} está na frase!")
            index = [i for i, letra in enumerate(frase) if letra == input_letra]
            frase_completa_lista = list(st.session_state.frase_completa)
            for i in index:
                frase_completa_lista[i] = input_letra
            st.session_state.frase_completa = "".join(frase_completa_lista)
            st.session_state.letras_adivinhadas.append(input_letra)

        img()

    if all(c in st.session_state.letras_adivinhadas or c in [' ', '?'] for c in frase):
        st.balloons()
        st.success('Parabéns! Você acertou a frase completa!')

    elif len(input_letra) > 1:
        st.warning("Escreva apenas uma letra.")
    elif input_letra and not input_letra.isalpha():
        st.warning('Digito inválido.')

    if st.session_state.tentativas <= 0:
        st.error('Você perdeu!')
        button_key = f"tentar_novamente_btn{st.session_state.tentativas}"
        if st.button("Tentar novamente", key=button_key):
            reset_game()

    columns = st.columns(len(frase))

    for i, col in enumerate(columns):
        with col:
            if i == 6:
                st.subheader(' ')
            elif i == 13:
                st.subheader('?')
            else:
                st.subheader(st.session_state.frase_completa[i])

jogar()
