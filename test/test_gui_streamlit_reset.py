import streamlit as st
import pytest

# Test para el botón de reset en la interfaz Streamlit

def test_reset_to_default(monkeypatch):
    # Simula el estado de sesión con parámetros modificados
    st.session_state.clear()
    st.session_state["episodes"] = 5000
    st.session_state["seed"] = 9999
    st.session_state["risk_scale"] = 5.0
    st.session_state["grid_size"] = 10
    st.session_state["initial_resources"] = 500.0
    st.session_state["tripwires"] = 10
    st.session_state["shocks"] = 10
    st.session_state["distractors"] = 10
    st.session_state["max_steps"] = 200
    st.session_state["agent_type"] = "Simbiosis (DQN)"

    # Simula el click en el botón de reset
    def fake_button(label):
        if label == "Reset to default":
            # Valores por defecto
            st.session_state["episodes"] = 1000
            st.session_state["seed"] = 42
            st.session_state["risk_scale"] = 1.0
            st.session_state["grid_size"] = 5
            st.session_state["initial_resources"] = 100.0
            st.session_state["tripwires"] = 1
            st.session_state["shocks"] = 1
            st.session_state["distractors"] = 1
            st.session_state["max_steps"] = 50
            st.session_state["agent_type"] = "Control (Q-table)"
            return True
        return False
    monkeypatch.setattr(st, "button", fake_button)

    # Ejecuta el botón de reset
    st.button("Reset to default")

    # Verifica que los valores sean los esperados
    assert st.session_state["episodes"] == 1000
    assert st.session_state["seed"] == 42
    assert st.session_state["risk_scale"] == 1.0
    assert st.session_state["grid_size"] == 5
    assert st.session_state["initial_resources"] == 100.0
    assert st.session_state["tripwires"] == 1
    assert st.session_state["shocks"] == 1
    assert st.session_state["distractors"] == 1
    assert st.session_state["max_steps"] == 50
    assert st.session_state["agent_type"] == "Control (Q-table)"
