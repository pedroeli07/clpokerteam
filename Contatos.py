import streamlit as st

def mostrar_contatos():
        st.write("### Desenvolvido por Pedro Eli Bernardes Maciel")
        st.write("Whatsapp:")
        # Link do WhatsApp com emoji e imagem
        st.markdown("[Mensagem no WhatsApp](https://wa.me/5537998734398) <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/1200px-WhatsApp.svg.png' alt='WhatsApp' width='20'>", unsafe_allow_html=True)

        # Link do LinkedIn com emoji e imagem
        st.write("Linkedin:")
        st.markdown("[Perfil no LinkedIn](https://www.linkedin.com/in/pedro-eli-bernardes-maciel-904828296/) <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Linkedin_icon.svg/1200px-Linkedin_icon.svg.png' alt='LinkedIn' width='20'>", unsafe_allow_html=True)
        st.markdown("Emails:")
        # Exibindo e-mails com emojis
        st.write("pedro-eli@hotmail.com 📧 ")
        st.write("pedro.eli@neothingsiot.com 📧 ")

        # Link do Instagram com emoji e imagem
        st.write("Instragram do CL Poker Team:")
        st.markdown("[@clpoker](https://www.instagram.com/clpoker/) <img src='https://emojiguide.com/wp-content/uploads/2020/01/Instagram-Logo-1024x1024.png' alt='Instagram' width='20'>", unsafe_allow_html=True)