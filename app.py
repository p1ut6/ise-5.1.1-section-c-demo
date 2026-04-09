import streamlit as st

if "ten_x" not in st.session_state:
    st.session_state.ten_x = False

if "count" not in st.session_state:
    st.session_state.count = 0


def increment():
    st.session_state.count += 10 if st.session_state.ten_x else 1


def decrement():
    st.session_state.count -= 10 if st.session_state.ten_x else 1
    if st.session_state.count < 0:
        st.session_state.count = 0


with st.expander("Options"):
    st.checkbox("10x mode", key="ten_x")

st.write(f"Total count is {st.session_state.count}")

st.button(
    f"plus {'10' if st.session_state.ten_x else '1'}",
    key="increment",
    on_click=increment,
)
st.button(
    f"minus {'10' if st.session_state.ten_x else '1'}",
    key="decrement",
    on_click=decrement,
)