import asyncio
import streamlit as st
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import root_agent

load_dotenv()

st.set_page_config(page_title="SG Transport Agent", page_icon="🇸🇬", layout="centered")

st.title("Singapore Transport Route Recommender")
st.markdown("Enter your start and end locations in Singapore to get the best route recommendations via MRT, Bus, Taxi, Cycling & Walking.")

start_location = st.text_input("Start Location", placeholder="e.g. Jurong East")
end_location = st.text_input("End Location", placeholder="e.g. Changi Airport")


async def run_agent(start: str, end: str) -> str:
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="transport_agent",
        user_id="streamlit_user",
    )

    runner = Runner(
        agent=root_agent,
        app_name="transport_agent",
        session_service=session_service,
    )

    user_message = f"I need to travel from {start} to {end}. Please recommend the best transport route."

    content = types.Content(
        role="user",
        parts=[types.Part(text=user_message)],
    )

    final_response = ""
    async for event in runner.run_async(
        user_id="streamlit_user",
        session_id=session.id,
        new_message=content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    final_response += part.text

    return final_response


if st.button("Find Best Route", type="primary", disabled=not (start_location and end_location)):
    if start_location and end_location:
        with st.spinner("Researching MRT, Bus, Taxi, Cycling & Walking options..."):
            result = asyncio.run(run_agent(start_location, end_location))
        if result:
            st.markdown("---")
            st.subheader("Route Recommendations")
            st.markdown(result)
        else:
            st.warning("No results returned. Please try again.")
