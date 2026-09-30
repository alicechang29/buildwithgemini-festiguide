import os
from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-04-fba319c13e3d"
db = firestore.Client(project=PROJECT_ID)

festivals = {
    "capitol_hill_block_party_2026": {
        "id": "capitol_hill_block_party_2026",
        "name": "Capitol Hill Block Party 2026",
        "location": "Capitol Hill, Seattle, WA",
        "dates": "July 24 - 26, 2026",
        "days": ["Friday (Day 1)", "Saturday (Day 2)", "Sunday (Day 3)"],
        "weather": {
            "afternoon": "Sunny, 77°F, low humidity",
            "evening": "Breezy Pacific Northwest twilight, 62°F"
        },
        "transit_times": {
            "Main Stage (East Pike St) -> Vera Stage": 4,
            "Vera Stage -> Neumos": 3,
            "Neumos -> Barboza": 1,
            "Barboza -> Cha Cha Lounge": 2,
            "Main Stage (East Pike St) -> Neumos": 2
        },
        "lineup": [
            # Day 1 - Friday
            {"artist": "Big Wild", "stage": "Main Stage (East Pike St)", "day": "Friday (Day 1)", "start_time": "21:15", "end_time": "22:30", "genres": ["electronic", "indie electronic", "funk", "groove"]},
            {"artist": "Joey Pecoraro", "stage": "Barboza", "day": "Friday (Day 1)", "start_time": "18:15", "end_time": "19:15", "genres": ["lo-fi beats", "jazz beats", "chillhop"]},
            {"artist": "Flamingosis", "stage": "Neumos", "day": "Friday (Day 1)", "start_time": "19:30", "end_time": "20:30", "genres": ["funk", "disco", "chillhop", "future funk"]},
            {"artist": "The Lagoons", "stage": "Vera Stage", "day": "Friday (Day 1)", "start_time": "17:00", "end_time": "18:00", "genres": ["indie pop", "retro soul", "synth pop"]},
            {"artist": "Couch", "stage": "Neumos", "day": "Friday (Day 1)", "start_time": "16:00", "end_time": "16:50", "genres": ["funk pop", "soul", "r&b"]},
            {"artist": "Chong the Nomad", "stage": "Vera Stage", "day": "Friday (Day 1)", "start_time": "15:00", "end_time": "15:45", "genres": ["electronic", "indie", "hip hop"]},
            {"artist": "Sudan Archives", "stage": "Main Stage (East Pike St)", "day": "Friday (Day 1)", "start_time": "19:45", "end_time": "20:45", "genres": ["r&b", "violin", "afrobeat"]},
            {"artist": "Sylvan Esso", "stage": "Main Stage (East Pike St)", "day": "Friday (Day 1)", "start_time": "18:00", "end_time": "19:00", "genres": ["electropop", "indie pop"]},
            {"artist": "Khruangbin (DJ Set)", "stage": "Barboza", "day": "Friday (Day 1)", "start_time": "20:45", "end_time": "22:00", "genres": ["psychedelic soul", "funk", "world"]},
            {"artist": "Balthvs", "stage": "Cha Cha Lounge", "day": "Friday (Day 1)", "start_time": "17:15", "end_time": "18:15", "genres": ["cumbia soul", "psychedelic funk", "chillhop"]},

            # Day 2 - Saturday
            {"artist": "Kaytranada", "stage": "Main Stage (East Pike St)", "day": "Saturday (Day 2)", "start_time": "21:30", "end_time": "23:00", "genres": ["electronic", "dance", "r&b", "funk"]},
            {"artist": "Remi Wolf", "stage": "Main Stage (East Pike St)", "day": "Saturday (Day 2)", "start_time": "19:45", "end_time": "20:45", "genres": ["indie pop", "funk pop", "neo soul"]},
            {"artist": "Channel Tres", "stage": "Neumos", "day": "Saturday (Day 2)", "start_time": "20:30", "end_time": "21:30", "genres": ["house", "hip hop", "west coast funk"]},
            {"artist": "Neil Frances", "stage": "Vera Stage", "day": "Saturday (Day 2)", "start_time": "18:30", "end_time": "19:30", "genres": ["indie electronic", "groove", "funk"]},
            {"artist": "Franc Moody", "stage": "Neumos", "day": "Saturday (Day 2)", "start_time": "17:15", "end_time": "18:15", "genres": ["nu-disco", "funk", "dance"]},
            {"artist": "The Dip", "stage": "Main Stage (East Pike St)", "day": "Saturday (Day 2)", "start_time": "16:30", "end_time": "17:30", "genres": ["retro soul", "r&b", "horn funk"]},
            {"artist": "Y La Bamba", "stage": "Cha Cha Lounge", "day": "Saturday (Day 2)", "start_time": "18:00", "end_time": "19:00", "genres": ["indie folk", "latin soul", "psychedelic"]},
            {"artist": "Sure Sure", "stage": "Barboza", "day": "Saturday (Day 2)", "start_time": "19:00", "end_time": "20:00", "genres": ["indie pop", "groove"]},

            # Day 3 - Sunday
            {"artist": "Leon Bridges", "stage": "Main Stage (East Pike St)", "day": "Sunday (Day 3)", "start_time": "20:45", "end_time": "22:15", "genres": ["retro soul", "r&b", "southern soul"]},
            {"artist": "Hiatus Kaiyote", "stage": "Main Stage (East Pike St)", "day": "Sunday (Day 3)", "start_time": "19:00", "end_time": "20:15", "genres": ["neo soul", "future jazz", "funk"]},
            {"artist": "Sammy Rae & The Friends", "stage": "Neumos", "day": "Sunday (Day 3)", "start_time": "18:00", "end_time": "19:15", "genres": ["funk", "soul rock", "jazz pop"]},
            {"artist": "Men I Trust", "stage": "Vera Stage", "day": "Sunday (Day 3)", "start_time": "17:15", "end_time": "18:15", "genres": ["indie pop", "lo-fi beats", "dream pop"]},
            {"artist": "Masego", "stage": "Neumos", "day": "Sunday (Day 3)", "start_time": "19:45", "end_time": "20:45", "genres": ["trap house jazz", "r&b", "saxophone soul"]},
            {"artist": "Ripe", "stage": "Barboza", "day": "Sunday (Day 3)", "start_time": "16:30", "end_time": "17:30", "genres": ["funk", "dance pop", "groove"]},
            {"artist": "Delvon Lamarr Organ Trio", "stage": "Cha Cha Lounge", "day": "Sunday (Day 3)", "start_time": "15:30", "end_time": "16:45", "genres": ["organ soul", "instrumental funk", "blues"]}
        ]
    },
    "coachella_2026": {
        "id": "coachella_2026",
        "name": "Coachella Valley Music and Arts Festival 2026",
        "location": "Empire Polo Club, Indio, CA",
        "dates": "April 17 - 19, 2026",
        "days": ["Friday (Day 1)", "Saturday (Day 2)", "Sunday (Day 3)"],
        "weather": {
            "afternoon": "Intense desert sunshine, 89°F",
            "evening": "Warm desert breeze, 74°F"
        },
        "transit_times": {
            "Coachella Stage -> Outdoor Theatre": 7,
            "Outdoor Theatre -> Gobi": 6,
            "Gobi -> Mojave": 4,
            "Mojave -> Sahara Tent": 11,
            "Sahara Tent -> Coachella Stage": 10,
            "Gobi -> Sonora": 5,
            "Sonora -> Yuma": 9
        },
        "lineup": [
            # Day 1
            {"artist": "Anderson .Paak & The Free Nationals", "stage": "Coachella Stage", "day": "Friday (Day 1)", "start_time": "21:30", "end_time": "23:00", "genres": ["retro soul", "funk", "hip hop", "r&b"]},
            {"artist": "The California Honeydrops", "stage": "Gobi", "day": "Friday (Day 1)", "start_time": "16:20", "end_time": "17:15", "genres": ["retro soul", "blues rock", "funk", "jam band"]},
            {"artist": "Berlioz", "stage": "Sonora", "day": "Friday (Day 1)", "start_time": "17:30", "end_time": "18:25", "genres": ["jazz house", "deep house", "chillhop"]},
            {"artist": "L'Impératrice", "stage": "Outdoor Theatre", "day": "Friday (Day 1)", "start_time": "18:40", "end_time": "19:35", "genres": ["french nu-disco", "funk", "synth pop"]},
            {"artist": "Jungle", "stage": "Mojave", "day": "Friday (Day 1)", "start_time": "20:00", "end_time": "21:05", "genres": ["nu-disco", "modern soul", "funk", "groove"]},
            {"artist": "Peggy Gou", "stage": "Sahara Tent", "day": "Friday (Day 1)", "start_time": "22:15", "end_time": "23:45", "genres": ["house", "disco", "techno"]},
            {"artist": "Chicano Batman", "stage": "Outdoor Theatre", "day": "Friday (Day 1)", "start_time": "15:15", "end_time": "16:05", "genres": ["psychedelic soul", "latin rock", "tropicalia"]},
            {"artist": "Say She She", "stage": "Gobi", "day": "Friday (Day 1)", "start_time": "14:15", "end_time": "15:05", "genres": ["discodelic soul", "harmonies", "funk"]},
            {"artist": "Folamour", "stage": "Yuma", "day": "Friday (Day 1)", "start_time": "19:00", "end_time": "20:30", "genres": ["french house", "disco funk", "groove"]},

            # Day 2
            {"artist": "Tyler, The Creator", "stage": "Coachella Stage", "day": "Saturday (Day 2)", "start_time": "22:30", "end_time": "00:00", "genres": ["hip hop", "neo soul", "funk"]},
            {"artist": "Bleachers", "stage": "Mojave", "day": "Saturday (Day 2)", "start_time": "19:30", "end_time": "20:30", "genres": ["indie pop", "heartland rock", "groove"]},
            {"artist": "Khruangbin", "stage": "Outdoor Theatre", "day": "Saturday (Day 2)", "start_time": "20:45", "end_time": "22:00", "genres": ["psychedelic soul", "thai funk", "dub"]},
            {"artist": "Parcels", "stage": "Gobi", "day": "Saturday (Day 2)", "start_time": "18:15", "end_time": "19:15", "genres": ["nu-disco", "funk", "electro-pop"]},
            {"artist": "SG Lewis", "stage": "Sahara Tent", "day": "Saturday (Day 2)", "start_time": "21:15", "end_time": "22:30", "genres": ["disco", "house", "synth funk"]},
            {"artist": "The Marías", "stage": "Sonora", "day": "Saturday (Day 2)", "start_time": "17:00", "end_time": "18:00", "genres": ["indie pop", "psychedelic soul", "dream pop"]},
            {"artist": "Cimafunk", "stage": "Gobi", "day": "Saturday (Day 2)", "start_time": "15:45", "end_time": "16:40", "genres": ["afro-cuban funk", "soul", "groove"]},

            # Day 3
            {"artist": "Doja Cat", "stage": "Coachella Stage", "day": "Sunday (Day 3)", "start_time": "22:00", "end_time": "23:30", "genres": ["hip hop", "pop", "r&b"]},
            {"artist": "Jhené Aiko", "stage": "Outdoor Theatre", "day": "Sunday (Day 3)", "start_time": "20:30", "end_time": "21:30", "genres": ["neo soul", "r&b", "ambient soul"]},
            {"artist": "BICEP", "stage": "Mojave", "day": "Sunday (Day 3)", "start_time": "21:45", "end_time": "23:00", "genres": ["electronic", "breakbeat", "house"]},
            {"artist": "Barry Can't Swim", "stage": "Gobi", "day": "Sunday (Day 3)", "start_time": "19:00", "end_time": "20:00", "genres": ["deep house", "jazz piano", "afrobeat"]},
            {"artist": "Victoria Monét", "stage": "Coachella Stage", "day": "Sunday (Day 3)", "start_time": "17:45", "end_time": "18:45", "genres": ["r&b", "funk", "traditional soul"]},
            {"artist": "Hermanos Gutiérrez", "stage": "Sonora", "day": "Sunday (Day 3)", "start_time": "16:15", "end_time": "17:15", "genres": ["desert guitar", "latin soul", "instrumental"]},
            {"artist": "Flight Facilities", "stage": "Sahara Tent", "day": "Sunday (Day 3)", "start_time": "18:00", "end_time": "19:15", "genres": ["indie dance", "electronic", "nu-disco"]}
        ]
    },
    "outside_lands_2026": {
        "id": "outside_lands_2026",
        "name": "Outside Lands Festival 2026",
        "location": "Golden Gate Park, San Francisco, CA",
        "dates": "August 7 - 9, 2026",
        "days": ["Friday (Day 1)", "Saturday (Day 2)", "Sunday (Day 3)"],
        "weather": {
            "afternoon": "Foggy marine layer breaking to sun, 64°F",
            "evening": "Chilly Karl the Fog rolls in, 54°F (Jacket recommended)"
        },
        "transit_times": {
            "Lands End -> Sutro": 6,
            "Sutro -> Panhandle": 8,
            "Panhandle -> Twin Peaks": 5,
            "Twin Peaks -> Lands End": 14,
            "Lands End -> SOMA Tent": 5
        },
        "lineup": [
            # Day 1
            {"artist": "Lake Street Dive", "stage": "Sutro", "day": "Friday (Day 1)", "start_time": "17:30", "end_time": "18:30", "genres": ["retro soul", "pop soul", "jazz pop"]},
            {"artist": "Leon Bridges", "stage": "Lands End", "day": "Friday (Day 1)", "start_time": "19:00", "end_time": "20:10", "genres": ["retro soul", "r&b", "southern soul"]},
            {"artist": "The Killers", "stage": "Lands End", "day": "Friday (Day 1)", "start_time": "20:45", "end_time": "22:00", "genres": ["indie rock", "alternative"]},
            {"artist": "Samm Henshaw", "stage": "Panhandle", "day": "Friday (Day 1)", "start_time": "16:15", "end_time": "17:05", "genres": ["gospel soul", "r&b", "funk"]},
            {"artist": "Shiba San", "stage": "SOMA Tent", "day": "Friday (Day 1)", "start_time": "18:30", "end_time": "20:00", "genres": ["bass house", "tech house", "funk"]},
            {"artist": "Daniel Caesar", "stage": "Twin Peaks", "day": "Friday (Day 1)", "start_time": "19:45", "end_time": "20:45", "genres": ["r&b", "neo soul", "smooth"]},

            # Day 2
            {"artist": "Sabrina Carpenter", "stage": "Lands End", "day": "Saturday (Day 2)", "start_time": "20:30", "end_time": "22:00", "genres": ["pop", "disco pop", "groove"]},
            {"artist": "Grace Potter", "stage": "Sutro", "day": "Saturday (Day 2)", "start_time": "17:45", "end_time": "18:45", "genres": ["blues rock", "southern soul", "roots"]},
            {"artist": "Men I Trust", "stage": "Twin Peaks", "day": "Saturday (Day 2)", "start_time": "18:30", "end_time": "19:30", "genres": ["lo-fi beats", "indie pop", "dream pop"]},
            {"artist": "Mindchatter", "stage": "Panhandle", "day": "Saturday (Day 2)", "start_time": "16:00", "end_time": "17:00", "genres": ["indie electronic", "chillhop", "funk"]},
            {"artist": "Channel Tres (Live)", "stage": "Twin Peaks", "day": "Saturday (Day 2)", "start_time": "19:45", "end_time": "20:45", "genres": ["house", "west coast funk", "hip hop"]},

            # Day 3
            {"artist": "Sturgill Simpson", "stage": "Lands End", "day": "Sunday (Day 3)", "start_time": "20:15", "end_time": "21:45", "genres": ["roots rock", "country soul", "blues"]},
            {"artist": "Chappell Roan", "stage": "Lands End", "day": "Sunday (Day 3)", "start_time": "18:00", "end_time": "19:15", "genres": ["synth pop", "dance", "glam"]},
            {"artist": "Kaytranada", "stage": "Twin Peaks", "day": "Sunday (Day 3)", "start_time": "20:15", "end_time": "21:30", "genres": ["electronic", "r&b", "funk"]},
            {"artist": "Corinne Bailey Rae", "stage": "Sutro", "day": "Sunday (Day 3)", "start_time": "17:15", "end_time": "18:15", "genres": ["neo soul", "r&b", "jazz pop"]},
            {"artist": "Postmodern Jukebox", "stage": "Panhandle", "day": "Sunday (Day 3)", "start_time": "15:45", "end_time": "16:45", "genres": ["vintage jazz", "retro swing", "soul"]}
        ]
    },
    "lollapalooza_2026": {
        "id": "lollapalooza_2026",
        "name": "Lollapalooza Chicago 2026",
        "location": "Grant Park, Chicago, IL",
        "dates": "July 30 - August 2, 2026",
        "days": ["Thursday (Day 1)", "Friday (Day 2)", "Saturday (Day 3)", "Sunday (Day 4)"],
        "weather": {
            "afternoon": "Midwest summer warmth, 82°F with Lake Michigan breeze",
            "evening": "Mild lakefront night, 69°F"
        },
        "transit_times": {
            "Bud Light Stage -> Perry's Stage": 5,
            "Perry's Stage -> Tito's Handmade Vodka Stage": 6,
            "Tito's Handmade Vodka Stage -> Bacardi Stage": 4,
            "Bacardi Stage -> T-Mobile Stage": 8,
            "Bud Light Stage -> T-Mobile Stage": 16
        },
        "lineup": [
            # Day 1
            {"artist": "Lawrence", "stage": "Bacardi Stage", "day": "Thursday (Day 1)", "start_time": "16:45", "end_time": "17:45", "genres": ["pop soul", "funk", "retro soul"]},
            {"artist": "St. Paul & The Broken Bones", "stage": "Tito's Handmade Vodka Stage", "day": "Thursday (Day 1)", "start_time": "18:00", "end_time": "19:00", "genres": ["retro soul", "southern soul", "blues rock"]},
            {"artist": "Tyler, The Creator", "stage": "T-Mobile Stage", "day": "Thursday (Day 1)", "start_time": "20:30", "end_time": "22:00", "genres": ["hip hop", "neo soul", "funk"]},
            {"artist": "Hozier", "stage": "Bud Light Stage", "day": "Thursday (Day 1)", "start_time": "20:45", "end_time": "22:00", "genres": ["blues soul", "indie rock", "folk"]},
            {"artist": "Fisher", "stage": "Perry's Stage", "day": "Thursday (Day 1)", "start_time": "19:15", "end_time": "20:30", "genres": ["tech house", "dance", "bass"]},

            # Day 2
            {"artist": "SZA", "stage": "T-Mobile Stage", "day": "Friday (Day 2)", "start_time": "20:30", "end_time": "22:00", "genres": ["r&b", "neo soul", "contemporary r&b"]},
            {"artist": "Stray Kids", "stage": "Bud Light Stage", "day": "Friday (Day 2)", "start_time": "20:30", "end_time": "22:00", "genres": ["dance", "k-pop", "electronic"]},
            {"artist": "Reneé Rapp", "stage": "Tito's Handmade Vodka Stage", "day": "Friday (Day 2)", "start_time": "17:30", "end_time": "18:30", "genres": ["pop soul", "r&b", "ballad"]},
            {"artist": "Victoria Monét", "stage": "Bacardi Stage", "day": "Friday (Day 2)", "start_time": "18:45", "end_time": "19:45", "genres": ["r&b", "funk", "groove"]},
            {"artist": "Galantis", "stage": "Perry's Stage", "day": "Friday (Day 2)", "start_time": "19:30", "end_time": "20:45", "genres": ["dance pop", "house", "electro"]},

            # Day 3
            {"artist": "The Killers", "stage": "T-Mobile Stage", "day": "Saturday (Day 3)", "start_time": "20:30", "end_time": "22:00", "genres": ["rock", "synth pop", "alternative"]},
            {"artist": "Future X Metro Boomin", "stage": "Bud Light Stage", "day": "Saturday (Day 3)", "start_time": "20:45", "end_time": "22:00", "genres": ["hip hop", "trap"]},
            {"artist": "Deftones", "stage": "Bud Light Stage", "day": "Saturday (Day 3)", "start_time": "18:45", "end_time": "19:45", "genres": ["alternative rock", "metal"]},
            {"artist": "Tate McRae", "stage": "T-Mobile Stage", "day": "Saturday (Day 3)", "start_time": "17:00", "end_time": "18:00", "genres": ["dance pop", "pop"]},
            {"artist": "Skrillex", "stage": "Perry's Stage", "day": "Saturday (Day 3)", "start_time": "19:30", "end_time": "21:00", "genres": ["electronic", "dubstep", "house"]},

            # Day 4
            {"artist": "Blink-182", "stage": "T-Mobile Stage", "day": "Sunday (Day 4)", "start_time": "20:30", "end_time": "22:00", "genres": ["pop punk", "rock"]},
            {"artist": "Melanie Martinez", "stage": "Bud Light Stage", "day": "Sunday (Day 4)", "start_time": "20:30", "end_time": "22:00", "genres": ["alt-pop", "art pop"]},
            {"artist": "Conan Gray", "stage": "T-Mobile Stage", "day": "Sunday (Day 4)", "start_time": "18:15", "end_time": "19:15", "genres": ["indie pop", "retro pop"]},
            {"artist": "Pierce the Veil", "stage": "Tito's Handmade Vodka Stage", "day": "Sunday (Day 4)", "start_time": "17:00", "end_time": "18:00", "genres": ["post-hardcore", "rock"]},
            {"artist": "Zeds Dead", "stage": "Perry's Stage", "day": "Sunday (Day 4)", "start_time": "19:15", "end_time": "20:45", "genres": ["bass music", "electronic", "dubstep"]}
        ]
    }
}

for fest_id, doc_data in festivals.items():
    db.collection("festivals").document(fest_id).set(doc_data)
    print(f"Seeded {fest_id} with {len(doc_data['lineup'])} acts across {len(doc_data['days'])} days.")
