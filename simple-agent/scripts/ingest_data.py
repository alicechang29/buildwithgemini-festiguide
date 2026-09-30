import csv
import json
import os
from collections import Counter
from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-04-fba319c13e3d"
db = firestore.Client(project=PROJECT_ID)

def ingest_user_profile():
    tsv_path = "/config/Desktop/BuildWithGemini/simple-agent/data/user_liked_songs.tsv"
    artists = Counter()
    genres = Counter()
    all_liked_artists = set()
    sample_tracks = []
    
    with open(tsv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            artist_field = row.get('Artist Name(s)') or ''
            for a in artist_field.split(','):
                name = a.strip()
                if name:
                    artists[name] += 1
                    all_liked_artists.add(name.lower())
            genre_field = row.get('Genres') or ''
            for g in genre_field.split(','):
                name = g.strip().lower()
                if name:
                    genres[name] += 1
            if len(sample_tracks) < 20:
                sample_tracks.append({
                    "track": row.get("Track Name"),
                    "artist": artist_field,
                    "genres": genre_field,
                    "energy": row.get("Energy"),
                    "danceability": row.get("Danceability")
                })

    top_artists = [a for a, _ in artists.most_common(40)]
    top_genres = [g for g, _ in genres.most_common(25)]

    profile_data = {
        "user_id": "alicechang94",
        "top_artists": top_artists,
        "all_liked_artists": list(all_liked_artists),
        "top_genres": top_genres,
        "total_liked_tracks": sum(artists.values()),
        "vibe_summary": "Loves retro soul, funk, lo-fi beats, neo soul, R&B, and tropical house grooves.",
        "sample_tracks": sample_tracks
    }

    db.collection("users").document("alicechang94").set(profile_data)
    print("Ingested user profile for alicechang94 into Firestore!")

def ingest_festivals():
    festivals = [
        {
            "id": "coachella_2026",
            "name": "Coachella Valley Music and Arts Festival",
            "location": "Empire Polo Club, Indio, California",
            "dates": "April 10-12, 2026",
            "weather": {
                "afternoon": "Sunny & Hot, 94°F (34°C). Strong UV index, high heat from 1:00 PM to 5:00 PM. Hydration and shaded tents recommended.",
                "evening": "Pleasant & Breezy, 72°F (22°C) dropping to 60°F late night."
            },
            "stages": [
                {"name": "Coachella Stage", "type": "Outdoor Main Stage", "shade": "None (Full Sun until 6 PM)"},
                {"name": "Outdoor Theatre", "type": "Outdoor Secondary", "shade": "Partial Sun"},
                {"name": "Sahara Tent", "type": "Massive Enclosed Mega-Structure", "shade": "Full Shade / High Energy"},
                {"name": "Mojave", "type": "Covered Tent", "shade": "Full Shade"},
                {"name": "Gobi", "type": "Covered Tent", "shade": "Full Shade / Intimate / Indie"},
                {"name": "Sonora", "type": "Air-Conditioned Indoor Stage", "shade": "Air-Conditioned / Chill"},
                {"name": "Yuma", "type": "Air-Conditioned Nightclub Tent", "shade": "Dark / Air-Conditioned / House & Techno"}
            ],
            "transit_times": {
                "Coachella Stage -> Outdoor Theatre": 7,
                "Coachella Stage -> Sahara Tent": 15,
                "Coachella Stage -> Gobi": 10,
                "Coachella Stage -> Mojave": 9,
                "Coachella Stage -> Sonora": 12,
                "Coachella Stage -> Yuma": 14,
                "Outdoor Theatre -> Gobi": 6,
                "Outdoor Theatre -> Mojave": 5,
                "Outdoor Theatre -> Sahara Tent": 12,
                "Gobi -> Mojave": 4,
                "Mojave -> Sonora": 6,
                "Sahara Tent -> Yuma": 8,
                "Sonora -> Yuma": 7
            },
            "amenities": {
                "food_clusters": ["Central Market (near Mojave)", "Indio Central Market (shaded food hall near Coachella Stage)", "VIP Rose Garden"],
                "bathrooms": ["Permanent Restrooms south of Mojave", "Sahara Restroom Bank", "Main Stage West Portables"],
                "hydration_stations": ["Free Refill Station next to Gobi", "Central Market Refill Station", "Main Stage Entrance Station"]
            },
            "lineup": [
                {"day": "Day 1", "artist": "Anderson .Paak & The Free Nationals", "stage": "Coachella Stage", "start_time": "20:45", "end_time": "22:00", "genres": ["retro soul", "funk", "hip hop", "r&b"], "match_type": "Direct Favorite"},
                {"day": "Day 1", "artist": "The California Honeydrops", "stage": "Gobi", "start_time": "16:20", "end_time": "17:15", "genres": ["retro soul", "blues rock", "funk", "jam band"], "match_type": "Direct Favorite"},
                {"day": "Day 1", "artist": "berlioz", "stage": "Mojave", "start_time": "17:45", "end_time": "18:40", "genres": ["jazz beats", "lo-fi beats", "house", "nu disco"], "match_type": "Direct Favorite / High Affinity"},
                {"day": "Day 1", "artist": "Deep Chills", "stage": "Sahara Tent", "start_time": "15:00", "end_time": "15:50", "genres": ["tropical house", "deep house"], "match_type": "Direct Favorite"},
                {"day": "Day 1", "artist": "FKJ (French Kiwi Juice)", "stage": "Outdoor Theatre", "start_time": "19:15", "end_time": "20:15", "genres": ["neo soul", "nu jazz", "lo-fi beats", "electronic"], "match_type": "Direct Favorite / Top Discovery"},
                {"day": "Day 1", "artist": "Say She She", "stage": "Sonora", "start_time": "14:10", "end_time": "15:00", "genres": ["retro soul", "discodelic soul", "funk"], "match_type": "Discovery Gem (Matches retro soul / funk)"},
                {"day": "Day 1", "artist": "Sammy Rae & The Friends", "stage": "Gobi", "start_time": "18:00", "end_time": "18:55", "genres": ["pop soul", "funk", "jazz pop"], "match_type": "Discovery Gem (Matches Lawrence / Couch)"},
                {"day": "Day 1", "artist": "Jungle", "stage": "Outdoor Theatre", "start_time": "21:00", "end_time": "22:10", "genres": ["nu disco", "neo soul", "funk"], "match_type": "Discovery Gem (Matches disco / funk)"},
                {"day": "Day 1", "artist": "Barry Can't Swim", "stage": "Mojave", "start_time": "22:15", "end_time": "23:20", "genres": ["deep house", "jazz beats", "lo-fi"], "match_type": "Discovery Gem (Matches berlioz / lo-fi beats)"},
                {"day": "Day 1", "artist": "Bad Bunny", "stage": "Coachella Stage", "start_time": "23:00", "end_time": "00:45", "genres": ["reggaeton", "latin pop"], "match_type": "Festival Headliner"}
            ]
        },
        {
            "id": "outside_lands_2026",
            "name": "Outside Lands Music Festival",
            "location": "Golden Gate Park, San Francisco, California",
            "dates": "August 7-9, 2026",
            "weather": {
                "afternoon": "Cool & Foggy, 62°F (17°C). San Francisco marine layer 'Karl the Fog', brisk wind. Jacket recommended all day.",
                "evening": "Chilly & Windy, 53°F (12°C). Warm layers and hot food/drinks recommended."
            },
            "stages": [
                {"name": "Lands End", "type": "Polo Field Main Stage", "shade": "Open Meadow"},
                {"name": "Twin Peaks", "type": "Hellman Hollow Big Stage", "shade": "Open Meadow"},
                {"name": "Sutro", "type": "Lindley Meadow Natural Amphitheater", "shade": "Surrounded by Eucalyptus Trees"},
                {"name": "Panhandle", "type": "Speedway Meadow Intimate Stage", "shade": "Lush Trees / Indie & Soul"},
                {"name": "SOMA Tent", "type": "Nightclub Structure", "shade": "Enclosed / Electronic Dance"}
            ],
            "transit_times": {
                "Lands End -> Sutro": 10,
                "Lands End -> Twin Peaks": 18,
                "Lands End -> Panhandle": 12,
                "Sutro -> Panhandle": 6,
                "Sutro -> Twin Peaks": 12,
                "Panhandle -> Twin Peaks": 7
            },
            "amenities": {
                "food_clusters": ["Taste of the Bay (Polo Field)", "Choco Lands", "Cheese Lands"],
                "bathrooms": ["Sutro Meadow Portables", "Polo Field Bleachers Restrooms", "Twin Peaks North Restrooms"],
                "hydration_stations": ["Water stations at every meadow entry"]
            },
            "lineup": [
                {"day": "Day 1", "artist": "Lake Street Dive", "stage": "Sutro", "start_time": "17:30", "end_time": "18:30", "genres": ["retro soul", "pop soul", "jazz pop"], "match_type": "Direct Favorite"},
                {"day": "Day 1", "artist": "Leon Bridges", "stage": "Lands End", "start_time": "19:00", "end_time": "20:10", "genres": ["retro soul", "r&b", "southern soul"], "match_type": "Direct Favorite / Top Discovery"},
                {"day": "Day 1", "artist": "Neal Francis", "stage": "Panhandle", "start_time": "15:15", "end_time": "16:05", "genres": ["funk", "blues rock", "retro soul"], "match_type": "Discovery Gem (Matches The Dip / Honeydrops)"},
                {"day": "Day 1", "artist": "Tom Misch", "stage": "Twin Peaks", "start_time": "18:45", "end_time": "19:45", "genres": ["neo soul", "jazz beats", "lo-fi beats"], "match_type": "Direct Favorite"},
                {"day": "Day 1", "artist": "The Dip", "stage": "Panhandle", "start_time": "16:45", "end_time": "17:35", "genres": ["retro soul", "funk", "rhythm and blues"], "match_type": "Direct Favorite"},
                {"day": "Day 1", "artist": "Kaytranada", "stage": "Twin Peaks", "start_time": "20:30", "end_time": "21:45", "genres": ["electronic", "r&b", "nu disco"], "match_type": "Discovery Gem (Matches Anderson .Paak / Groovy beats)"}
            ]
        },
        {
            "id": "lollapalooza_2026",
            "name": "Lollapalooza",
            "location": "Grant Park, Chicago, Illinois",
            "dates": "July 30 - August 2, 2026",
            "weather": {
                "afternoon": "Humid & Hot, 88°F (31°C). High humidity, sunny, sudden lake breeze or summer thunderstorms.",
                "evening": "Warm & Humid, 76°F (24°C)."
            },
            "stages": [
                {"name": "Bud Light Stage", "type": "North Field Main Stage", "shade": "Open Lawn"},
                {"name": "T-Mobile Stage", "type": "South Field Main Stage", "shade": "Open Lawn"},
                {"name": "Tito's Handmade Vodka Stage", "type": "Petrillo Bandshell", "shade": "Covered Bandshell Seating"},
                {"name": "Perry's Stage", "type": "EDM Megastructure", "shade": "Enclosed / Electronic"},
                {"name": "Bacardi Stage", "type": "Grove / Shaded Stage", "shade": "Surrounded by Lakefront Trees"}
            ],
            "transit_times": {
                "T-Mobile Stage -> Bud Light Stage": 22,
                "T-Mobile Stage -> Tito's Handmade Vodka Stage": 12,
                "T-Mobile Stage -> Bacardi Stage": 9,
                "Bud Light Stage -> Perry's Stage": 11,
                "Bacardi Stage -> Perry's Stage": 10
            },
            "amenities": {
                "food_clusters": ["Chow Town North", "Chow Town South", "Dessert Island"],
                "bathrooms": ["Grant Park permanent restrooms + mega portable banks"],
                "hydration_stations": ["Buckingham Fountain Hydration Hub", "North Lawn Hydration Station"]
            },
            "lineup": [
                {"day": "Day 1", "artist": "Lawrence", "stage": "Bacardi Stage", "start_time": "16:45", "end_time": "17:45", "genres": ["pop soul", "funk", "retro soul"], "match_type": "Direct Favorite (#1 Top Artist)"},
                {"day": "Day 1", "artist": "St. Paul & The Broken Bones", "stage": "Tito's Handmade Vodka Stage", "start_time": "18:00", "end_time": "19:00", "genres": ["retro soul", "southern soul", "blues rock"], "match_type": "Direct Favorite"},
                {"day": "Day 1", "artist": "Doechii", "stage": "Perry's Stage", "start_time": "19:30", "end_time": "20:30", "genres": ["hip hop", "r&b", "rap"], "match_type": "Direct Favorite"},
                {"day": "Day 1", "artist": "Couch", "stage": "Bacardi Stage", "start_time": "14:30", "end_time": "15:20", "genres": ["pop soul", "funk", "indie soul"], "match_type": "Direct Favorite"},
                {"day": "Day 1", "artist": "Victoria Monét", "stage": "Bud Light Stage", "start_time": "20:15", "end_time": "21:15", "genres": ["r&b", "neo soul", "pop soul"], "match_type": "Discovery Gem (Matches retro soul / r&b)"}
            ]
        }
    ]

    for fest in festivals:
        db.collection("festivals").document(fest["id"]).set(fest)
        print(f"Ingested festival: {fest['name']}")

if __name__ == "__main__":
    ingest_user_profile()
    ingest_festivals()
    print("All seed data successfully stored in Firestore!")
