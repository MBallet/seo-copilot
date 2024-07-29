import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 SEO Copilot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT model to generate responses. "
)

openai_api_key = st.secrets["OPENAI_API_KEY"]
if not openai_api_key:
    st.info("No API Key Found", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Dropdown to select model
    model = st.selectbox(
        "Choose a model:",
        ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"]
    )

    # File uploader for reference files
    uploaded_files = st.file_uploader("Upload reference files", accept_multiple_files=True)
    reference_contents = {}
    if uploaded_files:
        for uploaded_file in uploaded_files:
            reference_contents[uploaded_file.name] = uploaded_file.getvalue().decode("utf-8")

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare the messages and files for the OpenAI API request
        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
        if reference_contents:
            messages.append({"role": "system", "content": str(reference_contents)})

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
