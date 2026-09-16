import asyncio

import streamlit as st
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from briefing_agent.agent import root_agent


APP_NAME = "daily_briefing_app"
USER_ID = "streamlit_user"


st.set_page_config(
    page_title="AI Daily Briefing",
    page_icon="📰",
    layout="wide",
)


st.title("📰 AI Daily Briefing Agent")
st.write(
    "Get a concise briefing using current news, weather, "
    "and financial information."
)


if "session_service" not in st.session_state:
    st.session_state.session_service = InMemorySessionService()


if "session_id" not in st.session_state:
    session = asyncio.run(
        st.session_state.session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
        )
    )
    st.session_state.session_id = session.id


topic = st.text_input(
    "What would you like in your briefing?",
    value="artificial intelligence news",
)

location = st.text_input(
    "Location for weather",
    value="Hyderabad",
)

symbol = st.text_input(
    "Stock symbol",
    value="JPM",
)


if st.button("Generate Briefing", type="primary"):

    prompt = f"""
Prepare my daily briefing.

Include:
- Current news about {topic}
- Current weather in {location}
- Recent market information for {symbol}

Use the structured briefing format.
Keep the response concise.
"""

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=st.session_state.session_service,
    )

    content = types.Content(
        role="user",
        parts=[
            types.Part(text=prompt),
        ],
    )

    async def run_agent():
        final_response = None

        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=st.session_state.session_id,
            new_message=content,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response = event.content.parts[0].text

        return final_response

    with st.spinner("Collecting information and preparing your briefing..."):
        try:
            response = asyncio.run(run_agent())

            if response:
                st.markdown(response)
            else:
                st.warning("The agent did not return a response.")

        except Exception as exc:
            st.error(f"Unable to generate the briefing: {exc}")