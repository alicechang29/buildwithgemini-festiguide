# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types
from google.cloud import firestore

MODEL = "gemini-2.5-flash"
PROJECT_ID = "qwiklabs-gcp-04-fba319c13e3d"


def get_firestore_client():
    return firestore.Client(project=PROJECT_ID)


def list_available_festivals() -> str:
    """Lists all available music festivals with their locations and dates.
    Use this to see which festivals the user can choose from.

    Returns:
        A JSON string containing the list of festivals.
    """
    try:
        db = get_firestore_client()
        docs = db.collection("festivals").stream()
        festivals = []
        for doc in docs:
            d = doc.to_dict()
            festivals.append({
                "festival_id": d.get("id"),
                "name": d.get("name"),
                "location": d.get("location"),
                "dates": d.get("dates")
            })
        return json.dumps(festivals, indent=2)
    except Exception as e:
        return f"Error retrieving festivals: {str(e)}"


def get_user_music_profile(user_id: str = "alicechang94") -> str:
    """Retrieves the user's music taste profile derived from their liked songs,
    including their top favorite artists, liked genres, and overall musical vibe.

    Args:
        user_id: The ID of the user. Defaults to alicechang94.

    Returns:
        A JSON string containing the user's music taste profile.
    """
    try:
        db = get_firestore_client()
        doc = db.collection("users").document(user_id).get()
        if not doc.exists:
            return f"User profile {user_id} not found."
        data = doc.to_dict()
        profile_summary = {
            "user_id": data.get("user_id"),
            "vibe_summary": data.get("vibe_summary"),
            "top_genres": data.get("top_genres", [])[:15],
            "top_artists": data.get("top_artists", [])[:20],
            "total_liked_tracks": data.get("total_liked_tracks")
        }
        return json.dumps(profile_summary, indent=2)
    except Exception as e:
        return f"Error retrieving user profile: {str(e)}"


def get_festival_details_and_lineup(festival_id: str) -> str:
    """Retrieves comprehensive information about a festival including stages,
    walking transit times between stages, venue amenities (bathrooms, food hubs, hydration),
    weather forecast, and full lineup.

    Args:
        festival_id: ID of the festival, e.g. 'coachella_2026', 'outside_lands_2026', or 'lollapalooza_2026'.

    Returns:
        A JSON string with festival details, stages, transit times, amenities, weather, and lineup.
    """
    try:
        db = get_firestore_client()
        doc = db.collection("festivals").document(festival_id).get()
        if not doc.exists:
            return f"Festival {festival_id} not found. Call list_available_festivals() to see valid IDs."
        data = doc.to_dict()
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error retrieving festival details: {str(e)}"


INSTRUCTION = """You are FestiGuide, an intelligent festival itinerary planner and discovery concierge.
Your mission is to craft the ideal festival schedule tailored to the user's specific music tastes.

Here is how you operate:
1. When a user asks about festivals or wants a schedule:
   - Check the available festivals using `list_available_festivals` if not specified.
   - Look up their musical taste profile using `get_user_music_profile(user_id="alicechang94")`.
   - Retrieve the festival lineup, stage walking distances, amenities, and weather using `get_festival_details_and_lineup(festival_id)`.

2. Crafting the Schedule:
   - **Must-See Favorites**: Identify artists on the lineup that match the user's liked artists list.
   - **Discovery Gems**: Recommend artists whose genres/styles align with their taste (e.g. retro soul, lo-fi beats, neo soul, funk, nu disco) with a brief note on why they'll love them (e.g. 'If you like Anderson .Paak, check out...').
   - **Transit & Stage Navigation**: Account for walking times between stages. Don't schedule back-to-back sets across opposite sides of the venue without transit buffers.
   - **Rest, Food & Bathroom Logistics**:
     - Note the weather conditions (e.g. desert heat at Coachella vs fog/chill at Outside Lands).
     - Proactively schedule shaded breaks, water refill pitstops, and bathroom breaks near the stage they are departing or arriving at.
     - Recommend food clusters (e.g. Indio Central Market, Chow Town, Taste of the Bay) during mid-afternoon or before evening headliners.
   - **Format clearly**: Use clean chronological time blocks with artist, stage, why it was chosen (Favorite vs Discovery), and logistic tips (transit, shade, hydration).
"""

root_agent = Agent(
    name="festiguide_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=INSTRUCTION,
    tools=[list_available_festivals, get_user_music_profile, get_festival_details_and_lineup],
)

app = App(
    root_agent=root_agent,
    name="app",
)
