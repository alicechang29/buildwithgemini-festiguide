"""FestiGuide Web App backend.
Serves interactive festival scheduling, multi-day selection,
playlist/artist input, real GPS stage coordinates,
audio preview streams via iTunes Search, and dynamic alternative artist regeneration.
"""

import os
import sys
import json
import urllib.parse
import urllib.request
from typing import List, Optional

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
os.environ["GOOGLE_CLOUD_PROJECT"] = "qwiklabs-gcp-04-fba319c13e3d"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-east1"

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-04-fba319c13e3d"
db = firestore.Client(project=PROJECT_ID)

app = FastAPI(title="FestiGuide Interactive Map & Schedule App")

FESTIVAL_GEO_DATA = {
    "capitol_hill_block_party_2026": {
        "center": [47.6143, -122.3195],
        "zoom": 17,
        "stages": {
            "Main Stage (East Pike St)": {"lat": 47.6141, "lon": -122.3188, "color": "#ef4444", "desc": "Outdoor main stage on E Pike between 10th & 11th"},
            "Vera Stage": {"lat": 47.6152, "lon": -122.3210, "color": "#f59e0b", "desc": "Outdoor stage on 11th Ave near Pine"},
            "Neumos": {"lat": 47.6145, "lon": -122.3196, "color": "#8b5cf6", "desc": "Indoor iconic music venue (Air-Conditioned)"},
            "Barboza": {"lat": 47.6144, "lon": -122.3197, "color": "#ec4899", "desc": "Subterranean club below Neumos"},
            "Cha Cha Lounge": {"lat": 47.6143, "lon": -122.3201, "color": "#10b981", "desc": "Indoor lounge & cantina"}
        },
        "amenities": [
            {"name": "Food Trucks on 10th Ave", "lat": 47.6148, "lon": -122.3205, "type": "food", "icon": "restaurant"},
            {"name": "Hydration Station (10th & Pike)", "lat": 47.6142, "lon": -122.3202, "type": "water", "icon": "water_drop"},
            {"name": "Neumos Indoor Restrooms", "lat": 47.6146, "lon": -122.3194, "type": "wc", "icon": "wc"},
            {"name": "Local Eats: Tacos Chukis", "lat": 47.6149, "lon": -122.3190, "type": "food", "icon": "local_pizza"}
        ]
    },
    "coachella_2026": {
        "center": [33.6788, -116.2366],
        "zoom": 16,
        "stages": {
            "Coachella Stage": {"lat": 33.6775, "lon": -116.2335, "color": "#ef4444", "desc": "Main outdoor polo field stage"},
            "Outdoor Theatre": {"lat": 33.6800, "lon": -116.2350, "color": "#f59e0b", "desc": "Secondary open-air stage"},
            "Gobi": {"lat": 33.6820, "lon": -116.2370, "color": "#10b981", "desc": "Covered shaded tent"},
            "Mojave": {"lat": 33.6815, "lon": -116.2385, "color": "#3b82f6", "desc": "Covered shaded tent"},
            "Sahara Tent": {"lat": 33.6760, "lon": -116.2410, "color": "#8b5cf6", "desc": "High energy mega-structure tent"},
            "Sonora": {"lat": 33.6830, "lon": -116.2395, "color": "#06b6d4", "desc": "Air-conditioned indoor pavilion"},
            "Yuma": {"lat": 33.6770, "lon": -116.2425, "color": "#ec4899", "desc": "Air-conditioned nightclub tent"}
        },
        "amenities": [
            {"name": "Indio Central Market", "lat": 33.6780, "lon": -116.2355, "type": "food", "icon": "restaurant"},
            {"name": "Gobi Water Refill Hub", "lat": 33.6818, "lon": -116.2365, "type": "water", "icon": "water_drop"},
            {"name": "Sahara Restroom Cluster", "lat": 33.6755, "lon": -116.2405, "type": "wc", "icon": "wc"},
            {"name": "Permanent Restrooms (Mojave)", "lat": 33.6810, "lon": -116.2380, "type": "wc", "icon": "wc"}
        ]
    },
    "outside_lands_2026": {
        "center": [37.7695, -122.4862],
        "zoom": 16,
        "stages": {
            "Lands End": {"lat": 37.7685, "lon": -122.4930, "color": "#ef4444", "desc": "Polo Field main stage"},
            "Sutro": {"lat": 37.7720, "lon": -122.4880, "color": "#10b981", "desc": "Lindley Meadow amphitheater"},
            "Panhandle": {"lat": 37.7700, "lon": -122.4840, "color": "#f59e0b", "desc": "Speedway Meadow indie stage"},
            "Twin Peaks": {"lat": 37.7680, "lon": -122.4800, "color": "#3b82f6", "desc": "Hellman Hollow stage"},
            "SOMA Tent": {"lat": 37.7670, "lon": -122.4900, "color": "#8b5cf6", "desc": "Electronic dance nightclub tent"}
        },
        "amenities": [
            {"name": "Taste of the Bay", "lat": 37.7688, "lon": -122.4915, "type": "food", "icon": "restaurant"},
            {"name": "Choco Lands", "lat": 37.7695, "lon": -122.4850, "type": "food", "icon": "bakery_dining"},
            {"name": "Sutro Restrooms", "lat": 37.7725, "lon": -122.4885, "type": "wc", "icon": "wc"},
            {"name": "Polo Field Water Station", "lat": 37.7682, "lon": -122.4938, "type": "water", "icon": "water_drop"}
        ]
    },
    "lollapalooza_2026": {
        "center": [41.8745, -87.6190],
        "zoom": 15,
        "stages": {
            "Bud Light Stage": {"lat": 41.8810, "lon": -87.6195, "color": "#3b82f6", "desc": "North Field main stage"},
            "Perry's Stage": {"lat": 41.8780, "lon": -87.6215, "color": "#8b5cf6", "desc": "EDM Megastructure"},
            "Tito's Handmade Vodka Stage": {"lat": 41.8755, "lon": -87.6190, "color": "#f59e0b", "desc": "Petrillo Bandshell"},
            "Bacardi Stage": {"lat": 41.8740, "lon": -87.6170, "color": "#10b981", "desc": "Shaded Grove stage"},
            "T-Mobile Stage": {"lat": 41.8680, "lon": -87.6185, "color": "#ef4444", "desc": "South Field main stage"}
        },
        "amenities": [
            {"name": "Chow Town North", "lat": 41.8795, "lon": -87.6190, "type": "food", "icon": "restaurant"},
            {"name": "Chow Town South", "lat": 41.8700, "lon": -87.6180, "type": "food", "icon": "restaurant"},
            {"name": "Buckingham Fountain Hydration Hub", "lat": 41.8758, "lon": -87.6189, "type": "water", "icon": "water_drop"},
            {"name": "Main Restroom Banks", "lat": 41.8750, "lon": -87.6210, "type": "wc", "icon": "wc"}
        ]
    }
}

