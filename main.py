import streamlit as st

def img():
    if 'tentativas' in st.session_state:
        st.image(fases.get(st.session_state.tentativas))

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

if 'frase_escolhida' not in st.session_state:
    st.session_state.frase = st.selectbox("Escolha uma frase para jogar", frases_possiveis, key='frase_selecionada')
    if st.button("Confirmar frase"):
        st.session_state.frase_escolhida = st.session_state.frase
        st.session_state.tentativas = 7
        st.session_state.letras_adivinhadas = []
        st.session_state.frase_completa = '_' * len(st.session_state.frase_escolhida)
        st.experimental_rerun()  # Recarrega a página para esconder a seleção da frase
else:
    frase = st.session_state.frase_escolhida
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
        st.session_state.frase_completa = '_' * len(frase)
        img()

    def jogar():
        input_container = st.empty()
        input_letra = input_container.text_input("Digite uma letra 👇").upper()

        if st.button("Enviar letra"):
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
            else:
                if len(input_letra) > 1:
                    st.warning("Escreva apenas uma letra.")
                elif input_letra and not input_letra.isalpha():
                    st.warning('Digite um caractere válido.')

            if all(c in st.session_state.letras_adivinhadas or c in [' ', '?'] for c in frase):
                st.balloons()
                st.success('Parabéns! Você acertou a frase completa!')

            if st.session_state.tentativas <= 0:
                st.error('Você perdeu!')
                if st.button("Tentar novamente"):
                    reset_game()

            # Limpar o campo de entrada após o envio
            input_container.text_input("Digite uma letra 👇", value="", key="input_letra")

        columns = st.columns(len(frase))

        for i, col in enumerate(columns):
            with col:
                st.subheader(st.session_state.frase_completa[i])

    jogar()
