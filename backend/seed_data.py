"""
Seed Data Script
Creates initial data: admin user, genres, real-world developers and their popular games
Run with: python -m backend.seed_data
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal, engine, Base
from backend import models
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def seed_database():
    # Drop all tables and recreate
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        print("Seeding database with real-world data...")

        # Create Genres
        genres_data = [
            {"name": "Action", "slug": "action", "description": "Fast-paced action games with combat and challenges"},
            {"name": "Adventure", "slug": "adventure", "description": "Story-driven exploration and discovery games"},
            {"name": "RPG", "slug": "rpg", "description": "Role-playing games with character progression"},
            {"name": "Strategy", "slug": "strategy", "description": "Strategic thinking and planning games"},
            {"name": "Simulation", "slug": "simulation", "description": "Real-life simulation experiences"},
            {"name": "Sports", "slug": "sports", "description": "Sports and athletic competition games"},
            {"name": "Racing", "slug": "racing", "description": "High-speed racing experiences"},
            {"name": "Puzzle", "slug": "puzzle", "description": "Brain-teasing puzzle games"},
            {"name": "Horror", "slug": "horror", "description": "Scary and suspenseful horror games"},
            {"name": "Indie", "slug": "indie", "description": "Independent developer creations"},
            {"name": "Multiplayer", "slug": "multiplayer", "description": "Online multiplayer experiences"},
            {"name": "Free to Play", "slug": "free-to-play", "description": "Free-to-play games"},
            {"name": "Shooter", "slug": "shooter", "description": "First and third-person shooter games"},
            {"name": "Open World", "slug": "open-world", "description": "Open world exploration games"},
            {"name": "Survival", "slug": "survival", "description": "Survival and crafting games"},
            {"name": "Fighting", "slug": "fighting", "description": "Fighting and combat games"},
            {"name": "Platformer", "slug": "platformer", "description": "Platform jumping games"},
            {"name": "Sandbox", "slug": "sandbox", "description": "Creative sandbox games"},
            {"name": "Roguelike", "slug": "roguelike", "description": "Procedurally generated levels and permadeath"},
            {"name": "Metroidvania", "slug": "metroidvania", "description": "Action-adventure with guided non-linearity"},
            {"name": "Card Game", "slug": "card-game", "description": "Strategy games using cards"},
        ]

        genres = {}
        for g in genres_data:
            genre = models.Genre(**g)
            db.add(genre)
            db.flush()
            genres[g["name"]] = genre

        print(f"Created {len(genres)} genres")

        # Create Admin User
        admin = models.User(
            username="admin",
            email="admin@gamestore.com",
            hashed_password=hash_password("admin123"),
            role=models.UserRole.ADMIN,
            display_name="Store Administrator",
            bio="Game Store Administrator"
        )
        db.add(admin)
        db.flush()

        # Create Test User
        test_user = models.User(
            username="player",
            email="player@gamestore.com",
            hashed_password=hash_password("player123"),
            role=models.UserRole.USER,
            display_name="Player One",
            bio="Passionate gamer and collector"
        )
        db.add(test_user)
        db.flush()

        # Real-World Developers
        developers_data = [
            {
                "username": "rockstar_games",
                "email": "contact@rockstargames.com",
                "developer_name": "Rockstar Games",
                "display_name": "Rockstar Games",
                "bio": "Publishers of Grand Theft Auto, Red Dead Redemption, and other iconic franchises.",
                "developer_verified": True
            },
            {
                "username": "cdprojekt",
                "email": "contact@cdprojektred.com",
                "developer_name": "CD Projekt Red",
                "display_name": "CD Projekt Red",
                "bio": "Polish game development studio behind The Witcher series and Cyberpunk 2077.",
                "developer_verified": True
            },
            {
                "username": "bethesda",
                "email": "contact@bethesda.net",
                "developer_name": "Bethesda Game Studios",
                "display_name": "Bethesda Game Studios",
                "bio": "Creators of The Elder Scrolls and Fallout series.",
                "developer_verified": True
            },
            {
                "username": "valve",
                "email": "contact@valvesoftware.com",
                "developer_name": "Valve Corporation",
                "display_name": "Valve",
                "bio": "Creators of Half-Life, Portal, Counter-Strike, and Steam.",
                "developer_verified": True
            },
            {
                "username": "fromsoftware",
                "email": "contact@fromsoftware.jp",
                "developer_name": "FromSoftware",
                "display_name": "FromSoftware",
                "bio": "Japanese studio known for Dark Souls, Bloodborne, and Elden Ring.",
                "developer_verified": True
            },
            {
                "username": "ubisoft",
                "email": "contact@ubisoft.com",
                "developer_name": "Ubisoft",
                "display_name": "Ubisoft",
                "bio": "French publisher of Assassin's Creed, Far Cry, and Rainbow Six.",
                "developer_verified": True
            },
            {
                "username": "ea_games",
                "email": "contact@ea.com",
                "developer_name": "Electronic Arts",
                "display_name": "EA Games",
                "bio": "One of the world's largest game publishers.",
                "developer_verified": True
            },
            {
                "username": "naughtydog",
                "email": "contact@naughtydog.com",
                "developer_name": "Naughty Dog",
                "display_name": "Naughty Dog",
                "bio": "Creators of Uncharted and The Last of Us.",
                "developer_verified": True
            },
            {
                "username": "insomniac",
                "email": "contact@insomniacgames.com",
                "developer_name": "Insomniac Games",
                "display_name": "Insomniac Games",
                "bio": "Developers of Spider-Man, Ratchet & Clank, and Spyro.",
                "developer_verified": True
            },
            {
                "username": "mojang",
                "email": "contact@mojang.com",
                "developer_name": "Mojang Studios",
                "display_name": "Mojang Studios",
                "bio": "Swedish video game developer, creator of Minecraft.",
                "developer_verified": True
            },
            {
                "username": "re_logic",
                "email": "contact@re-logic.com",
                "developer_name": "Re-Logic",
                "display_name": "Re-Logic",
                "bio": "Independent game studio, creators of Terraria.",
                "developer_verified": True
            },
            {
                "username": "concerned_ape",
                "email": "eric@stardewvalley.net",
                "developer_name": "ConcernedApe",
                "display_name": "ConcernedApe (Eric Barone)",
                "bio": "Solo developer of the beloved farming simulator Stardew Valley.",
                "developer_verified": True
            },
            {
                "username": "supergiant",
                "email": "contact@supergiantgames.com",
                "developer_name": "Supergiant Games",
                "display_name": "Supergiant Games",
                "bio": "Indie studio known for Bastion, Transistor, and Hades.",
                "developer_verified": True
            },
            {
                "username": "team_cherry",
                "email": "contact@teamcherry.com.au",
                "developer_name": "Team Cherry",
                "display_name": "Team Cherry",
                "bio": "Australian indie studio behind Hollow Knight.",
                "developer_verified": True
            },
            {
                "username": "capcom",
                "email": "contact@capcom.com",
                "developer_name": "Capcom",
                "display_name": "Capcom",
                "bio": "Japanese publisher of Resident Evil, Monster Hunter, and Street Fighter.",
                "developer_verified": True
            },
            {
                "username": "battlefield_studios",
                "email": "contact@battlefield_studios.com",
                "developer_name": "Battlefield Studios",
                "display_name": "Battlefield Studios",
                "bio": "Creators of Battlefield 6 and other titles.",
                "developer_verified": True
            },
            {
                "username": "sandfall_interactive",
                "email": "contact@sandfall_interactive.com",
                "developer_name": "Sandfall Interactive",
                "display_name": "Sandfall Interactive",
                "bio": "Creators of Clair Obscur: Expedition 33 and other titles.",
                "developer_verified": True
            },
            {
                "username": "treyarch",
                "email": "contact@treyarch.com",
                "developer_name": "Treyarch",
                "display_name": "Treyarch",
                "bio": "Creators of Call of Duty: Black Ops 7 and other titles.",
                "developer_verified": True
            },
            {
                "username": "warhorse_studios",
                "email": "contact@warhorse_studios.com",
                "developer_name": "Warhorse Studios",
                "display_name": "Warhorse Studios",
                "bio": "Creators of Kingdom Come: Deliverance II and other titles.",
                "developer_verified": True
            },
            {
                "username": "sucker_punch",
                "email": "contact@sucker_punch.com",
                "developer_name": "Sucker Punch",
                "display_name": "Sucker Punch",
                "bio": "Creators of Ghost of Y\u014dtei and other titles.",
                "developer_verified": True
            },
            {
                "username": "firaxis_games",
                "email": "contact@firaxis_games.com",
                "developer_name": "Firaxis Games",
                "display_name": "Firaxis Games",
                "bio": "Creators of Civilization VII and other titles.",
                "developer_verified": True
            },
            {
                "username": "kojima_productions",
                "email": "contact@kojima_productions.com",
                "developer_name": "Kojima Productions",
                "display_name": "Kojima Productions",
                "bio": "Creators of Death Stranding 2: On The Beach and other titles.",
                "developer_verified": True
            },
            {
                "username": "obsidian_entertainment",
                "email": "contact@obsidian_entertainment.com",
                "developer_name": "Obsidian Entertainment",
                "display_name": "Obsidian Entertainment",
                "bio": "Creators of Avowed and other titles.",
                "developer_verified": True
            },
            {
                "username": "compulsion_games",
                "email": "contact@compulsion_games.com",
                "developer_name": "Compulsion Games",
                "display_name": "Compulsion Games",
                "bio": "Creators of South of Midnight and other titles.",
                "developer_verified": True
            },
            {
                "username": "dogubomb",
                "email": "contact@dogubomb.com",
                "developer_name": "Dogubomb",
                "display_name": "Dogubomb",
                "bio": "Creators of Blue Prince and other titles.",
                "developer_verified": True
            },
            {
                "username": "nintendo_epd",
                "email": "contact@nintendo_epd.com",
                "developer_name": "Nintendo EPD",
                "display_name": "Nintendo EPD",
                "bio": "Creators of Donkey Kong Bananza and other titles.",
                "developer_verified": True
            },
            {
                "username": "embark_studios",
                "email": "contact@embark_studios.com",
                "developer_name": "Embark Studios",
                "display_name": "Embark Studios",
                "bio": "Creators of ARC Raiders and other titles.",
                "developer_verified": True
            },
            {
                "username": "everstone_studio",
                "email": "contact@everstone_studio.com",
                "developer_name": "Everstone Studio",
                "display_name": "Everstone Studio",
                "bio": "Creators of Where Winds Meet and other titles.",
                "developer_verified": True
            },
            {
                "username": "intrepid_studios",
                "email": "contact@intrepid_studios.com",
                "developer_name": "Intrepid Studios",
                "display_name": "Intrepid Studios",
                "bio": "Creators of Ashes of Creation and other titles.",
                "developer_verified": True
            },
            {
                "username": "snk",
                "email": "contact@snk.com",
                "developer_name": "SNK",
                "display_name": "SNK",
                "bio": "Creators of Fatal Fury: City of the Wolves and other titles.",
                "developer_verified": True
            },
            {
                "username": "gearbox_software",
                "email": "contact@gearbox_software.com",
                "developer_name": "Gearbox Software",
                "display_name": "Gearbox Software",
                "bio": "Creators of Borderlands 4 and other titles.",
                "developer_verified": True
            },
            {
                "username": "visual_concepts",
                "email": "contact@visual_concepts.com",
                "developer_name": "Visual Concepts",
                "display_name": "Visual Concepts",
                "bio": "Creators of NBA 2K26 and other titles.",
                "developer_verified": True
            },
            {
                "username": "san_diego_studio",
                "email": "contact@san_diego_studio.com",
                "developer_name": "San Diego Studio",
                "display_name": "San Diego Studio",
                "bio": "Creators of MLB The Show 25 and other titles.",
                "developer_verified": True
            },
            {
                "username": "rebellion",
                "email": "contact@rebellion.com",
                "developer_name": "Rebellion",
                "display_name": "Rebellion",
                "bio": "Creators of Sniper Elite: Resistance and other titles.",
                "developer_verified": True
            },
            {
                "username": "omega_force",
                "email": "contact@omega_force.com",
                "developer_name": "Omega Force",
                "display_name": "Omega Force",
                "bio": "Creators of Dynasty Warriors Origins and other titles.",
                "developer_verified": True
            },
            {
                "username": "neople",
                "email": "contact@neople.com",
                "developer_name": "Neople",
                "display_name": "Neople",
                "bio": "Creators of The First Berserker: Khazan and other titles.",
                "developer_verified": True
            },
            {
                "username": "two_point_studios",
                "email": "contact@two_point_studios.com",
                "developer_name": "Two Point Studios",
                "display_name": "Two Point Studios",
                "bio": "Creators of Two Point Museum and other titles.",
                "developer_verified": True
            },
            {
                "username": "bad_guitar_studio",
                "email": "contact@bad_guitar_studio.com",
                "developer_name": "Bad Guitar Studio",
                "display_name": "Bad Guitar Studio",
                "bio": "Creators of FragPunk and other titles.",
                "developer_verified": True
            },
            {
                "username": "konami",
                "email": "contact@konami.com",
                "developer_name": "Konami",
                "display_name": "Konami",
                "bio": "Creators of Suikoden I & II HD Remaster and other titles.",
                "developer_verified": True
            },
            {
                "username": "jump_over_the_age",
                "email": "contact@jump_over_the_age.com",
                "developer_name": "Jump Over The Age",
                "display_name": "Jump Over The Age",
                "bio": "Creators of Citizen Sleeper 2 and other titles.",
                "developer_verified": True
            },
            {
                "username": "dont_nod",
                "email": "contact@dont_nod.com",
                "developer_name": "Don't Nod",
                "display_name": "Don't Nod",
                "bio": "Creators of Lost Records: Bloom & Rage and other titles.",
                "developer_verified": True
            },
            {
                "username": "milestone",
                "email": "contact@milestone.com",
                "developer_name": "Milestone",
                "display_name": "Milestone",
                "bio": "Creators of Monster Energy Supercross 25 and other titles.",
                "developer_verified": True
            },
            {
                "username": "bend_studio",
                "email": "contact@bend_studio.com",
                "developer_name": "Bend Studio",
                "display_name": "Bend Studio",
                "bio": "Creators of Days Gone Remastered and other titles.",
                "developer_verified": True
            },
            {
                "username": "2d_boy",
                "email": "contact@2d_boy.com",
                "developer_name": "2D Boy",
                "display_name": "2D Boy",
                "bio": "Creators of World of Goo 2 and other titles.",
                "developer_verified": True
            },
            {
                "username": "slipgate_ironworks",
                "email": "contact@slipgate_ironworks.com",
                "developer_name": "Slipgate Ironworks",
                "display_name": "Slipgate Ironworks",
                "bio": "Creators of Tempest Rising and other titles.",
                "developer_verified": True
            },
            {
                "username": "storm_in_a_teacup",
                "email": "contact@storm_in_a_teacup.com",
                "developer_name": "Storm in a Teacup",
                "display_name": "Storm in a Teacup",
                "bio": "Creators of Steel Seed and other titles.",
                "developer_verified": True
            },
            {
                "username": "red_soul_games",
                "email": "contact@red_soul_games.com",
                "developer_name": "Red Soul Games",
                "display_name": "Red Soul Games",
                "bio": "Creators of Post Trauma and other titles.",
                "developer_verified": True
            },
            {
                "username": "game_arts",
                "email": "contact@game_arts.com",
                "developer_name": "Game Arts",
                "display_name": "Game Arts",
                "bio": "Creators of Lunar Remastered Collection and other titles.",
                "developer_verified": True
            },
            {
                "username": "machinegames",
                "email": "contact@machinegames.com",
                "developer_name": "MachineGames",
                "display_name": "MachineGames",
                "bio": "Creators of Indiana Jones & The Great Circle and other titles.",
                "developer_verified": True
            },
            {
                "username": "psychoflow",
                "email": "contact@psychoflow.com",
                "developer_name": "Psychoflow",
                "display_name": "Psychoflow",
                "bio": "Creators of Bionic Bay and other titles.",
                "developer_verified": True
            },
            {
                "username": "netease",
                "email": "contact@netease.com",
                "developer_name": "NetEase",
                "display_name": "NetEase",
                "bio": "Creators of Rusty Rabbit and other titles.",
                "developer_verified": True
            },
            {
                "username": "sports_interactive",
                "email": "contact@sports_interactive.com",
                "developer_name": "Sports Interactive",
                "display_name": "Sports Interactive",
                "bio": "Creators of Football Manager 2025 and other titles.",
                "developer_verified": True
            },
            {
                "username": "game_science",
                "email": "contact@game_science.com",
                "developer_name": "Game Science",
                "display_name": "Game Science",
                "bio": "Creators of Black Myth: Wukong and other titles.",
                "developer_verified": True
            },
            {
                "username": "arrowhead",
                "email": "contact@arrowhead.com",
                "developer_name": "Arrowhead",
                "display_name": "Arrowhead",
                "bio": "Creators of Helldivers 2 and other titles.",
                "developer_verified": True
            },
            {
                "username": "pocketpair",
                "email": "contact@pocketpair.com",
                "developer_name": "Pocketpair",
                "display_name": "Pocketpair",
                "bio": "Creators of Palworld and other titles.",
                "developer_verified": True
            },
            {
                "username": "localthunk",
                "email": "contact@localthunk.com",
                "developer_name": "LocalThunk",
                "display_name": "LocalThunk",
                "bio": "Creators of Balatro and other titles.",
                "developer_verified": True
            },
            {
                "username": "billy_basso",
                "email": "contact@billy_basso.com",
                "developer_name": "Billy Basso",
                "display_name": "Billy Basso",
                "bio": "Creators of Animal Well and other titles.",
                "developer_verified": True
            },
            {
                "username": "square_enix",
                "email": "contact@square_enix.com",
                "developer_name": "Square Enix",
                "display_name": "Square Enix",
                "bio": "Creators of Final Fantasy VII Rebirth and other titles.",
                "developer_verified": True
            },
            {
                "username": "bandai_namco",
                "email": "contact@bandai_namco.com",
                "developer_name": "Bandai Namco",
                "display_name": "Bandai Namco",
                "bio": "Creators of Tekken 8 and other titles.",
                "developer_verified": True
            },
            {
                "username": "rgg_studio",
                "email": "contact@rgg_studio.com",
                "developer_name": "RGG Studio",
                "display_name": "RGG Studio",
                "bio": "Creators of Like a Dragon: Infinite Wealth and other titles.",
                "developer_verified": True
            },
            {
                "username": "p-studio",
                "email": "contact@p-studio.com",
                "developer_name": "P-Studio",
                "display_name": "P-Studio",
                "bio": "Creators of Persona 3 Reload and other titles.",
                "developer_verified": True
            },
            {
                "username": "gsc_game_world",
                "email": "contact@gsc_game_world.com",
                "developer_name": "GSC Game World",
                "display_name": "GSC Game World",
                "bio": "Creators of S.T.A.L.K.E.R. 2 and other titles.",
                "developer_verified": True
            },
            {
                "username": "saber_interactive",
                "email": "contact@saber_interactive.com",
                "developer_name": "Saber Interactive",
                "display_name": "Saber Interactive",
                "bio": "Creators of Space Marine 2 and other titles.",
                "developer_verified": True
            },
            {
                "username": "team_asobi",
                "email": "contact@team_asobi.com",
                "developer_name": "Team Asobi",
                "display_name": "Team Asobi",
                "bio": "Creators of Astro Bot and other titles.",
                "developer_verified": True
            },
        ]

        developers = {}
        for dev_data in developers_data:
            dev = models.User(
                username=dev_data["username"],
                email=dev_data["email"],
                hashed_password=hash_password("dev123"),
                role=models.UserRole.DEVELOPER,
                developer_name=dev_data["developer_name"],
                display_name=dev_data["display_name"],
                bio=dev_data["bio"],
                developer_verified=dev_data["developer_verified"]
            )
            db.add(dev)
            db.flush()
            developers[dev_data["developer_name"]] = dev

        print(f"Created {len(developers)} real-world developers")

        # Real-World Games
        games_data = [
            # Rockstar Games
            {
                "title": "Grand Theft Auto V",
                "description": "Experience the interwoven stories of three unique criminals in the sprawling city of Los Santos. Rob banks, run heists, and explore a massive open world filled with endless activities. GTA Online brings the experience to millions of players worldwide.",
                "short_description": "Open-world action-adventure in Los Santos",
                "price": 29.99,
                "discount_percent": 50,
                "developer": "Rockstar Games",
                "genres": ["Action", "Adventure", "Open World", "Multiplayer"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/a/a5/Grand_Theft_Auto_V.png"
            },
            {
                "title": "Red Dead Redemption 2",
                "description": "America, 1899. Arthur Morgan and the Van der Linde gang are outlaws on the run. With federal agents and bounty hunters closing in, the gang must rob, steal, and fight their way across the rugged heartland of America.",
                "short_description": "Epic Western open-world adventure",
                "price": 59.99,
                "discount_percent": 33,
                "developer": "Rockstar Games",
                "genres": ["Action", "Adventure", "Open World"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/4/44/Red_Dead_Redemption_II.jpg"
            },
            # CD Projekt Red
            {
                "title": "The Witcher 3: Wild Hunt",
                "description": "You are Geralt of Rivia, mercenary monster slayer. Before you stretches a war-torn, monster-infested continent. Your current contract? Track down Ciri — the Child of Prophecy, a living weapon that can alter the shape of the world.",
                "short_description": "Award-winning open-world RPG",
                "price": 39.99,
                "discount_percent": 80,
                "developer": "CD Projekt Red",
                "genres": ["RPG", "Action", "Adventure", "Open World"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/0/0c/Witcher_3_cover_art.jpg"
            },
            {
                "title": "Cyberpunk 2077",
                "description": "Cyberpunk 2077 is an open-world, action-adventure RPG set in the dark future of Night City — a dangerous megalopolis obsessed with power, glamour, and ceaseless body modification.",
                "short_description": "Open-world RPG in a dark future",
                "price": 59.99,
                "discount_percent": 50,
                "developer": "CD Projekt Red",
                "genres": ["RPG", "Action", "Open World", "Shooter"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/9/9f/Cyberpunk_2077_box_art.jpg"
            },
            # Bethesda
            {
                "title": "The Elder Scrolls V: Skyrim",
                "description": "Winner of more than 200 Game of the Year Awards, Skyrim is an epic action-RPG. Live another life in another world — be anyone, do anything. Dragons have returned to Skyrim and it's up to you to stop them.",
                "short_description": "Epic fantasy open-world RPG",
                "price": 39.99,
                "discount_percent": 75,
                "developer": "Bethesda Game Studios",
                "genres": ["RPG", "Action", "Adventure", "Open World"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/1/15/The_Elder_Scrolls_V_Skyrim_cover.png"
            },
            {
                "title": "Fallout 4",
                "description": "As the sole survivor of Vault 111, you enter a world destroyed by nuclear war. Every second is a fight for survival in the post-apocalyptic wasteland. Only you can rebuild and determine the fate of the Wasteland.",
                "short_description": "Post-apocalyptic open-world RPG",
                "price": 19.99,
                "discount_percent": 75,
                "developer": "Bethesda Game Studios",
                "genres": ["RPG", "Action", "Open World", "Shooter"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/7/70/Fallout_4_cover_art.jpg"
            },
            # Valve
            {
                "title": "Counter-Strike 2",
                "description": "For over two decades, Counter-Strike has offered an elite competitive experience. Counter-Strike 2 is the largest technical leap forward in CS history, ensuring new features and updates for years to come.",
                "short_description": "Legendary competitive FPS",
                "price": 0,
                "developer": "Valve Corporation",
                "genres": ["Shooter", "Action", "Multiplayer", "Free to Play"],
                "cover_image_url": "https://cdn.cloudflare.steamstatic.com/steam/apps/730/header.jpg"
            },
            {
                "title": "Half-Life 2",
                "description": "Set in the dystopian City 17, Half-Life 2 follows Gordon Freeman as he leads resistance against the alien Combine. Featuring groundbreaking physics gameplay and storytelling.",
                "short_description": "Revolutionary first-person shooter",
                "price": 9.99,
                "developer": "Valve Corporation",
                "genres": ["Shooter", "Action", "Adventure"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/2/25/Half-Life_2_cover.jpg"
            },
            {
                "title": "Portal 2",
                "description": "The acclaimed Portal returns with an all-new adventure. Create portals to solve puzzles, navigate through test chambers, and uncover the secrets of Aperture Science.",
                "short_description": "Mind-bending puzzle adventure",
                "price": 9.99,
                "discount_percent": 80,
                "developer": "Valve Corporation",
                "genres": ["Puzzle", "Adventure"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/f/f9/Portal2cover.jpg"
            },
            # FromSoftware
            {
                "title": "Elden Ring",
                "description": "THE NEW FANTASY ACTION RPG. Rise, Tarnished, and be guided by grace to brandish the power of the Elden Ring and become an Elden Lord in the Lands Between. Created by Hidetaka Miyazaki and George R. R. Martin.",
                "short_description": "Open-world action RPG masterpiece",
                "price": 59.99,
                "discount_percent": 35,
                "developer": "FromSoftware",
                "genres": ["RPG", "Action", "Open World"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/b/b9/Elden_Ring_Box_art.jpg"
            },
            {
                "title": "Dark Souls III",
                "description": "As fires fade and the world falls into ruin, journey into a universe filled with more colossal enemies and environments. Prepare yourself and embrace the darkness.",
                "short_description": "Challenging action RPG",
                "price": 59.99,
                "discount_percent": 75,
                "developer": "FromSoftware",
                "genres": ["RPG", "Action"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/b/bb/Dark_souls_3_cover_art.jpg"
            },
            {
                "title": "Sekiro: Shadows Die Twice",
                "description": "Carve your own clever path to vengeance in this critically acclaimed adventure from FromSoftware. Take revenge. Restore your honor. Kill Ingeniously.",
                "short_description": "Brutal action-adventure in Sengoku Japan",
                "price": 59.99,
                "discount_percent": 50,
                "developer": "FromSoftware",
                "genres": ["Action", "Adventure"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/6/6e/Sekiro_art.jpg"
            },
            # Ubisoft
            {
                "title": "Assassin's Creed Valhalla",
                "description": "Become Eivor, a legendary Viking raider on a quest for glory. Lead your clan from the harsh shores of Norway to England. Build settlements, engage in brutal combat, and forge alliances to win glory.",
                "short_description": "Viking open-world action RPG",
                "price": 59.99,
                "discount_percent": 70,
                "developer": "Ubisoft",
                "genres": ["Action", "Adventure", "RPG", "Open World"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/f/f4/Assassin%27s_Creed_Valhalla_cover.jpg"
            },
            {
                "title": "Far Cry 6",
                "description": "Welcome to Yara, a tropical paradise frozen in time. Join the revolution against dictator Antón Castillo and his son Diego in the largest Far Cry playground to date.",
                "short_description": "Revolutionary open-world FPS",
                "price": 59.99,
                "discount_percent": 75,
                "developer": "Ubisoft",
                "genres": ["Shooter", "Action", "Open World"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/3/35/Far_cry_6_cover.jpg"
            },
            {
                "title": "Rainbow Six Siege",
                "description": "Master the art of destruction in Tom Clancy's Rainbow Six Siege. Face intense 5v5 close-quarter combat, high lethality, tactical decision making, and team play.",
                "short_description": "Tactical multiplayer shooter",
                "price": 19.99,
                "discount_percent": 60,
                "developer": "Ubisoft",
                "genres": ["Shooter", "Multiplayer", "Strategy"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/4/47/Tom_Clancy%27s_Rainbow_Six_Siege_cover_art.jpg"
            },
            # EA Games
            {
                "title": "FIFA 24",
                "description": "EA SPORTS FC 24 brings you closer to the world's game with HyperMotion V technology and the most realistic gameplay ever. Play the World's Game with over 19,000 players across 700+ teams.",
                "short_description": "The world's most popular football game",
                "price": 69.99,
                "discount_percent": 40,
                "developer": "Electronic Arts",
                "genres": ["Sports", "Simulation", "Multiplayer"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/a/a6/FC_24_cover.jpg"
            },
            {
                "title": "Battlefield 2042",
                "description": "Enter a near-future world transformed by disorder. Adapt and overcome in a world where no battle is ever the same with 128 players, massive maps, and dynamic destruction.",
                "short_description": "Large-scale multiplayer warfare",
                "price": 59.99,
                "discount_percent": 85,
                "developer": "Electronic Arts",
                "genres": ["Shooter", "Action", "Multiplayer"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/3/3f/Battlefield_2042_cover_art.jpg"
            },
            # Naughty Dog
            {
                "title": "The Last of Us Part I",
                "description": "Experience the emotional storytelling and unforgettable characters of Joel and Ellie in The Last of Us, rebuilt from the ground up for the PC with enhanced graphics and gameplay.",
                "short_description": "Acclaimed survival action game",
                "price": 59.99,
                "discount_percent": 30,
                "developer": "Naughty Dog",
                "genres": ["Action", "Adventure", "Survival", "Horror"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/a/a7/The_Last_of_Us_Part_I_cover.jpg"
            },
            # Insomniac Games
            {
                "title": "Marvel's Spider-Man Remastered",
                "description": "Be greater. Be Spider-Man. Experience the iconic web-slinger's journey in this action-packed open-world adventure through Marvel's New York.",
                "short_description": "Open-world Spider-Man action",
                "price": 59.99,
                "discount_percent": 40,
                "developer": "Insomniac Games",
                "genres": ["Action", "Adventure", "Open World"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/e/e1/Spider-Man_PS4_cover.jpg"
            },
            # Mojang
            {
                "title": "Minecraft",
                "description": "Explore your own unique world, survive the night, and create anything you can imagine! The best-selling video game of all time with infinite possibilities.",
                "short_description": "Infinite creative sandbox adventure",
                "price": 26.95,
                "developer": "Mojang Studios",
                "genres": ["Sandbox", "Survival", "Adventure", "Multiplayer"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/5/51/Minecraft_cover.png"
            },
            # Re-Logic
            {
                "title": "Terraria",
                "description": "Dig, fight, explore, build! In this action-packed adventure game, the world is your canvas and the ground itself is your paint. Grab your tools and go!",
                "short_description": "2D sandbox action-adventure",
                "price": 9.99,
                "discount_percent": 50,
                "developer": "Re-Logic",
                "genres": ["Sandbox", "Survival", "Adventure", "Indie"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/1/1a/Terraria_Steam_artwork.jpg"
            },
            # ConcernedApe
            {
                "title": "Stardew Valley",
                "description": "You've inherited your grandfather's old farm plot in Stardew Valley. Armed with hand-me-down tools and a few coins, you set out to begin your new life.",
                "short_description": "Beloved farming simulation RPG",
                "price": 14.99,
                "developer": "ConcernedApe",
                "genres": ["Simulation", "RPG", "Indie"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/f/fd/Logo_of_Stardew_Valley.png"
            },
            # Supergiant Games
            {
                "title": "Hades",
                "description": "Defy the god of the dead as you hack and slash your way out of the Underworld in this rogue-like dungeon crawler. Winner of over 50 Game of the Year awards.",
                "short_description": "Award-winning roguelike action",
                "price": 24.99,
                "discount_percent": 40,
                "developer": "Supergiant Games",
                "genres": ["Action", "RPG", "Indie"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/c/cc/Hades_cover_art.jpg"
            },
            {
                "title": "Hades II",
                "description": "The Princess of the Underworld battles beyond the borders of time and space to bring down the Titan of Time himself. The next installment of the award-winning roguelike.",
                "short_description": "Highly anticipated roguelike sequel",
                "price": 29.99,
                "developer": "Supergiant Games",
                "genres": ["Action", "RPG", "Indie"],
                "cover_image_url": "https://cdn.cloudflare.steamstatic.com/steam/apps/1145350/header.jpg"
            },
            # Team Cherry
            {
                "title": "Hollow Knight",
                "description": "Forge your own path in Hollow Knight! An epic action adventure through a vast ruined kingdom of insects and heroes. Explore twisting caverns, battle tainted creatures, and befriend bizarre bugs.",
                "short_description": "Epic metroidvania adventure",
                "price": 14.99,
                "discount_percent": 50,
                "developer": "Team Cherry",
                "genres": ["Action", "Adventure", "Indie", "Platformer"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/0/04/Hollow_Knight_cover.jpg"
            },
            # Capcom
            {
                "title": "Resident Evil 4",
                "description": "Survival horror returns. Six years after the events of Resident Evil 2, Leon S. Kennedy embarks on a mission to rescue the President's kidnapped daughter, Ashley Graham.",
                "short_description": "Legendary survival horror remake",
                "price": 59.99,
                "discount_percent": 34,
                "developer": "Capcom",
                "genres": ["Horror", "Action", "Survival"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/d/df/Resident_Evil_4_remake_cover_art.jpg"
            },
            {
                "title": "Monster Hunter: World",
                "description": "Welcome to a new world! In Monster Hunter: World, you become the ultimate hunter as you journey to the New World to discover and hunt the fierce Elder Dragon Zorah Magdaros.",
                "short_description": "Epic monster hunting action RPG",
                "price": 29.99,
                "discount_percent": 67,
                "developer": "Capcom",
                "genres": ["Action", "RPG", "Multiplayer"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/1/1b/Monster_Hunter_World_cover_art.jpg"
            },
            {
                "title": "Street Fighter 6",
                "description": "The evolution of fighting games! Street Fighter 6 spans three distinct game modes: Fighting Ground, World Tour, and Battle Hub.",
                "short_description": "Next-generation fighting game",
                "price": 59.99,
                "discount_percent": 25,
                "developer": "Capcom",
                "genres": ["Fighting", "Action", "Multiplayer"],
                "cover_image_url": "https://upload.wikimedia.org/wikipedia/en/6/6a/Street_Fighter_6_logo.png"
            },
            {
                "title": "Battlefield 6",
                "description": "Battlefield 6 is a FPS game by Battlefield Studios. Released/Expected: Oct 10, 2025.",
                "short_description": "FPS game (#1 Best Seller)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Electronic Arts",
                "genres": ["Action", "Shooter"],
                "cover_image_url": "https://placehold.co/600x400?text=Battlefield+6"
            },
            {
                "title": "Monster Hunter Wilds",
                "description": "Monster Hunter Wilds is a Action RPG game by Capcom. Released/Expected: Feb 28, 2025.",
                "short_description": "Action RPG game (#3 Best Seller)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Capcom",
                "genres": ["RPG", "Action"],
                "cover_image_url": "https://placehold.co/600x400?text=Monster+Hunter+Wilds"
            },
            {
                "title": "Clair Obscur: Expedition 33",
                "description": "Clair Obscur: Expedition 33 is a Turn-Based RPG game by Sandfall Interactive. Released/Expected: Apr 24, 2025.",
                "short_description": "Turn-Based RPG game (GOTY Winner)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Sandfall Interactive",
                "genres": ["Strategy", "RPG"],
                "cover_image_url": "https://placehold.co/600x400?text=Clair+Obscur:+Expedition+33"
            },
            {
                "title": "Call of Duty: Black Ops 7",
                "description": "Call of Duty: Black Ops 7 is a FPS game by Treyarch. Released/Expected: Nov 14, 2025.",
                "short_description": "FPS game (#7 Best Seller)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Treyarch",
                "genres": ["Action", "Shooter"],
                "cover_image_url": "https://placehold.co/600x400?text=Call+of+Duty:+Black+Ops+7"
            },
            {
                "title": "Kingdom Come: Deliverance II",
                "description": "Kingdom Come: Deliverance II is a RPG game by Warhorse Studios. Released/Expected: Feb 4, 2025.",
                "short_description": "RPG game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Warhorse Studios",
                "genres": ["RPG"],
                "cover_image_url": "https://placehold.co/600x400?text=Kingdom+Come:+Deliverance+II"
            },
            {
                "title": "Ghost of Y\u014dtei",
                "description": "Ghost of Y\u014dtei is a Action Adventure game by Sucker Punch. Released/Expected: Oct 2, 2025.",
                "short_description": "Action Adventure game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Sucker Punch",
                "genres": ["Adventure", "Action"],
                "cover_image_url": "https://placehold.co/600x400?text=Ghost+of+Y\u014dtei"
            },
            {
                "title": "Civilization VII",
                "description": "Civilization VII is a Strategy game by Firaxis Games. Released/Expected: Feb 11, 2025.",
                "short_description": "Strategy game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Firaxis Games",
                "genres": ["Strategy"],
                "cover_image_url": "https://placehold.co/600x400?text=Civilization+VII"
            },
            {
                "title": "Death Stranding 2: On The Beach",
                "description": "Death Stranding 2: On The Beach is a Action game by Kojima Productions. Released/Expected: Jun 26, 2025.",
                "short_description": "Action game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Kojima Productions",
                "genres": ["Action"],
                "cover_image_url": "https://placehold.co/600x400?text=Death+Stranding+2:+On+The+Beach"
            },
            {
                "title": "Assassin's Creed Shadows",
                "description": "Assassin's Creed Shadows is a Action RPG game by Ubisoft Quebec. Released/Expected: Mar 20, 2025.",
                "short_description": "Action RPG game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Ubisoft",
                "genres": ["RPG", "Action"],
                "cover_image_url": "https://placehold.co/600x400?text=Assassin's+Creed+Shadows"
            },
            {
                "title": "Avowed",
                "description": "Avowed is a RPG game by Obsidian Entertainment. Released/Expected: Feb 18, 2025.",
                "short_description": "RPG game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Obsidian Entertainment",
                "genres": ["RPG"],
                "cover_image_url": "https://placehold.co/600x400?text=Avowed"
            },
            {
                "title": "Split Fiction",
                "description": "Split Fiction is a Co-op Action game by Hazelight Studios. Released/Expected: Mar 6, 2025.",
                "short_description": "Co-op Action game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Electronic Arts",
                "genres": ["Action", "Multiplayer"],
                "cover_image_url": "https://placehold.co/600x400?text=Split+Fiction"
            },
            {
                "title": "South of Midnight",
                "description": "South of Midnight is a Action Adventure game by Compulsion Games. Released/Expected: Apr 8, 2025.",
                "short_description": "Action Adventure game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Compulsion Games",
                "genres": ["Adventure", "Action"],
                "cover_image_url": "https://placehold.co/600x400?text=South+of+Midnight"
            },
            {
                "title": "Blue Prince",
                "description": "Blue Prince is a Puzzle game by Dogubomb. Released/Expected: Apr 10, 2025.",
                "short_description": "Puzzle game (Critical Acclaim)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Dogubomb",
                "genres": ["Puzzle"],
                "cover_image_url": "https://placehold.co/600x400?text=Blue+Prince"
            },
            {
                "title": "Hollow Knight: Silksong",
                "description": "Hollow Knight: Silksong is a Metroidvania game by Team Cherry. Released/Expected: Sep 4, 2025.",
                "short_description": "Metroidvania game (Released)",
                "price": 29.99,
                "discount_percent": 0,
                "developer": "Team Cherry",
                "genres": ["Adventure", "Action", "Indie", "Platformer"],
                "cover_image_url": "https://placehold.co/600x400?text=Hollow+Knight:+Silksong"
            },
            {
                "title": "Donkey Kong Bananza",
                "description": "Donkey Kong Bananza is a Platformer game by Nintendo EPD. Released/Expected: Jul 17, 2025.",
                "short_description": "Platformer game (Released)",
                "price": 29.99,
                "discount_percent": 0,
                "developer": "Nintendo EPD",
                "genres": ["Platformer"],
                "cover_image_url": "https://placehold.co/600x400?text=Donkey+Kong+Bananza"
            },
            {
                "title": "ARC Raiders",
                "description": "ARC Raiders is a Extraction Shooter game by Embark Studios. Released/Expected: Oct 30, 2025.",
                "short_description": "Extraction Shooter game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Embark Studios",
                "genres": ["Survival", "Action", "Shooter"],
                "cover_image_url": "https://placehold.co/600x400?text=ARC+Raiders"
            },
            {
                "title": "Where Winds Meet",
                "description": "Where Winds Meet is a Action RPG game by Everstone Studio. Released/Expected: Nov 14, 2025.",
                "short_description": "Action RPG game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Everstone Studio",
                "genres": ["RPG", "Action"],
                "cover_image_url": "https://placehold.co/600x400?text=Where+Winds+Meet"
            },
            {
                "title": "Ashes of Creation",
                "description": "Ashes of Creation is a MMORPG game by Intrepid Studios. Released/Expected: Dec 11, 2025.",
                "short_description": "MMORPG game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Intrepid Studios",
                "genres": ["RPG", "Open World", "Multiplayer"],
                "cover_image_url": "https://placehold.co/600x400?text=Ashes+of+Creation"
            },
            {
                "title": "Fatal Fury: City of the Wolves",
                "description": "Fatal Fury: City of the Wolves is a Fighting game by SNK. Released/Expected: Apr 24, 2025.",
                "short_description": "Fighting game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "SNK",
                "genres": ["Fighting"],
                "cover_image_url": "https://placehold.co/600x400?text=Fatal+Fury:+City+of+the+Wolves"
            },
            {
                "title": "Borderlands 4",
                "description": "Borderlands 4 is a FPS/RPG game by Gearbox Software. Released/Expected: 2025 (Mid).",
                "short_description": "FPS/RPG game (Top 5 Seller)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Gearbox Software",
                "genres": ["RPG", "Action", "Shooter"],
                "cover_image_url": "https://placehold.co/600x400?text=Borderlands+4"
            },
            {
                "title": "NBA 2K26",
                "description": "NBA 2K26 is a Sports game by Visual Concepts. Released/Expected: Sep 5, 2025.",
                "short_description": "Sports game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Visual Concepts",
                "genres": ["Sports"],
                "cover_image_url": "https://placehold.co/600x400?text=NBA+2K26"
            },
            {
                "title": "EA Sports FC 26",
                "description": "EA Sports FC 26 is a Sports game by EA Vancouver. Released/Expected: Sep 25, 2025.",
                "short_description": "Sports game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Electronic Arts",
                "genres": ["Sports"],
                "cover_image_url": "https://placehold.co/600x400?text=EA+Sports+FC+26"
            },
            {
                "title": "Madden NFL 26",
                "description": "Madden NFL 26 is a Sports game by Tiburon. Released/Expected: Aug 2025.",
                "short_description": "Sports game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Electronic Arts",
                "genres": ["Sports"],
                "cover_image_url": "https://placehold.co/600x400?text=Madden+NFL+26"
            },
            {
                "title": "MLB The Show 25",
                "description": "MLB The Show 25 is a Sports game by San Diego Studio. Released/Expected: Mar 18, 2025.",
                "short_description": "Sports game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "San Diego Studio",
                "genres": ["Sports"],
                "cover_image_url": "https://placehold.co/600x400?text=MLB+The+Show+25"
            },
            {
                "title": "WWE 2K25",
                "description": "WWE 2K25 is a Sports game by Visual Concepts. Released/Expected: Mar 14, 2025.",
                "short_description": "Sports game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Visual Concepts",
                "genres": ["Sports"],
                "cover_image_url": "https://placehold.co/600x400?text=WWE+2K25"
            },
            {
                "title": "Sniper Elite: Resistance",
                "description": "Sniper Elite: Resistance is a Shooter game by Rebellion. Released/Expected: Jan 30, 2025.",
                "short_description": "Shooter game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Rebellion",
                "genres": ["Shooter"],
                "cover_image_url": "https://placehold.co/600x400?text=Sniper+Elite:+Resistance"
            },
            {
                "title": "Dynasty Warriors Origins",
                "description": "Dynasty Warriors Origins is a Hack and Slash game by Omega Force. Released/Expected: Jan 17, 2025.",
                "short_description": "Hack and Slash game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Omega Force",
                "genres": ["Action"],
                "cover_image_url": "https://placehold.co/600x400?text=Dynasty+Warriors+Origins"
            },
            {
                "title": "The First Berserker: Khazan",
                "description": "The First Berserker: Khazan is a Action RPG game by Neople. Released/Expected: Mar 27, 2025.",
                "short_description": "Action RPG game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Neople",
                "genres": ["RPG", "Action"],
                "cover_image_url": "https://placehold.co/600x400?text=The+First+Berserker:+Khazan"
            },
            {
                "title": "Atomfall",
                "description": "Atomfall is a Survival game by Rebellion. Released/Expected: Mar 27, 2025.",
                "short_description": "Survival game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Rebellion",
                "genres": ["Survival"],
                "cover_image_url": "https://placehold.co/600x400?text=Atomfall"
            },
            {
                "title": "Two Point Museum",
                "description": "Two Point Museum is a Simulation game by Two Point Studios. Released/Expected: Mar 4, 2025.",
                "short_description": "Simulation game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Two Point Studios",
                "genres": ["Simulation"],
                "cover_image_url": "https://placehold.co/600x400?text=Two+Point+Museum"
            },
            {
                "title": "FragPunk",
                "description": "FragPunk is a Shooter game by Bad Guitar Studio. Released/Expected: Mar 6, 2025.",
                "short_description": "Shooter game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Bad Guitar Studio",
                "genres": ["Shooter"],
                "cover_image_url": "https://placehold.co/600x400?text=FragPunk"
            },
            {
                "title": "Suikoden I & II HD Remaster",
                "description": "Suikoden I & II HD Remaster is a RPG game by Konami. Released/Expected: Mar 6, 2025.",
                "short_description": "RPG game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Konami",
                "genres": ["RPG"],
                "cover_image_url": "https://placehold.co/600x400?text=Suikoden+I+&+II+HD+Remaster"
            },
            {
                "title": "Citizen Sleeper 2",
                "description": "Citizen Sleeper 2 is a RPG game by Jump Over The Age. Released/Expected: Jan 31, 2025.",
                "short_description": "RPG game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Jump Over The Age",
                "genres": ["RPG"],
                "cover_image_url": "https://placehold.co/600x400?text=Citizen+Sleeper+2"
            },
            {
                "title": "Lost Records: Bloom & Rage",
                "description": "Lost Records: Bloom & Rage is a Narrative Adventure game by Don't Nod. Released/Expected: Feb 18, 2025.",
                "short_description": "Narrative Adventure game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Don't Nod",
                "genres": ["Adventure"],
                "cover_image_url": "https://placehold.co/600x400?text=Lost+Records:+Bloom+&+Rage"
            },
            {
                "title": "Monster Energy Supercross 25",
                "description": "Monster Energy Supercross 25 is a Racing game by Milestone. Released/Expected: Apr 10, 2025.",
                "short_description": "Racing game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Milestone",
                "genres": ["Racing"],
                "cover_image_url": "https://placehold.co/600x400?text=Monster+Energy+Supercross+25"
            },
            {
                "title": "Oblivion Remastered",
                "description": "Oblivion Remastered is a RPG game by Virtuos (Rumored). Released/Expected: Apr 22, 2025.",
                "short_description": "RPG game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Bethesda Game Studios",
                "genres": ["RPG"],
                "cover_image_url": "https://placehold.co/600x400?text=Oblivion+Remastered"
            },
            {
                "title": "Days Gone Remastered",
                "description": "Days Gone Remastered is a Action game by Bend Studio. Released/Expected: Apr 25, 2025.",
                "short_description": "Action game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Bend Studio",
                "genres": ["Action"],
                "cover_image_url": "https://placehold.co/600x400?text=Days+Gone+Remastered"
            },
            {
                "title": "World of Goo 2",
                "description": "World of Goo 2 is a Puzzle game by 2D Boy. Released/Expected: Apr 25, 2025.",
                "short_description": "Puzzle game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "2D Boy",
                "genres": ["Puzzle"],
                "cover_image_url": "https://placehold.co/600x400?text=World+of+Goo+2"
            },
            {
                "title": "Tempest Rising",
                "description": "Tempest Rising is a RTS game by Slipgate Ironworks. Released/Expected: Apr 24, 2025.",
                "short_description": "RTS game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Slipgate Ironworks",
                "genres": [],
                "cover_image_url": "https://placehold.co/600x400?text=Tempest+Rising"
            },
            {
                "title": "Steel Seed",
                "description": "Steel Seed is a Action game by Storm in a Teacup. Released/Expected: Apr 22, 2025.",
                "short_description": "Action game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Storm in a Teacup",
                "genres": ["Action"],
                "cover_image_url": "https://placehold.co/600x400?text=Steel+Seed"
            },
            {
                "title": "Post Trauma",
                "description": "Post Trauma is a Horror game by Red Soul Games. Released/Expected: Apr 22, 2025.",
                "short_description": "Horror game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Red Soul Games",
                "genres": ["Horror"],
                "cover_image_url": "https://placehold.co/600x400?text=Post+Trauma"
            },
            {
                "title": "Lunar Remastered Collection",
                "description": "Lunar Remastered Collection is a RPG game by Game Arts. Released/Expected: Apr 18, 2025.",
                "short_description": "RPG game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Game Arts",
                "genres": ["RPG"],
                "cover_image_url": "https://placehold.co/600x400?text=Lunar+Remastered+Collection"
            },
            {
                "title": "Indiana Jones & The Great Circle",
                "description": "Indiana Jones & The Great Circle is a Adventure game by MachineGames. Released/Expected: Apr 17, 2025.",
                "short_description": "Adventure game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "MachineGames",
                "genres": ["Adventure"],
                "cover_image_url": "https://placehold.co/600x400?text=Indiana+Jones+&+The+Great+Circle"
            },
            {
                "title": "Bionic Bay",
                "description": "Bionic Bay is a Platformer game by Psychoflow. Released/Expected: Apr 17, 2025.",
                "short_description": "Platformer game (Released)",
                "price": 29.99,
                "discount_percent": 0,
                "developer": "Psychoflow",
                "genres": ["Platformer"],
                "cover_image_url": "https://placehold.co/600x400?text=Bionic+Bay"
            },
            {
                "title": "Rusty Rabbit",
                "description": "Rusty Rabbit is a Action game by NetEase. Released/Expected: Apr 17, 2025.",
                "short_description": "Action game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "NetEase",
                "genres": ["Action"],
                "cover_image_url": "https://placehold.co/600x400?text=Rusty+Rabbit"
            },
            {
                "title": "Football Manager 2025",
                "description": "Football Manager 2025 is a Simulation game by Sports Interactive. Released/Expected: Nov 2024/2025.",
                "short_description": "Simulation game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Sports Interactive",
                "genres": ["Simulation"],
                "cover_image_url": "https://placehold.co/600x400?text=Football+Manager+2025"
            },
            {
                "title": "F1 25",
                "description": "F1 25 is a Racing game by Codemasters. Released/Expected: Jun 2025.",
                "short_description": "Racing game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Electronic Arts",
                "genres": ["Racing"],
                "cover_image_url": "https://placehold.co/600x400?text=F1+25"
            },
            {
                "title": "Mario Kart World",
                "description": "Mario Kart World is a Racing game by Nintendo EPD. Released/Expected: 2025 (Late).",
                "short_description": "Racing game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Nintendo EPD",
                "genres": ["Racing"],
                "cover_image_url": "https://placehold.co/600x400?text=Mario+Kart+World"
            },
            {
                "title": "Black Myth: Wukong",
                "description": "Black Myth: Wukong is a Action RPG game by Game Science. Released/Expected: Aug 19, 2024.",
                "short_description": "Action RPG game (2024 Hit)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Game Science",
                "genres": ["RPG", "Action"],
                "cover_image_url": "https://placehold.co/600x400?text=Black+Myth:+Wukong"
            },
            {
                "title": "Helldivers 2",
                "description": "Helldivers 2 is a Shooter game by Arrowhead. Released/Expected: Feb 8, 2024.",
                "short_description": "Shooter game (2024 Hit)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Arrowhead",
                "genres": ["Shooter"],
                "cover_image_url": "https://placehold.co/600x400?text=Helldivers+2"
            },
            {
                "title": "Palworld",
                "description": "Palworld is a Survival game by Pocketpair. Released/Expected: Jan 19, 2024.",
                "short_description": "Survival game (2024 Hit)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Pocketpair",
                "genres": ["Survival"],
                "cover_image_url": "https://placehold.co/600x400?text=Palworld"
            },
            {
                "title": "Balatro",
                "description": "Balatro is a Roguelike game by LocalThunk. Released/Expected: Feb 20, 2024.",
                "short_description": "Roguelike game (2024 Hit)",
                "price": 29.99,
                "discount_percent": 0,
                "developer": "LocalThunk",
                "genres": ["RPG", "Action", "Indie"],
                "cover_image_url": "https://placehold.co/600x400?text=Balatro"
            },
            {
                "title": "Animal Well",
                "description": "Animal Well is a Metroidvania game by Billy Basso. Released/Expected: May 9, 2024.",
                "short_description": "Metroidvania game (2024 Hit)",
                "price": 29.99,
                "discount_percent": 0,
                "developer": "Billy Basso",
                "genres": ["Adventure", "Action", "Indie", "Platformer"],
                "cover_image_url": "https://placehold.co/600x400?text=Animal+Well"
            },
            {
                "title": "Final Fantasy VII Rebirth",
                "description": "Final Fantasy VII Rebirth is a RPG game by Square Enix. Released/Expected: Feb 29, 2024.",
                "short_description": "RPG game (2024 Hit)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Square Enix",
                "genres": ["RPG"],
                "cover_image_url": "https://placehold.co/600x400?text=Final+Fantasy+VII+Rebirth"
            },
            {
                "title": "Dragon's Dogma 2",
                "description": "Dragon's Dogma 2 is a Action RPG game by Capcom. Released/Expected: Mar 22, 2024.",
                "short_description": "Action RPG game (2024 Hit)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Capcom",
                "genres": ["RPG", "Action"],
                "cover_image_url": "https://placehold.co/600x400?text=Dragon's+Dogma+2"
            },
            {
                "title": "Tekken 8",
                "description": "Tekken 8 is a Fighting game by Bandai Namco. Released/Expected: Jan 26, 2024.",
                "short_description": "Fighting game (2024 Hit)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Bandai Namco",
                "genres": ["Fighting"],
                "cover_image_url": "https://placehold.co/600x400?text=Tekken+8"
            },
            {
                "title": "Like a Dragon: Infinite Wealth",
                "description": "Like a Dragon: Infinite Wealth is a RPG game by RGG Studio. Released/Expected: Jan 26, 2024.",
                "short_description": "RPG game (2024 Hit)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "RGG Studio",
                "genres": ["RPG"],
                "cover_image_url": "https://placehold.co/600x400?text=Like+a+Dragon:+Infinite+Wealth"
            },
            {
                "title": "Persona 3 Reload",
                "description": "Persona 3 Reload is a RPG game by P-Studio. Released/Expected: Feb 2, 2024.",
                "short_description": "RPG game (2024 Hit)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "P-Studio",
                "genres": ["RPG"],
                "cover_image_url": "https://placehold.co/600x400?text=Persona+3+Reload"
            },
            {
                "title": "S.T.A.L.K.E.R. 2",
                "description": "S.T.A.L.K.E.R. 2 is a FPS game by GSC Game World. Released/Expected: Nov 20, 2024.",
                "short_description": "FPS game (2024 Hit)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "GSC Game World",
                "genres": ["Action", "Shooter"],
                "cover_image_url": "https://placehold.co/600x400?text=S.T.A.L.K.E.R.+2"
            },
            {
                "title": "Space Marine 2",
                "description": "Space Marine 2 is a TPS game by Saber Interactive. Released/Expected: Sep 9, 2024.",
                "short_description": "TPS game (2024 Hit)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Saber Interactive",
                "genres": [],
                "cover_image_url": "https://placehold.co/600x400?text=Space+Marine+2"
            },
            {
                "title": "Astro Bot",
                "description": "Astro Bot is a Platformer game by Team Asobi. Released/Expected: Sep 6, 2024.",
                "short_description": "Platformer game (2024 Hit)",
                "price": 29.99,
                "discount_percent": 0,
                "developer": "Team Asobi",
                "genres": ["Platformer"],
                "cover_image_url": "https://placehold.co/600x400?text=Astro+Bot"
            },
            {
                "title": "Call of Duty: Black Ops 6",
                "description": "Call of Duty: Black Ops 6 is a FPS game by Treyarch. Released/Expected: Oct 25, 2024.",
                "short_description": "FPS game (2024 Hit)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "Treyarch",
                "genres": ["Action", "Shooter"],
                "cover_image_url": "https://placehold.co/600x400?text=Call+of+Duty:+Black+Ops+6"
            },
            {
                "title": "Elden Ring: Nightreign",
                "description": "Elden Ring: Nightreign is a Action RPG game by FromSoftware. Released/Expected: 2025.",
                "short_description": "Action RPG game (Released)",
                "price": 59.99,
                "discount_percent": 0,
                "developer": "FromSoftware",
                "genres": ["RPG", "Action"],
                "cover_image_url": "https://placehold.co/600x400?text=Elden+Ring:+Nightreign"
            },
        ]

        game_count = 0
        for game_data in games_data:
            developer_name = game_data.pop("developer")
            genre_names = game_data.pop("genres")

            developer = developers.get(developer_name)
            if not developer:
                print(f"Warning: Developer {developer_name} not found, skipping game {game_data['title']}")
                continue

            game = models.Game(
                title=game_data["title"],
                description=game_data["description"],
                short_description=game_data.get("short_description"),
                price=game_data["price"],
                discount_percent=game_data.get("discount_percent", 0),
                developer_id=developer.id,
                status=models.GameStatus.APPROVED,
                approved_by=admin.id,
                cover_image_url=game_data.get("cover_image_url"),
                total_sales=50 + hash(game_data["title"]) % 10000,  # Fake sales data
                total_revenue=(50 + hash(game_data["title"]) % 10000) * game_data["price"] * 0.7
            )
            game.genres = [genres[name] for name in genre_names if name in genres]
            db.add(game)
            game_count += 1

        print(f"Created {game_count} real-world games")

        db.commit()
        print("\n" + "="*50)
        print("Database seeded successfully!")
        print("="*50)
        print("\nTest Accounts:")
        print("  Admin:     admin / admin123")
        print("  Player:    player / player123")
        print("  Any Dev:   [username] / dev123")
        print("\nDevelopers (all with password 'dev123'):")
        for dev_name in developers.keys():
            print(f"  - {dev_name}")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