class GenerateRequest(BaseModel):
    festival_id: str
    selected_day: Optional[str] = None
    user_id: str = "alicechang94"
    custom_artists: Optional[List[str]] = None
    custom_genres: Optional[List[str]] = None
    pacing: str = "Moderate"
    diet_pref: str = "Casual & Quick Bites"

@app.get("/api/festivals")
async def get_festivals():
    docs = db.collection("festivals").stream()
    festivals = []
    for doc in docs:
        d = doc.to_dict()
        fid = d.get("id")
        festivals.append({
            "id": fid,
            "name": d.get("name"),
            "location": d.get("location"),
            "dates": d.get("dates"),
            "days": d.get("days", ["Friday (Day 1)"]),
            "weather": d.get("weather"),
            "geo_data": FESTIVAL_GEO_DATA.get(fid)
        })
    return festivals

@app.get("/api/user-profile")
async def get_user_profile(user_id: str = "alicechang94"):
    doc = db.collection("users").document(user_id).get()
    if not doc.exists:
        return {"user_id": user_id, "top_artists": [], "top_genres": [], "walking_pace": "Moderate", "diet_pref": "Casual & Quick Bites"}
    return doc.to_dict()

@app.get("/api/preview-track")
async def preview_track(artist: str):
    try:
        url = f"https://itunes.apple.com/search?term={urllib.parse.quote(artist)}&entity=musicTrack&limit=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=4) as response:
            res_data = json.loads(response.read().decode())
            results = res_data.get("results", [])
            if results:
                track = results[0]
                return {
                    "artist": artist,
                    "track_name": track.get("trackName"),
                    "preview_url": track.get("previewUrl"),
                    "artwork_url": track.get("artworkUrl100"),
                    "release_year": track.get("releaseDate", "")[:4]
                }
    except Exception as e:
        print(f"Error fetching preview for {artist}: {e}")
    
    return {
        "artist": artist,
        "track_name": "Preview unavailable",
        "preview_url": None,
        "artwork_url": None
    }

