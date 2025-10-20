#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import json
import random
import urllib
import urllib2
import tempfile
import os
import platform
import subprocess
import time

# Wingspan Birds - ALL birds from base game and all expansions
WINGSPAN_BIRDS = [
    # Base Game - North America (170 birds)
    "Acorn Woodpecker", "American Avocet", "American Bittern", "American Coot",
    "American Crow", "American Goldfinch", "American Kestrel", "American Redstart",
    "American Robin", "American Tree Sparrow", "American White Pelican", "American Wigeon",
    "American Woodcock", "Anna's Hummingbird", "Bald Eagle", "Baltimore Oriole",
    "Band-tailed Pigeon", "Barn Owl", "Barn Swallow", "Barred Owl",
    "Belted Kingfisher", "Bewick's Wren", "Black Skimmer", "Black Vulture",
    "Black-bellied Plover", "Black-billed Magpie", "Black-capped Chickadee", "Black-chinned Hummingbird",
    "Blue Grosbeak", "Blue Jay", "Blue-gray Gnatcatcher", "Boat-tailed Grackle",
    "Brewer's Blackbird", "Broad-winged Hawk", "Brown Creeper", "Brown Pelican",
    "Brown-headed Cowbird", "Bushtit", "Cackling Goose", "California Condor",
    "California Gull", "Canada Goose", "Canvasback", "Carolina Wren",
    "Chestnut-backed Chickadee", "Chihuahuan Raven", "Chimney Swift", "Chipping Sparrow",
    "Clark's Grebe", "Common Grackle", "Common Loon", "Common Merganser",
    "Common Nighthawk", "Common Raven", "Common Yellowthroat", "Cooper's Hawk",
    "Dark-eyed Junco", "Dickcissel", "Double-crested Cormorant", "Downy Woodpecker",
    "Dunlin", "Eastern Bluebird", "Eastern Kingbird", "Eastern Meadowlark",
    "Eastern Phoebe", "Eastern Screech-Owl", "Eastern Towhee", "Eastern Wood-Pewee",
    "Evening Grosbeak", "Ferruginous Hawk", "Fish Crow", "Forster's Tern",
    "Fox Sparrow", "Franklin's Gull", "Gadwall", "Golden Eagle",
    "Golden-crowned Kinglet", "Gray Catbird", "Great Black-backed Gull", "Great Blue Heron",
    "Great Crested Flycatcher", "Great Egret", "Great Gray Owl", "Great Horned Owl",
    "Greater Prairie-Chicken", "Greater Roadrunner", "Greater Scaup", "Greater White-fronted Goose",
    "Greater Yellowlegs", "Green Heron", "Green-winged Teal", "Hairy Woodpecker",
    "Hermit Thrush", "Hooded Merganser", "Horned Grebe", "Horned Lark",
    "House Finch", "House Sparrow", "House Wren", "Indigo Bunting",
    "Killdeer", "Least Flycatcher", "Least Sandpiper", "Lesser Scaup",
    "Lesser Yellowlegs", "Lincoln's Sparrow", "Loggerhead Shrike", "Long-billed Curlew",
    "Long-billed Dowitcher", "Mallard", "Marbled Godwit", "Marsh Wren",
    "Mountain Bluebird", "Mourning Dove", "Mute Swan", "Northern Bobwhite",
    "Northern Cardinal", "Northern Flicker", "Northern Gannet", "Northern Harrier",
    "Northern Mockingbird", "Northern Pintail", "Northern Shoveler", "Osprey",
    "Painted Bunting", "Painted Whitestart", "Peregrine Falcon", "Pied-billed Grebe",
    "Pileated Woodpecker", "Prairie Falcon", "Purple Martin", "Pyrrhuloxia",
    "Red Crossbill", "Red Knot", "Red-bellied Woodpecker", "Red-breasted Merganser",
    "Red-breasted Nuthatch", "Red-headed Woodpecker", "Red-shouldered Hawk", "Red-tailed Hawk",
    "Red-winged Blackbird", "Ring-billed Gull", "Ring-necked Duck", "Ring-necked Pheasant",
    "Rock Pigeon", "Roseate Spoonbill", "Rose-breasted Grosbeak", "Royal Tern",
    "Ruby-crowned Kinglet", "Ruby-throated Hummingbird", "Ruddy Duck", "Ruddy Turnstone",
    "Ruffed Grouse", "Rufous Hummingbird", "Sanderling", "Sandhill Crane",
    "Savannah Sparrow", "Scaled Quail", "Scissor-tailed Flycatcher", "Sharp-shinned Hawk",
    "Short-eared Owl", "Snow Goose", "Snowy Egret", "Song Sparrow",
    "Spotted Sandpiper", "Spotted Towhee", "Steller's Jay", "Swainson's Hawk",
    "Tree Swallow", "Trumpeter Swan", "Tufted Titmouse", "Turkey Vulture",
    "Veery", "Vesper Sparrow", "Virginia Rail", "Western Grebe",
    "Western Gull", "Western Meadowlark", "Western Sandpiper", "Western Tanager",
    "White-breasted Nuthatch", "White-crowned Sparrow", "White-throated Sparrow", "Wild Turkey",
    "Willet", "Wilson's Snipe", "Wood Duck", "Wood Thrush",
    "Yellow Warbler", "Yellow-bellied Sapsucker", "Yellow-breasted Chat", "Yellow-rumped Warbler",
    
    # European Expansion (81 birds)
    "Audouin's Gull", "Black Redstart", "Black Woodpecker", "Black-headed Gull",
    "Black-tailed Godwit", "Black-throated Diver", "Bluethroat", "Bonelli's Eagle",
    "Bullfinch", "Carrion Crow", "Cetti's Warbler", "Coal Tit",
    "Common Blackbird", "Common Buzzard", "Common Chaffinch", "Common Chiffchaff",
    "Common Cuckoo", "Common Goldeneye", "Common Kingfisher", "Common Little Bittern",
    "Common Moorhen", "Common Nightingale", "Common Starling", "Common Swift",
    "Corsican Nuthatch", "Dunnock", "Eastern Imperial Eagle", "Eleonora's Falcon",
    "Eurasian Collared-Dove", "Eurasian Golden Oriole", "Eurasian Green Woodpecker", "Eurasian Hobby",
    "Eurasian Jay", "Eurasian Magpie", "Eurasian Nutcracker", "Eurasian Nuthatch",
    "Eurasian Sparrowhawk", "Eurasian Tree Sparrow", "European Bee-Eater", "European Goldfinch",
    "European Honey Buzzard", "European Robin", "European Roller", "European Turtle Dove",
    "Goldcrest", "Great Crested Grebe", "Great Tit", "Greater Flamingo",
    "Grey Heron", "Greylag Goose", "Griffon Vulture", "Hawfinch",
    "Hooded Crow", "House Sparrow", "Lesser Whitethroat", "Little Bustard",
    "Little Owl", "Long-tailed Tit", "Moltoni's Warbler", "Montagu's Harrier",
    "Mute Swan", "Northern Gannet", "Northern Goshawk", "Parrot Crossbill",
    "Red Kite", "Red Knot", "Red-backed Shrike", "Red-legged Partridge",
    "Ruff", "Savi's Warbler", "Short-toed Treecreeper", "Snow Bunting",
    "Snowy Owl", "Squacco Heron", "Thekla's Lark", "White Stork",
    "White Wagtail", "White-backed Woodpecker", "White-throated Dipper", "Wilson's Storm-Petrel",
    "Yellowhammer",
    
    # Oceania Expansion (95 birds)
    "Abbott's Booby", "Australasian Pipit", "Australasian Shoveler", "Australian Ibis",
    "Australian Magpie", "Australian Owlet-Nightjar", "Australian Raven", "Australian Reed Warbler",
    "Australian Shelduck", "Australian Zebra Finch", "Black Noddy", "Black Swan",
    "Black-shouldered Kite", "Blyth's Hornbill", "Brolga", "Brown Falcon",
    "Budgerigar", "Cockatiel", "Count Raggi's Bird-of-Paradise", "Crested Pigeon",
    "Crimson Chat", "Eastern Rosella", "Eastern Whipbird", "Emu",
    "Galah", "Golden-headed Cisticola", "Gould's Finch", "Green Pygmy-Goose",
    "Grey Butcherbird", "Grey Shrike-thrush", "Grey Teal", "Grey Warbler",
    "Grey-headed Mannikin", "Horsfield's Bronze-Cuckoo", "Horsfield's Bushlark", "Kakapo",
    "Kea", "Kelp Gull", "Kereru", "Korimako",
    "Laughing Kookaburra", "Lesser Frigatebird", "Lewin's Honeyeater", "Little Penguin",
    "Little Pied Cormorant", "Magpie-lark", "Major Mitchell's Cockatoo", "Malleefowl",
    "Maned Duck", "Many-colored Fruit-Dove", "Masked Lapwing", "Mistletoebird",
    "Musk Duck", "New Holland Honeyeater", "Noisy Miner", "North Island Brown Kiwi",
    "Orange-footed Scrubfowl", "Pacific Black Duck", "Peaceful Dove", "Pesquet's Parrot",
    "Pheasant Coucal", "Pink-eared Duck", "Plains-wanderer", "Princess Stephanie's Astrapia",
    "Pukeko", "Rainbow Lorikeet", "Red Wattlebird", "Red-backed Fairywren",
    "Red-capped Robin", "Red-necked Avocet", "Red-winged Parrot", "Regent Bowerbird",
    "Royal Spoonbill", "Rufous Banded Honeyeater", "Rufous Night Heron", "Rufous Owl",
    "Sacred Kingfisher", "Silvereye", "South Island Robin", "Southern Cassowary",
    "Spangled Drongo", "Splendid Fairywren", "Spotless Crake", "Stubble Quail",
    "Sulphur-crested Cockatoo", "Superb Lyrebird", "Tawny Frogmouth", "Tui",
    "Wedge-tailed Eagle", "Welcome Swallow", "White-bellied Sea-Eagle", "White-breasted Woodswallow",
    "White-faced Heron", "Willie Wagtail", "Wrybill",
    
    # Asia Expansion (90 birds)
    "Ashy Drongo", "Asian Barred Owlet", "Asian Emerald Cuckoo", "Asian Fairy-bluebird",
    "Asian Koel", "Asian Openbill", "Baikal Teal", "Bar-headed Goose",
    "Black Drongo", "Black Kite", "Black-crowned Night Heron", "Black-naped Monarch",
    "Black-naped Oriole", "Blue Rock Thrush", "Blue Whistling Thrush", "Cattle Egret",
    "Chinese Bamboo Partridge", "Chinese Grosbeak", "Cinereous Vulture", "Common Hoopoe",
    "Common Iora", "Common Kingfisher", "Common Myna", "Common Tailorbird",
    "Coppersmith Barbet", "Crested Serpent Eagle", "Crested Wood Partridge", "Dollarbird",
    "Eurasian Curlew", "Eurasian Hoopoe", "Forest Owlet", "Great Hornbill",
    "Great Indian Bustard", "Greater Adjutant", "Greater Coucal", "Greater Painted-Snipe",
    "Green Imperial Pigeon", "Hill Myna", "House Crow", "Indian Cormorant",
    "Indian Grey Hornbill", "Indian Peafowl", "Indian Pitta", "Indian Pond Heron",
    "Indian Roller", "Indian Vulture", "Japanese Bush Warbler", "Japanese Tit",
    "Jungle Crow", "Kalij Pheasant", "Large-billed Crow", "Long-tailed Minivet",
    "Long-tailed Shrike", "Mandarin Duck", "Narcissus Flycatcher", "Nutmeg Mannikin",
    "Oriental Magpie-Robin", "Oriental White-eye", "Pied Bushchat", "Pied Myna",
    "Pin-tailed Snipe", "Plain Prinia", "Puff-throated Babbler", "Purple Heron",
    "Purple Sunbird", "Red Junglefowl", "Red-billed Blue Magpie", "Red-vented Bulbul",
    "Red-wattled Lapwing", "Red-whiskered Bulbul", "Rock Pigeon", "Rook",
    "Rose-ringed Parakeet", "Rufous Treepie", "Scaly-breasted Munia", "Siberian Crane",
    "Spot-billed Duck", "Spotted Dove", "Striated Heron", "Tufted Duck",
    "Violet Cuckoo", "White Wagtail", "White-breasted Kingfisher", "White-rumped Shama",
    "White-throated Kingfisher", "Yellow-billed Babbler", "Yellow-browed Bunting", "Yellow-footed Green Pigeon",
]


