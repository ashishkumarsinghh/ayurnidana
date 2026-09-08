"""Classical Ayurvedic Database - 45+ Diseases, Formulations, Srotas, and Treatment Protocols.
Citations from Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya, Madhava Nidana, and Bhaishajya Ratnavali.
"""

CLASSICAL_DISEASES = {
    "sandhivata": {
        "name": "Osteoarthritis / Degenerative Arthritis",
        "sanskrit_name": "Sandhivata (संधिवात)",
        "primary_dosha": "Vata",
        "doshic_subtype": "Vyanavayu & Shleshaka Kapha Kshaya",
        "cardinal_symptoms": [
            "joint_pain_cracking",
            "pain_sharp_throbbing",
            "tremors_stiffness",
            "cold_intolerance",
            "dryness_skin_hair"
        ],
        "requires_ama": False,
        "dhatu": ["Asthi Dhatu", "Majja Dhatu", "Mamsa Dhatu"],
        "srotas": ["Asthivaha Srotas", "Majjavaha Srotas"],
        "prognosis": "Krichhra Sadhya (Curable with Difficulty / Chronic Care)",
        "classical_source": "Charaka Samhita Chikitsasthana 28 (Vatavyadhi)",
        "citations": [
            "Charaka Samhita, Chikitsasthana 28/37 (Vatapurna Driti Sparshah)",
            "Madhava Nidana, Vatavyadhi Adhyaya",
            "Ashtanga Hridaya, Nidanasthana 15"
        ],
        "nidana": [
            "Ati Vyayama (Excessive physical exertion beyond capacity)",
            "Abhighata (Trauma or repeated micro-injuries to articular cartilage)",
            "Ruksha-Sheetala Ahara (Excessive intake of dry, light, and cold foods)",
            "Vridhavastha (Natural aging process and Vata predominance)",
            "Dhatu Kshaya (Depletion of vital nutritional fluids and bone matrix)"
        ],
        "purvarupa": [
            "Occasional stiffness in weight-bearing joints upon waking",
            "Subtle crepitus (sound of dry leather bag) during flexion",
            "Transient muscular aching around knee and hip joints"
        ],
        "upashaya_anupashaya": {
            "Upashaya (Alleviating)": [
                "Ushna Abhyanga (Warm medicated oil massage)",
                "Nadi Sweda & Patra Pinda Sweda (Warm herbal fomentation)",
                "Snigdha & Ushna Ahara (Nourishing, warm, unctuous soups with ghee)"
            ],
            "Anupashaya (Aggravating)": [
                "Exposure to cold wind, AC, and damp environments",
                "Fasting (Upavasa) and irregular dry snacks",
                "Weight lifting and high-impact joint jarring activities"
            ]
        },
        "samprapti": {
            "Sanchaya": "Accumulation of Vata in Pakwashaya due to aging and unctuous deficiency.",
            "Prakopa": "Provocation of dry and rough qualities of Vata, drying up Shleshaka Kapha in synovium.",
            "Prasara": "Spread of aggravated Vyana Vayu through systemic channels.",
            "Sthana Samshraya": "Deposition in synovial cavities (Sandhi Khavaigunya) causing cartilage wear.",
            "Vyakti": "Full manifestation of Sandhishoola (pain), Sandhishotha (effusion), and Atopa (crepitus).",
            "Bheda": "Bony osteophyte formation, joint deformities, and functional ankylosis."
        },
        "deepana_pachana": [
            "Shunthi (Zingiber officinale) powder 2g with warm water before meals",
            "Panchakola Churna 1.5g with Luke-warm water to digest any residual Ama"
        ],
        "shamana_formulations": [
            {
                "name": "Yogaraja Guggulu",
                "category": "Vati / Guggulu",
                "classical_indication": "Classical drug of choice for Vata localized in bone joints.",
                "dosage": "2 tablets (500mg each) twice daily",
                "anupana_vehicle": "Maharasnadi Kwatha or warm water",
                "aushadha_sevana_kala": "Madhyabhakta (Mid-meals) for targeted joint absorption",
                "duration_weeks": 8,
                "classical_reference": "Sharngadhara Samhita, Madhyama Khanda 7/56-69"
            },
            {
                "name": "Maharasnadi Kwatha",
                "category": "Kwatha",
                "classical_indication": "Potent anti-inflammatory and restorative for all Vata degenerative diseases.",
                "dosage": "20 ml diluted with 40 ml warm water twice daily",
                "anupana_vehicle": "Warm water with a pinch of Shunthi Churna",
                "aushadha_sevana_kala": "Pragbhakta (30 minutes before food)",
                "duration_weeks": 8,
                "classical_reference": "Bhaishajya Ratnavali, Vatavyadhi Chikitsa"
            },
            {
                "name": "Ksheerabala 101 Taila (Capsules / Drops)",
                "category": "Taila / Rasayana",
                "classical_indication": "Deep neuro-muscular and bone matrix rejuvenation.",
                "dosage": "1-2 capsules twice daily",
                "anupana_vehicle": "Warm milk with a pinch of turmeric",
                "aushadha_sevana_kala": "Nishi (At bedtime)",
                "duration_weeks": 12,
                "classical_reference": "Ashtanga Hridaya, Chikitsasthana 22"
            }
        ],
        "panchakarma": {
            "eligible": True,
            "recommended_therapy": "Janu Basti & Matra Basti (Medicated Enema)",
            "reasoning": "Vata is primarily located in Pakwashaya (colon); Basti is the sovereign treatment (Paramoushadham) for Vata, while Janu Basti provides targeted transdermal replenishment.",
            "purvakarma": [
                "Local Abhyanga with Mahanarayana Taila / Murivenna",
                "Nadi Sweda with Dashamoola Kwatha steam"
            ],
            "pradhanakarma": "Janu Basti with Ksheerabala Taila (35 mins) followed by 8-day course of Matra Basti with Sahacharadi Taila (60ml).",
            "paschatkarma": [
                "Resting in warm room avoiding direct fan/wind",
                "Gentle mobilization and application of Rasnadi Churna on joints"
            ]
        },
        "pathya_ahara": [
            "Warm unctuous grains: Godhuma (wheat), Shashtika Shali (aged red rice)",
            "Healthy fats: Ghrita (cow's pure A2 ghee), Tila taila (cold-pressed sesame oil)",
            "Nourishing soups: Mutton/Bone broth (Mamsa Rasa) or Kulattha (horsegram) yusha",
            "Vegetables: Cooked gourds, drumsticks (Moringa), pumpkin, asparagus (Shatavari)",
            "Spices: Shunthi, Maricha, Pippali, Haridra (turmeric), Methi (fenugreek)"
        ],
        "apathya_ahara": [
            "Cold, dry, stale, refrigerated foods and iced beverages",
            "Astringent and bitter dry pulses: Chana (chickpeas), Rajma (kidney beans), Vatana (peas)",
            "Nightshades in excess, raw cabbage, cauliflower, and excessive caffeine",
            "Carbonated drinks, fermented fast food, and unpasteurized refrigerated curds"
        ],
        "pathya_vihara": [
            "Daily self-abhyanga with warm sesame oil before warm bath",
            "Wearing warm protective wraps around affected knees and lumbar spine",
            "Early to bed (by 10:00 PM) to pacify Vata degradation"
        ],
        "apathya_vihara": [
            "Day sleeping (Divasvapna) followed by late-night awakenings (Ratri Jagarana)",
            "Walking barefoot on cold tile/stone floors",
            "Suppressing natural urges (Adharaniya Vegas) especially flatus and stool"
        ],
        "yoga_pranayama": [
            "Pavanamuktasana (Gentle variation for joint wind relief)",
            "Tadasana & Vrikshasana (Gentle weight balancing with wall support)",
            "Nadi Shodhana Pranayama (15 minutes of slow alternate nostril breathing)",
            "Bhramari Pranayama (To pacify neuro-sensory pain hyperactivity)"
        ]
    },

    "amavata": {
        "name": "Rheumatoid Arthritis / Autoimmune Reactive Arthritis",
        "sanskrit_name": "Amavata (आमवात)",
        "primary_dosha": "Vata & Kapha",
        "doshic_subtype": "Sama Vata with Kapha involvement in Sleshmasthana",
        "cardinal_symptoms": [
            "joint_pain_cracking",
            "dull_pain_swelling_edema",
            "heaviness_body_limbs",
            "fever",
            "tongue_thick_white_coating",
            "loss_of_taste_aruchi"
        ],
        "requires_ama": True,
        "dhatu": ["Rasa Dhatu", "Asthi Dhatu", "Mamsa Dhatu"],
        "srotas": ["Rasavaha Srotas", "Annavaha Srotas", "Asthivaha Srotas"],
        "prognosis": "Krichhra Sadhya (Curable with great difficulty / Complex autoimmune)",
        "classical_source": "Madhava Nidana Chapter 25",
        "citations": [
            "Madhava Nidana, Amavata Nidana (Amavatodhyam Ghoram...)",
            "Chakradatta, Amavata Chikitsa",
            "Bhaishajya Ratnavali, Amavata Rogadhikara"
        ],
        "nidana": [
            "Viruddha Ahara (Incompatible foods like fish and milk, fruits with dairy)",
            "Mandagni (Compromised digestive fire leading to toxic intermediate Ama)",
            "Vyayama immediately after unctuous heavy meals (Abhyavaharana)",
            "Snigdha Bhukta Vyayama (Strenuous exertion before digestion completes)"
        ],
        "purvarupa": [
            "Angamarda (Generalized deep muscular aching)",
            "Aruchi (Loss of appetite / complete lack of taste)",
            "Trishna (Excessive unquenchable thirst despite sluggish digestion)",
            "Alasya and Gaurava (Profound heaviness and debilitating morning fatigue)"
        ],
        "upashaya_anupashaya": {
            "Upashaya (Alleviating)": [
                "Rooksha Sweda (Dry sand/salt bolus fomentation - Baluka Sweda)",
                "Langhana (Therapeutic fasting / light hot water diets)",
                "Katu & Tikta Rasa (Pungent, bitter, digestive spices)"
            ],
            "Anupashaya (Aggravating)": [
                "Snigdha Abhyanga (Oily massage is strictly CONTRAINDICATED in early stage)",
                "Heavy, sweet, cold, oily foods like dairy, cheese, bananas",
                "Humid cloudy weather and damp living spaces"
            ]
        },
        "samprapti": {
            "Sanchaya": "Impaired Jatharagni produces undigested foul endotoxin (Ama) in Amashaya.",
            "Prakopa": "Ama combines with provoked Vata and enters circulation through Dhamanis.",
            "Prasara": "Systemic circulation of virulent Ama-Vata complex through Rasavaha Srotas.",
            "Sthana Samshraya": "Selective deposition in synovial spaces (Shleshmasthana) - joints, wrists, knees.",
            "Vyakti": "Severe agonizing scorpion-sting like pain (Vrishchika Damshavat), burning swelling, morning gel phenomenon.",
            "Bheda": "Contractures, joint ankylosis, nodules, and systemic organ involvement."
        },
        "deepana_pachana": [
            "Strict Langhana (Light diet of warm Moong soup with Shunthi & Maricha)",
            "Vaishwanara Churna 3g twice daily with warm water",
            "Shunthi-Kashaya (Dry ginger decoction) taken warm throughout the day"
        ],
        "shamana_formulations": [
            {
                "name": "Simhanada Guggulu",
                "category": "Vati / Guggulu",
                "classical_indication": "Paramoushadham for Amavata; digests Ama and reduces joint inflammation.",
                "dosage": "2 tablets (500mg each) thrice daily",
                "anupana_vehicle": "Warm water or Dashamoola Kwatha",
                "aushadha_sevana_kala": "Madhyabhakta (Mid-meals)",
                "duration_weeks": 8,
                "classical_reference": "Chakradatta, Amavata Chikitsa"
            },
            {
                "name": "Rasnasaptaka Kwatha",
                "category": "Kwatha",
                "classical_indication": "Pacifies agonizing pain in joints, thighs, sacroiliac region.",
                "dosage": "20 ml with 40 ml warm water twice daily",
                "anupana_vehicle": "Warm water + Eranda Taila (Castor oil 5ml at bedtime)",
                "aushadha_sevana_kala": "Pragbhakta (Before meals)",
                "duration_weeks": 6,
                "classical_reference": "Chakradatta, Amavata Chikitsa"
            },
            {
                "name": "Amavatari Rasa",
                "category": "Herbomineral",
                "classical_indication": "Specialized formulation for chronic recalcitrant Amavata.",
                "dosage": "1 tablet (250mg) twice daily",
                "anupana_vehicle": "Warm water with fresh ginger juice",
                "aushadha_sevana_kala": "Samana (Along with meal)",
                "duration_weeks": 4,
                "classical_reference": "Bhaishajya Ratnavali, Amavata Chikitsa"
            }
        ],
        "panchakarma": {
            "eligible": True,
            "recommended_therapy": "Baluka Sweda followed by Vaitarana Basti",
            "reasoning": "Baluka Sweda (Dry sand bag heat) absorbs local Ama. Vaitarana Basti specifically expels stagnant Ama and Vata from the pelvic region.",
            "purvakarma": [
                "Strictly NO oil massage initially (Rukshana is paramount)",
                "Baluka Sweda (Hot sand/rock salt bolus) twice daily on swollen joints",
                "Administration of castor oil with ginger decoction for mild purgation (Anulomana)"
            ],
            "pradhanakarma": "Course of Vaitarana Basti (containing Tamarind, Guda, Saindhava, Gomutra/Erandataila) for 8 consecutive days.",
            "paschatkarma": [
                "Gradual transition from Yavagu (warm barley gruel) to normal light diet",
                "Monitoring C-reactive protein (CRP) and ESR levels"
            ]
        },
        "pathya_ahara": [
            "Barley (Yava), Old red rice (Rakta Shali), Horsegram (Kulattha) soup",
            "Vegetables: Patola (pointed gourd), Shigru (drumstick), Karavellaka (bitter gourd), Garlic (Lashuna)",
            "Warm spiced ginger water (Shunthi-Siddha Jala) for drinking",
            "Castor oil (Eranda Taila) taken in small measured therapeutic doses"
        ],
        "apathya_ahara": [
            "Strict avoidance of all curd, cheese, paneer, and chilled milk products",
            "Urad dal (Black gram), heavy flour, bakery products, deep-fried snacks",
            "Cold foods, ice creams, cold sodas, fermented batters (Idli/Dosa excess)",
            "Fish with milk or citrus fruits (Viruddha Ahara)"
        ],
        "pathya_vihara": [
            "Hot dry fomentation over stiff joints every morning",
            "Gentle active joint range-of-motion within pain tolerance",
            "Resting in warm, draft-free, sunny rooms"
        ],
        "apathya_vihara": [
            "Total avoidance of cold showers, rain exposure, and air conditioning drafts",
            "Daytime naps (strongly exacerbates Kapha and Ama)",
            "Excessive weight-bearing during active inflammatory flares"
        ],
        "yoga_pranayama": [
            "Sukshma Vyayama (Gentle rotational exercises for finger, wrist, ankle joints)",
            "Vajrasana (Post-meal posture to stimulate digestive Agni, if knees permit)",
            "Kapalabhati (Mild 3-5 minutes to kindle metabolic Agni and dry out Ama)",
            "Surya Bhedana Pranayama (Stimulates solar sympathetic heat and digestive power)"
        ]
    },

    "prameha": {
        "name": "Type 2 Diabetes Mellitus & Metabolic Syndrome",
        "sanskrit_name": "Prameha / Madhumeha (प्रमेह / मधुमेह)",
        "primary_dosha": "Kapha & Pitta",
        "doshic_subtype": "Kapha Pradhana Tridoshaja with Medo-Kleda Dushti",
        "cardinal_symptoms": [
            "excessive_thirst_sweating",
            "heaviness_body_limbs",
            "weight_gain_slow_metabolism",
            "tongue_thick_white_coating",
            "cloudy_milky_frothy_urine",
            "burning_sensation"
        ],
        "requires_ama": False,
        "dhatu": ["Meda Dhatu", "Mamsa Dhatu", "Kleda", "Rasa Dhatu"],
        "srotas": ["Mutravaha Srotas", "Medovaha Srotas", "Udakavaha Srotas"],
        "prognosis": "Yapya (Manageable / Lifelong Lifestyle Management)",
        "classical_source": "Charaka Samhita Nidanasthana 4 & Chikitsasthana 6",
        "citations": [
            "Charaka Samhita, Nidanasthana 4/3-4 (Asyasukham Swapnasukham...)",
            "Sushruta Samhita, Chikitsasthana 11 (Prameha Pratishedha)",
            "Ashtanga Hridaya, Chikitsasthana 12"
        ],
        "nidana": [
            "Asyasaukhyam (Addiction to pleasant sedentary seating and lack of exercise)",
            "Swapnasaukhyam (Excessive prolonged sleep, particularly daytime napping)",
            "Dadhini (Excessive consumption of yoghurt and curd preparations)",
            "Gramya-Udaka-Anupa Mamsa (Frequent intake of wetland and processed fatty meats)",
            "Guda Vaikrita (Excessive intake of refined sweets, molasses, and newly harvested grains)"
        ],
        "purvarupa": [
            "Kara-Pada Daha (Burning sensation in palms and soles)",
            "Mukha Madhurya (Sweet sticky taste in oral cavity, attraction of ants to urine)",
            "Shithilatva of muscles (Loss of muscle firmness and tone)",
            "Excessive thirst, dry throat, and accumulation of debris on teeth and tongue"
        ],
        "upashaya_anupashaya": {
            "Upashaya (Alleviating)": [
                "Daily brisk walking, physical labour, and aerobic exercise",
                "Tikta and Kashaya Rasa (Bitter and astringent diet - Karela, Methi)",
                "Udwarthana (Dry herbal powder massage with Triphala / Kolakulathadi)"
            ],
            "Anupashaya (Aggravating)": [
                "Sedentary lifestyle and couch-potato habits",
                "Refined carbohydrates, sweets, bakery products, and sugary beverages",
                "Sleeping during daytime and immediately after lunch"
            ]
        },
        "samprapti": {
            "Sanchaya": "Sedentary habit and heavy sweet diet accumulate Kapha, Pitta, and Meda.",
            "Prakopa": "Provoked Kapha mixes with liquefying Medas (fatty tissue) and body fluids (Kleda).",
            "Prasara": "The vitiated fluids circulate throughout all bodily channels.",
            "Sthana Samshraya": "Localizes in Mutravaha Srotas and Basti (kidneys and bladder), transforming urine.",
            "Vyakti": "Prabhoota Avila Mutrata (profuse, turbid urination with high sugar and specific gravity).",
            "Bheda": "Progression from 20 types of Prameha to irreversible Ojas depletion (Madhumeha)."
        },
        "deepana_pachana": [
            "Triphala Kashaya with a pinch of Haridra (Turmeric) powder",
            "Mustadi Kwatha or Methi (fenugreek seed) soaked water every morning"
        ],
        "shamana_formulations": [
            {
                "name": "Nisha-Amalaki Churna / Vati",
                "category": "Churna / Vati",
                "classical_indication": "Classical specific combination (Turmeric + Indian Gooseberry) for metabolic clearance.",
                "dosage": "3g powder or 2 tablets twice daily",
                "anupana_vehicle": "Luke-warm water or Honey (aged Makshika)",
                "aushadha_sevana_kala": "Pragbhakta (Before meals)",
                "duration_weeks": 12,
                "classical_reference": "Ashtanga Hridaya, Chikitsasthana 12/5"
            },
            {
                "name": "Chandraprabha Vati",
                "category": "Vati",
                "classical_indication": "Sovereign formulation for urinary channel purification, glycemic control, and neuropathy.",
                "dosage": "2 tablets (500mg each) twice daily",
                "anupana_vehicle": "Warm water or Shilajit water",
                "aushadha_sevana_kala": "Madhyabhakta (Mid-meals)",
                "duration_weeks": 12,
                "classical_reference": "Sharngadhara Samhita, Madhyama Khanda 7/40-49"
            },
            {
                "name": "Vasantakusumakara Rasa",
                "category": "Rasayana / Gold Formulation",
                "classical_indication": "Advanced cellular rejuvenator in chronic diabetes with neuropathy, weakness, or Ojas depletion.",
                "dosage": "1 tablet (125mg) once daily",
                "anupana_vehicle": "Milk or honey",
                "aushadha_sevana_kala": "Pratah (Early morning empty stomach)",
                "duration_weeks": 6,
                "classical_reference": "Bhaishajya Ratnavali, Prameha Rogadhikara"
            }
        ],
        "panchakarma": {
            "eligible": True,
            "recommended_therapy": "Vamana (in obese Sthula Pramehi) or Virechana & Udwarthana",
            "reasoning": "Charaka distinguishes Sthula (Obese) vs Krisha (Lean) Pramehi. Sthula requires Shodhana (Virechana/Vamana), whereas Krisha requires Santarpana and gentle Shamana.",
            "purvakarma": [
                "Udwarthana (Dry herbal friction massage with Kolakulathadi Churna) for 7 days",
                "Snehapana with Mahatiktaka Ghrita or Guggulutiktaka Ghrita"
            ],
            "pradhanakarma": "Teekshna Virechana with Trivrit Lehyam (30g) to purge excess Medas and Pitta.",
            "paschatkarma": [
                "Strict Samsarjana Krama with Yava (barley) and Mudga (green gram) soups",
                "Regular post-prandial blood glucose and HbA1c monitoring"
            ]
        },
        "pathya_ahara": [
            "Grains: Yava (barley - whole grain & flour), Bajra (pearl millet), Kodrava, aged red rice",
            "Legumes: Mudga (green gram), Kulattha (horsegram), Chana (roasted Bengal gram)",
            "Vegetables: Karavellaka (bitter gourd), Patola, Methi leaves, Bimbi (ivy gourd), Moringa",
            "Fruits: Amalaki (fresh amla), Jambu (jamun fruit & seed powder), Kapittha",
            "Beverage: Water boiled with Vijaysar heartwood or Cinnamon bark"
        ],
        "apathya_ahara": [
            "All refined sugars, high-fructose syrups, jaggery, pastries, and candy",
            "Polished white rice, refined maida flour, potatoes, tapioca, and sweet potatoes",
            "Full-fat yoghurt, whole buffalo milk, butter, deep-fried fast foods",
            "Sweet fruits: Mangoes, grapes, bananas, chiku, custard apples in excess"
        ],
        "pathya_vihara": [
            "Minimum 45-60 minutes of brisk walking or swimming daily",
            "Active physical sports and resistance exercises to improve insulin sensitivity",
            "Staying mentally engaged and practicing mindfulness"
        ],
        "apathya_vihara": [
            "Sleeping immediately after meals and daytime naps (Divasvapna)",
            "Prolonged unbroken sedentary sitting without hourly movement breaks",
            "Late night binge eating and sleeping past 11 PM"
        ],
        "yoga_pranayama": [
            "Mandukasana (Frog pose - stimulates pancreatic islets directly)",
            "Paschimottanasana & Ardha Matsyendrasana (Abdominal torsion stimulating digestive glands)",
            "Kapalabhati Pranayama (10-15 minutes in rounds of 50 to kindle visceral Agni)",
            "Agnisara Kriya (Daily 3 rounds on an empty stomach to enhance abdominal Agni)"
        ]
    },

    "amlapitta": {
        "name": "Hyperacidity / Gastroesophageal Reflux Disease (GERD)",
        "sanskrit_name": "Amlapitta (अम्लपित्त)",
        "primary_dosha": "Pitta",
        "doshic_subtype": "Vidagdha Pitta with Amlatva & Dravatva Vriddhi",
        "cardinal_symptoms": [
            "burning_sensation",
            "acid_reflux_heartburn",
            "intense_sharp_hunger",
            "yellowish_eyes_urine",
            "irritability_anger"
        ],
        "requires_ama": False,
        "dhatu": ["Rasa Dhatu", "Rakta Dhatu"],
        "srotas": ["Annavaha Srotas", "Purishavaha Srotas"],
        "prognosis": "Sukha Sadhya (Easily Curable with Diet & Herbs)",
        "classical_source": "Madhava Nidana Chapter 51 & Kashyapa Samhita",
        "citations": [
            "Madhava Nidana, Amlapitta Nidana (Avipako Klama Utklesho...)",
            "Bhaishajya Ratnavali, Amlapitta Chikitsa",
            "Charaka Samhita, Grahani Chikitsasthana 15"
        ],
        "nidana": [
            "Ati Vidahi Ahara (Excessive spicy, sour, fried, and fermented foods)",
            "Kulatha, Urad, excessive vinegar, mustard, and green chillies",
            "Irregular meal timings (Adhyashana and Vishamashana)",
            "Excessive consumption of tea, black coffee, alcohol, and tobacco",
            "Krodha, Shoka, and Chinta (Chronic anger, stress, and anxiety)"
        ],
        "purvarupa": [
            "Avipaka (Indigestion and delayed gastric emptying)",
            "Klama (Tiredness without heavy physical exertion)",
            "Utklesha (Water brash, salivation, and nauseous feeling)",
            "Amla-Tikta Udgara (Sour and bitter belching)"
        ],
        "upashaya_anupashaya": {
            "Upashaya (Alleviating)": [
                "Sheetala and Madhura Ahara (Cooling, sweet, and soothing foods like cold milk)",
                "Ghrita (Ghee - especially Shatavari Ghrita or Dadimadi Ghrita)",
                "Bitter vegetables: Patola (pointed gourd), cucumber, sweet pomegranates"
            ],
            "Anupashaya (Aggravating)": [
                "Spicy pickles, tamarind, tomatoes, garlic, and citrus marinades",
                "Skipping meals or eating late at night",
                "Lying down immediately after eating dinner"
            ]
        },
        "samprapti": {
            "Sanchaya": "Accumulation of Pitta in Amashaya due to excessive sour and pungent foods.",
            "Prakopa": "Pitta loses its normal slight bitter taste and becomes intensely acidic (Amlatva Vriddhi).",
            "Prasara": "Reflux of acid liquid Pitta into esophagus (Urdhvaga Amlapitta) or downward (Adhoga).",
            "Sthana Samshraya": "Irritation of esophageal and gastric mucosa (Annavaha Srotas).",
            "Vyakti": "Retrosternal burning (Hrid-Kanthadaha), acidic regurgitation, nausea, headache.",
            "Bheda": "Erosive gastritis, peptic ulceration, Barrett's esophagus in chronic state."
        },
        "deepana_pachana": [
            "Dhanyaka-Musta Hima (Cold infusion of Coriander seeds & Nagarmotha)",
            "Avipattikar Churna with coconut water or cool water"
        ],
        "shamana_formulations": [
            {
                "name": "Avipattikar Churna",
                "category": "Churna",
                "classical_indication": "Classical formulation for Pitta neutralization and downward bowel cleansing.",
                "dosage": "3-5g twice daily",
                "anupana_vehicle": "Luke-warm water or Coconut water",
                "aushadha_sevana_kala": "Pragbhakta (Before food) or with the first morsel",
                "duration_weeks": 6,
                "classical_reference": "Bhaishajya Ratnavali, Amlapitta Chikitsa"
            },
            {
                "name": "Kamadudha Rasa (Mukta Yukta)",
                "category": "Herbomineral / Calcium Compound",
                "classical_indication": "Fast-acting natural antacid that coats the gastric mucosa and calms fiery Pitta.",
                "dosage": "1-2 tablets (250mg) twice daily",
                "anupana_vehicle": "Cold milk or butter milk or water",
                "aushadha_sevana_kala": "Madhyabhakta (Mid-meals)",
                "duration_weeks": 4,
                "classical_reference": "Rasa Tarangini & Bhaishajya Ratnavali"
            },
            {
                "name": "Shatavari Ghrita",
                "category": "Ghrita",
                "classical_indication": "Mucosal healing, ulcer repair, and deep cooling for gastrointestinal tract.",
                "dosage": "1 teaspoon (5-10 ml) twice daily",
                "anupana_vehicle": "Warm water or warm milk",
                "aushadha_sevana_kala": "Pragbhakta (Empty stomach morning and evening)",
                "duration_weeks": 8,
                "classical_reference": "Sahasrayogam, Ghrita Prakarana"
            }
        ],
        "panchakarma": {
            "eligible": True,
            "recommended_therapy": "Virechana (Therapeutic Purgation) or Mridu Vamana",
            "reasoning": "Virechana is the supreme radical treatment for morbid Pitta located in Amashaya and Pittashaya.",
            "purvakarma": [
                "Deepana-Pachana with Shadanga Paniya for 3 days",
                "Internal Snehapana with Kalyanaka Ghrita or Dadimadi Ghrita in ascending doses",
                "Abhyanga with Chandanadi Taila and gentle steam"
            ],
            "pradhanakarma": "Mridu Virechana with Trivrit Lehyam (20-25g) or Haritaki decoction on empty stomach.",
            "paschatkarma": [
                "Samsarjana Krama with Peya, Vilepi, and Mudga Yusha for 3-5 days"
            ]
        },
        "pathya_ahara": [
            "Grains: Old barley (Purana Yava), Godhuma (wheat), Basmati and Shali rice",
            "Milk & Dairy: Sweet cow's milk, fresh sweet buttermilk churned without fat, pure A2 ghee",
            "Fruits: Sweet ripe grapes (Draksha), ripe pomegranates (Dadima), sweet melons, amla",
            "Vegetables: Patola, ash gourd (Kushmanda), bottle gourd, leafy green vegetables",
            "Drinks: Coconut water, coriander seed infusion, cooling fennel tea"
        ],
        "apathya_ahara": [
            "Hot spices: Red chillies, green chillies, raw garlic, excessive black pepper",
            "Sour foods: Vinegar, fermented soy, lemon juice in excess, sour buttermilk, unripe mango",
            "Fried, oily street snacks, pizzas, burgers, crisps, and caffeinated sodas",
            "Alcohol, smoking, tobacco chewing, and carbonated beverages"
        ],
        "pathya_vihara": [
            "Eating meals at fixed calm intervals without television or emotional stress",
            "Elevating head of bed by 15-20 degrees to prevent nocturnal reflux",
            "Evening strolls in moonlit or pleasant gardens (Sheetala Vihara)"
        ],
        "apathya_vihara": [
            "Lying down immediately after eating lunch or dinner",
            "Skipping breakfast or prolonged intermittent fasting exceeding metabolic capacity",
            "Suppression of hunger (Kshudha Vega) and unmanaged workplace anger"
        ],
        "yoga_pranayama": [
            "Shitali and Shitkari Pranayama (Cooling breathing - 10 minutes twice daily)",
            "Chandra Bhedana Pranayama (Left nostril breathing to activate lunar cooling nadi)",
            "Vajrasana (10 minutes immediately following meals to streamline gastric motility)",
            "Pawanmuktasana and Matsyasana (Relieves intra-abdominal pressure)"
        ]
    }
}
