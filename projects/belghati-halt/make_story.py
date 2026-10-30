#!/usr/bin/env python3
"""Write scenes.json + SCRIPT.md for "Belghati Halt Ke 7 Rules" (Hinglish, ~20 min).

Original story. Format chosen from Oct 2026 research: Indian railway-station night horror
(the fastest-breaking Hindi horror setting) + the "rules" hook + a first-person night-duty
worker, modern Hinglish narration (Devanagari, English words transliterated)
with short dialogue, no intro, sticky last line.

Each scene: (chapter or None, slug, narration, shots). "CARD:" = text card rendered locally
with a Devanagari font (image models can't write Hindi); anything else is a FLUX.2 still.
Numbers are spelled out in the narration so the TTS reads them naturally.
Run from the project dir: python3 make_story.py
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
WPM = 120  # Hindi narration, slow horror pacing

STYLE = ("dark cinematic horror illustration, realistic digital painting, realistic human faces and proportions, "
         "serious and grim tone, muted desaturated palette of sodium orange, sickly green and deep blue-black, "
         "deep shadows, volumetric fog, film grain, cinematic 16:9 wide shot, small Indian railway station in a forest, "
         "no text, no words, no letters")
AKASH = "a young Indian railway clerk in a navy blue sweater over a white shirt, seen from behind or in silhouette, face hidden"
BHOLA = "a thin old Indian man in a brown woollen shawl and dhoti holding a glowing kerosene lantern, face lost in shadow"
TIWARI = "a nervous middle-aged Indian station master in a white railway uniform and a black woollen coat, face turned away"
SLEEPER = "a human shape lying on a wooden platform bench, wrapped head to toe in a soaked brown shawl, water dripping onto the concrete"
RAGHU = "a gaunt figure in a mud-stained old white Indian railway uniform with a small brass name badge, face in deep shadow"
MAA = "an Indian mother in a simple cotton saree, seen from behind or with her face turned away"
HALT = ("a tiny Indian railway halt station deep in a forest at night: one short platform, a small brick "
        "booking office with a barred ticket window, a signal cabin, a few sodium lamps glowing in thick fog")
WINDOW = "a small barred railway ticket window with a wooden shutter, seen from inside a dim booking office"
TICKET = "a small old brown cardboard railway ticket, soaking wet"
TRAIN = ("an old Indian passenger train with faded maroon coaches, water pouring from the carriages, "
         "river weeds hanging from the windows, dim yellow light inside")

S = [
    # ---------------- HOOK ----------------
    ("Belghati Halt", "timetable",
     "रेलवे में हर स्टेशन का एक टाइम-टेबल होता है। सब जानते हैं। लेकिन कुछ स्टेशनों का एक सीक्रेट टाइम-टेबल भी होता है… जो किसी बोर्ड पर नहीं, एक पुराने रजिस्टर के लास्ट पेज पर लिखा होता है।",
     ["a single railway track vanishing into thick fog at night, one red signal light glowing high on a post, forest on both sides",
      "close-up of the last page of an old cloth-bound railway register lit by a kerosene lantern, rows of faded handwriting too blurred to read"]),
    (None, "rule-four-tease",
     "बेलघाटी हॉल्ट के रजिस्टर में ऐसे सात रूल्स थे। और रूल नंबर फ़ोर था… अगर कोई तुम्हें भूरे कलर का पुराना, गत्ते वाला टिकट दे, तो उसे भूल के भी पंच मत करना।",
     [f"extreme close-up of {TICKET} lying on a worn wooden counter beside an old brass ticket punching machine, a drop of water rolling off it",
      "CARD: rule — RULE 4: भूरे गत्ते वाला टिकट कभी पंच मत करना"]),
    (None, "my-name",
     "मेरा नाम आकाश है। चार साल पहले, विंटर्स में, बेलघाटी हॉल्ट पर मेरी फ़र्स्ट पोस्टिंग हुई थी। नाइट शिफ़्ट। और ये स्टोरी मैं आज इसलिए बता रहा हूँ… क्योंकि उस स्टेशन की वैकेंसी फिर से निकली है।",
     [f"wide shot of {HALT}, a lone figure on the platform",
      "CARD: title — BELGHATI HALT के 7 RULES"]),

    # ---------------- 1 ----------------
    ("Pehli Sarkari Naukri", "letter",
     "मैं चौबीस का था। तीन बार एग्ज़ाम दिया, दो बार फ़ेल, और थर्ड अटेम्प्ट में रेलवे का लेटर आ गया। उस दिन मम्मी ने पूरे मोहल्ले में लड्डू बाँटे। सरकारी नौकरी, यार। हमारी फ़ैमिली में फ़र्स्ट टाइम।",
     [f"{AKASH} holding an official letter in both hands in a small lamplit room, a calendar and old schoolbooks on a shelf",
      f"{MAA} handing out sweets from a steel plate to neighbours in a narrow lane at dusk, warm lamplight from doorways"]),
    (None, "red-thread",
     "निकलते टाइम मम्मी ने मेरी कलाई पर लाल धागा बाँधा, और बोलीं — बेटा, कुछ भी हो जाए, जॉब मत छोड़ना। मैंने हँस के बोला — मम्मी, एक छोटे से स्टेशन पर क्या ही हो जाएगा?",
     ["close-up of an older woman's hands tying a red sacred thread around a young man's wrist, an old suitcase behind them",
      f"{AKASH} waving from the door of a train at a small town station at dusk, a woman's silhouette on the platform"]),
    (None, "the-halt",
     "बेलघाटी हॉल्ट। जंगल के बीचों-बीच एक छोटा सा स्टेशन। एक प्लेटफ़ॉर्म, एक टिकट विंडो, एक सिग्नल केबिन, और उसमें लोहे के तीन बड़े-बड़े लीवर। दिन में बस दो लोकल रुकती थीं। और रात में… सिर्फ़ कोहरा।",
     [f"aerial view of {HALT}, dense dark forest all around, fog rolling over the tracks",
      "inside a small railway signal cabin at night: three tall iron levers in a row, an old black telephone on a wooden desk, a lantern"]),
    (None, "dead-line",
     "स्टेशन के आगे ट्रैक जंगल में जाकर एक पुराने लोहे के गेट पर ख़त्म हो जाता था। गेट पर ज़ंग लगी चेन। उसके पार की लाइन कभी सोनाली नदी के ब्रिज तक जाती थी। अब वहाँ कोई ब्रिज नहीं था।",
     ["a rusted railway track ending at an old iron gate chained shut in a foggy forest, weeds growing between the sleepers",
      "the broken stone pillars of a collapsed railway bridge standing in a dark river at night, no bridge between them"]),
    (None, "bhola",
     "स्टेशन के बाहर भोला काका की चाय की टपरी थी। दुबले-पतले, भूरी शॉल, और हाथ में हमेशा एक पुरानी लालटेन। फ़र्स्ट डे ही उन्होंने कुल्हड़ में चाय पकड़ाई, और पूछा — साहब, नाइट ड्यूटी है?",
     [f"a tiny roadside tea stall outside a railway station at dusk, a kettle steaming on a clay stove, {BHOLA}",
      "close-up of steaming tea in a small clay cup held out toward the viewer by a thin old hand, lantern light"]),
    (None, "count-knocks",
     "मैंने हाँ बोला, तो वो थोड़ी देर चुप रहे। फिर बोले — रात में विंडो खोलने से पहले गिन लेना, साहब। दस्तक कितनी बार हुई। और ठीक आठ बजे टपरी बंद करके, लालटेन उठाके, कोहरे में ग़ायब हो गए।",
     [f"{BHOLA} sitting by his clay stove at dusk, turned toward a young clerk, lantern on the ground, face in shadow",
      f"{BHOLA} seen from behind walking away into thick fog along the railway track, the lantern a small orange glow"]),
    (None, "tiwari",
     "मुझसे पहले वहाँ तिवारी जी थे, स्टेशन मास्टर। चार्ज हैंडओवर में उन्होंने दस मिनट भी नहीं लगाए। चाबियाँ दीं, कैश काउंट करवाया, और एक मोटा, पुराना रजिस्टर मेरे हाथ में थमा दिया।",
     [f"{TIWARI} pushing a thick old cloth-bound register across a desk toward {AKASH}, a ring of keys beside it, one bulb overhead"]),
    (None, "last-page",
     "बोले — आकाश बाबू, लास्ट पेज पढ़ लेना। जो लिखा है, बस वही करना। सवाल मत करना। और शाम की लास्ट लोकल में बैठ गए। पूरे रास्ते उन्होंने खिड़की की तरफ़ पीठ करके रखी… उस पुराने गेट की तरफ़।",
     [f"{TIWARI} sitting stiffly inside a departing train coach with his back to the window, the fog and the old chained gate visible outside",
      "a passenger train pulling away from a tiny forest station at dusk, red tail lamp shrinking into the fog"]),

    # ---------------- 2 ----------------
    ("Register Ka Last Page", "seven-rules",
     "उस रात, लालटेन की लाइट में, मैंने लास्ट पेज खोला। सात रूल्स। और तीन अलग-अलग हैंडराइटिंग… जैसे सालों में तीन अलग लोगों ने डरते-डरते उसमें कुछ ऐड किया हो।",
     [f"{AKASH} at a desk in a dark booking office opening an old register under a kerosene lantern",
      "extreme close-up of handwritten lines in three different inks on a yellowed register page, blurred and unreadable, lantern glow"]),
    (None, "rule-one",
     "रूल नंबर वन: रात एक बजे के बाद टिकट विंडो तभी खोलना, जब कोई तीन बार नॉक करे। अगर चार बार नॉक करे… तो कोई भी हो, विंडो मत खोलना।",
     ["CARD: rule — RULE 1: तीन नॉक पर विंडो खोलना। चार नॉक पर कभी नहीं।",
      f"{WINDOW}, the wooden shutter closed, fog pressing against the bars outside"]),
    (None, "rules-two-three",
     "रूल टू: प्लेटफ़ॉर्म की लास्ट बेंच पर अगर कोई सोता दिखे, तो उसे जगाना मत। रूल थ्री: रात तीन बजकर तैंतीस मिनट पर कंट्रोल का फ़ोन बजे, तो उठा लेना… पर एक वर्ड भी मत बोलना।",
     ["CARD: rule — RULE 2: लास्ट बेंच पर सोने वाले को मत जगाना",
      "the last wooden bench at the dark far end of a railway platform under a flickering lamp, empty, fog drifting past",
      "CARD: rule — RULE 3: 3:33 पर फ़ोन उठाना, पर एक वर्ड मत बोलना"]),
    (None, "rules-four-five",
     "रूल फ़ोर: अगर कोई भूरे गत्ते वाला पुराना टिकट दे, तो उसे कभी पंच मत करना। सीधा जला देना। रूल फ़ाइव: ब्रिज वाली बंद लाइन पर लाल लालटेन दिखे, तो सिग्नल ग्रीन मत करना… चाहे ऑर्डर ख़ुद कंट्रोल से आए।",
     ["an old black railway telephone on a wooden desk in a dark signal cabin, its receiver on the hook",
      "CARD: rule — RULE 5: लाल लालटेन दिखे तो सिग्नल ग्रीन मत करना",
      "a red lantern swinging in thick fog beside a rusted chained railway gate, nobody visible holding it"]),
    (None, "rule-six",
     "रूल सिक्स: सुबह पाँच बजे की फ़र्स्ट लोकल की सीटी से पहले, स्टेशन छोड़कर मत जाना। चाहे कोई भी बुलाए।",
     ["CARD: rule — RULE 6: सुबह 5 बजे की सीटी से पहले स्टेशन मत छोड़ना",
      "the open door of a small booking office looking out onto a black foggy platform, the light from inside spilling only a few steps"]),
    (None, "rule-seven",
     "और रूल सेवन… आधा फटा हुआ था। बस इतना बचा था — अगर कोई तुम्हें तुम्हारी अपनी आवाज़ में… उसके आगे पेज फटा था। जैसे किसी ने जल्दी में, पैनिक में, उसे नोच लिया हो।",
     ["close-up of the bottom of an old register page torn off in a jagged line, the last handwritten line cut in half, lantern light",
      "CARD: rule — RULE 7: अगर कोई तुम्हें तुम्हारी अपनी आवाज़ में…"]),
    (None, "laugh",
     "सच बोलूँ? मुझे हँसी आ गई। लगा, नए स्टाफ़ के साथ कोई पुराना प्रैंक है। मैंने रजिस्टर बंद किया, टिकट पंचिंग मशीन सेट की, और रेडियो पे पुराने गाने लगा दिए।",
     [f"{AKASH} leaning back in a chair in the booking office, an old transistor radio glowing on the shelf, the register closed on the desk"]),
    (None, "habit",
     "फ़र्स्ट छह दिन, कुछ नहीं हुआ। दिन की लोकल में गाँव वाले आते, मैं टिकट काटता, और मशीन में डेट पंच। इतनी बार किया, कि हाथ को आदत पड़ गई। आँख बंद करके भी।",
     ["villagers with bundles queueing at a small ticket window on a sunny morning, a train waiting behind them",
      "close-up of a hand pressing a small brown ticket into an old brass ticket punching machine, motion blur"]),
    (None, "kalu",
     "बस एक चीज़ वीयर्ड थी। स्टेशन का कुत्ता, कालू। पूरा दिन प्लेटफ़ॉर्म पे घूमता, लेकिन लास्ट लैंप-पोस्ट से आगे कभी नहीं जाता था। और रात को… वो उसी पुराने गेट की तरफ़ मुँह करके रोता था।",
     ["a thin black stray dog standing under the last lamp post at the end of a railway platform at night, howling toward a dark foggy forest",
      "a black stray dog sitting at the very edge of the lamp light on a platform, refusing to step into the darkness beyond"]),

    # ---------------- 3 ----------------
    ("Chaar Dastak", "seventh-night",
     "सेवंथ नाइट। रात के एक बजकर दस मिनट। कोहरा इतना घना, कि प्लेटफ़ॉर्म की लाइट्स धुंधले चाँद जैसी लग रही थीं। और तभी, टिकट विंडो पर नॉक हुआ।",
     [f"{HALT}, the platform lamps reduced to blurry moons in the fog",
      "a clock on a booking office wall showing ten past one, a lantern below it"]),
    (None, "three-knocks",
     "तीन बार। मैंने विंडो खोली। बाहर एक बूढ़ी अम्मा थीं, सिर पे पल्लू। पूछा — बेटा, सुबह वाली गाड़ी कितने बजे है? मैंने बताया। वो आशीर्वाद देके चली गईं। बस। एकदम नॉर्मल।",
     [f"{WINDOW}, the shutter open, an old village woman with her saree over her head outside in the fog, face hidden"]),
    (None, "fourth-knock",
     "मैंने सोचा, देखा? कुछ नहीं होता। मैं चेयर पे बैठा ही था, कि फिर से नॉक हुआ।",
     [f"{WINDOW}, the shutter closed, the wood trembling slightly, the room dark",
      "extreme close-up of a clerk's hand frozen above the iron latch of a wooden shutter"]),
    (None, "sonali-pul",
     "चार बार। मेरा हाथ कुंडी पर था। बाहर से एक आदमी की आवाज़ आई, बहुत धीमी… जैसे पानी के अंदर से बोल रहा हो — बाबूजी… एक टिकट दे दो। सोनाली पुल।",
     ["the gap under a closed ticket window shutter, dark water slowly seeping in across the counter"]),
    (None, "wet-ticket",
     "मैंने विंडो नहीं खोली। कुछ सेकंड बाद, विंडो के नीचे की दरार से कुछ अंदर सरका। एक छोटा, भूरा, गत्ते का टिकट। ओल्ड स्टाइल वाला। पूरा भीगा हुआ। और उसमें से नदी की कीचड़ की स्मेल आ रही थी।",
     [f"{TICKET} sliding in under the shutter of a ticket window onto the counter, pushed by unseen fingers",
      "close-up of river mud and a strand of green river weed clinging to the edge of a wet cardboard ticket on a wooden counter"]),
    (None, "drawer",
     "उस पर फ़ेडेड इंक में लिखा था — बेलघाटी टू सोनाली पुल। फ़िफ़्टी सेवन डाउन। मैंने उसे पंच नहीं किया। पर जलाया भी नहीं। पता नहीं क्यों… मैंने उसे ड्रॉअर में रख दिया। बिग मिस्टेक।",
     [f"close-up of {TICKET} in a clerk's fingers under lamplight, faded printing blurred and unreadable",
      "a wooden desk drawer sliding shut on a small wet brown ticket"]),
    (None, "the-sleeper",
     "दो बजे मैं प्लेटफ़ॉर्म का राउंड लेने निकला। लास्ट बेंच पर कोई सो रहा था। सिर से पैर तक भूरी शॉल में लिपटा। और शॉल से पानी टपक रहा था… जबकि उस रात बारिश हुई ही नहीं थी।",
     [f"{AKASH} with a torch walking along a foggy railway platform toward its far dark end",
      f"{SLEEPER}, under the last flickering platform lamp"]),
    (None, "dont-wake",
     "रूल टू। मैंने उसे नहीं जगाया। चुपचाप उल्टे पाँव वापस आ गया। कालू बेंच की तरफ़ देखकर गुर्रा रहा था, पर पास जाने की हिम्मत उसकी भी नहीं हुई।",
     ["a black stray dog with raised hackles growling at a shrouded figure on a far bench, keeping its distance, fog",
      f"{AKASH} walking quickly back toward the lit booking office, not looking behind him"]),
    (None, "phone-rings",
     "और फिर, ठीक तीन बजकर तैंतीस मिनट पर, केबिन का काला कंट्रोल फ़ोन बजा। इतनी ज़ोर से, कि पूरा स्टेशन गूँज गया।",
     ["an old black railway telephone ringing violently on a wooden desk in a dark signal cabin, the receiver rattling",
      "a clock on a cabin wall at three thirty three, the hands sharp in lantern light"]),
    (None, "breathing",
     "मैंने रिसीवर उठाया, और कुछ नहीं बोला। दूसरी तरफ़ हवा की आवाज़ थी। लोहे के ब्रिज पर दौड़ती ट्रेन की खड़खड़ाहट। और बहुत सारे लोगों की साँसें… जैसे पूरा भरा हुआ कोच एक साथ साँस ले रहा हो।",
     [f"{AKASH} holding a black telephone receiver to his ear in a dark cabin, his other hand over his mouth",
      "a dark railway coach packed with silent passengers in shadow, all faces hidden, water on the floor"]),
    (None, "line-clear",
     "फिर एक भारी, थकी हुई आवाज़ — बेलघाटी… फ़िफ़्टी सेवन डाउन के लिए लाइन क्लियर दो। मैंने मुँह पे हाथ रख लिया। एक वर्ड नहीं बोला। एक मिनट बाद कॉल कट गई।",
     ["close-up of a black telephone receiver set gently back on its hook by a trembling hand"]),
    (None, "wet-outline",
     "सुबह पाँच बजे फ़र्स्ट लोकल की सीटी बजी, तब जाके मेरी साँस में साँस आई। लास्ट बेंच ख़ाली थी। बस लकड़ी पर एक इंसान के शेप का गीला निशान था… और नीचे नदी की रेत।",
     ["a morning train approaching a foggy forest station at dawn, headlight glowing",
      "an empty wooden platform bench at dawn with a dark wet outline of a human body on it and river sand beneath"]),

    # ---------------- 4 ----------------
    ("14 December 1981", "you-counted",
     "उस सुबह मैं सीधा भोला काका के पास गया। उन्होंने बस मेरा चेहरा देखा, और बिना कुछ पूछे चाय पकड़ा दी। फिर धीरे से बोले — चार बार हुई थी न, साहब?",
     [f"{BHOLA} at his tea stall in pale morning fog handing a clay cup to {AKASH}"]),
    (None, "the-story",
     "तब उन्होंने मुझे वो स्टोरी सुनाई, जो बेलघाटी में कोई ज़ोर से नहीं सुनाता। चौदह दिसंबर, नाइनटीन एटी वन। सर्दी की रात। ऐसा ही कोहरा। फ़िफ़्टी सेवन डाउन, सोनाली पैसेंजर, एक सौ बयालीस लोगों को लेकर बेलघाटी पहुँची थी।",
     [f"{TRAIN.split(', water')[0]} standing at a tiny forest station at night in 1981, passengers dozing at the windows, thick fog",
      "a crowded old train coach interior at night, families with bundles and sleeping children, a single bulb"]),
    (None, "lantern-man",
     "उस रात नदी में फ़्लड था। ब्रिज का एक पिलर हिल चुका था। और ब्रिज की तरफ़ से एक गैंगमैन लाल लालटेन लेकर भागता हुआ आया — ट्रेन रोको! ब्रिज मत खोलो!",
     ["a swollen dark river in flood smashing against the stone pillar of an old railway bridge at night",
      "a thin railway trackman running along the tracks through fog swinging a red lantern above his head, face in shadow"]),
    (None, "the-lever",
     "लेकिन ड्यूटी पर जो स्टेशन मास्टर थे, रघुनाथ प्रसाद… ट्रेन पहले से लेट थी, ऊपर से कंट्रोल का प्रेशर। उन्हें लगा, गैंगमैन ओवररिएक्ट कर रहा है। और उन्होंने लीवर खींच दिया। सिग्नल ग्रीन।",
     ["a station master's hands in white uniform sleeves pulling a tall iron signal lever in a dark cabin",
      "a railway signal light turning green high on its post in the fog"]),
    (None, "the-fall",
     "तीन बजकर तैंतीस मिनट पर, फ़िफ़्टी सेवन डाउन ब्रिज के बीच में थी, जब ब्रिज टूटा। एक सौ बयालीस लोग। एक भी नहीं बचा। उसके बाद वो लाइन बंद कर दी गई, और सोनाली पुल हॉल्ट हमेशा के लिए मैप से मिट गया।",
     ["silhouette of an old train on a long iron bridge over a flooded river at night, the middle span buckling",
      "the dark flooded river at dawn, the broken bridge pillars, nothing else"]),
    (None, "raghunath",
     "मैंने पूछा — और रघुनाथ प्रसाद? काका काफ़ी देर चुप रहे। फिर बोले — वो अगली सर्दी तक ड्यूटी करते रहे, साहब। हर रात उसी लास्ट बेंच पे बैठके। और एक सुबह… उसी बेंच पे मिले।",
     [f"{RAGHU} sitting alone hunched on the last platform bench at night, staring toward the dark forest",
      "the last platform bench in grey dawn fog with a folded brown shawl left on it"]),
    (None, "nobody-listens",
     "और वो गैंगमैन? काका ने अपनी लालटेन की बत्ती ठीक की। बोले — उसकी बात किसी ने नहीं सुनी, साहब। आज भी कोई नहीं सुनता। और जाते-जाते बोले… वो टिकट जला देना। आज ही।",
     [f"close-up of {BHOLA.split(' holding')[0]} adjusting the wick of a kerosene lantern, only his thin hands and chin lit",
      f"{BHOLA} pointing toward a booking office with a thin finger, his lantern held low, morning fog"]),
    (None, "old-register",
     "उस दोपहर मैंने स्टेशन की पुरानी अलमारी खोली। धूल के नीचे नाइनटीन एटी वन का ड्यूटी रजिस्टर मिला। चौदह दिसंबर वाला पेज। लास्ट एंट्री — तीन बजकर तीस मिनट, फ़िफ़्टी सेवन डाउन को लाइन क्लियर। साइन: आर. प्रसाद।",
     [f"{AKASH} pulling a dusty old register out of a rusty steel almirah in a dim storeroom, dust in a beam of light",
      "close-up of an old register page with a single handwritten entry and a signature, blurred and unreadable, a water stain"]),
    (None, "same-hand",
     "और उसी पेज के कॉर्नर में, किसी ने काँपते हाथ से लिखा था — लालटेन देखी थी। फिर भी। …और वो हैंडराइटिंग, एग्ज़ैक्टली वही थी, जिसमें हमारे रजिस्टर का रूल नंबर वन लिखा था।",
     ["two old registers lying open side by side on a desk, the same shaky handwriting on both pages, unreadable, lantern light"]),
    (None, "first-lie",
     "उस रात मम्मी का कॉल आया। रोज़ की तरह — खाना खाया? ठंड तो नहीं लग रही? मैंने बोला, सब ठीक है मम्मी। लाइफ़ में फ़र्स्ट टाइम मैंने मम्मी से झूठ बोला था। और ड्रॉअर में… वो गीला टिकट अभी भी पड़ा था।",
     [f"{AKASH} on a mobile phone in the dark booking office, the screen lighting his hand, his face hidden",
      "a closed wooden desk drawer with a thin line of water seeping out from under it"]),

    # ---------------- 5 ----------------
    ("Kohre Wali Raat", "the-date",
     "चौदह दिसंबर की रात। मुझे डेट का ध्यान तक नहीं था। कोहरा इतना घना, कि केबिन में अपना ही हाथ धुंधला दिख रहा था। और कालू शाम से ही गेट की तरफ़ मुँह करके रो रहा था।",
     ["a wall calendar in a dim office with one date circled in old red ink, unreadable, a lantern below",
      "a black stray dog howling at the end of a fog-drowned platform toward an unseen gate"]),
    (None, "sitting-up",
     "दो बजे लास्ट बेंच पर फिर वही शॉल वाली शेप थी। लेकिन आज वो सो नहीं रही थी। बैठी थी। एकदम सीधी। और उसका सिर… केबिन की तरफ़ मुड़ा हुआ था।",
     ["a figure wrapped head to toe in a soaked brown shawl sitting bolt upright on the last platform bench, its covered head turned toward the viewer, fog"]),
    (None, "baby-cries",
     "तीन बजकर बीस मिनट पर विंडो पर नॉक हुआ। चार बार। और फिर… एक बच्चे के रोने की आवाज़।",
     [f"{WINDOW}, the shutter closed and shaking, fog glowing behind the cracks"]),
    (None, "mother-begs",
     "एक औरत की आवाज़ आई, काँपती हुई — बाबूजी, प्लीज़ विंडो खोलो। बच्चा ठंड से अकड़ रहा है। बस एक मिनट अंदर आने दो। भगवान के लिए।",
     ["the silhouette of a young woman clutching a wrapped baby outside a closed ticket window in thick fog, seen through a crack, faces hidden"]),
    (None, "the-choice",
     "मुझे रूल याद था। सच में याद था। लेकिन बच्चा रो रहा था, यार। और मेरे दिमाग़ में बस एक बात थी — अगर सच में कोई माँ बाहर ठंड में खड़ी है, और मैंने विंडो नहीं खोली… तो मैं ख़ुद को कभी माफ़ नहीं कर पाऊँगा।",
     [f"{AKASH} standing frozen in front of a closed ticket window, one hand on the latch, a red thread on his wrist",
      "extreme close-up of a red sacred thread on a young man's wrist, his fingers on a cold iron latch"]),
    (None, "open",
     "मैंने कुंडी खोल दी।",
     ["an iron latch sliding open on a wooden shutter, fog pouring in through the gap"]),
    (None, "khat",
     "बाहर कोई नहीं था। सिर्फ़ कोहरा। और काउंटर पर एक गीला, ठंडा हाथ… जो एक भूरा टिकट मेरी तरफ़ सरका रहा था। और मेरे हाथ ने वही किया… जो छह दिन से करता आ रहा था।",
     [f"a pale dripping hand reaching in through an open ticket window, pushing {TICKET} across the counter, nobody visible outside",
      "close-up of a hand slamming a brown ticket into a brass ticket punching machine"]),
    (None, "punched",
     "मैंने नीचे देखा। टिकट पंच हो चुका था। डेट की मुहर एकदम क्लियर — चौदह, बारह, इक्यासी। मैंने ड्रॉअर खोला। मेरा रखा हुआ टिकट वहाँ नहीं था। ये… वही टिकट था।",
     [f"extreme close-up of {TICKET} with a fresh punched hole and a stamped date, the numbers blurred",
      "an open wooden desk drawer, empty except for a small puddle of water"]),
    (None, "lights-out",
     "उसी सेकंड पूरे स्टेशन की लाइट्स चली गईं। और बंद लाइन की पटरियाँ… गुनगुनाने लगीं। जैसे दूर से कोई ट्रेन आ रही हो।",
     [f"{HALT} with every lamp suddenly dark, only the fog faintly glowing",
      "close-up of rusted rails vibrating in the dark, dew drops jumping off the steel"]),
    (None, "57-down",
     "पीछे वाली लाइन से एक पीली रोशनी आई। धीरे-धीरे। बिना किसी आवाज़ के। पुराने, मैरून कलर के डिब्बे। उनसे पानी झर रहा था, और खिड़कियों से नदी की घास लटक रही थी।",
     [f"a single dim yellow headlight approaching through thick fog along a railway line, the train behind it barely visible",
      f"{TRAIN}, gliding silently into a dark platform"]),
    (None, "faces",
     "फ़िफ़्टी सेवन डाउन, बेलघाटी के प्लेटफ़ॉर्म पर आकर रुकी। हर खिड़की में कोई बैठा था। भीगे हुए लोग। किसी का चेहरा नहीं दिख रहा था… पर मुझे पता था, सब मुझे ही देख रहे थे।",
     ["a row of train windows at night, a dark soaked silhouette motionless in every window, faces hidden in shadow, water dripping from the frames"]),
    (None, "the-guard",
     "गार्ड के डिब्बे से एक आदमी झुका, हाथ में हरी झंडी। बोला — टिकट पंच हो गया, बाबूजी। सवारी पूरी है। बस लाइन क्लियर दे दो।",
     ["an old train guard leaning out of the last coach holding a green flag, his uniform soaked, face in shadow, fog"]),

    # ---------------- 6 ----------------
    ("Lever", "special-order",
     "तीन बजकर तैंतीस मिनट। केबिन का फ़ोन बजा। मैंने उठाया। इस बार आवाज़ एकदम रियल कंट्रोल जैसी थी — बेलघाटी, स्पेशल ऑर्डर। फ़िफ़्टी सेवन डाउन को तुरंत लाइन क्लियर दो। ऑर्डर नहीं माना, तो सुबह सस्पेंशन लेटर रेडी रहेगा।",
     ["an old black telephone ringing in a dark signal cabin, a clock behind it at three thirty three",
      f"{AKASH} gripping a telephone receiver, staring at the tall iron levers in front of him"]),
    (None, "suspension",
     "सस्पेंशन। मेरी फ़र्स्ट सरकारी जॉब। मम्मी के लड्डू। मोहल्ले वालों के चेहरे। और मेरा हाथ… अपने आप लीवर की तरफ़ बढ़ने लगा।",
     [f"{MAA} in a lamplit doorway at home, waiting, seen from behind",
      "a young man's hand with a red thread on the wrist reaching slowly toward a tall iron signal lever"]),
    (None, "red-lantern",
     "तभी मैंने उसे देखा। बंद लाइन पर, पुराने गेट के पास, कोहरे में एक लाल लालटेन हिल रही थी। राइट से लेफ़्ट। राइट से लेफ़्ट। रुको। रुको। रुको।",
     ["a red lantern swinging left and right in thick fog beside a rusted chained railway gate, the holder only a thin shadow"]),
    (None, "we-want-home",
     "रूल फ़ाइव। मैंने लीवर छोड़ दिया। और फ़ोन वाली आवाज़ बदल गई। पहले ग़ुस्सा, फिर रोना, फिर एक साथ बहुत सारी आवाज़ें… बच्चे, औरतें, बूढ़े। सब एक ही बात बोल रहे थे — हमें घर जाना है।",
     ["a telephone receiver hanging off its desk on its cord, swinging, in a dark signal cabin",
      "the dark windows of an old train at night, many pale soaked hands pressed flat against the glass from inside"]),
    (None, "name-badge",
     "केबिन का दरवाज़ा अपने आप खुला। शॉल वाली शेप अंदर आ रही थी। शॉल नीचे गिरी। अंदर पुरानी, सफ़ेद रेलवे यूनिफ़ॉर्म थी, कीचड़ से सनी। और सीने पर पीतल की नेमप्लेट — आर. प्रसाद।",
     ["the door of a signal cabin creaking open onto fog, a shrouded figure in the doorway, water pooling at its feet",
      f"close-up of a mud-stained old white railway uniform chest with a small brass name badge, the letters blurred, dripping"]),
    (None, "every-year",
     "उसके हाथ सीधे लीवर पर गए। वही हाथ, जिसने नाइनटीन एटी वन में ये लीवर खींचा था। वो फिर से खींच रहा था। हर साल की तरह।",
     [f"{RAGHU} gripping a tall iron signal lever with both grey dripping hands"]),
    (None, "struggle",
     "मैंने दोनों हाथों से लीवर पकड़ लिया। लोहा बर्फ़ जैसा ठंडा। वो खींचता रहा, मैं रोकता रहा। लीवर काँप रहा था, और बाहर सिग्नल की लाइट… रेड। येलो। रेड।",
     [f"two pairs of hands fighting over one iron signal lever in a dark cabin: grey dripping hands pulling, a young man's hands with a red thread holding it back",
      "a railway signal light high on its post in the fog flickering between red and yellow"]),
    (None, "own-voice",
     "और तभी, बाहर प्लेटफ़ॉर्म से, किसी ने मुझे पुकारा — आकाश! बाहर आ जा यार। छोड़ दे लीवर। सब ठीक है। मैं हूँ। …वो आवाज़ मेरी अपनी थी।",
     [f"a silhouette on the foggy platform outside the cabin window that looks exactly like {AKASH}, standing perfectly still, face hidden"]),
    (None, "lips-shut",
     "मेरी अपनी आवाज़। सेम टोन, सेम खराश। मेरे मुँह से लगभग निकल गया — कौन है? लेकिन तभी वो फटा हुआ रूल याद आया। अगर कोई तुम्हें तुम्हारी अपनी आवाज़ में… मैंने होंठ भींच लिए। एक वर्ड नहीं।",
     ["CARD: rule — RULE 7: अगर कोई तुम्हें तुम्हारी अपनी आवाज़ में…",
      f"{AKASH} in the dark cabin with his jaw clenched and eyes shut, hands locked on the lever, seen from the side in shadow"]),
    (None, "keep-red",
     "लालटेन अब केबिन की विंडो के ठीक बाहर थी। उसकी लाइट में एक पल के लिए मुझे भूरी शॉल दिखी… और एक जानी-पहचानी, दुबली परछाईं। कोई चिल्लाया — साहब, लाल रखना! चाहे कुछ भी हो जाए!",
     [f"a red lantern glowing right outside a signal cabin window in the fog, lighting the edge of a brown shawl and a thin shoulder",
      "a railway signal on its post burning steady red through the fog, a thin figure with a lantern standing beneath it"]),
    (None, "counting",
     "मुझे नहीं पता मैंने कितनी देर लीवर पकड़े रखा। हथेलियों से ख़ून निकल आया था। मम्मी का बाँधा लाल धागा भीग चुका था। मैं बस गिनता रहा। एक-एक साँस।",
     ["extreme close-up of bleeding palms gripping an iron lever, a soaked red thread on the wrist, frost on the metal"]),

    # ---------------- 7 ----------------
    ("Subah Ki Pehli Seeti", "whistle",
     "और फिर, बहुत दूर से, एक सीटी सुनाई दी। असली सीटी। सुबह पाँच बजे की फ़र्स्ट लोकल।",
     ["the first light of dawn behind a foggy forest, a distant train headlight appearing on the working line"]),
    (None, "still-red",
     "लीवर पर से ठंडे हाथ हट गए। फ़ोन चुप। प्लेटफ़ॉर्म पर कोई ट्रेन नहीं थी। बस गीली पटरियाँ, उन पर नदी की घास। और सिग्नल… रेड था।",
     ["an empty railway platform at grey dawn, wet tracks with river weeds draped across them",
      "a railway signal glowing red on its post in pale dawn fog"]),
    (None, "142",
     "टिकट विंडो के काउंटर पर भूरे टिकटों का ढेर पड़ा था। मैंने काउंट किए। एक सौ बयालीस। सब पंच किए हुए। सब पर एक ही डेट। चौदह, बारह, इक्यासी।",
     ["a large pile of small wet brown cardboard railway tickets heaped on a ticket counter in dawn light, every one punched"]),
    (None, "run-to-bhola",
     "सुबह होते ही मैं भोला काका की टपरी की तरफ़ भागा। उन्हें बताना था। थैंक यू बोलना था। उस रात उन्होंने ही मेरी जान बचाई थी।",
     [f"{AKASH} running along a railway track in morning fog toward the place where a tea stall stood"]),
    (None, "ruin",
     "पर टपरी वहाँ थी ही नहीं। जहाँ रोज़ शाम को चाय बनती थी, वहाँ बेलों से ढकी एक टूटी झोपड़ी थी। ज़ंग खाई केतली। कील पर टँगी पुरानी लाल लालटेन। और उसके नीचे, चुपचाप बैठा… कालू।",
     ["a collapsed abandoned tea shack overgrown with vines in morning fog, a rusted kettle on a broken clay stove",
      "an old red kerosene lantern hanging from a nail on a crumbling wall, a black stray dog sitting quietly beneath it"]),
    (None, "photo",
     "दीवार पर एक फ़्रेम में पीली पड़ चुकी फ़ोटो थी, उस पर सूखी माला। नीचे लिखा था — स्वर्गीय भोलानाथ, गैंगमैन। चौदह दिसंबर, नाइनटीन एटी वन।",
     ["an old faded framed photograph of a thin railway trackman on a crumbling wall, a dried marigold garland hanging over it, face too faded to see"]),
    (None, "who-he-was",
     "वही गैंगमैन, जिसकी बात उस रात किसी ने नहीं सुनी। वो आज भी हर शाम आता है। हर नए स्टेशन मास्टर को चाय पिलाने। और बस एक बात बोलने… दस्तक गिन लेना, साहब।",
     [f"{BHOLA} standing beside the railway track at dusk, seen from far away, lantern glowing, almost transparent in the fog"]),
    (None, "torn-half",
     "फ़्रेम के पीछे एक मुड़ा हुआ, पीला पेपर फँसा था। रजिस्टर का वो फटा हुआ आधा पेज। पता नहीं वो वहाँ कैसे पहुँचा। उस पर रूल सेवन का बाक़ी हिस्सा लिखा था।",
     ["close-up of trembling fingers unfolding a torn yellowed half page pulled from behind an old photo frame, handwriting blurred and unreadable"]),
    (None, "rule-seven-full",
     "अगर कोई तुम्हें तुम्हारी अपनी आवाज़ में पुकारे, तो जवाब मत देना। क्योंकि जो जवाब देता है… अगली सर्दी में लीवर वही खींचता है।",
     ["CARD: rule — RULE 7: अपनी आवाज़ को जवाब मत देना। जो जवाब देता है, अगली सर्दी में लीवर वही खींचता है।",
      f"{RAGHU} standing at the dark end of a foggy platform beside the last bench, waiting"]),
    (None, "transfer",
     "उसी वीक मैंने ट्रांसफ़र की एप्लीकेशन डाल दी। जॉब नहीं छोड़ी… मम्मी से किया प्रॉमिस निभाया। आज मैं शहर के एक बड़े स्टेशन पर डे शिफ़्ट करता हूँ। भीड़, शोर, लाइट्स। अब मुझे भीड़ अच्छी लगती है।",
     [f"{AKASH} handing a folded transfer application across a desk to an officer in a railway office, daylight",
      f"a huge crowded Indian city railway station in bright daylight, {AKASH} small among the crowd at a ticket counter"]),
    (None, "three-thirty-three",
     "लेकिन हर रात, ठीक तीन बजकर तैंतीस मिनट पर, मेरा फ़ोन बजता है। अननोन नंबर। मैं उठाता हूँ। कुछ नहीं बोलता। और दूसरी तरफ़ से, मेरी अपनी आवाज़ पूछती है — आकाश… लाइन क्लियर?",
     ["a mobile phone ringing on a bedside table in a dark city apartment, its screen glowing, a clock beside it at three thirty three",
      f"{AKASH} sitting up in bed in the dark holding a phone to his ear, a hand pressed over his mouth"]),
    (None, "new-posting",
     "मैंने आज तक जवाब नहीं दिया। और बेलघाटी हॉल्ट की वैकेंसी फिर से निकली है। अगर वहाँ तुम्हारी फ़र्स्ट पोस्टिंग हो… तो रजिस्टर का लास्ट पेज ज़रूर पढ़ना। और दस्तक… गिन लेना।",
     [f"wide shot of {HALT}, a new young clerk silhouetted in the lit ticket window, the last bench at the far end of the platform not empty",
      "CARD: end — दस्तक गिन लेना।"]),
]

SFX = {
    "habit": [("khat", "end")], "three-knocks": [("knock3", "start")], "fourth-knock": [("knock4", "end")],
    "the-sleeper": [("drip", "end")], "phone-rings": [("phone", "start")],
    "baby-cries": [("knock4", "start"), ("baby", "under")],
    "open": [("latch", "start")], "khat": [("khat", "end")], "lights-out": [("power-down", "start")],
    "special-order": [("phone", "start")], "whistle": [("whistle", "start")],
    # real-world beds that play under the narration
    "kalu": [("dog-howl", "under")], "the-date": [("dog-howl", "under")],
    "the-story": [("train-arrive", "under")], "the-fall": [("bridge-collapse", "under")],
    "57-down": [("ghost-train", "under")], "red-lantern": [("lantern", "under")],
    "struggle": [("lever", "under")], "transfer": [("city", "under")],
}

TITLE = "Belghati Halt Ke 7 Rules | Raat 3:33 Ki Train | Hindi Horror Story Animated"


def main() -> None:
    scenes, md, words = [], [], 0
    stills = cards = 0
    md.append(f"# {TITLE}\n")
    for i, (ch, slug, text, shots) in enumerate(S, 1):
        sid = f"{i:03d}"
        assets, notes = [], []
        for j, shot in enumerate(shots):
            suffix = "" if len(shots) == 1 else "abcdef"[j]
            if shot.startswith("CARD:"):
                assets.append(f"images/{sid}{suffix}_{slug}-card.png"); cards += 1
                notes.append(("Card", shot[5:].strip()))
            else:
                assets.append(f"images/{sid}{suffix}_{slug}.png"); stills += 1
                notes.append(("Image", shot))
        sc = {"id": sid, "slug": slug, "text": text,
              "asset": assets[0] if len(assets) == 1 else assets,
              "shots": [{"kind": k.lower(), "prompt": f"{STYLE}. {p}" if k != "Card" else p}
                        for k, p in notes]}
        if slug in SFX:
            sc["sfx"] = [list(x) for x in SFX[slug]]
        if ch:
            sc["chapter"] = ch
            md.append(f"\n## {ch}\n")
        scenes.append(sc)
        words += len(text.split())
        md.append(f"**{sid}** — {text}\n")
        for k, p in notes:
            md.append(f"> *{k}:* {p}\n")
        md.append("")
    mins = words / WPM
    data = {
        "title": TITLE,
        "description": ("Belghati Halt — jungle ke beech ek chhota sa railway station. Akash ki pehli sarkari "
                        "naukri, night shift, aur ek purana register jiske last page pe 7 rules likhe hain. "
                        "4 baar knock ho toh window mat kholna. Bhoore gatte wala ticket kabhi punch mat karna. "
                        "Aur raat 3:33 pe phone baje… toh ek word mat bolna.\n"
                        "Original animated Hindi horror story."),
        "descriptionFooter": ("Ye ek kaalpanik kahani hai. This is original fiction. Narration and images are AI-generated.\n"
                              "#hindihorrorstory #horrorstoryinhindi #railwayhorror #bhootiyakahani #animatedhorror"),
        "styleNote": STYLE,
        "scenes": scenes,
    }
    (HERE / "scenes.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    md.insert(1, f"_{len(scenes)} scenes · {words} words · ≈{mins:.1f} min at {WPM} wpm · "
                 f"{stills} stills, {cards} text cards_\n")
    (HERE / "SCRIPT.md").write_text("\n".join(md) + "\n")
    print(f"{len(scenes)} scenes, {words} words, ~{mins:.1f} min; {stills} stills, {cards} cards")


if __name__ == "__main__":
    main()