class Game(object):
    def __init__(self):
        self.score = 0
        self.total_questions = 0
        self.current_audio = None


def get_recording(bird_name, max_retries=3):
    """Fetch a recording from Xeno-canto API."""
    base_url = "https://xeno-canto.org/api/2/recordings"
    
    # Try quality A first
    qualities = ["A", "B", ""]
    
    for quality in qualities:
        query = bird_name
        if quality:
            query += " q:" + quality
        
        encoded_query = urllib.quote(query.encode('utf-8'))
        url = base_url + "?query=" + encoded_query
        
        try:
            response = urllib2.urlopen(url, timeout=60)
            data = json.loads(response.read().decode('utf-8'))
            response.close()
            
            valid_recordings = filter_valid_recordings(data.get("recordings", []))
            
            if valid_recordings:
                return random.choice(valid_recordings)
        except Exception as e:
            print("Error fetching recordings: " + str(e))
            continue
    
    return None


def filter_valid_recordings(recordings):
    """Filter for valid recordings with proper URLs."""
    valid = []
    
    # First try to get xeno-canto.org recordings
    for rec in recordings:
        file_url = rec.get("file", "")
        if file_url and file_url.startswith("http") and "xeno-canto.org" in file_url:
            valid.append(rec)
    
    # If none found, accept any valid URL
    if not valid:
        for rec in recordings:
            file_url = rec.get("file", "")
            if file_url and file_url.startswith("http"):
                valid.append(rec)
    
    return valid


