import streamlit as st

def img():
    st.image(fases.get((st.session_state.tentativas)))

st.title('Jogo da Forca')

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

fases = {
    7: "https://via.placeholder.com/150?text=7",
    6: "https://via.placeholder.com/150?text=6",
    5: "https://via.placeholder.com/150?text=5",
    4: "https://via.placeholder.com/150?text=4",
    3: "https://via.placeholder.com/150?text=3",
    2: "https://via.placeholder.com/150?text=2",
    1: "https://via.placeholder.com/150?text=1",
    0: "https://via.placeholder.com/150?text=0"
}

if 'tentativas' not in st.session_state:
    st.session_state.tentativas = 7
    st.session_state.letras_adivinhadas = []
    st.session_state.palavras_em_lista = []
    st.session_state.frase_completa = ''
    img()

def definir_palavra():
    if 'frase' not in st.session_state:
        st.session_state.frase = st.text_input("Jogador 1, digite a palavra para o Jogo da Forca:").upper()
        if st.session_state.frase:
            st.session_state.frase_completa = '_' * len(st.session_state.frase)
            st.experimental_rerun()

def jogar():
    if 'frase' in st.session_state and st.session_state.frase:
        input_letra = st.text_input("Jogador 2, digite uma letra 👇", key="input_letra").upper()
        if len(input_letra) == 1 and input_letra.isalpha():
            if input_letra in st.session_state.letras_adivinhadas:
                st.error(f"Você já adivinhou a letra {input_letra}")
            elif input_letra not in st.session_state.frase:
                st.error(f"{input_letra} não está na palavra.")
                st.session_state.tentativas -= 1
                st.session_state.letras_adivinhadas.append(input_letra)
                st.warning('Você errou!')
            else:
                st.success(f"Parabéns, {input_letra} está na frase!")
                index = [i for i, letra in enumerate(st.session_state.frase) if letra == input_letra]
                frase_completa_lista = list(st.session_state.frase_completa)
                for i in index:
                    frase_completa_lista[i] = input_letra
                st.session_state.frase_completa = "".join(frase_completa_lista)
                st.session_state.letras_adivinhadas.append(input_letra)
                st.success('Você acertou!')

            img()

        if all(c in st.session_state.letras_adivinhadas or c in [' ', '?'] for c in st.session_state.frase):
            st.balloons()
            st.success('Parabéns! Você acertou a frase completa!')
            if st.button("Jogar novamente"):
                reset_game()

        elif len(input_letra) > 1:
            st.warning("Escreva apenas uma letra.")
        elif input_letra and not input_letra.isalpha():
            st.warning('Digito inválido.')

        if st.session_state.tentativas <= 0:
            st.error('Você perdeu!')
            if st.button("Tentar novamente"):
                reset_game()

        columns = st.columns(len(st.session_state.frase))

        for i, col in enumerate(columns):
            with col:
                if i == 6:
                    st.subheader(' ')
                elif i == 13:
                    st.subheader('?')
                else:
                    st.subheader(st.session_state.frase_completa[i])

        if st.session_state.tentativas <= 0 or all(c in st.session_state.letras_adivinhadas or c in [' ', '?'] for c in st.session_state.frase):
            if st.button("Jogar novamente"):
                reset_game()
            else:
                st.info("Obrigado por jogar! Volte depois.")

def main():
    definir_palavra()
    jogar()

if __name__ == "__main__":
    main()
