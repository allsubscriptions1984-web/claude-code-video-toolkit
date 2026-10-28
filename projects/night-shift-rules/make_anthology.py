#!/usr/bin/env python3
"""Write scenes.json + SCRIPT.md for "3 Night Shift Horror Stories Animated".

Each scene: (chapter or None, slug, narration, shots). A shot starting with
"CLIP:" is an LTX-2 motion clip, "CARD:" is a locally rendered text card
(exact typography, no AI-generated letters), anything else is a FLUX.2 still.
Run from the project dir: uv run make_anthology.py
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
WPM = 145

STYLE = ("dark 2D animated horror illustration, flat cel shading, muted desaturated palette of "
         "sodium orange, sickly green and deep blue-black, heavy black shadows, thick clean outlines, "
         "film grain, cinematic 16:9 wide shot, no text, no words, no letters")
SAM = "a young night-shift clerk in a dark green work vest, seen from behind or in silhouette, face hidden"
NADIA = "a night nurse in dark navy scrubs, seen from behind or in silhouette, face hidden"
JONAH = "a young motel night clerk in a faded flannel shirt, seen from behind or in silhouette, face hidden"
WET_MAN = "a very tall gaunt man in a long black soaked coat, face lost in shadow"
WADE = "a gaunt man in a long dark soaked coat, hair plastered flat, face in shadow"

S = [
    # ---------------- COLD OPEN ----------------
    ("Three Night Shifts", "rules", "Every night shift comes with rules. And every rule was written by someone who broke it first.",
     ["CLIP: slow push in along an empty two-lane highway at night through fog, a single flickering sodium streetlight, a green road sign reading nothing, light snow"]),
    (None, "tease-coins", "At a gas station on Route 9, rule seven says: never serve the man who pays in wet coins.",
     ["CLIP: extreme close-up of old green rusted coins on a glass counter, water slowly spreading from each coin in rings, fluorescent flicker"]),
    (None, "tease-314", "At Saint Agnes Hospital, the call light in room three fourteen comes on every night. That patient went home three years ago.",
     ["CLIP: an empty hospital corridor at night, one red call light glowing above a closed door at the far end, linoleum reflecting it, every other room dark"]),
    (None, "tease-room-nine", "And at the Pinewood Motor Lodge, the same guest checks into room nine at three thirty three in the morning. He's been checking in since nineteen eighty seven.",
     ["CLIP: a small roadside motel at night in pouring rain, a buzzing red neon vacancy sign, one door numbered nine slightly open with darkness inside, a wet handprint on the door"]),
    (None, "one-road", "Three night shifts. One road. Stay for the last one, because the third story explains the first.",
     ["CARD: title — 3 NIGHT SHIFT HORROR STORIES over the fog highway clip, neon-flicker reveal"]),

    # ---------------- STORY 1 ----------------
    ("Story 1: The Gas Station Rules", "listing", "My name is Sam, and for three weeks last winter I worked the night shift at a gas station on Route 9. I'm only telling this now because the listing is up again. Same pay. Same words. No experience needed.",
     ["CLIP: a lonely gas station at night in winter, canopy lights humming, a paper help wanted sign taped to the door glass flutters, highway disappearing into black fog",
      "close-up of a paper help wanted sign taped inside dirty door glass, frost at the edges, blurred canopy lights behind"]),
    (None, "rent", "The pay was almost double anything else in town, and I was two months behind on rent. So I didn't ask why a gas station in the middle of nowhere needed someone awake from ten at night until six in the morning.",
     [f"{SAM} sitting in a tiny cold apartment at night holding an overdue rent notice, a single lamp",
      "a gas station alone at the edge of a pine forest at night, nothing else for miles, wide establishing shot"]),
    (None, "hale", "The owner, Mr. Hale, met me at ten. He had a heavy coat on, and he never took it off. He handed me the keys, said the regulars were quiet, and left. Fast. He didn't check the till, didn't show me the safe, and didn't turn his headlights on until he hit the highway.",
     [f"{SAM} receiving a ring of keys from a nervous older man in a heavy grey coat who is already turning to leave, gas station doorway at night",
      "CLIP: an old pickup truck pulling away from the gas station into the dark with its headlights off, red brake lights only"]),
    (None, "sheet", "Under the register, taped to the wood, was a sheet of yellow paper. Ten rules. Three different handwritings, like three different people had added to it over the years.",
     ["close-up under a cash register counter: a yellowed sheet of paper taped to old wood, rows of scrawled lines, harsh fluorescent glow, a hand reaching toward it"]),
    (None, "rules-1-3", "Rule one: if a car pulls up with no headlights, do not look at the driver. Rule two: if anyone asks for the bathroom key, the bathroom is broken. Rule three: never open the freezer at the back after three in the morning. Not even if something inside is knocking.",
     ["extreme close-up of an old rules sheet in shadow, a finger tracing the first lines, the writing too blurred to read",
      "an old chest freezer at the back of a dim convenience store, its lid closed, frost creeping out from under the seal"]),
    (None, "rules-5-9", "Rule five: the radio stays on the country station. If it changes by itself, don't change it back. Rule nine: if you hear someone call your name from the parking lot, it is not anyone you know.",
     ["an old portable radio on a shelf behind the counter, its dial glowing amber",
      "an empty gas station parking lot seen from inside through the window, snow falling, darkness between the pumps"]),
    (None, "rule-seven", "And rule seven was underlined twice, so hard the pen had torn the paper. Never serve the man who pays in wet coins.",
     ["extreme close-up of one line on the rules sheet underlined twice in red ink so hard the paper is torn, a single drop of water landing on it"]),
    (None, "two-am", "I laughed. I thought it was a prank for the new kid. I put the sheet back, opened a bag of chips, and didn't think about it again. Until two in the morning.",
     [f"{SAM} slouched behind the counter scrolling a phone, a wall clock at two, the store empty and humming, dark windows"]),

    ("No Headlights", "no-headlights", "The lights over the pumps flickered, all at once, and a black car rolled up to pump four. No headlights. No engine sound. It just arrived, like it had been there all along and I'd only now noticed.",
     ["CLIP: a black sedan with headlights off rolls silently up to pump four under flickering canopy lights, the windshield a void of shadow"]),
    (None, "dont-look", "I didn't look. I don't know why, but I didn't. I stared at the cigarette rack so hard my eyes watered, and I listened to the pump click and hum, click and hum, for almost ten minutes.",
     [f"{SAM} staring rigidly at a cigarette rack, shoulders tense, while in the window reflection a dark car waits at the pump"]),
    (None, "nozzle", "When it stopped, the car was gone. The register showed no sale. But the nozzle was hanging back in its holster, dripping, and what dripped from it wasn't gas. It was thick, and dark, and it was warm.",
     ["CLIP: close-up of a gas pump nozzle in its holster slowly dripping thick dark liquid onto wet concrete, steam rising, sodium light"]),
    (None, "bare-feet", "The next night, a woman in a thin summer dress came in and asked for the bathroom key. It was January. Her feet were bare, and they left no prints on the wet floor.",
     ["a pale barefoot woman in a thin faded summer dress standing in a convenience store, snow on the window behind her, wet floor with no footprints, her face in shadow"]),
    (None, "too-wide", "I said it was broken. She smiled, and her smile kept going, a little wider than a face should allow. That's alright, she said. I'll wait for the next one. Then she walked out toward the highway, and the snow didn't seem to touch her.",
     ["CLIP: the pale woman's smile stretched unnaturally wide, eyes hidden in shadow, harsh fluorescent light, unsettling but not gory",
      "a woman in a summer dress walking away down a dark snowy highway, snowflakes passing through her"]),
    (None, "like-a-prayer", "By the end of the first week, I'd stopped laughing at the rules. I read them at the start of every shift, like a prayer. And I started noticing things. The freezer at the back was never plugged in. It was always cold anyway.",
     [f"{SAM} reading the rules sheet under a single flickering tube light, aisles fading into darkness",
      "close-up of an unplugged freezer cord lying on the floor beside a frosted freezer, breath visible in the cold air"]),
    (None, "knocks", "On the ninth night, at three ten, something inside it knocked. Three slow knocks. Then a pause. Then three more. I turned the radio up and sang along to songs I didn't know, until the sun came up.",
     ["CLIP: the lid of a frosted chest freezer at the back of a dark store jolts slightly three times, frost cracking, a single bulb swaying",
      f"{SAM} hunched behind the counter with hands over ears, a radio turned up loud, pale dawn light at the windows"]),
    (None, "static", "On the eleventh night, the radio changed by itself. The country station turned to static, and under the static was a voice, reading numbers. I didn't touch it. At five, it switched back, mid-song, like nothing had happened.",
     ["close-up of an old radio dial sliding on its own, the amber glow turning sickly green, static lines in the air"]),
    (None, "my-name", "Then, on the fourteenth night, I broke a rule. Just a small one. Someone called my name from the parking lot. Sam. In my mom's voice. And for one second, I forgot, and I looked up.",
     [f"{SAM} looking up sharply toward the store window, the dark parking lot beyond"]),
    (None, "canopy-lights", "There was no one at the pumps. But every single light on the canopy had turned to face the store. And in the dark between them, something was standing very still, and it was wearing my mom's coat.",
     ["CLIP: gas station canopy lights slowly swivel to face the camera, and in the darkness between two pumps a tall still figure in a woman's winter coat stands motionless"]),
    (None, "footprints", "I locked the doors. I called my mom. She picked up on the first ring, half asleep, and asked why I was calling at three in the morning. When I looked back outside, the lot was empty. But there were footprints in the snow. They led right up to the glass, and stopped.",
     [f"{SAM} on a phone, one hand pressed against the locked glass door",
      "a line of footprints in fresh snow leading straight up to the store window and stopping at the glass, a faint handprint of frost on the window"]),
    (None, "every-rule", "After that, I followed every rule. All of them. Every night. And every night, I read rule seven, because it was the only one that didn't say what would happen.",
     ["the rules sheet taped under the counter, rule seven's red underline glowing faintly in the dark"]),

    ("Wet Coins", "thursday", "He came in on a Thursday, at three fifteen. Tall, long coat, soaked through, though it hadn't rained in a month. Water ran off him and pooled on the floor, and he didn't seem to notice.",
     [f"CLIP: {WET_MAN} steps inside a gas station door, water streaming off him and pooling on the tile floor, dry night outside, fluorescent light buzzing"]),
    (None, "quiet", "The radio went quiet. Not static. Just quiet. Even the fridges stopped humming, like the whole store was holding its breath.",
     ["a row of convenience store fridges going dark one by one, the aisle silent and still"]),
    (None, "coins", "He put a can of coffee on the counter. Then, one by one, he laid down coins. Old ones. Green with rust. Each one left a ring of water on the glass.",
     ["close-up on a glass counter: a can of coffee and a row of old green rust-crusted coins, each leaving a ring of water, a long pale dripping hand placing one more"]),
    (None, "took-coins", "I should have said no. Rule seven was right there, under my hand. But he looked so tired. His hands were shaking. And it was only coffee. So I took the coins. They were cold, colder than ice, and they kept dripping in the drawer.",
     ["the rules sheet visible under a clerk's hand on the counter, the tall wet man's shaking hands beyond",
      "close-up of hands sliding dripping rusty coins into an open cash drawer, frost spreading across the metal"]),
    (None, "smile", "For the first time, he looked up at me. He smiled, and his mouth was full of black water. Thank you, he said. I've been waiting so long for someone new.",
     [f"CLIP: {WET_MAN} slowly raises his head and smiles, black water spilling over his lips, eyes hidden, flickering light"]),
    (None, "rule-eleven", "When he left, I turned the sheet of rules over. There was an eleventh rule on the back that I'd never seen. The ink was still wet. If you served him, you are the night shift now.",
     ["the back of the yellowed rules sheet, a single line of fresh dark ink still glistening and running, a trembling hand holding the corner"]),
    (None, "phone", "I called Mr. Hale. His number rang and rang. Then, somewhere behind me, another phone started ringing. The old phone under the counter. The one with its cord cut clean through.",
     ["an old beige wall phone under the counter, its cord cut clean through and dangling, the handset trembling as if ringing"]),
    (None, "walk", "I didn't answer it. At the first grey light of dawn, I grabbed my coat, pushed through the doors, and walked. Past pump four. Past the sign. Toward the highway. And I walked. And I walked.",
     [f"{SAM} walking away from the gas station along the snowy highway shoulder in grey dawn light"]),
    (None, "loop", "And the gas station was in front of me again. Same canopy. Same lights. Same pump four, dripping.",
     [f"CLIP: {SAM} walks up a foggy highway and the same gas station slowly emerges from the fog ahead, canopy lights flickering on"]),
    (None, "still-here", "I don't know how long I've been here. The sun comes up, but it never quite reaches the store. The coins in the drawer are still wet. Sometimes, late at night, I hear my name from the parking lot. I don't look up anymore.",
     ["a gas station under a strange sky where dawn light stops at the edge of the lot, the store still in darkness",
      f"{SAM} sitting very still behind the counter, head bowed, the dark lot beyond the window"]),
    (None, "fourth-hand", "So I wrote a new sheet of rules, for whoever answers the listing next. It's in my handwriting now. That's four handwritings on the page. I added one rule at the bottom.",
     ["a hand writing at the bottom of a yellowed rules sheet by the light of a flickering tube, the writing too small to read"]),
    (None, "rule-twelve", "Rule twelve. If a car rolls up with no headlights, don't look at the driver. It might be me. And I've been waiting so long for someone new.",
     ["CLIP: a black car with no headlights rolls slowly out of the fog toward the camera on an empty highway, a silhouette in a green vest behind the wheel"]),

    # ---------------- STORY 2 ----------------
    ("Story 2: The Night Nurse", "pager", "My name is Nadia, and I was a night nurse on the third floor of Saint Agnes Hospital, out on Route 9. I lasted nine weeks. I still have the pager. It still goes off.",
     ["CLIP: a small old hospital on a dark highway at night in light rain, one lit window on the third floor",
      "close-up of an old hospital pager in a dark kitchen drawer, its tiny screen glowing green"]),
    (None, "loans", "I took nights for the money. The night differential, plus a bonus nobody else wanted, because nobody else stayed. I had sixty thousand dollars in nursing school loans, and in the interview they told me the third floor pays for itself.",
     [f"{NADIA} at a kitchen table at night covered in loan statements",
      "a dim hospital interview office, a clipboard and a pen pushed across a desk"]),
    (None, "ruth", "The charge nurse was named Ruth. She'd worked nights at Saint Agnes for thirty one years. On my first shift, she walked me down the hall, stopped outside room three fourteen, and put her hand flat on the door, like she was checking it for heat.",
     ["an older nurse with grey hair in a bun, seen from behind, pressing her palm flat against a closed hospital door at the end of a dim corridor"]),
    (None, "warning", "This room is empty, she said. It has been for three years. The call light will come on tonight. It comes on every night. Don't answer it after three. And whatever you do, don't let anyone sign you out.",
     ["a dark hospital corridor seen from the nurses station, one call light glowing above room three fourteen at the far end"]),
    (None, "youll-know", "I asked what that meant. She just said, you'll know. Then she went back to her charts like we'd been talking about the weather.",
     ["an older nurse calmly writing in paper charts under a desk lamp at a nurses station, the corridor behind her black"]),
    (None, "first-light", "At one forty, the board at the nurses station lit up. Room three fourteen. A soft little chime, over and over. I looked at Ruth. She didn't even look up. Before three, she said. Go on. It's just him asking for water.",
     ["CLIP: a call light board at a hospital nurses station, one small red light blinking on and off steadily in the dark"]),

    ("Room 314", "cold-room", "The room was dark and cold, colder than the hall, and it smelled like a hospital from when I was a kid. Old soap. Old flowers. The bed was made with tight corners, the way nobody makes beds anymore.",
     [f"CLIP: {NADIA} standing in the doorway of a cold dark hospital room, an old-fashioned bed made with tight corners, wilted flowers on the sill"]),
    (None, "dent", "But the pillow had a dent in it. A deep one. Like someone heavy had just lifted his head. And on the tray table, there was a plastic cup, full of water, and it was still sweating.",
     ["close-up of a hospital pillow with a deep fresh dent, and a plastic cup of water beading with condensation on a tray table"]),
    (None, "thank-you", "I said hello. Nobody answered. The call light over the bed clicked off by itself, and from the bathroom, very quietly, someone said: thank you, nurse.",
     ["CLIP: in a dark hospital room the red call light above the bed clicks off, and the bathroom door stands slightly ajar on pure darkness"]),
    (None, "polite", "I didn't open the bathroom door. I walked out, very calmly, and then I walked a lot faster. Ruth handed me a cup of coffee like she'd been expecting me. Mister Ward, she said. He's polite. That's the worst part.",
     [f"{NADIA} walking fast down a dark corridor away from the camera",
      "an older nurse holding out a paper cup of coffee at the nurses station, her face in shadow"]),
    (None, "file", "I looked him up. Ellis Ward, seventy eight. Admitted for pneumonia. Discharged three years ago, on the night shift, at three thirty in the morning. The nurse who signed him out used only initials. And there was no record of anyone picking him up.",
     ["a glowing old computer monitor in a dark nurses station showing a blurred patient record, a hand on the mouse"]),
    (None, "blinds", "For three weeks, I learned the third floor. The call light in three fourteen came on every night. Before three, it was always something small. Water. A blanket. Once, he asked me to open the blinds, so he could see the road.",
     ["a hospital window with half-open blinds looking down on a dark empty highway, a faint reflection of a thin old man in the glass"]),
    (None, "elevator", "And I learned other things. The elevator stops on the third floor at two in the morning, even when nobody calls it. The doors open. Nobody gets out. Ruth said to always say good evening to it, and I did, every time, and I felt stupid, and I kept doing it.",
     ["CLIP: hospital elevator doors slide open on an empty brightly lit elevator in a dark corridor, the light flickering, nobody inside",
      f"{NADIA} standing facing the open empty elevator, head slightly bowed"]),
    (None, "census", "Every night at midnight, the printer at the station prints the census, the list of everybody on the floor. Every night, room three fourteen was on it. Ward, Ellis. Status: pending discharge.",
     ["an old printer at a nurses station slowly feeding out a sheet of paper in the dark, its green light the only glow"]),
    (None, "pending", "Pending. For three years.",
     ["close-up of a printed hospital census sheet, one row highlighted by a shaking pen, the words too blurred to read"]),
    (None, "ruth-out", "On my twenty first shift, Ruth didn't come in. Called out sick, they said, the first time in thirty one years. They sent a traveling nurse up from the second floor who'd never worked nights here. She didn't know the rules. I hadn't thought to tell her.",
     ["an empty chair at the nurses station with Ruth's cardigan still on it",
      "a young cheerful nurse in light blue scrubs, seen from behind, arriving at the nurses station with a coffee"]),
    (None, "ive-got-it", "At three fifteen, the call light in three fourteen came on. And before I could stop her, she said, I've got it, and she was already walking down the hall.",
     ["CLIP: a young nurse in light blue scrubs walks away down a long dark corridor toward a single red call light, the corridor stretching"]),

    ("Pending Discharge", "light", "I ran after her. By the time I got there, the door was closed, and through the little window the room was full of light. Warm, bright, normal light. And the bed wasn't empty anymore.",
     ["CLIP: the small wired-glass window in a hospital door, warm golden light glowing through it into the dark corridor"]),
    (None, "old-man", "There was an old man sitting up in it. Thin, grey, a hospital bracelet loose on his wrist. And standing next to him, holding a clipboard, was the traveling nurse. She was smiling at him, and nodding, and there was a pen in her hand.",
     ["seen through a door window: a thin grey old man sitting up in a hospital bed in warm light, a young nurse beside him holding a clipboard and pen, both turned away"]),
    (None, "her-name", "Except it wasn't her clipboard. It was his. He was holding it out to her. And the papers on it weren't his discharge papers. The name at the top was hers.",
     ["close-up of a frail old hand holding out a clipboard of discharge forms, a young nurse's pen hovering over the signature line, writing unreadable"]),
    (None, "locked", "I hit the door with my shoulder. It didn't move. I punched the code into the keypad, and it beeped, and it beeped, and it wouldn't open. I grabbed the wall phone to call security, and the line was just water. The sound of running water.",
     [f"{NADIA} slamming a shoulder into a locked hospital door, a keypad blinking red",
      "close-up of a hospital wall phone handset dripping water from the earpiece"]),
    (None, "dont-sign", "Then I remembered what Ruth said. Don't let anyone sign you out. I banged on the glass and screamed her name. Don't sign it. Don't sign anything.",
     [f"{NADIA} pounding both fists on the small glass window of a hospital door, warm light on the other side"]),
    (None, "white-eyes", "She didn't look at me. But the old man did. He turned his head toward the window, slowly, and he smiled. It was a kind smile. A grandfather's smile. And his eyes were completely white.",
     ["CLIP: through a door window an old man in a hospital bed slowly turns his head toward the camera and smiles kindly, his eyes completely white, warm light flickering"]),
    (None, "go-home", "Then a hand touched my shoulder. Ruth. Still in her coat, rain on her hair. She wasn't supposed to be here. Go home, Nadia, she said. This one was always mine.",
     ["an older nurse in a wet raincoat seen from behind, one hand on a younger nurse's shoulder, both facing the glowing door"]),
    (None, "ruth-signs", "She put her hand flat on the door, and it opened for her like it had been waiting. She walked in, took the clipboard out of the traveling nurse's hands, and signed it herself.",
     ["an older nurse in a raincoat inside the warm glowing room taking a clipboard from a young nurse, an old man in bed watching her"]),
    (None, "lights-out", "The lights went out. When they came back on, the room was dark and cold, and the bed was made with tight corners. The traveling nurse was standing in the middle of the room, alone, holding an empty clipboard. Ruth was gone.",
     ["CLIP: a hospital room plunges into darkness then flickers back cold and empty, a young nurse standing alone in the middle holding an empty clipboard",
      "a perfectly made empty hospital bed in cold blue light, no dent in the pillow"]),
    (None, "forty-minutes", "The traveling nurse didn't remember anything. She said she'd walked in, the room was empty, and she'd been standing there for maybe ten seconds. It had been forty minutes.",
     ["a young nurse sitting dazed at the nurses station holding a cup, a wall clock behind her"]),
    (None, "new-census", "At midnight the next night, the printer at the station woke up and printed the census. Room three fourteen was still on it. But the name had changed. Marsh, Ruth. Status: pending discharge.",
     ["CLIP: an old printer at a dark nurses station slowly feeds out a census sheet, a nurse's hand reaching for it"]),
    (None, "letter", "I quit that week. I paid back the bonus and moved two states away. Six months later, a letter came from Saint Agnes. A patient survey. Thank you for your recent stay with us. Clipped to it was a discharge form. Patient name: mine.",
     ["an envelope with a hospital crest on a doormat in a bright new apartment",
      "a discharge form clipped to a letter on a kitchen table, the patient name line circled, writing unreadable"]),
    (None, "not-yet", "At the bottom, in shaky handwriting I'd seen on a thousand charts, there was one line. Not yet, Nadia. I'm still holding your spot.",
     ["close-up of a shaky handwritten line in blue ink at the bottom of a hospital form, slightly damp, the words unreadable"]),
    (None, "drawer", "I never signed it. It's in a drawer with the pager. Every night at three fifteen, the pager goes off. Three numbers on the screen. Three one four. And some nights, if I'm awake, I can hear a voice from the drawer, very quietly. Thank you, nurse.",
     ["CLIP: a kitchen drawer in a dark apartment glows faintly green from inside as an old pager buzzes",
      f"{NADIA} sitting awake in bed in the dark, staring at a closed drawer"]),

    # ---------------- STORY 3 ----------------
    ("Story 3: The Motel Night Desk", "pinewood", "My name is Jonah, and I worked the night desk at the Pinewood Motor Lodge, the last motel on Route 9 before the road goes into the pines. Twelve rooms. A sign that only says vacancy. And one guest who checks in every night at three thirty three.",
     ["CLIP: a small twelve-room roadside motel at the edge of a pine forest at night, a buzzing red neon vacancy sign flickering, empty lot",
      f"{JONAH} behind a wood-panelled motel front desk with a brass bell and key hooks"]),
    (None, "odell", "I needed somewhere to live more than I needed a job. The owner, Mrs. Odell, offered me both. Room one, free, plus cash every Friday. All I had to do was sit at the desk from eleven to seven and hand out keys.",
     ["an elderly woman with a cardigan and reading glasses on a chain, face in shadow, handing over a motel key with a plastic number tag"]),
    (None, "room-nine", "She gave me one instruction. Just one. Room nine is never rented. Not to anyone. Not if every other room is full. Room nine is held for Mister Wade.",
     ["a wall of motel key hooks, every hook with a key, one hook set apart with a key on a faded red tag"]),
    (None, "who-is-wade", "Who's Mister Wade, I asked. And she said: he'll check in tonight. Three thirty three. Give him the key, take his cash, don't make conversation. And don't wipe the counter until the sun is up.",
     ["the elderly owner's hand resting flat on the worn motel counter, a closed guest ledger beside it"]),
    (None, "three-thirty-three", "At three thirty two, every light in the parking lot went out. At three thirty three, the bell over the door rang. There was nobody in the doorway. Then I heard footsteps crossing the lobby. Wet ones. And a man was standing at the desk like he'd always been there.",
     ["CLIP: motel parking lot lights go dark one by one, then the bell above the lobby door swings and rings with nobody in the doorway",
      f"{WADE} standing at the motel desk, water dripping onto the carpet"]),
    (None, "river", "Long dark coat. Soaked. Hair plastered flat. He smelled like a river. He put a hand on the counter, flat, and slid a few folded bills toward me. The bills were wet. Everything about him was wet.",
     ["close-up of a pale wet hand sliding soaked folded dollar bills across a wooden counter, water beading"]),
    (None, "handprint", "He signed the ledger. Wade. Room nine. Then he took the key and walked out into the dark. When I looked down, there was a handprint on the counter. A wet handprint. It didn't dry. It just stayed there, perfectly still, until dawn.",
     ["a gaunt man in a soaked coat walking away from the motel lobby into the black night, a key in his hand",
      "close-up of a perfect wet handprint glistening on a wooden motel counter under a desk lamp"]),

    ("The Ledger", "bathtub", "The next morning, I checked room nine. The bed was made. The towels were folded. The key was back on its hook behind the desk, though nobody ever returned it. But the bathtub was full to the brim. Cold, brown water. And the drain was bone dry.",
     ["a neat old motel room in grey morning light, bed made, towels folded",
      "CLIP: a motel bathtub filled to the brim with still murky brown water, a single ripple spreading across the surface"]),
    (None, "every-night", "He came back the next night. And the next. Every night at three thirty three. Same coat. Same bills. Same handprint, in exactly the same place, down to the crease of the palm.",
     ["three identical wet handprints overlapping perfectly on a motel counter, desk lamp glow"]),
    (None, "ledgers", "One slow night, I pulled the old ledgers out of the back office. Boxes of them, going back decades. And on every single page, at three thirty three, in the same handwriting, there it was. Wade. Room nine.",
     [f"{JONAH} sitting on the floor of a cluttered back office surrounded by stacks of old guest ledgers",
      "close-up of old ledger pages being flipped, the same faded signature repeating line after line, unreadable"]),
    (None, "flood", "I followed it back to the very first entry. October twelfth, nineteen eighty seven. The week Route 9 flooded. The river came over the road and into the ground floor of the Pinewood, and one guest never made it out. Room nine.",
     ["CLIP: archival-looking night scene of a river flooding over a two-lane road into a motel lot, water rising against doors, rain",
      "a motel door numbered nine half underwater at night, a dark coat floating in the water"]),
    (None, "easier", "So I knew what he was. And honestly, it got easier. He never hurt anyone. He paid. He left. I left the counter wet. It was the best job I ever had, for almost two months.",
     [f"{JONAH} reading a paperback at the desk at night, relaxed, a wet handprint glistening beside the book"]),
    (None, "storm", "Then came the storm. Real rain, the kind that turns Route 9 back into a river. By midnight, every room was full. Truckers. A couple on their honeymoon. An old man with a dog. Every room except nine.",
     ["CLIP: torrential rain hammering a motel parking lot full of trucks and cars at night, the vacancy sign flickering, water streaming across the asphalt"]),
    (None, "family", "At one in the morning, a car slid into the lot. A family. A mom, a dad, two little kids asleep in the back. The road ahead was closed. The road behind them was closed. They had nowhere to go.",
     ["a station wagon with fogged windows in the flooded motel lot, two small silhouettes asleep in the back seat, parents' silhouettes in front"]),
    (None, "gave-key", "I looked at the key for room nine for a long time. I told myself he'd understand. It was one night. It's what anybody would have done. I gave them the key.",
     ["close-up of a hand lifting the key with the faded red tag off its hook, other hand hesitating"]),

    ("Three Thirty Three", "empty-hook", "At three thirty two, the lights in the lot went out. At three thirty three, the bell rang. Wet footsteps across the lobby. And Mister Wade put his hand flat on the counter and looked at the empty hook where his key should have been.",
     [f"CLIP: {WADE} at the motel desk staring past the clerk at one empty key hook, water pooling at his feet"]),
    (None, "ill-wait", "He didn't get angry. He just looked at me. Then he said, in a voice like water moving through a pipe, then I'll wait. And he stood there. Dripping. Not moving. And the water around his feet didn't stop spreading.",
     ["CLIP: a dark puddle spreads slowly and endlessly across a motel lobby carpet from the feet of a motionless man in a soaked coat"]),
    (None, "rising", "It spread across the lobby. Under the door. Out into the lot. The rain outside got louder, and louder, until I couldn't hear anything else. The water was over my shoes. Then my ankles. And it was coming from him.",
     ["a motel lobby filling with dark water up to the ankles, a desk lamp reflected in it, rain streaming down the windows"]),
    (None, "bathtub-call", "The phone rang. Room nine. It was the dad. His voice was shaking. He said, there's someone in our bathtub. Under the water. With his eyes open. And my kids can hear him talking.",
     ["an old motel desk phone ringing, water around its base, a room nine light lit on the switchboard",
      "CLIP: a motel bathtub full of dark water, the faint pale shape of a face just beneath the surface, eyes open"]),
    (None, "give-yours", "I called Mrs. Odell. She answered on the first ring, like she'd been sitting by the phone for thirty years waiting for this call. I told her. She was quiet for a long time. Then she said: if room nine is ever taken, you give him yours.",
     ["an elderly woman sitting awake in a dark armchair beside an old phone, her hand already on the receiver"]),
    (None, "room-one", "So I did. I took the key to room one, my room, everything I had in the world, and I set it down on the counter, inside the wet handprint. He picked it up. He nodded, once. And the water stopped.",
     ["close-up of a motel key with a tag numbered one being placed inside a wet handprint on the counter, a pale hand reaching for it"]),
    (None, "until-sun", "He signed the ledger. Then he walked out into the rain toward room one. And I sat at the desk, soaked to the knees, until the sun came up.",
     [f"{JONAH} sitting alone at the desk in grey dawn light, soaked trousers, the lobby floor wet but the water gone"]),
    (None, "checkout", "At seven, the family checked out early. The kids were fine. They didn't remember anything. The dad couldn't look at me. And for the first time in two months, room nine's tub was empty. The drain was wet.",
     ["a station wagon pulling out of the motel lot in grey morning light, a child's face in the rear window"]),
    (None, "even", "Room one was another story. My bed was soaked through. My clothes. My books. Everything I owned was full of river water. And on the bathroom mirror, written in the fog, was one word. Even.",
     ["a small motel room with everything soaked, water dripping off the bed, clothes and books sodden",
      "close-up of a fogged bathroom mirror with a single word smeared into the condensation by a finger, the word too blurred to read"]),
    (None, "quiet-week", "Mister Wade never came back after that. I thought it was over. The ledger stayed empty at three thirty three, night after night, for almost a week.",
     ["an open guest ledger on the motel counter with an empty line, a dry counter, desk lamp"]),
    (None, "headlights", "Then, last Tuesday, at three thirty two, the lights in the lot went out. And a black car rolled in. No headlights. No engine. It just arrived. I didn't look at the driver. Something told me not to.",
     ["CLIP: a black sedan with no headlights glides silently into a dark motel parking lot under the red vacancy sign"]),
    (None, "dry-steps", "At three thirty three, the bell rang. The footsteps weren't wet this time. They were slow, and crunching, like someone walking in from the snow. And a young guy in a dark green work vest put a handful of coins on the counter. Old ones. Green with rust. Still dripping.",
     [f"{SAM} standing at the motel desk with snow on his shoulders",
      "close-up of old green rusted coins dripping water onto a wooden motel counter next to the brass bell"]),
    (None, "sam", "He signed the ledger. Then he slid it back to me, and he said, the night shift at the gas station gets lonely. Do you have a room for one night? I looked down at the name. Sam.",
     ["close-up of a guest ledger turned toward the camera, a fresh signature on the newest line, the writing unreadable, a drop of water beside it"]),
    (None, "route-nine", "I gave him room nine. And if you ever drive Route 9 at night, and you pass a gas station with a help wanted sign, or a hospital with one light on, on the third floor, or a motel with a sign that only says vacancy...",
     ["CLIP: slow drive at night down a foggy two-lane highway past a lit gas station, then a hospital with one lit window, then a red neon motel sign"]),
    (None, "keep-headlights", "Keep your headlights on. And don't stop. We're all still working the night shift.",
     ["CARD: end screen — 3 NIGHT SHIFT HORROR STORIES over a dark highway with headlights receding, space for YouTube end-screen elements"]),
]

# Extra stills for motion scenes: an LTX clip runs ~6.7s and build.py boomerangs a clip
# that is shorter than its slot (a car rolling backwards gives the AI away). Each list is
# the scene's full shot order; "@" stands for the scene's own shots in S.
EXTRA = {
    "rules": ["@", "a weathered wooden signpost beside a foggy highway at night, a yellowed paper nailed to it, writing blurred"],
    "tease-coins": ["a gas station alone on a winter highway at night, canopy lights glowing in fog", "@"],
    "tease-314": ["@", "close-up of a hospital call button on a bed rail glowing red in the dark, an empty pillow beside it"],
    "tease-room-nine": ["@", "a brass motel bell on a wooden counter beside a wet handprint, an old wall clock behind it",
                        "an old guest ledger open on a counter, a column of identical faded signatures, unreadable"],
    "listing": ["@", "a phone screen glowing in a dark room showing a job listing, the text blurred and unreadable"],
    "hale": ["an older man in a heavy grey coat standing under the gas station canopy at night, hands deep in his pockets, face in shadow, staring at the road",
             "@0", "a dusty old cash register and a closed safe behind the counter, untouched, fluorescent light", "@1"],
    "no-headlights": ["@", "close-up of a black car's dark windshield at a gas pump, only shadow inside, canopy light reflecting",
                      "a gas pump display counting up on its own, glowing green in the dark, digits unreadable"],
    "nozzle": ["an empty pump bay under flickering lights, the black car gone, faint tire tracks on wet concrete",
               "close-up of a cash register screen glowing in the dark showing no sale, unreadable", "@"],
    "too-wide": ["close-up of a pale bare foot on a wet tile floor, snow on the doormat behind it", "@0",
                 "a convenience store glass door swinging shut, a figure in a summer dress outside in the snow, back turned", "@1"],
    "knocks": ["@0", "an old radio on a shelf with its volume knob turned all the way up, store shelves trembling", "@1"],
    "canopy-lights": ["the empty parking lot seen through the store window, snow falling, pumps standing silent", "@",
                      "a figure in a long woman's winter coat standing between two gas pumps in deep shadow, no face visible"],
    "thursday": ["a wall clock in a convenience store at a quarter past three, the second hand frozen", "@",
                 "a spreading pool of water on a tile floor around the hem of a long soaked black coat"],
    "smile": ["close-up of a can of coffee on the counter, a dripping coin beside it, a long wet coat out of focus behind",
              f"a clerk's hands frozen on the counter, {WET_MAN} looming beyond, head still bowed", "@"],
    "loop": ["@", "a gas station canopy glowing ahead on a foggy highway, footprints in the snow leading toward it"],
    "rule-twelve": ["close-up of the bottom of a handwritten rules sheet, a fresh line of ink, unreadable",
                    "a dark windshield with the faint silhouette of a driver in a green vest, face hidden, hands on the wheel", "@"],
    "pager": ["@0", "a nurse's badge and a ring of keys on a locker room bench under a flickering light", "@1"],
    "first-light": ["@", "a nurses station at night, an older nurse writing under a desk lamp, the long corridor black behind her",
                    "close-up of an older nurse's hand still writing, not looking up, a coffee cup steaming",
                    "the dark corridor toward room three fourteen, a red light glowing at the far end"],
    "cold-room": ["@", "close-up of wilted flowers in a vase on a windowsill, dust on the petals, cold blue light",
                  "the corner of a hospital bed sheet tucked crisp and perfect, cold light"],
    "thank-you": ["a nurse's hand on a light switch in a dark hospital room, the bed empty", "@"],
    "elevator": ["a hospital elevator floor indicator glowing above closed doors, the hall empty", "@0", "@1",
                 "close-up of an empty elevator floor with one faint wet footprint"],
    "ive-got-it": ["the call light board at a nurses station blinking red beside a wall clock at a quarter past three",
                   "a young nurse in light blue scrubs standing up from a chair, coffee left behind, seen from behind", "@"],
    "light": ["a nurse running down a dark hospital corridor, seen from behind, motion blur", "@",
              "close-up of a nurse's hand gripping a hospital door handle, warm light spilling from under the door"],
    "white-eyes": ["a young nurse in light blue scrubs standing perfectly still beside a hospital bed in warm light, seen through glass",
                   "a frail old hand with a loose hospital bracelet resting on a blanket", "@"],
    "lights-out": ["a hospital corridor ceiling light flickering and dying, darkness spreading", "@0", "@1",
                   "an empty clipboard lying on a hospital floor in cold light"],
    "new-census": ["a nurses station at midnight, a wall clock at twelve, a printer's light blinking on", "@",
                   "close-up of a printed census sheet in a trembling hand, one row circled, unreadable"],
    "drawer": ["a dark bedroom in a small apartment, a digital clock glowing in the night", "@0",
               "close-up of an old pager's tiny green screen glowing inside a drawer, digits blurred", "@1"],
    "pinewood": ["a dark two-lane highway entering a dense pine forest at night, a red glow behind the trees", "@0", "@1",
                 "a dim wood-panelled motel lobby, an old wall clock and a small TV showing static"],
    "three-thirty-three": ["a motel wall clock at three thirty two, a clerk's silhouette behind the desk", "@0",
                           "wet footprints appearing one by one across a motel lobby carpet with no one making them", "@1"],
    "bathtub": ["a motel door numbered nine pushed open by a clerk's hand in grey morning light", "@0",
                "a key with a faded red tag hanging back on its hook behind the empty desk, a drop of water falling from it", "@1"],
    "flood": ["close-up of the first page of an old guest ledger, a yellowed date line and one faded signature, unreadable", "@0",
              "a flooded motel lot at dawn after a storm, rescue lights in the distance, debris in brown water", "@1"],
    "storm": ["@", "a motel lobby crowded at night with tired truckers and travelers dripping rain, the clerk handing out keys",
              "a wall of motel key hooks all empty except one key on a faded red tag"],
    "empty-hook": ["a motel parking lot going dark in heavy rain, the vacancy sign the only light",
                   "the brass bell over a motel door swinging, the doorway empty and black",
                   "close-up of a pale wet hand pressed flat on a counter beside an empty key hook", "@"],
    "ill-wait": ["close-up of a soaked coat collar and a shadowed jaw, water running off the chin", "@",
                 "a clerk behind a motel desk staring down at dark water reaching the base of the counter"],
    "bathtub-call": ["@0", "a frightened father's silhouette in a motel bathroom doorway holding a phone, two small children behind him", "@1"],
    "headlights": ["a motel wall clock at three thirty two, the lot lights outside going dark", "@",
                   "a clerk behind the desk with eyes fixed down on the ledger, refusing to look at the window"],
    "route-nine": ["a gas station with a help wanted sign glowing alone beside a dark highway",
                   "a small hospital at night with a single lit window on the third floor",
                   "a red neon motel sign buzzing in fog beside the highway", "@"],
    # second shot for scenes that would otherwise hold one still for 16s+
    "dont-look": ["@", "the reflection of a dark car at a pump in the glass of a cigarette rack, a clerk's blurred shoulder in the foreground"],
    "static": ["@", "the speaker grille of an old radio glowing sickly green, static lines rippling in the dark air around it"],
    "my-name": ["the snowy parking lot at night seen through the store window, empty pumps, deep shadow between them", "@"],
    "rule-eleven": ["a clerk turning over a yellowed sheet of paper under the counter light, seen from behind", "@"],
    "walk": ["@", "a highway sign at dawn half buried in snow beside an endless empty road, the writing unreadable"],
    "ruth": ["@", "close-up of an older nurse's wrinkled palm pressed flat against a door, the room number plate above blurred"],
    "warning": ["close-up of an older nurse's face half in shadow, only her lips and chin lit, speaking quietly", "@"],
    "dent": ["a hospital bed seen from the doorway, the dented pillow catching the corridor light, the room otherwise dark", "@"],
    "file": ["@", "an old paper discharge record in a manila folder, a signature line with two scrawled initials, unreadable"],
    "blinds": ["a call light glowing over a hospital door at night, a nurse carrying a folded blanket toward it", "@"],
    "old-man": ["@", "close-up of a thin wrist with a loose plastic hospital bracelet, a pen in a young nurse's hand nearby"],
    "odell": ["@", "a modest motel room numbered one with its door open, a narrow bed and a single warm lamp"],
    "who-is-wade": ["@", "close-up of an elderly woman's eyes in shadow behind reading glasses, looking toward the dark door"],
    "river": ["a gaunt man in a soaked coat seen from the side at the motel desk, water dripping from his sleeve onto the floor", "@"],
    "easier": ["@", "the motel at dawn seen from the lot, a clerk at the desk through the lit window, peaceful"],
    "family": ["a car sliding into a flooded motel parking lot at night, headlights smeared by rain", "@"],
    "rising": ["@", "close-up of a clerk's shoes in dark water up to the ankles behind the motel desk"],
    "give-yours": ["@", f"{JONAH} gripping a phone receiver at the flooded desk, head bowed, listening"],
    "room-one": ["close-up of a key with a tag numbered one being lifted off its hook", "@"],
    "checkout": ["two small children in pajamas holding their parents' hands across the motel lot in grey morning light, faces turned away", "@"],
    "sam": ["@", "close-up of a dark green work vest and a snowy shoulder at the motel counter, the face out of frame"],
}


def expand(slug: str, shots: list[str]) -> list[str]:
    order = EXTRA.get(slug)
    if not order:
        return shots
    out = []
    for item in order:
        if item == "@":
            out += shots
        elif item.startswith("@") and item[1:].isdigit():
            out.append(shots[int(item[1:])])
        else:
            out.append(item)
    assert all(s in out for s in shots), slug
    return out


def main() -> None:
    scenes, md, words, chapter = [], [], 0, None
    md.append("# 3 Night Shift Horror Stories Animated\n")
    clips = stills = cards = 0
    for i, (ch, slug, text, shots) in enumerate(S, 1):
        sid = f"{i:03d}"
        assets, notes = [], []
        shots = expand(slug, shots)
        for j, shot in enumerate(shots):
            suffix = "" if len(shots) == 1 else "abcdef"[j]
            if shot.startswith("CLIP:"):
                assets.append(f"clips/{sid}{suffix}_{slug}.mp4"); clips += 1
                notes.append(("Clip", shot[5:].strip()))
            elif shot.startswith("CARD:"):
                assets.append(f"clips/{sid}{suffix}_{slug}-card.mp4"); cards += 1
                notes.append(("Card", shot[5:].strip()))
            else:
                assets.append(f"images/{sid}{suffix}_{slug}.png"); stills += 1
                notes.append(("Image", shot))
        sc = {"id": sid, "slug": slug, "text": text,
              "asset": assets[0] if len(assets) == 1 else assets,
              "shots": [{"kind": k.lower(), "prompt": f"{STYLE}. {p}" if k != "Card" else p}
                        for k, p in notes]}
        if ch:
            sc["chapter"] = ch
            chapter = ch
            md.append(f"\n## {ch}\n")
        scenes.append(sc)
        n = len(text.split())
        words += n
        md.append(f"**{sid}** — {text}\n")
        for k, p in notes:
            md.append(f"> *{k}:* {p}\n")
        md.append("")
    mins = words / WPM
    data = {
        "title": "3 Night Shift Horror Stories Animated",
        "description": ("Three night shifts on the same stretch of Route 9. A gas station with ten rules taped under "
                        "the register. A hospital room whose call light comes on every night, three years after its "
                        "patient went home. A motel guest who checks into room nine at 3:33 a.m. Stay for the last "
                        "story: it explains the first.\nOriginal animated horror fiction."),
        "descriptionFooter": ("Original fiction. Narration, images and animation are AI-generated.\n"
                              "#animatedhorror #horrorstories #scarystories #nightshift #horroranimated"),
        "styleNote": STYLE,
        "scenes": scenes,
    }
    (HERE / "scenes.json").write_text(json.dumps(data, indent=2) + "\n")
    md.insert(1, f"_{len(scenes)} scenes · {words} words · ≈{mins:.1f} min at {WPM} wpm · "
                 f"{stills} stills, {clips} motion clips, {cards} text cards_\n")
    (HERE / "SCRIPT.md").write_text("\n".join(md) + "\n")
    print(f"{len(scenes)} scenes, {words} words, ~{mins:.1f} min; {stills} stills, {clips} clips, {cards} cards")


if __name__ == "__main__":
    main()