def download_audio(audio_url):
    """Download audio file to temporary location."""
    if not audio_url:
        return None
    
    try:
        response = urllib2.urlopen(audio_url, timeout=60)
        data = response.read()
        response.close()
        
        if not data:
            return None
        
        # Create temporary file
        fd, temp_path = tempfile.mkstemp(suffix=".mp3", prefix="bird-")
        
        with os.fdopen(fd, 'wb') as f:
            f.write(data)
        
        return temp_path
    except Exception as e:
        print("Error downloading audio: " + str(e))
        return None


def play_audio_file(filename):
    """Play audio file using system audio player."""
    system = platform.system()
    
    try:
        if system == "Darwin":  # macOS
            ret = subprocess.call(["afplay", filename])
            return ret == 0
        elif system == "Linux":
            # Try different players
            players = [
                ["mpg123", "-q", filename],
                ["ffplay", "-nodisp", "-autoexit", "-t", "10", filename],
                ["mplayer", "-really-quiet", filename],
                ["play", "-q", filename]
            ]
            
            devnull = open(os.devnull, 'w')
            for cmd in players:
                try:
                    ret = subprocess.call(cmd, stdout=devnull, stderr=devnull)
                    devnull.close()
                    if ret == 0 or ret == -15:  # 0 = success, -15 = SIGTERM (timeout ok)
                        return True
                    # If command exists but failed, try next
                except OSError:
                    # Command not found, try next
                    continue
            devnull.close()
            
            print("No audio player found. Install mpg123, ffplay, mplayer, or sox.")
            return False
        elif system == "Windows":
            # Use PowerShell
            cmd = ["powershell", "-c", 
                   "(New-Object Media.SoundPlayer '" + filename + "').PlaySync()"]
            ret = subprocess.call(cmd)
            return ret == 0
        else:
            print("Unsupported OS: " + system)
            return False
        
    except Exception as e:
        print("Error playing audio: " + str(e))
        return False


