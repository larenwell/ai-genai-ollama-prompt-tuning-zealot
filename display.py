import ast
import pandas as pd
import streamlit as st

CSV_FILE_PATH = "results/best_combinations.csv"

st.title("Asistente Callcenter 📞")

df_clientes = pd.read_csv(CSV_FILE_PATH)

cliente_seleccionado = st.selectbox("Selecciona un cliente", df_clientes['customer_name'].unique())

if cliente_seleccionado:
    flashcard_cliente = df_clientes[df_clientes['customer_name'] == cliente_seleccionado]['flashcard'].values[0]
    flash_card_data = ast.literal_eval(flashcard_cliente)

    metadata = df_clientes[df_clientes['customer_name'] == cliente_seleccionado]['metadata'].values[0]
    metadata = ast.literal_eval(metadata)

    academic_scores = df_clientes[df_clientes['customer_name'] == cliente_seleccionado]['academic_scores'].values[0]
    

    st.markdown("""
    ### Estado actual del cliente
    """)

    columns = st.columns(2)
    with columns[0]:
        st.markdown(""" ### 🚦 Nivel de presión""")
        st.markdown(f""" {flash_card_data['nivel_presion']}
        """)
    with columns[1]:
        st.markdown(""" ### 🏷️ Tipificación operativa""")
        st.markdown(f""" {flash_card_data['tipificacion_operativa']} """)


    st.success(f"{flash_card_data['primer_dialogo']}")

    columns = st.columns(2)
    with columns[0]:
        st.markdown(""" ### ✅ Acción si responde si""")
        st.markdown(f""" {flash_card_data['accion_si_responde_si']} """)
    with columns[1]:
        st.markdown(""" ### ❌ Acción si responde no""")
        st.markdown(f""" {flash_card_data['accion_si_responde_no']} """)

    
    st.markdown(""" ### 🙅‍♂️ Acciones a evitar""")
    st.markdown(f""" {', '.join(flash_card_data['acciones_a_evitar'])} """)

    st.markdown("### 🧾 Síntesis")
    st.markdown("**Ultimo Contacto:** " + flash_card_data['ultimo_contacto'])
    st.markdown("**Canal:** " + flash_card_data['canal'])
    st.markdown("**Canal Recomendado:** " + flash_card_data['canal_recomendado'])
    st.markdown("**Cliente:** " + flash_card_data['cliente'])


    st.info(f"Modelo: {metadata['model_name']}")
    st.info(f"Prompt: {metadata['prompt_variation']}")
    st.info(f"Score: {academic_scores:.2f} %")