@app.post("/api/save-profile")
async def save_profile(req: Request):
    body = await req.json()
    user_id = body.get("user_id", "alicechang94")
    walking_pace = body.get("walking_pace", "Moderate")
    diet_pref = body.get("diet_pref", "Casual & Quick Bites")
    artists_raw = body.get("artists", "")
    
    user_ref = db.collection("users").document(user_id)
    doc = user_ref.get()
    current = doc.to_dict() if doc.exists else {}
    
    merged_artists = current.get("top_artists", [])
    if artists_raw:
        new_list = [a.strip() for a in artists_raw.replace("\n", ",").split(",") if a.strip()]
        merged_artists = list(dict.fromkeys(new_list + merged_artists))
    
    updated_data = {
        **current,
        "user_id": user_id,
        "walking_pace": walking_pace,
        "diet_pref": diet_pref,
        "top_artists": merged_artists,
        "all_liked_artists": list(set([a.lower() for a in merged_artists]))
    }
    user_ref.set(updated_data)
    return {"status": "success", "walking_pace": walking_pace, "diet_pref": diet_pref, "total_artists": len(merged_artists)}

@app.post("/api/generate-schedule")
async def generate_schedule(req: GenerateRequest):
    fest_doc = db.collection("festivals").document(req.festival_id).get()
    if not fest_doc.exists:
        return JSONResponse(status_code=404, content={"error": "Festival not found"})
    fest_data = fest_doc.to_dict()
    
    available_days = fest_data.get("days", ["Friday (Day 1)"])
    selected_day = req.selected_day or available_days[0]
    
    user_doc = db.collection("users").document(req.user_id).get()
    user_data = user_doc.to_dict() if user_doc.exists else {}
    
    artists_set = set(a.lower() for a in (req.custom_artists or user_data.get("top_artists", [])))
    user_genres = req.custom_genres or user_data.get("top_genres", [])
    
    pacing = req.pacing or user_data.get("walking_pace", "Moderate")
    diet = req.diet_pref or user_data.get("diet_pref", "Casual & Quick Bites")

    pace_multipliers = {
        "Speedy": 0.8,
        "Moderate": 1.15,
        "Leisurely": 1.6
    }
    mult = pace_multipliers.get(pacing, 1.15)
    
    full_lineup = fest_data.get("lineup", [])
    # Filter lineup to selected day
    day_lineup = [act for act in full_lineup if act.get("day") == selected_day]
    if not day_lineup:
        day_lineup = full_lineup  # fallback

    geo_data = FESTIVAL_GEO_DATA.get(req.festival_id, {})
    stages_coords = geo_data.get("stages", {})
    amenities = geo_data.get("amenities", [])
    
    # Classify acts
    scored_lineup = []
    for act in day_lineup:
        artist_name = act["artist"]
        genres = act.get("genres", [])
        is_favorite = any(artist_name.lower() in a or a in artist_name.lower() for a in artists_set)
        genre_match = any(g.lower() in [ug.lower() for ug in user_genres] for g in genres)
        
        if is_favorite:
            cat = "must_see"
            tag = "⭐ Must-See Favorite"
            reason = f"Direct match with your liked songs! Known for {', '.join(genres[:2])}."
            score = 10
        elif genre_match:
            cat = "discovery"
            tag = "✨ Discovery Gem"
            matched_g = [g for g in genres if any(ug.lower() == g.lower() for ug in user_genres)]
            reason = f"Vibe match with your taste in {', '.join(matched_g[:2])}."
            score = 6
        else:
            cat = "optional"
            tag = "🎵 Festival Highlight"
            reason = f"Renowned set on {act['stage']} ({', '.join(genres[:2])})."
            score = 2
            
        scored_lineup.append({**act, "cat": cat, "tag": tag, "reason": reason, "score": score})

    # Sort chronological
    sorted_lineup = sorted(scored_lineup, key=lambda x: x.get("start_time", "00:00"))
    
    # Select schedule
    if pacing == "Leisurely":
        # Keep top score favorites & discoveries
        selected_acts = [a for a in sorted_lineup if a["score"] >= 6]
        if len(selected_acts) < 3:
            selected_acts = sorted_lineup[:4]
    else:
        selected_acts = sorted_lineup

    timeline_items = []
    prev_stage = None
    
    food_amenity = next((a for a in amenities if a.get("type") == "food"), {"name": "Festival Food Village", "lat": geo_data.get("center", [0,0])[0], "lon": geo_data.get("center", [0,0])[1]})

    acted_count = 0
    for act in selected_acts:
        stage = act["stage"]
        stage_geo = stages_coords.get(stage, {"lat": geo_data.get("center", [0, 0])[0], "lon": geo_data.get("center", [0, 0])[1]})

        acted_count += 1
        if (pacing == "Leisurely" and acted_count == 2) or (pacing == "Moderate" and acted_count == 3):
            break_mins = 45 if "Sit-down" in diet else (25 if "Casual" in diet else 15)
            timeline_items.append({
                "type": "break",
                "title": f"🍽️ Wellness & Meal Break: {diet}",
                "location": food_amenity["name"],
                "duration_mins": break_mins,
                "lat": food_amenity["lat"],
                "lon": food_amenity["lon"],
                "note": f"Pacing preference ({pacing}): Grab food at {food_amenity['name']} and rehydrate before the next set."
            })
            prev_stage = None

        if prev_stage and prev_stage != stage:
            transit_key = f"{prev_stage} -> {stage}"
            rev_key = f"{stage} -> {prev_stage}"
            base_mins = fest_data.get("transit_times", {}).get(transit_key) or fest_data.get("transit_times", {}).get(rev_key) or 8
            calculated_mins = int(round(base_mins * mult))
            prev_geo = stages_coords.get(prev_stage, stage_geo)
            
            timeline_items.append({
                "type": "transit",
                "from_stage": prev_stage,
                "to_stage": stage,
                "duration_mins": calculated_mins,
                "start_coords": [prev_geo["lat"], prev_geo["lon"]],
                "end_coords": [stage_geo["lat"], stage_geo["lon"]],
                "note": f"{pacing} walk pace: ~{calculated_mins} mins transit from {prev_stage} to {stage}"
            })
        
        timeline_items.append({
            "type": "performance",
            "artist": act["artist"],
            "stage": stage,
            "day": selected_day,
            "start_time": act["start_time"],
            "end_time": act["end_time"],
            "category": act["cat"],
            "tag": act["tag"],
            "reason": act["reason"],
            "genres": act["genres"],
            "lat": stage_geo["lat"],
            "lon": stage_geo["lon"]
        })
        
        prev_stage = stage

    return {
        "festival": {
            "id": fest_data.get("id"),
            "name": fest_data.get("name"),
            "location": fest_data.get("location"),
            "dates": fest_data.get("dates"),
            "weather": fest_data.get("weather", {})
        },
        "days": available_days,
        "selected_day": selected_day,
        "day_lineup": day_lineup,
        "pacing": pacing,
        "diet_pref": diet,
        "geo_data": geo_data,
        "timeline": timeline_items
    }

app.mount("/", StaticFiles(directory="/config/Desktop/BuildWithGemini/frontend/static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