def generate_options(correct_bird):
    """Generate multiple choice options."""
    options = [correct_bird]
    
    while len(options) < 4:
        random_bird = random.choice(WINGSPAN_BIRDS)
        if random_bird not in options:
            options.append(random_bird)
    
    random.shuffle(options)
    return options


def play_round(game):
    """Play one round of the game."""
    # Clean up previous audio
    if game.current_audio and os.path.exists(game.current_audio):
        os.remove(game.current_audio)
        game.current_audio = None
    
    # Select random bird
    correct_bird = random.choice(WINGSPAN_BIRDS)
    
    print("Fetching bird call for question " + str(game.total_questions + 1) + "...")
    
    # Try to get a recording
    max_retries = 5
    recording = None
    
    for attempt in range(1, max_retries + 1):
        recording = get_recording(correct_bird)
        if recording and recording.get("file"):
            break
        if attempt < max_retries:
            print("Retry " + str(attempt) + "/" + str(max_retries - 1) + "...")
            time.sleep(1)
    
    if not recording or not recording.get("file"):
        print("Error: Could not fetch recording for " + correct_bird + " after " + str(max_retries) + " attempts")
        print("Skipping this round...")
        return True
    
    print("Found recording: " + recording['file'])
    print("Downloading audio (this may take a moment)...")
    
    # Download audio
    audio_file = None
    for attempt in range(1, max_retries + 1):
        audio_file = download_audio(recording["file"])
        if audio_file:
            break
        if attempt < max_retries:
            print("Download retry " + str(attempt) + "/" + str(max_retries) + "...")
            time.sleep(1)
    
    if not audio_file:
        print("Error downloading audio after " + str(max_retries) + " attempts")
        print("Skipping this round...")
        return True
    
    game.current_audio = audio_file
    
    # Verify file
    try:
        file_size = os.path.getsize(audio_file)
        if file_size == 0:
            print("Error: Downloaded file is empty")
            print("Skipping this round...")
            os.remove(audio_file)
            return True
        print("✓ Audio ready (" + str(file_size // 1024) + " KB)")
    except Exception:
        print("Error: Invalid audio file")
        print("Skipping this round...")
        return True
    
    # Generate options
    options = generate_options(correct_bird)
    
    # Play audio
    print()
    print("🎵 Playing bird call...")
    if not play_audio_file(audio_file):
        print("Error playing audio. The file may be corrupted.")
        print("Skipping this round...")
        return True
    
    # Quiz loop
    while True:
        print()
        print("Which bird species is this?")
        print()
        
        for i, option in enumerate(options, 1):
            print(str(i) + ". " + option)
        print("R. Replay bird call")
        
        print()
        user_input = raw_input("Your answer (1-4 or R to replay): ").strip().upper()
        
        if user_input == "R":
            print("🎵 Replaying bird call...")
            play_audio_file(audio_file)
            continue
        
        try:
            answer = int(user_input)
        except ValueError:
            print("Invalid input! Please enter 1-4 or R")
            continue
        
        game.total_questions += 1
        
        if answer < 1 or answer > 4:
            print("❌ Invalid choice!")
            print("The correct answer was: " + correct_bird)
            break
        
        if options[answer - 1] == correct_bird:
            game.score += 1
            print("✅ Correct! Well done!")
        else:
            print("❌ Incorrect! The correct answer was: " + correct_bird)
        
        # Show recording info
        loc = recording.get("loc", "")
        cnt = recording.get("cnt", "")
        if loc and cnt:
            print("   Recording location: " + loc + ", " + cnt)
        
        quality = recording.get("q", "")
        length = recording.get("length", "")
        info = "   Quality: " + quality
        if length:
            info += " | Length: " + length
        print(info)
        
        # Option to replay after answering
        while True:
            print()
            replay = raw_input("Listen again? (y/n): ").strip().lower()
            if replay == "y":
                print("🎵 Replaying bird call...")
                play_audio_file(audio_file)
            else:
                break
        
        break
    
    return True


def main():
    random.seed()
    
    print("🦅 Welcome to the Wingspan Bird Quiz! 🦅")
    print("========================================")
    print("Featuring birds from all Wingspan expansions!")
    print("Listen to bird calls and guess the species!")
    print()
    
    game = Game()
    
    while True:
        if not play_round(game):
            break
        
        print()
        print("Current Score: " + str(game.score) + "/" + str(game.total_questions))
        print()
        
        response = raw_input("Play another round? (y/n): ").strip().lower()
        if response != "y":
            break
        print()
    
    # Clean up
    if game.current_audio and os.path.exists(game.current_audio):
        os.remove(game.current_audio)
    
    print()
    print("========================================")
    if game.total_questions > 0:
        percentage = (float(game.score) / game.total_questions) * 100
        print("Final Score: " + str(game.score) + "/" + str(game.total_questions) + " (" + "{:.1f}".format(percentage) + "%)")
    print("Thanks for playing!")


if __name__ == "__main__":
    main()
