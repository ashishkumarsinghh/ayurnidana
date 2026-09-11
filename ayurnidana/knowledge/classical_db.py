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
    },

    "gridhrasi": {
        "name": "Sciatica / Lumbar Radiculopathy",
        "sanskrit_name": "Gridhrasi (गृध्रसी)",
        "primary_dosha": "Vata",
        "doshic_subtype": "Vata-Kapha Pradhana with Snayu & Kandara Stambha",
        "cardinal_symptoms": [
            "sciatica_radiating_leg_pain",
            "pain_sharp_throbbing",
            "tremors_stiffness",
            "constipation_hard_stools"
        ],
        "requires_ama": False,
        "dhatu": ["Asthi Dhatu", "Majja Dhatu", "Mamsa Dhatu", "Kandara"],
        "srotas": ["Asthivaha Srotas", "Majjavaha Srotas", "Mamsavaha Srotas"],
        "prognosis": "Krichhra Sadhya (Curable with Difficulty / Chronic Care)",
        "classical_source": "Charaka Samhita Chikitsasthana 28/56 & Madhava Nidana 22",
        "citations": [
            "Charaka Samhita, Chikitsasthana 28/56 (Sphik-purva-kati-prishta-uru-janu-jangha-padam kramat)",
            "Madhava Nidana, Vatavyadhi 22/37-41",
            "Chakradatta, Vatavyadhi Chikitsa"
        ],
        "nidana": [
            "Ati Bhaaravahana (Excessive lifting of heavy weights with bent spine)",
            "Vishamashana & Yanayana (Jerky two-wheeler riding and prolonged seated vibration)",
            "Abhighata (Trauma or disk herniation compressing neuro-vascular bundles)",
            "Ruksha Ahara (Dry, cold, light dietary habits depleting spinal lubrication)"
        ],
        "purvarupa": [
            "Transient stiffness in lumbar spine upon prolonged sitting",
            "Numbness or tingling sensation in gluteal region and posterior thigh",
            "Difficulty straightening back after rising from low seats"
        ],
        "upashaya_anupashaya": {
            "Upashaya (Alleviating)": [
                "Warm medicated oil pooling (Kati Basti) and Nadisweda",
                "Gentle spine extension and hot sesame oil fomentation",
                "Warm unctuous diet with garlic, ghee, and warming spices"
            ],
            "Anupashaya (Aggravating)": [
                "Forward bending, lifting heavy objects, and running on hard surfaces",
                "Exposure to cold drafts and air-conditioned environments",
                "Constipation and straining at stool (increases intra-thecal pressure)"
            ]
        },
        "samprapti": {
            "Sanchaya": "Vata accumulates in Pakwashaya due to aging, strain, and unctuous deficiency.",
            "Prakopa": "Provoked Vyana Vayu affects the great tendon/nerve trunk extending from gluteal area to foot.",
            "Prasara": "Radiating neuralgia travelling down the Kandara (sciatic nerve pathway).",
            "Sthana Samshraya": "Deposition in Kati-Prishta-Janu-Pada (L4-S1 nerve root distribution).",
            "Vyakti": "Severe shooting pain (Toda), stiffness (Stambha), and gait impediment like a vulture (Gridhra).",
            "Bheda": "Motor weakness, muscular wasting of calf, and sensory foot drop."
        },
        "deepana_pachana": [
            "Shunthi Churna 2g with warm water before meals",
            "Erandabhrishta Haritaki 3g at bedtime with warm water for gentle downward Vata anulomana"
        ],
        "shamana_formulations": [
            {
                "name": "Trayodashanga Guggulu",
                "category": "Vati / Guggulu",
                "classical_indication": "Classical specific for lumbar radiculopathy, sacroiliitis, and sciatic neuralgia.",
                "dosage": "2 tablets (500mg) twice daily",
                "anupana_vehicle": "Warm water or Dashamoola Kwatha",
                "aushadha_sevana_kala": "Madhyabhakta (Mid-meals)",
                "duration_weeks": 8,
                "classical_reference": "Bhaishajya Ratnavali, Vatavyadhi Chikitsa"
            },
            {
                "name": "Sahacharadi Kashaya",
                "category": "Kwatha",
                "classical_indication": "Master formulation for all Vata disorders localized from lumbar spine to lower extremities.",
                "dosage": "20 ml with 40 ml warm water twice daily",
                "anupana_vehicle": "Warm water with a pinch of rock salt or castor oil",
                "aushadha_sevana_kala": "Pragbhakta (Before meals)",
                "duration_weeks": 6,
                "classical_reference": "Ashtanga Hridaya, Chikitsasthana 21"
            },
            {
                "name": "Ekangaveera Rasa",
                "category": "Herbomineral",
                "classical_indication": "Potent neuro-regenerator for compressed and inflamed peripheral nerve pathways.",
                "dosage": "1 tablet (125mg) twice daily",
                "anupana_vehicle": "Warm milk or ginger honey water",
                "aushadha_sevana_kala": "Samana (With meals)",
                "duration_weeks": 4,
                "classical_reference": "Bhaishajya Ratnavali, Vatavyadhi Chikitsa"
            }
        ],
        "panchakarma": {
            "eligible": True,
            "recommended_therapy": "Kati Basti with Sahacharadi Taila + Matra Basti with Murivenna",
            "reasoning": "Kati Basti provides intense local transdermal neuro-nourishment while Matra Basti directly pacifies Pakwashaya-seated Vata.",
            "purvakarma": [
                "Local Snehana with Mahanarayana Taila",
                "Nadi Sweda with Dashamoola decoction steam"
            ],
            "pradhanakarma": "Kati Basti (retaining warm medicated oil over lumbar spine for 35 mins daily for 7 days) and Agnikarma / Siravyadha if pain is refractory.",
            "paschatkarma": [
                "Lumbosacral support belt during travel",
                "Resting on firm orthopedic mattress avoiding low sofas"
            ]
        },
        "pathya_ahara": [
            "Warm unctuous wheat, aged rice, and moong dal",
            "Lashuna Ksheerapaka (Garlic milk decoction) taken warm in the evening",
            "Cow's pure ghee, cold-pressed sesame oil, and bone/marrow broth",
            "Cooked vegetables: Drumstick, gourd, carrot, pumpkin, and spinach"
        ],
        "apathya_ahara": [
            "Dry cold snacks, crackers, chips, and chilled soft drinks",
            "Excessive astringent beans: Black gram, kidney beans, raw sprouts",
            "Refrigerated leftovers and fermented batters"
        ],
        "pathya_vihara": [
            "Maintaining erect posture with ergonomic lumbar curve support",
            "Daily self-massage of lumbar region and feet with warm sesame oil",
            "Sleeping on a firm, supportive mattress on the back with pillow under knees"
        ],
        "apathya_vihara": [
            "Bending forward from waist to lift weights (always bend knees)",
            "Riding on bumpy, unpaved roads and prolonged continuous driving",
            "Suppressing natural urges to defecate or pass flatus"
        ],
        "yoga_pranayama": [
            "Bhujangasana (Cobra pose - gentle lumbar extension within comfort)",
            "Shalabhasana (Gentle back strengthening)",
            "Setu Bandhasana (Supported bridge pose)",
            "Nadi Shodhana Pranayama (Alternate nostril breathing for 15 minutes)"
        ]
    },

    "vatarakta": {
        "name": "Gout / Hyperuricemia / Metabolic Arthritis",
        "sanskrit_name": "Vatarakta / Adhyavata (वातरक्त)",
        "primary_dosha": "Vata & Pitta",
        "doshic_subtype": "Vata aggravated by morbid Rakta Dhatu obstruction (Avarana)",
        "cardinal_symptoms": [
            "gout_big_toe_burning_pain",
            "burning_sensation",
            "dull_pain_swelling_edema",
            "pain_sharp_throbbing"
        ],
        "requires_ama": False,
        "dhatu": ["Rakta Dhatu", "Asthi Dhatu", "Mamsa Dhatu", "Rasa Dhatu"],
        "srotas": ["Raktavaha Srotas", "Asthivaha Srotas", "Rasavaha Srotas"],
        "prognosis": "Krichhra Sadhya (Curable with Difficulty / Chronic Metabolic Care)",
        "classical_source": "Charaka Samhita Chikitsasthana 29 & Ashtanga Hridaya Chikitsa 22",
        "citations": [
            "Charaka Samhita, Chikitsasthana 29/11 (Adhyavata / Khudaroga)",
            "Ashtanga Hridaya, Chikitsasthana 22",
            "Madhava Nidana, Vatarakta Rogadhikara 23"
        ],
        "nidana": [
            "Lavana-Amla-Katu-Kshara Ahara (Excessive salty, sour, spicy, and alkaline foods)",
            "Gramya-Anupa Mamsa & Matsya (Heavy consumption of red meat, organs, and seafood)",
            "Surasava-Madya (Excessive beer, alcohol, and fermented beverages)",
            "Asyasaukhya with high vehicle riding (Sedentary aristocrat lifestyle - hence Adhyavata)",
            "Divasvapna (Day sleeping after heavy non-vegetarian meals)"
        ],
        "purvarupa": [
            "Transient burning and tingling sensation in the great toe (Angushtha)",
            "Excessive sweating or total absence of perspiration in feet",
            "Pricking sensation like needle jabs in ankle and small joints",
            "Laxity of joints and occasional skin discoloration over foot"
        ],
        "upashaya_anupashaya": {
            "Upashaya (Alleviating)": [
                "Sheetala Pradeha (Cooling herbal paste application with Chandana, Manjishta)",
                "Jalaukavacharana (Leech therapy to remove hot morbid blood)",
                "Tikta and Madhura herbs like Guduchi (Tinospora cordifolia)"
            ],
            "Anupashaya (Aggravating)": [
                "Hot fermentations, warm oil massage, and sun exposure (strictly contraindicated)",
                "Alcohol, red meat, shellfish, lentils, and sour curd",
                "Tight footwear and walking long distances during acute attacks"
            ]
        },
        "samprapti": {
            "Sanchaya": "Vata provoked by dry food and travel combines with Rakta vitiated by salty spicy alcohol.",
            "Prakopa": "Provoked Rakta obstructs the circulatory channels (Avarana) of Vata.",
            "Prasara": "The obstructed Vata becomes intensely aggravated, circulating along with toxic Rakta.",
            "Sthana Samshraya": "Gravitates toward dependent small joints: first the Metatarsophalangeal joint of the great toe.",
            "Vyakti": "Excruciating fiery pain, bright red-purple swelling, extreme hyperesthesia to touch.",
            "Bheda": "Tophi formation, joint destruction, chronic renal uric acid calculi."
        },
        "deepana_pachana": [
            "Guduchi Kashaya with Amalaki juice every morning",
            "Dhanyaka-Musta cold infusion for gentle Pitta-Rakta cooling"
        ],
        "shamana_formulations": [
            {
                "name": "Kaishore Guggulu",
                "category": "Vati / Guggulu",
                "classical_indication": "Supreme drug of choice for Vatarakta, purifies Rakta, lowers uric acid, and eases joint fire.",
                "dosage": "2 tablets (500mg) thrice daily",
                "anupana_vehicle": "Manjishtadi Kwatha or warm water",
                "aushadha_sevana_kala": "Madhyabhakta (Mid-meals)",
                "duration_weeks": 8,
                "classical_reference": "Sharngadhara Samhita, Madhyama Khanda 7/70-81"
            },
            {
                "name": "Amritadi Kwatha (Guduchi Kwatha)",
                "category": "Kwatha",
                "classical_indication": "Classical anti-gout and blood-purifying formulation; clears Avarana of Vata.",
                "dosage": "20 ml with 40 ml water twice daily",
                "anupana_vehicle": "Honey or warm water",
                "aushadha_sevana_kala": "Pragbhakta (Before food)",
                "duration_weeks": 8,
                "classical_reference": "Bhaishajya Ratnavali, Vatarakta Chikitsa"
            },
            {
                "name": "Pinda Taila (External Application Only)",
                "category": "Taila (External)",
                "classical_indication": "Cooling medicated oil with bees wax, Manjishta, and Sariva; relieves acute fiery redness.",
                "dosage": "Gentle local application twice daily (no vigorous massage)",
                "anupana_vehicle": "External topical application",
                "aushadha_sevana_kala": "External",
                "duration_weeks": 4,
                "classical_reference": "Ashtanga Hridaya, Chikitsasthana 22"
            }
        ],
        "panchakarma": {
            "eligible": True,
            "recommended_therapy": "Raktamokshana (Jalauka - Leech Therapy) & Ksheera Basti",
            "reasoning": "Charaka states: 'Raktamokshana is the foremost therapy in Vatarakta when burning redness is intense'.",
            "purvakarma": [
                "Cooling Parisheka with Dashamoola-Ksheera or Dhanyamla",
                "Mild Deepana with Guduchi"
            ],
            "pradhanakarma": "Application of 2-4 medicinal leeches (Jalauka) around the inflamed great toe/joint to let morbid venous blood.",
            "paschatkarma": [
                "Application of Haridra and Shatadhauta Ghrita to bite sites",
                "Gentle Mridu Virechana with Trivrit or Castor oil in milk"
            ]
        },
        "pathya_ahara": [
            "Grains: Old barley (Yava), Shali rice, wheat",
            "Dairy: Sweet cow's milk, pure cow's ghee",
            "Vegetables: Patola, bitter gourd (Karela), ash gourd, cucumber, leafy greens",
            "Fruits: Sweet ripe grapes, pomegranates, amla (fresh gooseberry)",
            "Fluid: Adequate clean water (3 liters daily) to flush metabolic urates"
        ],
        "apathya_ahara": [
            "Total avoidance of red meat, organ meats, shellfish, and sardines",
            "Beer, whiskey, wine, and all fermented alcoholic drinks",
            "High-purine legumes: Urad dal, whole masoor, horsegram (Kulattha)",
            "Sour curds, sharp cheeses, vinegar, excessive pickles, and deep-fried foods"
        ],
        "pathya_vihara": [
            "Elevating affected foot during acute painful episodes",
            "Wearing open, soft-soled, non-constricting footwear",
            "Remaining in cool, well-ventilated rooms"
        ],
        "apathya_vihara": [
            "Hot baths, saunas, direct sun exposure (exacerbates Rakta Pitta)",
            "Vigorous deep-tissue massage on swollen hot joints",
            "Daytime sleeping followed by late night eating"
        ],
        "yoga_pranayama": [
            "Gentle seated ankle and toe flexing (Sukshma Vyayama) after acute flare clears",
            "Shitali and Shitkari Pranayama (15 minutes to cool down body temperature and blood heat)",
            "Chandra Bhedana Pranayama (Calms metabolic Pitta)",
            "Viparita Karani (Legs-up-the-wall pose to drain dependent inflammatory edema)"
        ]
    },

    "grahani": {
        "name": "Irritable Bowel Syndrome (IBS) / Malabsorption Syndrome",
        "sanskrit_name": "Grahani Roga (ग्रहणी रोग)",
        "primary_dosha": "Vata & Pitta",
        "doshic_subtype": "Agni Mandya with Samana Vayu & Pachaka Pitta impairment",
        "cardinal_symptoms": [
            "malabsorption_mucus_stools",
            "bloating_flatulence",
            "loose_stools_diarrhea",
            "constipation_hard_stools",
            "loss_of_taste_aruchi"
        ],
        "requires_ama": True,
        "dhatu": ["Rasa Dhatu", "Mamsa Dhatu", "Asthi Dhatu"],
        "srotas": ["Annavaha Srotas", "Purishavaha Srotas", "Rasavaha Srotas"],
        "prognosis": "Krichhra Sadhya (Curable with Difficulty / Strict Dietetic Management)",
        "classical_source": "Charaka Samhita Chikitsasthana 15 & Madhava Nidana 4",
        "citations": [
            "Charaka Samhita, Chikitsasthana 15/56 (Muhurbaddham Muhurdravam...)",
            "Madhava Nidana, Grahani Rogadhikara 4",
            "Bhaishajya Ratnavali, Grahani Rogadhikara"
        ],
        "nidana": [
            "Abhojana & Atibhojana (Fasting followed by binge eating or irregular meal intervals)",
            "Vishamashana (Eating without hunger or during emotional distress)",
            "Guru-Sheeta-Ati-Ruksha Ahara (Heavy, cold, dry, ultra-processed foods)",
            "Vega Vidharana (Suppression of natural bowel urges)",
            "Chronic mental stress, anxiety, and grief (Manovaha Srotas connection)"
        ],
        "purvarupa": [
            "Praseka (Excessive watery salivation in mouth)",
            "Aruchi (Lack of relish for food)",
            "Vidaha (Delayed digestion with sour burning in stomach)",
            "Gaurava and Alasya (Heaviness in abdomen and malaise)"
        ],
        "upashaya_anupashaya": {
            "Upashaya (Alleviating)": [
                "Takra Sevana (Fresh churned buttermilk spiced with roasted cumin, rock salt, and ginger)",
                "Warm freshly prepared digestive soups (Mudga Yusha)",
                "Deepana-Pachana spices like Bilva, Maricha, Pippali, Shunthi"
            ],
            "Anupashaya (Aggravating)": [
                "Raw salads, cold raw fruits, iced water, and smoothies",
                "Full-fat whole milk, heavy sweets, greasy gravies, and bakery products",
                "Eating when anxious, stressed, or rushed"
            ]
        },
        "samprapti": {
            "Sanchaya": "Suppressed Jatharagni fails to digest even light wholesome food.",
            "Prakopa": "Formation of acidic, toxic intermediate (Ama) in the duodenum (Grahani).",
            "Prasara": "Ama mixes with Doshas and impairs the holding power (Dharana Shakti) of Grahani organ.",
            "Sthana Samshraya": "Weakness of Annavaha Srotas lining; transit time becomes erratic.",
            "Vyakti": "Alternating bouts of loose watery stools and hard constipated pellets (Muhur Baddham Muhur Dravam), abdominal colic, mucus discharge.",
            "Bheda": "Systemic wasting (Dhatukshaya), anemia (Pandu), and chronic fatigue."
        },
        "deepana_pachana": [
            "Takra Kalpa: Drinking 1 glass of fresh sweet buttermilk churned with roasted Jeera, Hing, and rock salt after meals",
            "Chitrakadi Vati: 2 tablets twice daily 10 minutes before meals"
        ],
        "shamana_formulations": [
            {
                "name": "Kutajarishta",
                "category": "Asava / Arishta",
                "classical_indication": "Classical fermented preparation for intestinal inflammation, loose stools, and mucosal healing.",
                "dosage": "20 ml diluted with 20 ml water twice daily",
                "anupana_vehicle": "Equal quantity of water",
                "aushadha_sevana_kala": "Pashchadbhakta (Immediately after meals)",
                "duration_weeks": 8,
                "classical_reference": "Bhaishajya Ratnavali, Atisara-Grahani Chikitsa"
            },
            {
                "name": "Bilvadi Lehyam / Churna",
                "category": "Avaleha / Churna",
                "classical_indication": "Astringent digestive tonic that binds loose stools and restores normal intestinal transit.",
                "dosage": "1 teaspoon (5g) twice daily",
                "anupana_vehicle": "Warm water or buttermilk",
                "aushadha_sevana_kala": "Pragbhakta (Before meals)",
                "duration_weeks": 6,
                "classical_reference": "Sahasrayogam, Leha Prakarana"
            },
            {
                "name": "Dadimashtaka Churna",
                "category": "Churna",
                "classical_indication": "Pomegranate-based carminative powder for Agni kindling, gas, and bowel colic.",
                "dosage": "3g twice daily",
                "anupana_vehicle": "Warm water or Takra",
                "aushadha_sevana_kala": "Madhyabhakta (With middle mouthful of food)",
                "duration_weeks": 6,
                "classical_reference": "Sharngadhara Samhita, Madhyama Khanda 6/87-91"
            }
        ],
        "panchakarma": {
            "eligible": False,
            "recommended_therapy": "Shodhana Deferred / Takra Kalpa & Pichha Basti Priority",
            "reasoning": "Radical purification (Vamana/Virechana) is contraindicated in acute Grahani due to severely compromised digestive fire (Mandagni). Mild Deepana followed by healing Piccha Basti is preferred.",
            "purvakarma": [
                "Exclusive Takra Kalpa (Buttermilk diet) for 7-14 days",
                "Warm compress over abdomen with hot water bottle"
            ],
            "pradhanakarma": "Piccha Basti (medicated milk/mucilage enema with Mocharasa) if mucosal irritation is persistent.",
            "paschatkarma": [
                "Gradual reintroduction of soft boiled red rice with moong soup"
            ]
        },
        "pathya_ahara": [
            "Takra (Freshly churned non-fat buttermilk) with roasted cumin and dry ginger",
            "Bilva fruit pulp, Dadima (fresh sweet pomegranates)",
            "Aged red rice (Shali), roasted barley flour, cooked moong dal",
            "Cooked bottle gourd, ridge gourd, carrots, and boiled sweet potatoes in moderation"
        ],
        "apathya_ahara": [
            "All raw salads, uncooked leafy greens, raw vegetables",
            "Fresh cold cow's milk, ice cream, cheese, paneer, and commercial yoghurt",
            "Deep-fried items, hot chili curries, garlic in excess, and alcohol",
            "Artificial sweeteners, chewing gums, and fizzy carbonated sodas"
        ],
        "pathya_vihara": [
            "Eating in a peaceful, quiet environment without phones or multitasking",
            "Allowing at least 4-5 hours between meals for complete digestion",
            "Gentle walking for 100 paces (Shatapadi) after lunch and dinner"
        ],
        "apathya_vihara": [
            "Eating while stressed, rushing out the door, or driving",
            "Day sleeping immediately after eating (Divasvapna)",
            "Staying awake late into the night (vitiates Vata and digestive fire)"
        ],
        "yoga_pranayama": [
            "Vajrasana (10 minutes immediately after meals - essential for digestive Agni)",
            "Pavanamuktasana (Gently releases trapped abdominal gas)",
            "Agnisara Kriya (Daily on empty stomach to tone visceral smooth muscle)",
            "Nadi Shodhana Pranayama (To soothe gut-brain axis autonomic dysregulation)"
        ]
    },

    "tamaka_shwasa": {
        "name": "Bronchial Asthma / Asthmatic Bronchitis",
        "sanskrit_name": "Tamaka Shwasa (तमक श्वास)",
        "primary_dosha": "Vata & Kapha",
        "doshic_subtype": "Prana Vayu obstructed by morbid Kapha in Pranavaha Srotas",
        "cardinal_symptoms": [
            "wheezing_shortness_of_breath",
            "cough_chronic",
            "excess_mucus_congestion",
            "anxiety_restlessness"
        ],
        "requires_ama": False,
        "dhatu": ["Rasa Dhatu", "Prana"],
        "srotas": ["Pranavaha Srotas", "Annavaha Srotas", "Udakavaha Srotas"],
        "prognosis": "Yapya (Manageable / Chronic Respiratory Care)",
        "classical_source": "Charaka Samhita Chikitsasthana 17 & Madhava Nidana 12",
        "citations": [
            "Charaka Samhita, Chikitsasthana 17/55-62 (Pratilomam yada vayuh...)",
            "Madhava Nidana, Shwasa Rogadhikara 12",
            "Sushruta Samhita, Uttaratantra 51"
        ],
        "nidana": [
            "Raja-Dhooma-Vata Sevana (Exposure to dust, smoke, smog, pollen, and cold wind)",
            "Sheeta Ahara & Sheeta Vari (Consumption of cold refrigerated foods, ice creams, cold drinks)",
            "Kaphakara Ahara (Excessive curd, black gram, heavy oily sweets, and bananas)",
            "Dwishta Gandha (Inhalation of strong pungent odors, perfumes, or chemical paint fumes)",
            "Climatic changes: Cloudy, rainy, damp, and unseasonal cold weather (Megha-Ambu-Sheeta)"
        ],
        "purvarupa": [
            "Aanaha (Fullness and distention in chest and flank)",
            "Parshwashoola (Pricking pain in thoracic ribs during inhalation)",
            "Vaktra Vairasya (Abnormal taste in mouth)",
            "Prana Vilomata (Abnormal upward sensation of air in throat)"
        ],
        "upashaya_anupashaya": {
            "Upashaya (Alleviating)": [
                "Ushna Upachara (Warm steam inhalation, hot water sipping, warm chest compress)",
                "Sitting upright with head propped up (Aasino labhate saukhyam)",
                "Ushna and Katu herbs like Maricha, Pippali, Shunthi, and Vasa"
            ],
            "Anupashaya (Aggravating)": [
                "Lying down flat in supine position (Shayanasya cha shwasa bhrisham bhavati)",
                "Cold showers, swimming in cold water, and air conditioning",
                "Cloudy, rainy weather and exposure to dust/pets"
            ]
        },
        "samprapti": {
            "Sanchaya": "Accumulation of Kapha in Amashaya and chest due to heavy cold food habits.",
            "Prakopa": "Provoked Kapha obstructs the bronchial airways (Pranavaha Srotas).",
            "Prasara": "Vitiated Prana Vayu reverses its natural downward course (Pratiloma Gati).",
            "Sthana Samshraya": "Entrapment of upward Vayu in the bronchopulmonary tree by sticky phlegm.",
            "Vyakti": "Audible wheezing (Ghurghuruka), dyspnea, paroxysmal cough, relief only after sputum is expectorated.",
            "Bheda": "Santataka / Pratamaka Shwasa with blackouts, nocturnal panic, and respiratory exhaustion."
        },
        "deepana_pachana": [
            "Sipping hot water boiled with dry ginger and basil leaves (Tulsi-Shunthi Jala)",
            "Trikatu Churna 1g with honey twice daily to liquefy sticky bronchial Kapha"
        ],
        "shamana_formulations": [
            {
                "name": "Kanakasava",
                "category": "Asava / Arishta",
                "classical_indication": "Classical bronchodilator asava; quickly relieves bronchial spasm and wheezing.",
                "dosage": "15-20 ml with equal warm water twice daily",
                "anupana_vehicle": "Equal quantity of warm water",
                "aushadha_sevana_kala": "Pashchadbhakta (After food)",
                "duration_weeks": 8,
                "classical_reference": "Bhaishajya Ratnavali, Shwasa Rogadhikara"
            },
            {
                "name": "Swasakasachintamani Rasa",
                "category": "Herbomineral (Gold Formulation)",
                "classical_indication": "Potent classical formulation for acute asthmatic dyspnea and lung tissue strength.",
                "dosage": "1 tablet (125mg) twice daily",
                "anupana_vehicle": "Honey and ginger juice",
                "aushadha_sevana_kala": "Madhyabhakta (Mid-meals)",
                "duration_weeks": 4,
                "classical_reference": "Bhaishajya Ratnavali, Shwasachikitsa"
            },
            {
                "name": "Agastya Haritaki Rasayana",
                "category": "Avaleha / Rasayana",
                "classical_indication": "Long-term respiratory rejuvenator; prevents recurrence of seasonal bronchitis and asthma attacks.",
                "dosage": "1 teaspoon (10g) twice daily",
                "anupana_vehicle": "Warm water or warm goat/cow milk",
                "aushadha_sevana_kala": "Pragbhakta (Early morning & bedtime)",
                "duration_weeks": 12,
                "classical_reference": "Charaka Samhita, Chikitsasthana 17/57-61"
            }
        ],
        "panchakarma": {
            "eligible": True,
            "recommended_therapy": "Sadhya Vamana or Mridu Virechana with Castor Oil",
            "reasoning": "Charaka recommends: 'In Tamaka Shwasa, Kapha is the obstructing culprit; expelling Kapha through gentle Vamana or clearing downward path with Virechana gives immediate relief'.",
            "purvakarma": [
                "Gentle chest Abhyanga with warm Til oil mixed with Saindhava (rock salt)",
                "Nadi Sweda (Herbal steam) over chest and back to liquefy sticky bronchial mucus"
            ],
            "pradhanakarma": "Mridu Vamana with Yashtimadhu Phanta or Virechana with Eranda Taila in ginger decoction.",
            "paschatkarma": [
                "Dhoomapana (Herbal therapeutic smoking with Haridra and Ghee)",
                "Warm light diet (Yavagu with Pippali)"
            ]
        },
        "pathya_ahara": [
            "Warm freshly cooked light food with dry ginger, black pepper, and garlic",
            "Aged barley (Yava), aged rice (Purana Shali), Kulattha (horsegram) soup",
            "Vegetables: Drumsticks, patola, bitter gourd, radishes (cooked), garlic",
            "Hot herbal teas: Tulsi, ginger, cinnamon, clove, licorice (Yashtimadhu)"
        ],
        "apathya_ahara": [
            "Cold drinks, iced water, ice cream, refrigerated food items",
            "Heavy dairy: Curd, cheese, cold milk, heavy milk puddings, bananas",
            "Oily deep-fried foods, bakery items, black gram (Urad), and mustard oil",
            "Fish, seafood, and heavy pork/beef meats"
        ],
        "pathya_vihara": [
            "Keeping chest, throat, and head warmly covered in chilly or windy weather",
            "Sleeping with head elevated on 2 pillows during symptomatic nights",
            "Staying in clean, sunny, dust-free, well-ventilated rooms"
        ],
        "apathya_vihara": [
            "Exposure to direct fans, AC drafts, damp basements, or smoggy streets",
            "Daytime naps (Divasvapna - causes instantaneous Kapha accumulation in chest)",
            "Vigorous strenuous exercise during humid or pollen-heavy mornings"
        ],
        "yoga_pranayama": [
            "Matsyasana (Fish pose - expands chest and lung alveolar volume)",
            "Bhujangasana and Ushtrasana (Open thoracic cage and broncho-tracheal tree)",
            "Nadi Shodhana Pranayama (Alternate nostril breathing - 15 minutes slow and deep)",
            "Bhastrika & Kapalabhati (Gentle practice only when NOT in acute bronchospasm)"
        ]
    },

    "kasa": {
        "name": "Chronic Bronchitis / Chronic Cough",
        "sanskrit_name": "Kasa Roga (कास रोग)",
        "primary_dosha": "Kapha & Vata",
        "doshic_subtype": "Udana-Prana Vayu with Kaphaja obstruction in Uras",
        "cardinal_symptoms": [
            "cough_chronic",
            "excess_mucus_congestion",
            "heaviness_body_limbs",
            "loss_of_taste_aruchi"
        ],
        "requires_ama": False,
        "dhatu": ["Rasa Dhatu", "Mamsa Dhatu"],
        "srotas": ["Pranavaha Srotas", "Rasavaha Srotas"],
        "prognosis": "Sukha Sadhya (Easily Curable if Acute / Krichhra if Chronic)",
        "classical_source": "Charaka Samhita Chikitsasthana 18 & Madhava Nidana 11",
        "citations": [
            "Charaka Samhita, Chikitsasthana 18/9-15",
            "Madhava Nidana, Kasa Rogadhikara 11",
            "Sushruta Samhita, Uttaratantra 52"
        ],
        "nidana": [
            "Dhooma-Rajo Sevana (Inhalation of smoke, dust, industrial pollutants)",
            "Vyayama during hunger or cold weather",
            "Ruksha-Sheeta Ahara (Dry cold crackers, cold refrigerated food)",
            "Vega Vidharana of coughing and sneezing"
        ],
        "purvarupa": [
            "Kanthakanduti (Tickling sensation in throat and pharynx)",
            "Bhojane Aruchi (Slight loss of taste)",
            "Galashundika irritation (scratchy throat)"
        ],
        "upashaya_anupashaya": {
            "Upashaya (Alleviating)": [
                "Warm herbal decoctions with honey (Kantakari, Vasa, Pippali)",
                "Warm water steam with eucalyptus or camphor",
                "Warm soothing soups with black pepper and ginger"
            ],
            "Anupashaya (Aggravating)": [
                "Cold drinks, ice creams, citrus fruits at night",
                "Dust, chemical sprays, cold AC air drafts"
            ]
        },
        "samprapti": {
            "Sanchaya": "Accumulation of phlegm in chest due to cold intake.",
            "Prakopa": "Udana Vayu is obstructed by Kapha in the throat and lungs.",
            "Prasara": "Upward propulsion of trapped air striking the vocal tract and pharynx.",
            "Sthana Samshraya": "Irritation and localization in Pranavaha Srotas lining.",
            "Vyakti": "Explosive hacking sound like broken bell (Bhanna-Kamsyavat Swana), expectoration or dry cough.",
            "Bheda": "Vataja, Pittaja, Kaphaja, Kshataja, and Kshayaja Kasa."
        },
        "deepana_pachana": [
            "Sitopaladi Churna with honey and ghee in unequal proportions",
            "Trikatu Churna with warm water"
        ],
        "shamana_formulations": [
            {
                "name": "Sitopaladi Churna",
                "category": "Churna",
                "classical_indication": "Classical supreme remedy for all forms of cough, bronchitis, and respiratory debility.",
                "dosage": "3g thrice daily",
                "anupana_vehicle": "Honey and pure cow's ghee (unequal quantity)",
                "aushadha_sevana_kala": "Muhur-muhuh (Frequent small licks throughout the day)",
                "duration_weeks": 4,
                "classical_reference": "Sharngadhara Samhita, Madhyama Khanda 6/134-137"
            },
            {
                "name": "Vasavaleha",
                "category": "Avaleha",
                "classical_indication": "Potent mucolytic and anti-tussive; liquefies stubborn phlegm and heals bronchial mucosa.",
                "dosage": "1 teaspoon (10g) twice daily",
                "anupana_vehicle": "Warm water or warm milk",
                "aushadha_sevana_kala": "Pragbhakta (Before food)",
                "duration_weeks": 6,
                "classical_reference": "Bhaishajya Ratnavali, Kasachikitsa"
            },
            {
                "name": "Kantakaryavaleha",
                "category": "Avaleha",
                "classical_indication": "Specific classical herbal jam for persistent allergic cough and throat tickle.",
                "dosage": "1 teaspoon (5-10g) twice daily",
                "anupana_vehicle": "Warm water",
                "aushadha_sevana_kala": "Pashchadbhakta (After meals)",
                "duration_weeks": 4,
                "classical_reference": "Charaka Samhita, Chikitsasthana 18/52-56"
            }
        ],
        "panchakarma": {
            "eligible": False,
            "recommended_therapy": "Dhoomapana & Kavala (Gargling) - Shodhana not indicated for uncomplicated Kasa",
            "reasoning": "Uncomplicated Kasa is successfully managed through oral Shamana, herbal inhalation (Dhooma), and gargling.",
            "purvakarma": ["Local warm fomentation on neck and upper chest"],
            "pradhanakarma": "Dhoomapana with Haridra and ghee; Kavala (warm saline and turmeric water gargle).",
            "paschatkarma": ["Avoid speaking loudly or cold winds"]
        },
        "pathya_ahara": [
            "Warm barley soups, aged wheat bread, moong dal soup with black pepper",
            "Warm goat's or cow's milk with a pinch of turmeric and dry ginger",
            "Garlic, onions, ginger, tulsi, and pomegranates"
        ],
        "apathya_ahara": [
            "Cold drinks, chilled water, ice creams, refrigerated leftovers",
            "Sour curd, bananas, heavy creamy sweets, deep-fried snacks",
            "Dry roasted pulses without fat (aggravates Vata cough)"
        ],
        "pathya_vihara": [
            "Covering throat with warm scarf when going outside",
            "Drinking warm water throughout the day",
            "Resting vocal cords"
        ],
        "apathya_vihara": [
            "Shouting, loud public speaking, or singing with irritated throat",
            "Sleeping under direct fan or AC blowing on face",
            "Daytime naps"
        ],
        "yoga_pranayama": [
            "Ujjayi Pranayama (Ocean breath - soothes tracheal inflammation)",
            "Simhasana (Lion pose - tones vocal cords and clears pharyngeal congestion)",
            "Surya Bhedana (Gentle heat generating breathing)"
        ]
    },

    "kushtha": {
        "name": "Chronic Dermatitis / Psoriasis / Eczema",
        "sanskrit_name": "Kushtha / Twak Roga (कुष्ठ / त्वग्दोष)",
        "primary_dosha": "Tridoshaja (Pitta-Kapha Pradhana)",
        "doshic_subtype": "Tridoshas localized in Sapta Dhatu (Twak, Rakta, Mamsa, Lasika)",
        "cardinal_symptoms": [
            "skin_rashes_inflammation_acne",
            "burning_sensation",
            "dryness_skin_hair",
            "dull_pain_swelling_edema"
        ],
        "requires_ama": False,
        "dhatu": ["Twak (Skin)", "Rakta Dhatu", "Mamsa Dhatu", "Lasika (Lymph)"],
        "srotas": ["Raktavaha Srotas", "Svedavaha Srotas", "Rasavaha Srotas"],
        "prognosis": "Krichhra Sadhya (Curable with Great Difficulty / Long-term Management)",
        "classical_source": "Charaka Samhita Chikitsasthana 7 & Sushruta Nidana 5",
        "citations": [
            "Charaka Samhita, Chikitsasthana 7/9-10 (Sapta Dravyani...)",
            "Sushruta Samhita, Nidanasthana 5",
            "Ashtanga Hridaya, Chikitsasthana 19"
        ],
        "nidana": [
            "Viruddha Ahara (Food incompatibilities: Fish with milk, melons with dairy)",
            "Sheetoshna Vyatyasa (Sudden cold water bath immediately after hot sun exposure)",
            "Vega Vidharana (Suppression of natural vomiting reflex)",
            "Ati Snigdha-Guru-Amla-Lavana Ahara (Excessive heavy greasy sour salty foods)",
            "Papashila & Manasika Hetu (Chronic guilt, psychological stress, suppressed anger)"
        ],
        "purvarupa": [
            "Sparsha Ajnana (Numbness or reduced tactile sensation on skin patches)",
            "Atisveda or Asvedana (Excessive sweating or localized inability to sweat)",
            "Kandu (Unbearable itching, prickling sensation)",
            "Vaivarnya (Erythematous or hyperpigmented skin discoloration)"
        ],
        "upashaya_anupashaya": {
            "Upashaya (Alleviating)": [
                "Tikta & Kashaya herbal washes (Neem, Khadira, Triphala decoctions)",
                "Purifying medicated ghee (Maha Tiktaka Ghrita)",
                "Cooling blood purifiers like Sariva, Manjishta, Chandana"
            ],
            "Anupashaya (Aggravating)": [
                "Fermented batters, sour curd, vinegar, tamarind, tomatoes",
                "Harsh chemical soaps, synthetic clothing, direct sun exposure",
                "Scratching and hot water showers"
            ]
        },
        "samprapti": {
            "Sanchaya": "Tridosha accumulation from incompatible diet and lifestyle.",
            "Prakopa": "Provoked Doshas simultaneously vitiate the 4 essential tissue substrates (Dushyas): Twak, Rakta, Mamsa, Lasika.",
            "Prasara": "Circulation of virulent toxins through Raktavaha and Svedavaha Srotas.",
            "Sthana Samshraya": "Localization in epidermis and dermis with occlusion of sweat ducts.",
            "Vyakti": "Silvery plaques, weeping lesions, burning erythematous rash, chronic scaling.",
            "Bheda": "7 Maha Kushthas and 11 Kshudra Kushthas (Kitibha/Psoriasis, Vicharchika/Eczema)."
        },
        "deepana_pachana": [
            "Khadiraradi Kashaya with honey or warm water",
            "Nimbadi Churna 2g with warm water before meals"
        ],
        "shamana_formulations": [
            {
                "name": "Maha Tiktaka Ghrita",
                "category": "Ghrita",
                "classical_indication": "Sovereign classical formulation for deep chronic skin diseases, psoriasis, and blood purification.",
                "dosage": "10-15 ml on empty stomach with warm water",
                "anupana_vehicle": "Luke-warm water",
                "aushadha_sevana_kala": "Pragbhakta (Early morning empty stomach)",
                "duration_weeks": 12,
                "classical_reference": "Ashtanga Hridaya, Chikitsasthana 19/8-17"
            },
            {
                "name": "Khadirarishta",
                "category": "Asava / Arishta",
                "classical_indication": "Khadira is the supreme herb (Agrya Aushadha) for skin; purifies blood and stops chronic weeping lesions.",
                "dosage": "20 ml with 20 ml water twice daily",
                "anupana_vehicle": "Equal quantity of water",
                "aushadha_sevana_kala": "Pashchadbhakta (After meals)",
                "duration_weeks": 12,
                "classical_reference": "Sharngadhara Samhita, Madhyama Khanda 10/60-65"
            },
            {
                "name": "Gandhaka Rasayana",
                "category": "Rasayana / Mineral",
                "classical_indication": "Purified sulphur preparation for severe itching, microbial skin infections, and cell turnover.",
                "dosage": "2 tablets (500mg) twice daily",
                "anupana_vehicle": "Warm milk or water with honey",
                "aushadha_sevana_kala": "Madhyabhakta (Mid-meals)",
                "duration_weeks": 8,
                "classical_reference": "Yoga Ratnakara, Rasayana Adhyaya"
            }
        ],
        "panchakarma": {
            "eligible": True,
            "recommended_therapy": "Vamana followed by Virechana (Repeated Mild Shodhana - Muhur Muhur Shodhana)",
            "reasoning": "Charaka rules: 'In chronic Kushtha, Doshas are deeply rooted; patient must undergo repeated mild purification (Virechana/Vamana) rather than a single violent detox'.",
            "purvakarma": [
                "Internal Snehapana with Maha Tiktaka Ghrita in increasing doses",
                "Herbal bath with Khadira and Nimba decoction"
            ],
            "pradhanakarma": "Virechana with Trivrit Lehyam (25g) followed by Siravyadha / Leech therapy if localized.",
            "paschatkarma": [
                "Strict non-salted, non-sour diet (Amlavarjita Ahara) for 7 days"
            ]
        },
        "pathya_ahara": [
            "Old barley (Purana Yava), aged wheat, Mudga (green gram) soup",
            "Vegetables: Patola (pointed gourd), Karavellaka (bitter gourd), Nimba leaves, Moringa",
            "Ghee prepared with bitter herbs (Tikta Ghrita)",
            "Pomegranate, amla, triphala water"
        ],
        "apathya_ahara": [
            "Total avoidance of fish with milk, sour curd, jaggery, and sesame seeds",
            "Fermented foods (Idli, Dosa, bread, cheese, vinegar, pickles)",
            "Excessive salt, pungent spices, red chillies, tomatoes, and eggplant",
            "Pork, heavy fatty meats, and alcohol"
        ],
        "pathya_vihara": [
            "Wearing loose, soft cotton clothing (avoid synthetic and tight friction)",
            "Washing skin with boiled neem water instead of chemical soaps",
            "Applying pure coconut oil or Shatadhauta Ghrita to moisturize dry plaques"
        ],
        "apathya_vihara": [
            "Scratching lesions with fingernails (leads to Koebner phenomenon and secondary infection)",
            "Hot showers and harsh chemical detergents",
            "Daytime sleeping (increases Kapha-Pitta toxicity)"
        ],
        "yoga_pranayama": [
            "Shitali and Shitkari Pranayama (Directly cools systemic Rakta heat)",
            "Anuloma Viloma (15 minutes to reduce sympathetic autoimmune stress)",
            "Surya Namaskara (Gentle, avoiding excessive friction and sweating)"
        ]
    },

    "kamala": {
        "name": "Jaundice / Hepatic Disorders & Hepatitis",
        "sanskrit_name": "Kamala / Yakrit Roga (कामला / यकृद्रोग)",
        "primary_dosha": "Pitta",
        "doshic_subtype": "Pitta Pradhana localized in Rakta-Mamsa and Kostha-Shakha",
        "cardinal_symptoms": [
            "yellowish_eyes_urine",
            "burning_sensation",
            "loss_of_taste_aruchi",
            "loose_stools_diarrhea"
        ],
        "requires_ama": False,
        "dhatu": ["Rakta Dhatu", "Mamsa Dhatu", "Rasa Dhatu"],
        "srotas": ["Raktavaha Srotas", "Annavaha Srotas", "Svedavaha Srotas"],
        "prognosis": "Sukha Sadhya (if Kosthashrita) / Krichhra (if Shakhashrita / Obstructive)",
        "classical_source": "Charaka Samhita Chikitsasthana 16 & Madhava Nidana 8",
        "citations": [
            "Charaka Samhita, Chikitsasthana 16/34-37 (Haridranana Netra Twak...)",
            "Madhava Nidana, Pandu-Kamala 8",
            "Bhaishajya Ratnavali, Pandu-Kamala Chikitsa"
        ],
        "nidana": [
            "Excessive consumption of sour, salty, hot, and pungent foods by a Pitta-dominant person",
            "Alcoholism, viral hepatitis infection, toxic drug ingestion",
            "Excessive anger, grief, direct exposure to blazing sun and fire"
        ],
        "purvarupa": [
            "Avipaka (Sluggish digestion and persistent nausea)",
            "Klama (Profound exhaustion without exertion)",
            "Aruchi (Repulsion toward oily food)",
            "Mild yellowness of sclera and dark concentrated urine"
        ],
        "upashaya_anupashaya": {
            "Upashaya (Alleviating)": [
                "Tikta and Madhura cooling herbs (Bhumyamalaki, Katuki, Punarnava)",
                "Sugarcane juice (Ikshu Rasa), sweet grape juice, amla juice",
                "Complete physical rest (Vishrama)"
            ],
            "Anupashaya (Aggravating)": [
                "Fried oily food, spices, alcohol, heavy meat gravies",
                "Physical exercise and sun exposure"
            ]
        },
        "samprapti": {
            "Sanchaya": "Fiery Pitta provoked in liver (Yakrit) and spleen (Pleeha).",
            "Prakopa": "Pitta burns and liquefies the blood tissue (Rakta Dhatu).",
            "Prasara": "Circulation of bile pigment throughout all body tissues.",
            "Sthana Samshraya": "Deposition in skin, eyes, mucous membranes, and nails.",
            "Vyakti": "Deep yellowish-orange eyes and skin (Haridra Netra Twak), dark turmeric urine, clay-colored stools in obstructive type.",
            "Bheda": "Kosthashrita (Hemolytic/Hepatocellular) vs Shakhashrita (Obstructive)."
        },
        "deepana_pachana": [
            "Bhumyamalaki Swarasa (Fresh phyllanthus niruri juice) 15ml empty stomach",
            "Phalatrikadi Kwatha 20ml with honey twice daily"
        ],
        "shamana_formulations": [
            {
                "name": "Arogyavardhini Vati",
                "category": "Herbomineral",
                "classical_indication": "Supreme classical liver tonic; contains Katuki which promotes healthy bile flow and regenerates hepatocytes.",
                "dosage": "2 tablets (500mg) twice daily",
                "anupana_vehicle": "Luke-warm water or Punarnava Kwatha",
                "aushadha_sevana_kala": "Madhyabhakta (Mid-meals)",
                "duration_weeks": 6,
                "classical_reference": "Rasa Ratna Samucchaya & Bhaishajya Ratnavali"
            },
            {
                "name": "Punarnavadi Mandura",
                "category": "Vati / Iron Formulation",
                "classical_indication": "Treats liver enlargement, jaundice, anemia (Pandu), and abdominal water retention.",
                "dosage": "2 tablets twice daily",
                "anupana_vehicle": "Takra (buttermilk) or warm water",
                "aushadha_sevana_kala": "Pragbhakta (Before meals)",
                "duration_weeks": 8,
                "classical_reference": "Charaka Samhita, Chikitsasthana 16/93-96"
            },
            {
                "name": "Bhumyamalaki Churna",
                "category": "Churna",
                "classical_indication": "Proven hepatoprotective and antiviral; normalizes elevated liver enzymes (SGOT/SGPT).",
                "dosage": "3g twice daily",
                "anupana_vehicle": "Honey or warm water",
                "aushadha_sevana_kala": "Pragbhakta (Early morning)",
                "duration_weeks": 8,
                "classical_reference": "Bhavaprakasha Nighantu, Guduchyadi Varga"
            }
        ],
        "panchakarma": {
            "eligible": True,
            "recommended_therapy": "Mridu Virechana (Gentle therapeutic purgation with Trivrit or Katuki)",
            "reasoning": "Charaka dictum: 'Kamalinaam tu nishpannam mrudubhih tikta shitaishcha shodhanaih' — Jaundice must be cleared with gentle, bitter, cooling purgatives.",
            "purvakarma": ["Snehana is done with medicated ghee (Kalyanaka Ghrita or Dadimadi Ghrita)"],
            "pradhanakarma": "Mridu Virechana with Trivrit Lehyam (15-20g) to purge excess bile.",
            "paschatkarma": ["Light diet of rice gruel (Manda/Peya) with pomegranate juice"]
        },
        "pathya_ahara": [
            "Sugarcane juice (fresh, hygienic), sweet pomegranates, black raisins",
            "Barley water, light red rice gruel, boiled green gram soup without oil",
            "Radish juice (Moolaka Swarasa), tender coconut water, amla juice"
        ],
        "apathya_ahara": [
            "Total avoidance of oil, ghee, butter, and all fried items during acute phase",
            "Hot spices: Green chillies, red chillies, mustard, garlic, excessive salt",
            "Alcohol, tobacco, tea, coffee, and packaged processed snacks",
            "Hard-to-digest meats, eggs, and heavy dairy products"
        ],
        "pathya_vihara": [
            "Strict bed rest (Vishrama) to facilitate hepatic metabolic regeneration",
            "Staying in cool, shaded, comfortable quarters"
        ],
        "apathya_vihara": [
            "Physical exertion, gym workouts, running, manual labor",
            "Direct sunlight, hot furnaces, daytime anger and sexual intercourse"
        ],
        "yoga_pranayama": [
            "Shitali Pranayama (Cooling breath to reduce liver heat)",
            "Shavasana (Deep restorative relaxation pose)",
            "No strenuous abdominal asanas during acute liver inflammation"
        ]
    },

    "arsha": {
        "name": "Hemorrhoids / Anorectal Disorders",
        "sanskrit_name": "Arsha (अर्शः)",
        "primary_dosha": "Vata & Pitta",
        "doshic_subtype": "Apana Vayu vitiation localized in Guda Valis (anal sphincters)",
        "cardinal_symptoms": [
            "anal_pain_bleeding_piles",
            "constipation_hard_stools",
            "bloating_flatulence",
            "burning_sensation"
        ],
        "requires_ama": False,
        "dhatu": ["Mamsa Dhatu", "Meda Dhatu", "Rakta Dhatu"],
        "srotas": ["Purishavaha Srotas", "Annavaha Srotas", "Raktavaha Srotas"],
        "prognosis": "Sukha Sadhya (if Fresh) / Krichhra (if Chronic or Secondary)",
        "classical_source": "Charaka Samhita Chikitsasthana 14 & Sushruta Chikitsasthana 6",
        "citations": [
            "Charaka Samhita, Chikitsasthana 14/9-15",
            "Sushruta Samhita, Chikitsasthana 6 (Arsho Chikitsa)",
            "Bhaishajya Ratnavali, Arsho Rogadhikara"
        ],
        "nidana": [
            "Vega Vidharana (Voluntary suppression of stool and flatus urges)",
            "Utkatukasana (Squatting for prolonged hours or sitting on hard seats)",
            "Pravahana (Severe habitual straining at stool due to chronic constipation)",
            "Mandagni (Poor digestive fire producing dry, compact, scybalous feces)"
        ],
        "purvarupa": [
            "Vishtambha (Persistent lower abdominal distension and sluggish bowels)",
            "Guda Kandu (Anal itching, prickling discomfort, or fullness)",
            "Katiprishta Daurbalya (Weakness and aching in lower back and sacrum)"
        ],
        "upashaya_anupashaya": {
            "Upashaya (Alleviating)": [
                "Avagaha Sweda (Warm sitz bath with Triphala decoction)",
                "Surana (Elephant foot yam) preparations cooked in ghee",
                "Gentle mild laxatives (Anulomana) like Haritaki and Abhayarishta"
            ],
            "Anupashaya (Aggravating)": [
                "Hard straining on toilet commode",
                "Spicy chillies, red pepper, dry astringent snacks, low-fiber fast food",
                "Prolonged sedentary sitting on unpadded chairs"
            ]
        },
        "samprapti": {
            "Sanchaya": "Dry compact stool accumulates in rectum from suppressed Agni and Vata.",
            "Prakopa": "Provoked Apana Vayu becomes sluggish and reverses upward pressure.",
            "Prasara": "Engorgement of the hemorrhoidal venous plexuses (Guda Dhamanis).",
            "Sthana Samshraya": "Deposition in the three anal sphincter folds (Samvarani, Visarjani, Pravahani).",
            "Vyakti": "Fleshy polypoid masses (Mamsa Ankurah), rectal bleeding, excruciating pain during defecation.",
            "Bheda": "Shushka (Dry Vataja) vs Sravi (Bleeding Pittaja-Raktaja)."
        },
        "deepana_pachana": [
            "Abhayarishta 20ml with warm water after meals",
            "Triphala Churna 3-5g at bedtime with warm water"
        ],
        "shamana_formulations": [
            {
                "name": "Arshakuthar Rasa",
                "category": "Herbomineral",
                "classical_indication": "Premier classical remedy for hemorrhoidal masses; shrinks piles and normalizes Apana Vayu.",
                "dosage": "1-2 tablets (250mg) twice daily",
                "anupana_vehicle": "Luke-warm water or buttermilk",
                "aushadha_sevana_kala": "Madhyabhakta (Mid-meals)",
                "duration_weeks": 6,
                "classical_reference": "Bhaishajya Ratnavali, Arsho Rogadhikara"
            },
            {
                "name": "Abhayarishta",
                "category": "Asava / Arishta",
                "classical_indication": "Supreme fermented digestive wine for chronic constipation, piles, and spleen disorders.",
                "dosage": "20 ml with equal warm water twice daily",
                "anupana_vehicle": "Equal quantity of water",
                "aushadha_sevana_kala": "Pashchadbhakta (Immediately after meals)",
                "duration_weeks": 8,
                "classical_reference": "Sharngadhara Samhita, Madhyama Khanda 10/18-27"
            },
            {
                "name": "Kasiadya Taila (Local Application)",
                "category": "Taila (External)",
                "classical_indication": "Medicated alkaline oil applied per rectum to dissolve and shrink painful piles.",
                "dosage": "Apply locally with cotton swab before and after bowel movement",
                "anupana_vehicle": "External application",
                "aushadha_sevana_kala": "External",
                "duration_weeks": 4,
                "classical_reference": "Bhaishajya Ratnavali, Arsho Rogadhikara"
            }
        ],
        "panchakarma": {
            "eligible": True,
            "recommended_therapy": "Avagaha Sweda (Medicated Warm Sitz Bath) & Ksharasootra (if high grade)",
            "reasoning": "Warm Triphala sitz bath relieves sphincter spasm. High grade prolapsed piles are definitively treated with Ksharasootra parasurgical ligation.",
            "purvakarma": ["Local warm fomentation (Swedana)"],
            "pradhanakarma": "Warm Avagaha Sweda for 15 minutes twice daily; Ksharasootra application if piles are Grade 3-4.",
            "paschatkarma": ["Soft high-fiber diet, Jatyadi Taila local application"]
        },
        "pathya_ahara": [
            "Surana (Elephant foot yam - proven classical specific for piles)",
            "Takra (Fresh churned buttermilk) with rock salt and roasted cumin",
            "High fiber foods: Papaya, soaked raisins, figs (Anjeer), green leafy vegetables",
            "Adequate hydration (2.5 - 3 liters warm water daily)"
        ],
        "apathya_ahara": [
            "Dry astringent legumes: Rajma, chana, dry peas (produces hard stony stool)",
            "Intensely hot red and green chillies, black pepper in excess, raw garlic",
            "Refined white flour (Maida), bakery items, burgers, pizzas",
            "Alcohol and carbonated caffeinated beverages"
        ],
        "pathya_vihara": [
            "Responding immediately to natural bowel urges without delay",
            "Using soft ergonomic seating cushions",
            "Daily brisk walking to stimulate peristaltic colonic contractions"
        ],
        "apathya_vihara": [
            "Sitting on toilet commode for prolonged periods with smartphones",
            "Straining aggressively to force bowel evacuation",
            "Riding horses, bicycles, or two-wheelers for long hours"
        ],
        "yoga_pranayama": [
            "Ashwini Mudra (Anal sphincter contraction and relaxation exercise - 30 times twice daily)",
            "Mula Bandha (Root lock to tone pelvic floor musculature)",
            "Malasana (Garland squat pose to open natural defecation angle)"
        ]
    },

    "sthaulya": {
        "name": "Obesity / Dyslipidemia / Medoroga",
        "sanskrit_name": "Sthaulya / Medoroga (स्थौल्य / मेदोरोग)",
        "primary_dosha": "Kapha",
        "doshic_subtype": "Kaphaja Medo Vriddhi with Jatharagni hyperactivity and Dhatwagni sluggishness",
        "cardinal_symptoms": [
            "weight_gain_slow_metabolism",
            "heaviness_body_limbs",
            "excessive_thirst_sweating",
            "intense_sharp_hunger"
        ],
        "requires_ama": False,
        "dhatu": ["Meda Dhatu", "Mamsa Dhatu", "Kleda"],
        "srotas": ["Medovaha Srotas", "Svedavaha Srotas", "Annavaha Srotas"],
        "prognosis": "Krichhra Sadhya (Curable with Difficulty / Lifelong Discipline)",
        "classical_source": "Charaka Samhita Sutrasthana 21 (Ashtaninditiya Adhyaya)",
        "citations": [
            "Charaka Samhita, Sutrasthana 21/4 (Medomamsa ati-vriddhatvat...)",
            "Ashtanga Hridaya, Sutrasthana 14",
            "Madhava Nidana, Medoroga 34"
        ],
        "nidana": [
            "Atisampoorana (Over-nutrition, excessive caloric intake beyond bodily expenditure)",
            "Guru-Madhura-Sheeta-Snigdha Ahara (Heavy, sweet, cold, oily, fried foods)",
            "Avyayama & Asyasaukhya (Total absence of physical exertion and sedentary lounging)",
            "Divasvapna (Day sleeping which instantly provokes Kapha and liquefies Medas)",
            "Beeja Svabhava (Genetic predisposition and sluggish metabolic constitution)"
        ],
        "purvarupa": [
            "Sweda-Abadhadha (Foul-smelling excessive perspiration with minimal effort)",
            "Alasya & Nidradhikya (Lethargy, daytime somnolence, aversion to movement)",
            "Shwasa Kashtata (Exertional dyspnea even when climbing one flight of stairs)"
        ],
        "upashaya_anupashaya": {
            "Upashaya (Alleviating)": [
                "Guru cha Atarpana Ahara (Foods that fill stomach without adding calories - Barley, millets)",
                "Udwarthana (Vigorous dry herbal powder massage with Triphala, Kolakulathadi)",
                "Ushna Madhudaka (Warm water with raw honey taken early morning)"
            ],
            "Anupashaya (Aggravating)": [
                "Sweet desserts, refined carbohydrates, ice cream, butter, cheese",
                "Sleeping immediately after meals and prolonged daytime naps",
                "Sitting unbroken for 8 hours without movement"
            ]
        },
        "samprapti": {
            "Sanchaya": "Vitiated Kapha and Medas obstruct the internal channels of circulation.",
            "Prakopa": "Because all nutrients are diverted exclusively to adipose tissue (Meda Dhatu), other Dhatus starve.",
            "Prasara": "Trapped Vata enters digestive fire (Koshtha), kindling an intense ravenous appetite (Tikshnagni).",
            "Sthana Samshraya": "Excessive accumulation of subcutaneous and visceral fat in abdomen, breasts, buttocks.",
            "Vyakti": "Flabby pendulous abdomen and buttocks, shortness of breath, excessive thirst and sweating.",
            "Bheda": "Atherosclerosis, hypertension, fatty liver, diabetes, osteoarthritis of knees."
        },
        "deepana_pachana": [
            "Warm water with 1 teaspoon raw honey and a pinch of black pepper at dawn",
            "Triphala Guggulu 2 tablets with warm water before meals"
        ],
        "shamana_formulations": [
            {
                "name": "Medohar Guggulu",
                "category": "Vati / Guggulu",
                "classical_indication": "Classical fat-scraping (Lekhaniya) formulation; lowers cholesterol, visceral fat, and weight.",
                "dosage": "2 tablets (500mg) thrice daily",
                "anupana_vehicle": "Warm water or honey water",
                "aushadha_sevana_kala": "Pragbhakta (30 minutes before meals)",
                "duration_weeks": 12,
                "classical_reference": "Bhaishajya Ratnavali, Medorogadhikara"
            },
            {
                "name": "Varunadi Kwatha",
                "category": "Kwatha",
                "classical_indication": "Potent Kapha-Medo reducing decoction; dissolves deep visceral and peritoneal fat.",
                "dosage": "20 ml with 40 ml warm water twice daily",
                "anupana_vehicle": "Warm water with a pinch of honey",
                "aushadha_sevana_kala": "Pragbhakta (Before meals)",
                "duration_weeks": 8,
                "classical_reference": "Ashtanga Hridaya, Chikitsasthana 14"
            },
            {
                "name": "Lekhaniya Gana Churna (Guggulu, Vacha, Musta, Haridra)",
                "category": "Churna",
                "classical_indication": "Charaka's 10 sovereign fat-scraping herbs that cleanse circulatory channels.",
                "dosage": "3g twice daily",
                "anupana_vehicle": "Luke-warm water with honey",
                "aushadha_sevana_kala": "Madhyabhakta (Mid-meals)",
                "duration_weeks": 12,
                "classical_reference": "Charaka Samhita, Sutrasthana 4/9"
            }
        ],
        "panchakarma": {
            "eligible": True,
            "recommended_therapy": "Udwarthana (Dry Herbal Friction Massage) & Lekhana Basti",
            "reasoning": "Udwarthana liquefies subcutaneous fat (Kapha Medo Vilayana) and tones skin. Lekhana Basti directly scrapes lipids from Pakwashaya.",
            "purvakarma": [
                "Daily vigorous Udwarthana with Kolakulathadi Churna for 14 days"
            ],
            "pradhanakarma": "Course of Lekhana Basti (containing Triphala, Gomutra, Kshara, and Honey) for 8 days.",
            "paschatkarma": [
                "Daily dynamic Surya Namaskara and light millet diet"
            ]
        },
        "pathya_ahara": [
            "Grains: Yava (Barley - whole grain, flour, chapati), Kodrava, Bajra, aged red rice",
            "Legumes: Kulattha (Horsegram soup - premier fat burner), Mudga (green gram)",
            "Vegetables: Bitter gourd, pointed gourd, cabbage, cucumber, radish, leafy greens",
            "Warm water only for drinking; hot ginger-lemon water between meals"
        ],
        "apathya_ahara": [
            "All refined sugars, candies, sweets, bakery cakes, and chocolates",
            "High-fat dairy: Full-cream milk, cheese, butter, paneer, sweet condensed milk",
            "Deep-fried samosas, chips, processed meats, and fast foods",
            "Sleeping immediately after drinking water or eating heavy meals"
        ],
        "pathya_vihara": [
            "Minimum 45-60 minutes of vigorous aerobic exercise or brisk walking daily",
            "Nighttime fasting (early light dinner by 7 PM)",
            "Remaining mentally active, awake, and alert throughout the daytime"
        ],
        "apathya_vihara": [
            "Day sleeping (Divasvapna - strongly contraindicated in Medoroga)",
            "Continuous prolonged sedentary sitting without standing breaks",
            "Over-sleeping beyond 7 hours"
        ],
        "yoga_pranayama": [
            "Surya Namaskara (Dynamic, 12-16 cycles daily)",
            "Kapalabhati Pranayama (15 minutes in rapid rounds of 60 to kindle visceral Agni)",
            "Bhastrika Pranayama (Bellows breath to burn metabolic sluggishness)",
            "Paschimottanasana and Dhanurasana (Intense abdominal stretch)"
        ]
    },

    "anidra_chittodvega": {
        "name": "Insomnia & Chronic Anxiety / Stress",
        "sanskrit_name": "Anidra / Chittodvega (अनिद्रा / चित्तोद्वेग)",
        "primary_dosha": "Vata & Pitta",
        "doshic_subtype": "Prana-Vyana Vayu & Sadhaka Pitta hyperactivity with Tarpaka Kapha Kshaya",
        "cardinal_symptoms": [
            "insomnia_disturbed_sleep",
            "anxiety_restlessness",
            "irritability_anger",
            "dryness_skin_hair"
        ],
        "requires_ama": False,
        "dhatu": ["Majja Dhatu", "Rasa Dhatu", "Ojas"],
        "srotas": ["Manovaha Srotas (Mental Channel)", "Majjavaha Srotas", "Pranavaha Srotas"],
        "prognosis": "Sukha Sadhya (Easily Curable with Shirodhara & Medhya Rasayanas)",
        "classical_source": "Charaka Samhita Sutrasthana 21 & Ashtanga Hridaya Sutrasthana 7",
        "citations": [
            "Charaka Samhita, Sutrasthana 21/35-39 (Nidrayattam sukham dukham...)",
            "Ashtanga Hridaya, Sutrasthana 7/53-65",
            "Bhavaprakasha, Purva Khanda"
        ],
        "nidana": [
            "Chinta, Shoka, Bhaya, Krodha (Chronic overthinking, grief, fear, workplace anxiety)",
            "Ratri Jagarana (Late-night screen viewing, blue light exposure, nocturnal shift work)",
            "Ati Vyayama & Ati Langhana (Excessive strenuous gym workouts or fasting depleting Ojas)",
            "Excessive consumption of coffee, black tea, energy drinks, and stimulant drugs"
        ],
        "purvarupa": [
            "Jrimbha (Excessive yawning without sleep fulfillment)",
            "Shirashoola (Tension headaches and ocular strain)",
            "Gaurava of head with racing thoughts at night"
        ],
        "upashaya_anupashaya": {
            "Upashaya (Alleviating)": [
                "Shirodhara with warm Ksheerabala Taila or medicated buttermilk (Takradhara)",
                "Pada-Abhyanga (Warm sesame oil foot massage before bedtime)",
                "Warm cow's milk with a pinch of nutmeg (Jatiphala) and Ashwagandha"
            ],
            "Anupashaya (Aggravating)": [
                "Late night smartphone screen exposure, intense movies, loud music",
                "Caffeine after 2 PM, fasting at night, cold windy bedrooms",
                "Engaging in heated arguments or financial worries at bedtime"
            ]
        },
        "samprapti": {
            "Sanchaya": "Vata provoked in Manovaha Srotas due to mental over-exertion.",
            "Prakopa": "Raja and Tama mental doshas obscure Sattva; Prana Vayu becomes hyperactive.",
            "Prasara": "Depletion of Tarpaka Kapha (cerebral lubricant) and Ojas.",
            "Sthana Samshraya": "Dislodgement of consciousness from Hridaya (cardiac-neurological seat).",
            "Vyakti": "Inability to fall asleep, nocturnal panic awakenings, racing heart, restless leg syndrome.",
            "Bheda": "Chronic depressive exhaustion, cognitive brain fog, memory impairment."
        },
        "deepana_pachana": [
            "Warm milk boiled with 1 pinch of Nutmeg (Jatiphala) 30 mins before sleep",
            "Brahmi Churna 2g with warm water in the morning"
        ],
        "shamana_formulations": [
            {
                "name": "Brahmi Vati (Swarna Yukta / Plain)",
                "category": "Vati / Medhya Rasayana",
                "classical_indication": "Premier classical neuro-calmative; tranqualizes hyperactive nervous system and promotes deep REM sleep.",
                "dosage": "1-2 tablets twice daily",
                "anupana_vehicle": "Warm milk or water with honey",
                "aushadha_sevana_kala": "Nishi (At bedtime and after breakfast)",
                "duration_weeks": 8,
                "classical_reference": "Bhaishajya Ratnavali, Manasaroga Chikitsa"
            },
            {
                "name": "Ashwagandha Churna / Capsules",
                "category": "Churna / Rasayana",
                "classical_indication": "Supreme adaptogen; replenishes Majja Dhatu, lowers cortisol, and stabilizes Vata.",
                "dosage": "3g powder or 1 capsule twice daily",
                "anupana_vehicle": "Warm cow's milk with a pinch of cardamom",
                "aushadha_sevana_kala": "Nishi (Before bedtime)",
                "duration_weeks": 12,
                "classical_reference": "Charaka Samhita, Chikitsasthana 1/1"
            },
            {
                "name": "Saraswatarishta",
                "category": "Asava / Arishta",
                "classical_indication": "Famous Ayurvedic brain tonic for memory, cognitive clarity, emotional resilience, and anxiety.",
                "dosage": "15-20 ml with equal water twice daily",
                "anupana_vehicle": "Equal quantity of water",
                "aushadha_sevana_kala": "Pashchadbhakta (After meals)",
                "duration_weeks": 8,
                "classical_reference": "Bhaishajya Ratnavali, Rasayana Rogadhikara"
            }
        ],
        "panchakarma": {
            "eligible": True,
            "recommended_therapy": "Shirodhara with Ksheerabala Taila & Nasya with Ksheerabala 101",
            "reasoning": "Shirodhara stimulates the Ajna Chakra and frontal cortex, triggering deep parasympathetic activation. Nasya directly nourishes Shringataka Marma (brain sensory center).",
            "purvakarma": [
                "Shiroabhyanga (gentle head massage with Brahmi Taila)",
                "Pada-Abhyanga (foot massage with Ksheerabala Taila)"
            ],
            "pradhanakarma": "Shirodhara (continuous rhythmic pouring of warm medicated oil across forehead for 45 minutes for 7 days).",
            "paschatkarma": [
                "Resting in quiet, dim room; warm head wash with soapnut/herbal powder"
            ]
        },
        "pathya_ahara": [
            "Warm sweet cow's milk with ghee, cardamom, and saffron at night",
            "Almonds (soaked and peeled), walnuts, pumpkin seeds, dates",
            "Wholesome grains: Aged wheat, basmati rice, moong dal with pure cow's ghee",
            "Sweet ripe fruits: Mangoes, grapes, sweet apples, bananas"
        ],
        "apathya_ahara": [
            "Caffeine: Black coffee, espresso, green tea, dark chocolate after 2 PM",
            "Energy drinks, alcoholic binge drinking (causes fragmented rebound wakefulness)",
            "Dry cold snacks, excessive bitter pungent spices, raw salads at dinner",
            "Fasting or skipping dinner (Vata rises sharply on empty nocturnal stomach)"
        ],
        "pathya_vihara": [
            "Strict sleep hygiene: Bedroom dark, cool (68°F), quiet, and screen-free 60 mins before bed",
            "Pada-Abhyanga: Massaging soles of feet with warm sesame oil for 5 minutes before sleeping",
            "Reading peaceful literature or listening to calming Vedic chanting (Sama Veda)"
        ],
        "apathya_vihara": [
            "Checking work emails, social media, or sensational news in bed",
            "Exercising intensely late in the evening past 8 PM",
            "Daytime sleeping (messes up circadian sleep pressure)"
        ],
        "yoga_pranayama": [
            "Bhramari Pranayama (Humming bee breath - 10 minutes right before sleep in bed)",
            "Nadi Shodhana Pranayama (Alternate nostril breathing with slow 1:2 exhalation ratio)",
            "Yoga Nidra (Guided psychophysical deep sleep relaxation - 20 minutes)",
            "Viparita Karani (Legs-up-the-wall pose before bedtime to discharge nervous tension)"
        ]
    },
    "shirashoola": {
        "name": "Migraine & Vascular Headache / Ardhavabhedaka",
        "sanskrit_name": "Ardhavabhedaka / Shirashoola (अर्धावभेदक / शिरःशूल)",
        "primary_dosha": "Vata",
        "doshic_subtype": "Vata-Pitta Pradhana (Pranavayu & Alochaka/Pachaka Pitta)",
        "cardinal_symptoms": [
            "headache_migraine_throbbing",
            "pain_sharp_throbbing",
            "irritability_anger",
            "insomnia_disturbed_sleep",
            "burning_sensation"
        ],
        "requires_ama": False,
        "dhatu": ["Majja Dhatu", "Rasa Dhatu", "Rakta Dhatu"],
        "srotas": ["Majjavaha Srotas", "Manovaha Srotas (Mental Channel)", "Pranavaha Srotas"],
        "prognosis": "Krichhra Sadhya (Curable with Systematic Protocol)",
        "classical_source": "Charaka Samhita Siddhisthana 9 (Trimarmiya Siddhi) & Sushruta Uttaratantra 25",
        "citations": [
            "Charaka Samhita Siddhisthana 9/74-78 (Ardhavabhedaka)",
            "Sushruta Samhita Uttaratantra 25/15",
            "Bhaishajya Ratnavali, Shirorogadhikara"
        ],
        "nidana": [
            "Ruksha-Sheeta Ahara (Excessive dry, stale food and irregular meal times)",
            "Vegadharana (Suppression of natural urges, especially sleep, tears, hunger)",
            "Ati-Bhashya & Chinta (Excessive mental stress, continuous loud talking)",
            "Exposure to direct sun, cold wind, and glare (Atapa & Pragvata)"
        ],
        "purvarupa": [
            "Aura, blurred vision, flickering lights, neck stiffness, and irritability"
        ],
        "upashaya_anupashaya": {
            "Upashaya (Alleviating)": [
                "Nasya with medicated oil or ghee",
                "Warm herbal paste application (Lepa) on forehead",
                "Rest in dark, soundproof room with warm hydration"
            ],
            "Anupashaya (Aggravating)": [
                "Direct exposure to sunlight, screen glare, loud noise, hunger"
            ]
        },
        "samprapti": {
            "Sanchaya": "Vata and Pitta accumulate due to erratic meals and sensory overuse.",
            "Prakopa": "Doshas aggravate, drying unctuous fluids in intracranial micro-channels.",
            "Prasara": "Vitiated Pranavayu ascends upward (Urdhwaga) through vascular networks.",
            "Sthana Samshraya": "Doshas lodge in the cranial marmas and Shira (head vessels).",
            "Vyakti": "Unilateral severe throbbing, temple pounding, photophobia, nausea.",
            "Bheda": "Chronic recurring neurological migraine syndrome and vascular tension."
        },
        "shamana_formulations": [
            {
                "name": "Shirashooladivajra Rasa",
                "category": "Rasaushadhi / Vati",
                "classical_indication": "Potent classical formulation specifically indicated for unilateral and bilateral vascular headaches (Ardhavabhedaka & Suryavarta).",
                "dosage": "1 tablet (250mg) twice daily",
                "anupana_vehicle": "Warm water or Dashamula Kwatha",
                "aushadha_sevana_kala": "Madhyabhakta (Mid-meals for cranial neural action)",
                "duration_weeks": 6,
                "classical_reference": "Bhaishajya Ratnavali, Shirorogadhikara"
            },
            {
                "name": "Pathyadi Kwatha",
                "category": "Kwatha",
                "classical_indication": "Classical decoction of Haritaki, Bibhitaki, Amalaki, Kalamegha, and Nimba; purifies intracranial channels and pacifies Pitta-Vata.",
                "dosage": "20 ml diluted with 40 ml warm water twice daily",
                "anupana_vehicle": "Warm water with a pinch of raw jaggery",
                "aushadha_sevana_kala": "Pragbhakta (30 mins before breakfast and dinner)",
                "duration_weeks": 8,
                "classical_reference": "Sharangadhara Samhita, Madhyama Khanda"
            },
            {
                "name": "Shadbindu Taila (Nasya)",
                "category": "Taila / Nasya",
                "classical_indication": "Administered via nostrils; directly accesses the brain and Shringataka Marma to eradicate chronic cranial pain.",
                "dosage": "2-4 drops in each nostril in the morning",
                "anupana_vehicle": "Direct nasal instillation with gentle warm facial fomentation",
                "aushadha_sevana_kala": "Pratah-kala (Morning after bowel movement)",
                "duration_weeks": 4,
                "classical_reference": "Bhaishajya Ratnavali, Shirorogadhikara"
            }
        ],
        "panchakarma": {
            "eligible": True,
            "recommended_therapy": "Marsha Nasya with Ksheerabala Taila & Shirodhara",
            "reasoning": "Nasa hi shiraso dwaram (the nose is the direct gateway to the brain). Nasya clears neurological channel blockages.",
            "purvakarma": ["Mukha Abhyanga (facial massage) & Nadi Sweda to sinuses"],
            "pradhanakarma": "Nasya administration (4-6 drops each nostril) followed by gentle spitting of residue.",
            "paschatkarma": ["Gandusha (warm saline gargling) and rest away from drafts"]
        },
        "pathya_ahara": [
            "Warm cooked grains with pure cow's A2 ghee",
            "Sweet pomegranates, raisins, almonds, coconut water",
            "Cow's milk with cardamom and saffron"
        ],
        "apathya_ahara": [
            "Aged fermented cheeses, chocolates, monosodium glutamate (MSG)",
            "Skipping meals or fasting (triggers hypovolemic Vata migraine)",
            "Fermented alcoholic drinks, sour curd at night"
        ],
        "pathya_vihara": [
            "Regular sleep-wake cycle; dimming lights by 9 PM",
            "Wear sunglasses or brimmed hats in bright outdoor sun",
            "Gentle neck and shoulder stretching"
        ],
        "apathya_vihara": [
            "Prolonged staring at high-contrast blue screens without breaks",
            "Suppression of natural biological urges (especially tears, yawns, and sleep)"
        ],
        "yoga_pranayama": [
            "Sheetali & Sheetkari Pranayama (Cooling breath to calm cranial Pitta)",
            "Bhramari Pranayama (Soothing sonic vibrations)",
            "Shavasana (Total sensory relaxation)"
        ]
    },
    "pandu": {
        "name": "Anemia & Tissue Exhaustion",
        "sanskrit_name": "Pandu Roga (पाण्डुरोग)",
        "primary_dosha": "Pitta",
        "doshic_subtype": "Pitta Pradhana Tridoshaja (Sadhaka Pitta & Rakta Dhatu Kshaya)",
        "cardinal_symptoms": [
            "pallor_fatigue_anemia",
            "heaviness_body_limbs",
            "cold_intolerance",
            "weight_loss_emaciation",
            "loss_of_taste_aruchi"
        ],
        "requires_ama": False,
        "dhatu": ["Rasa Dhatu", "Rakta Dhatu", "Meda Dhatu", "Ojas"],
        "srotas": ["Rasavaha Srotas", "Raktavaha Srotas"],
        "prognosis": "Sukha Sadhya (Readily Curable in early stages)",
        "classical_source": "Charaka Samhita Chikitsasthana 16 (Pandu Roga Chikitsa)",
        "citations": [
            "Charaka Samhita Chikitsasthana 16/4-12",
            "Sushruta Samhita Uttaratantra 44",
            "Ashtanga Hridaya Chikitsasthana 16"
        ],
        "nidana": [
            "Kshara-Amla-Lavana Atisevana (Excessive intake of sour, salty, and alkali foods)",
            "Nishpava-Masha (Excess consumption of incompatible legumes)",
            "Divasvapna (Daytime sleeping disrupting metabolic circulation)",
            "Rakta-Srava (Chronic occult blood loss, heavy menstrual cycles, bleeding piles)"
        ],
        "purvarupa": [
            "Hrid-drava (Heart palpitations on mild exertion), dryness of skin, lack of sweat, tasting earth/clay"
        ],
        "upashaya_anupashaya": {
            "Upashaya (Alleviating)": [
                "Nourishing iron-rich Rasayana herbs, pomegranate juice, raisins, iron bhasmas",
                "Warm easily digestible soups with cow's ghee"
            ],
            "Anupashaya (Aggravating)": [
                "Sour tamarind, pickles, vinegar, heavy fried foods, unwholesome day sleeping"
            ]
        },
        "samprapti": {
            "Sanchaya": "Pitta increases due to sour, salty, and acidic dietary indiscretions.",
            "Prakopa": "Pitta vitiates Rasa and Rakta, reducing their biological unctuousness.",
            "Prasara": "Circulates systemically, diminishing Ojas and muscular firmness.",
            "Sthana Samshraya": "Affects liver, spleen, and bone marrow hematopoiesis.",
            "Vyakti": "Visible pallor (Panduta) of sclera, nail beds, tongue, accompanied by profound fatigue.",
            "Bheda": "Severe Dhatukshaya, tissue edema, breathlessness, and cardiac strain."
        },
        "shamana_formulations": [
            {
                "name": "Punarnava Mandura",
                "category": "Vati / Lauha Kalpa",
                "classical_indication": "Premier classical iron formulation processed with Punarnava and Triphala; restores hemoglobin and treats microvascular sluggishness.",
                "dosage": "2 tablets (500mg each) twice daily",
                "anupana_vehicle": "Takra (fresh buttermilk) or warm water",
                "aushadha_sevana_kala": "Madhyabhakta (Mid-meals for optimal hematinic absorption)",
                "duration_weeks": 10,
                "classical_reference": "Charaka Samhita Chikitsasthana 16"
            },
            {
                "name": "Draksharishta",
                "category": "Asava / Arishta",
                "classical_indication": "Fermented raisin tonic; nourishes Rasa-Rakta, kindles Agni, and corrects chronic debility.",
                "dosage": "20 ml with equal water twice daily after meals",
                "anupana_vehicle": "Equal quantity of water",
                "aushadha_sevana_kala": "Adhobhakta (Immediately after meals)",
                "duration_weeks": 8,
                "classical_reference": "Bhaishajya Ratnavali, Pandurogadhikara"
            },
            {
                "name": "Dhatri Lauha",
                "category": "Lauha Rasayana",
                "classical_indication": "Purified iron calx processed with fresh Amalaki juice; rapidly increases red blood cell vitality without causing constipation.",
                "dosage": "250mg twice daily",
                "anupana_vehicle": "Warm water with 1/2 tsp pure honey and cow's ghee",
                "aushadha_sevana_kala": "Pragbhakta (Before meals)",
                "duration_weeks": 8,
                "classical_reference": "Bhaishajya Ratnavali, Pandurogadhikara"
            }
        ],
        "panchakarma": {
            "eligible": True,
            "recommended_therapy": "Mridu Shodhana (Gentle Virechana with Kalyanaka Ghrita)",
            "reasoning": "Charaka advises: 'Pandurogi tu snigdha syat mridubhih shodhanairhritah' - gentle purgation clears hepatic Pitta stagnation.",
            "purvakarma": ["Snehana with Dadimadi Ghrita for 3-5 days"],
            "pradhanakarma": "Mridu Virechana with Trivrit Lehya (15-20g)",
            "paschatkarma": ["Light diet of mung dal soup and boiled red rice (Samsarjana Krama)"]
        },
        "pathya_ahara": [
            "Fresh pomegranate juice (Dadima), black raisins soaked in water, dates, beetroot",
            "Amla (Indian gooseberry) in fresh or powdered form daily",
            "Moong dal soup, aged Shashtika rice, barley, and cow's A2 ghee"
        ],
        "apathya_ahara": [
            "Pungent, sour, and excessively salty foods (pickles, vinegar, fried chilies)",
            "Clay, chalk, or unwashed raw items (soil eating habited in Pandu)",
            "Alcohol and smoking (worsens bone marrow hematopoietic exhaustion)"
        ],
        "pathya_vihara": [
            "Adequate restorative nocturnal sleep; avoiding strenuous heavy labor during recovery",
            "Mild morning sunbathing for 15 minutes (Pratah Tapam)"
        ],
        "apathya_vihara": [
            "Day sleeping (Divasvapna), anger, severe physical strain beyond capacity"
        ],
        "yoga_pranayama": [
            "Gentle Surya Namaskara (2-3 rounds only without breath exhaustion)",
            "Anuloma Viloma Pranayama (10 minutes twice daily)",
            "Matsyasana (To stimulate thoracic blood flow and thyroid metabolism)"
        ]
    },
    "shotha": {
        "name": "Edema & Water Retention",
        "sanskrit_name": "Shotha / Shopha (शोथ / शोफ)",
        "primary_dosha": "Kapha",
        "doshic_subtype": "Kapha-Vata Pradhana (Kledaka Kapha & Vyana Vayu Obstruction)",
        "cardinal_symptoms": [
            "dull_pain_swelling_edema",
            "heaviness_body_limbs",
            "weight_gain_slow_metabolism",
            "cold_intolerance"
        ],
        "requires_ama": False,
        "dhatu": ["Rasa Dhatu", "Rakta Dhatu", "Mamsa Dhatu"],
        "srotas": ["Rasavaha Srotas", "Udakavaha Srotas (Fluid Regulation Channel)", "Mutravaha Srotas"],
        "prognosis": "Krichhra Sadhya (Curable with Systematic Fluid Clearance)",
        "classical_source": "Charaka Samhita Chikitsasthana 12 (Shotha Chikitsa)",
        "citations": [
            "Charaka Samhita Chikitsasthana 12/3-18",
            "Sushruta Samhita Chikitsasthana 23",
            "Madhava Nidana, Shotha Nidana"
        ],
        "nidana": [
            "Excessive salt (Lavana) and sour food intake causing fluid extravasation",
            "Heavy sedentary lifestyle after unctuous meals (Snigdha-Guru Ahara)",
            "Suppression of urine and sweat urges",
            "Kidney, cardiac, or liver microvascular congestion"
        ],
        "purvarupa": [
            "Feeling of tightness in rings or footwear, heaviness in eyelids upon morning awakening"
        ],
        "upashaya_anupashaya": {
            "Upashaya (Alleviating)": [
                "Diuretic herbs (Punarnava, Gokshura), dry hot fomentation, salt-free diet",
                "Barley water and horsegram soup (Kulattha Yusha)"
            ],
            "Anupashaya (Aggravating)": [
                "Table salt, pickles, curd, day sleeping, excessive water drinking"
            ]
        },
        "samprapti": {
            "Sanchaya": "Kapha and Vata accumulate due to excessive salt and sluggish kidneys.",
            "Prakopa": "Doshas vitiate the fluid regulating channels (Udakavaha Srotas).",
            "Prasara": "Fluid extravasates from intravascular spaces into interstitial subcutaneous tissues.",
            "Sthana Samshraya": "Lodges in lower extremities, periorbital spaces, or abdominal wall.",
            "Vyakti": "Pitting edema, visible swelling that retains impression on finger pressure, heaviness.",
            "Bheda": "Chronic fibrosis, secondary skin trophic changes, systemic fluid overload."
        },
        "shamana_formulations": [
            {
                "name": "Punarnavadi Kwatha",
                "category": "Kwatha",
                "classical_indication": "Master classical diuretic and nephro-protective decoction; swiftly expels interstitial fluid and relieves periorbital and pedal edema.",
                "dosage": "20 ml diluted with 40 ml warm water twice daily",
                "anupana_vehicle": "Warm water",
                "aushadha_sevana_kala": "Pragbhakta (30 mins before food)",
                "duration_weeks": 6,
                "classical_reference": "Bhaishajya Ratnavali, Shotharogadhikara"
            },
            {
                "name": "Punarnavarishta",
                "category": "Asava / Arishta",
                "classical_indication": "Stimulates Jatharagni and renal filtration; cleanses micro-channels (Srotoshodhana).",
                "dosage": "20 ml with equal water twice daily after meals",
                "anupana_vehicle": "Equal quantity of water",
                "aushadha_sevana_kala": "Adhobhakta (Immediately after meals)",
                "duration_weeks": 8,
                "classical_reference": "Bhaishajya Ratnavali, Shotharogadhikara"
            },
            {
                "name": "Chandraprabha Vati",
                "category": "Vati / Guggulu",
                "classical_indication": "Cleanses the urinary tract, eliminates Kleda (metabolic moisture), and tonifies the bladder and kidneys.",
                "dosage": "2 tablets (500mg each) twice daily",
                "anupana_vehicle": "Warm water or Punarnava Kwatha",
                "aushadha_sevana_kala": "Madhyabhakta (Mid-meals)",
                "duration_weeks": 6,
                "classical_reference": "Sharangadhara Samhita, Madhyama Khanda"
            }
        ],
        "panchakarma": {
            "eligible": True,
            "recommended_therapy": "Nadi Sweda (Dry herbal steam) & Virechana with Eranda Taila",
            "reasoning": "Ruksha Sweda (dry sweat therapy) and downward purgation eliminate excessive fluid accumulation.",
            "purvakarma": ["Ruksha Baluka Sweda (hot sand-bag fomentation) to edematous limbs"],
            "pradhanakarma": "Mridu Nitya Virechana with castor oil and Haritaki (10-15ml)",
            "paschatkarma": ["Low-sodium barley gruel diet"]
        },
        "pathya_ahara": [
            "Barley (Yava), aged red rice, green gram soup without added salt",
            "Radish, bitter gourd, pointed gourd (Patola), drumsticks (Shigru)",
            "Kulattha (horsegram) soup - excellent classical fluid scraper"
        ],
        "apathya_ahara": [
            "Added table salt, salty snacks, potato chips, canned soups",
            "Yoghurt, heavy paneer, buffalo milk, bakery items with baking soda",
            "Excessive fluid intake beyond thirst"
        ],
        "pathya_vihara": [
            "Leg elevation while resting; brisk walking to promote venous return",
            "Warm dry environments"
        ],
        "apathya_vihara": [
            "Daytime sleep (strongly increases Kapha edema), sitting with legs dangling for hours"
        ],
        "yoga_pranayama": [
            "Viparita Karani (Legs-up-the-wall pose - 15 minutes to facilitate venous drainage)",
            "Bhastrika Pranayama (Mild pace to ignite metabolic cellular fire)",
            "Surya Bhedana Pranayama (To stimulate catabolic sweat release)"
        ]
    },
    "mutrakrichhra": {
        "name": "Dysuria & Urinary Tract Infection",
        "sanskrit_name": "Mutrakrichhra (मूत्रकृच्छ्र)",
        "primary_dosha": "Pitta",
        "doshic_subtype": "Pitta-Vata Pradhana (Apana Vayu & Pitta Dushti)",
        "cardinal_symptoms": [
            "burning_painful_urination",
            "burning_sensation",
            "frequent_cloudy_urination",
            "fever"
        ],
        "requires_ama": False,
        "dhatu": ["Rasa Dhatu", "Mutra (Mala)"],
        "srotas": ["Mutravaha Srotas (Urinary Channel)"],
        "prognosis": "Sukha Sadhya (Readily Curable)",
        "classical_source": "Charaka Samhita Chikitsasthana 26 (Trimarmiya Chikitsa)",
        "citations": [
            "Charaka Samhita Chikitsasthana 26/32-44",
            "Madhava Nidana, Mutrakrichhra Adhyaya",
            "Bhavaprakasha, Mutrakrichhradhikara"
        ],
        "nidana": [
            "Ati-Tikshna-Ushna Ahara (Excessive spicy, pungent, and sour food consumption)",
            "Vyayama & Atapa (Excessive physical exertion in boiling heat with inadequate water)",
            "Suppression of micturition urges (Mutra-Vegadharana)",
            "Inadequate daily hydration"
        ],
        "purvarupa": [
            "Heaviness in the suprapubic area, mild urinary urgency, dark yellow concentrated urine"
        ],
        "upashaya_anupashaya": {
            "Upashaya (Alleviating)": [
                "Cooling diuretic infusions (Coriander seed water, Gokshura decoction, tender coconut)",
                "Cold pelvic sponge / sitz bath"
            ],
            "Anupashaya (Aggravating)": [
                "Alcohol, red chilies, vinegar, citrus fruits, holding urine, sun exposure"
            ]
        },
        "samprapti": {
            "Sanchaya": "Pitta and Vata accumulate in the lower abdomen due to dehydration and spice.",
            "Prakopa": "Pitta inflames the mucosal lining of the bladder and urethra.",
            "Prasara": "Vitiated Apana Vayu produces painful spasmodic contractions during urination.",
            "Sthana Samshraya": "Lodges in the Basti (urinary bladder) and Mutramarga.",
            "Vyakti": "Intense burning sensation, sharp stinging pain on voiding, drop-by-drop urination (Muhur-muhuh).",
            "Bheda": "Ascending kidney infection, urinary gravel formation, hematuria."
        },
        "shamana_formulations": [
            {
                "name": "Gokshuradi Guggulu",
                "category": "Vati / Guggulu",
                "classical_indication": "Premier classical urinary rejuvenator and anti-inflammatory; eliminates micro-organisms and soothes the urinary epithelium.",
                "dosage": "2 tablets (500mg each) twice daily",
                "anupana_vehicle": "Warm water or coriander seed infusion (Dhanyaka Hima)",
                "aushadha_sevana_kala": "Madhyabhakta (Mid-meals for targeted lower urinary action)",
                "duration_weeks": 4,
                "classical_reference": "Sharangadhara Samhita, Madhyama Khanda"
            },
            {
                "name": "Chandanasava",
                "category": "Asava / Arishta",
                "classical_indication": "Classical sandalwood tonic; provides rapid systemic cooling, relieves burning micturition, and pacifies irritated urinary mucosa.",
                "dosage": "20 ml with equal water twice daily after meals",
                "anupana_vehicle": "Equal quantity of water",
                "aushadha_sevana_kala": "Adhobhakta (Immediately after meals)",
                "duration_weeks": 4,
                "classical_reference": "Bhaishajya Ratnavali, Mutrakrichhradhikara"
            },
            {
                "name": "Trinapanchamoola Kwatha",
                "category": "Kwatha",
                "classical_indication": "Classical decoction of five sacred cooling root grasses (Kusha, Kasha, Shara, Darbha, Ikshu); powerfully calms burning dysuria.",
                "dosage": "30 ml twice daily",
                "anupana_vehicle": "Warm water with 1 tsp raw sugar (Sharkara)",
                "aushadha_sevana_kala": "Pragbhakta (Before meals)",
                "duration_weeks": 3,
                "classical_reference": "Charaka Samhita Chikitsasthana 26"
            }
        ],
        "panchakarma": {
            "eligible": True,
            "recommended_therapy": "Avagaha Sweda (Cooling sitz bath) & Uttarabasti (in chronic cases)",
            "reasoning": "Pelvic soothing immersion reduces urethral spasms and calms Pitta inflammation.",
            "purvakarma": ["Local gentle pelvic massage with Chandanadi Taila"],
            "pradhanakarma": "Avagaha Sweda (sitting in lukewarm water steeped with decoction of Triphala/Dashamula for 20 mins).",
            "paschatkarma": ["Drinking a cup of tender coconut water"]
        },
        "pathya_ahara": [
            "Tender coconut water, barley water, sugarcane juice (Ikshu Rasa)",
            "Coriander seed cold infusion (steep 1 tbsp crushed coriander in water overnight)",
            "Watermelon, cucumber, sweet grapes, cow's milk with sugar candy"
        ],
        "apathya_ahara": [
            "Hot red/green chilies, mustard, vinegar, tamarind, black pepper",
            "Alcohol, strong coffee, energy drinks, artificial sodas",
            "Heavy greasy meats and deep-fried fast food"
        ],
        "pathya_vihara": [
            "Urinate immediately upon urge; do not hold urine",
            "Maintain meticulous personal hygiene",
            "Wear loose, breathable cotton undergarments"
        ],
        "apathya_vihara": [
            "Sitting on hot sunbaked surfaces, excessive cycling or horse riding, sexual intercourse during acute infection"
        ],
        "yoga_pranayama": [
            "Sheetali Pranayama (Cooling tongue-hiss breath - 15 rounds)",
            "Sheetkari Pranayama (Teeth cooling breath)",
            "Bhadrasana (Auspicious butterfly pose to enhance pelvic floor microcirculation)"
        ]
    },
    "atisara": {
        "name": "Acute Diarrheal Disorder & Enteritis",
        "sanskrit_name": "Atisara (अतिसार)",
        "primary_dosha": "Pitta",
        "doshic_subtype": "Pitta-Vata Pradhana (Samana Vayu & Pachaka Pitta Dushti)",
        "cardinal_symptoms": [
            "severe_acute_diarrhea",
            "loose_stools_diarrhea",
            "burning_sensation",
            "bloating_flatulence"
        ],
        "requires_ama": True,
        "dhatu": ["Rasa Dhatu", "Udaka (Body water)", "Pureesha (Feces)"],
        "srotas": ["Annavaha Srotas", "Purishavaha Srotas", "Udakavaha Srotas"],
        "prognosis": "Sukha Sadhya (Quickly curable with immediate Grahi / Deepana care)",
        "classical_source": "Charaka Samhita Chikitsasthana 19 (Atisara Chikitsa)",
        "citations": [
            "Charaka Samhita Chikitsasthana 19/4-22",
            "Sushruta Samhita Uttaratantra 40",
            "Madhava Nidana, Atisara Nidana"
        ],
        "nidana": [
            "Contaminated water or spoiled unhygienic foods (Dusta-Jala-Ahara)",
            "Excessive intake of watery, greasy, unctuous, or incompatible substances",
            "Sudden climate change and severe seasonal humidity",
            "Extreme mental fear, shock, or anxiety (Bhayaja / Shokaja Atisara)"
        ],
        "purvarupa": [
            "Abdominal rumbling (Antrakujana), loss of appetite, mild griping periumbilical pain"
        ],
        "upashaya_anupashaya": {
            "Upashaya (Alleviating)": [
                "Strict Langhana (fasting from solid food), warm water boiled with dry ginger and coriander",
                "Astringent digestive soups (Mudga Yusha, Bilva Phala)"
            ],
            "Anupashaya (Aggravating)": [
                "Milk, fruit juices, oily gravies, raw salads, cold drinks"
            ]
        },
        "samprapti": {
            "Sanchaya": "Watery element (Dravamsha) increases, quenching the digestive fire (Agni-Nashana).",
            "Prakopa": "Samana and Apana Vayu force fluid down the GI tract without proper absorption.",
            "Prasara": "Stools liquefy and pass continuously through the colon.",
            "Sthana Samshraya": "Affects the Pakvashaya (colon) and Grahani.",
            "Vyakti": "Frequent profuse watery, foul, burning evacuations accompanied by dehydration.",
            "Bheda": "Severe electrolyte depletion, hypovolemia, and extreme weakness."
        },
        "shamana_formulations": [
            {
                "name": "Kutajaghan Vati",
                "category": "Vati / Kashaya",
                "classical_indication": "Gold standard classical bowel astringent (Grahi & Deepana); stops microbial diarrhea, soothes intestinal inflammation, and consolidates stool.",
                "dosage": "2 tablets (500mg each) thrice daily",
                "anupana_vehicle": "Warm water or fresh buttermilk (Takra)",
                "aushadha_sevana_kala": "Pragbhakta (Before meals) or during acute purging",
                "duration_weeks": 2,
                "classical_reference": "Siddha Yoga Sangraha, Atisaradhikara"
            },
            {
                "name": "Bilvadi Gutika",
                "category": "Vati / Gutika",
                "classical_indication": "Precious unripe Bael fruit formulation; neutralizes toxins (Ama Visha) in the gut and checks loose watery motions.",
                "dosage": "1 tablet twice daily",
                "anupana_vehicle": "Warm water with a pinch of dry ginger",
                "aushadha_sevana_kala": "Madhyabhakta (Mid-meals)",
                "duration_weeks": 2,
                "classical_reference": "Ashtanga Hridaya, Uttarasthana"
            },
            {
                "name": "Gangadhara Churna",
                "category": "Churna",
                "classical_indication": "Master classical compound of Musta, Bilva, Lodhra, and Dhataki; cures chronic and acute diarrheal disorders.",
                "dosage": "3g twice daily",
                "anupana_vehicle": "Fresh buttermilk with roasted cumin and rock salt",
                "aushadha_sevana_kala": "Pragbhakta (Before meals)",
                "duration_weeks": 3,
                "classical_reference": "Sharangadhara Samhita, Madhyama Khanda"
            }
        ],
        "panchakarma": {
            "eligible": False,
            "recommended_therapy": "Panchakarma Contraindicated in Acute Atisara (Langhana & Stambhana Only)",
            "reasoning": "Charaka Chikitsa 19 states: 'Shodhana is strictly contraindicated during active acute purging, as it will exhaust vital fluids (Ojas and Dhatus)'.",
            "purvakarma": ["Langhana (therapeutic fasting from solid foods)"],
            "pradhanakarma": "N/A - Medical management via Deepana-Grahi herbs",
            "paschatkarma": ["Gradual reintroduction of thin rice gruel (Peya, Vilepi)"]
        },
        "pathya_ahara": [
            "Thin rice gruel boiled with dry ginger and pomegranate rind (Peya / Vilepi)",
            "Fresh churned buttermilk (Takra) seasoned with roasted cumin and rock salt",
            "Unripe Bael fruit (Bilva) pulp, stewed green apples"
        ],
        "apathya_ahara": [
            "Whole cow's or buffalo's milk (strictly contraindicated in Atisara)",
            "Oils, ghee, deep-fried snacks, sugarcane juice, raw fruits",
            "Cold unboiled tap water, leafy salads"
        ],
        "pathya_vihara": [
            "Complete physical bed rest; keep abdomen warm with flannel cloth",
            "Sip warm rehydration fluids constantly throughout the day"
        ],
        "apathya_vihara": [
            "Physical exertion, traveling, exposure to cold wind, daytime bathing"
        ],
        "yoga_pranayama": [
            "Rest in Shavasana (Corpse pose)",
            "Gentle belly breathing without abdominal strain",
            "No vigorous asanas during active fluid loss"
        ]
    },
    "cittodvega": {
        "name": "Generalized Anxiety & Manovaha Disturbance",
        "sanskrit_name": "Cittodvega / Vishada (चित्तोद्वेग)",
        "primary_dosha": "Vata",
        "doshic_subtype": "Vata Pradhana (Pranavayu & Raja Guna Aggravation)",
        "cardinal_symptoms": [
            "panic_intense_worry",
            "anxiety_restlessness",
            "insomnia_disturbed_sleep",
            "tremors_stiffness"
        ],
        "requires_ama": False,
        "dhatu": ["Majja Dhatu", "Rasa Dhatu", "Ojas", "Manas"],
        "srotas": ["Manovaha Srotas (Mental Channel)", "Pranavaha Srotas", "Majjavaha Srotas"],
        "prognosis": "Sukha Sadhya (Curable with Medhya Rasayana and Sattvavajaya)",
        "classical_source": "Charaka Samhita Sharirasthana 1 & Ashtanga Hridaya Uttarasthana 6",
        "citations": [
            "Charaka Samhita Sutrasthana 1/58",
            "Charaka Samhita Sharirasthana 1/98-105",
            "Bhaishajya Ratnavali, Unmadadhikara"
        ],
        "nidana": [
            "Prajnaparadha (Intellectual blasphemy / continuous burnout and overworking)",
            "Asatmendriyartha Samyoga (Excessive sensory overload, doom-scrolling, alarming stimuli)",
            "Ruksha-Alpa Ahara (Irregular malnourished dieting aggravating Vata)",
            "Suppression of emotional and biological needs"
        ],
        "purvarupa": [
            "Sudden unfounded palpitations, feeling of internal trembling, difficulty switching off racing thoughts"
        ],
        "upashaya_anupashaya": {
            "Upashaya (Alleviating)": [
                "Medhya Rasayana herbs (Brahmi, Shankhapushpi, Ashwagandha)",
                "Warm oil Shirodhara, warm foot massage with sesame oil, quiet natural environments"
            ],
            "Anupashaya (Aggravating)": [
                "Caffeine, stimulants, alarming news, conflict, isolation, sleep deprivation"
            ]
        },
        "samprapti": {
            "Sanchaya": "Pranavayu accumulates due to excessive mental strain and sensory hyper-stimulation.",
            "Prakopa": "Raja Guna rises in the Manas (mind), displacing the peaceful Sattva quality.",
            "Prasara": "Vitiated Vayu travels through the ten major vessels radiating from the heart (Hridaya).",
            "Sthana Samshraya": "Lodges in the Manovaha Srotas and cranial nerve centers.",
            "Vyakti": "Acute episodes of dread, trembling, palpitations, restlessness, and inability to settle.",
            "Bheda": "Chronic generalized anxiety disorder, panic syndrome, and emotional burnout."
        },
        "shamana_formulations": [
            {
                "name": "Saraswatarishta",
                "category": "Asava / Medhya Arishta",
                "classical_indication": "Premier classical cerebral tonic formulated with Brahmi, Shatavari, and Haritaki; tranquilizes racing thoughts, sharpens memory, and restores restful peace.",
                "dosage": "20 ml with equal water twice daily after meals",
                "anupana_vehicle": "Equal quantity of water",
                "aushadha_sevana_kala": "Adhobhakta (Immediately after meals)",
                "duration_weeks": 8,
                "classical_reference": "Bhaishajya Ratnavali, Rasayanadhikara"
            },
            {
                "name": "Brahmi Vati (Gold Fortified / Swarna Yukta)",
                "category": "Rasaushadhi / Vati",
                "classical_indication": "Potent neuro-psychiatric calming tablet; stabilizes autonomic hyper-arousal and stops palpitations and trembling.",
                "dosage": "1 tablet (250mg) twice daily",
                "anupana_vehicle": "Warm cow's milk with a pinch of nutmeg",
                "aushadha_sevana_kala": "Nishi (At bedtime and morning)",
                "duration_weeks": 6,
                "classical_reference": "Siddha Bhaishajya Manimala"
            },
            {
                "name": "Ashwagandharishta",
                "category": "Asava / Arishta",
                "classical_indication": "Deep neuromuscular tonic; pacifies systemic Vata, builds nervous system resilience, and dispels chronic fatigue.",
                "dosage": "20 ml with equal water twice daily",
                "anupana_vehicle": "Equal quantity of water",
                "aushadha_sevana_kala": "Adhobhakta (After meals)",
                "duration_weeks": 8,
                "classical_reference": "Bhaishajya Ratnavali, Murchhadhikara"
            }
        ],
        "panchakarma": {
            "eligible": True,
            "recommended_therapy": "Shirodhara with Brahmi / Ksheerabala Taila & Nasya",
            "reasoning": "Continuous warm oil stream over forehead stimulates the Ajna center and downregulates the sympathetic nervous system.",
            "purvakarma": ["Shiro-Abhyanga (calming head massage) & Pada-Abhyanga (warm foot rub)"],
            "pradhanakarma": "Shirodhara (continuous rhythmic pouring of warm herbal oil for 45 minutes for 7-14 days).",
            "paschatkarma": ["Quiet rest in dim room, drinking warm herbal tea"]
        },
        "pathya_ahara": [
            "Warm sweet cow's milk with ghee, nutmeg, and cardamom before sleep",
            "Soaked almonds, walnuts, dates, sweet ripe seasonal fruits",
            "Warm nourishing soups with pumpkin, sweet potato, and basmati rice"
        ],
        "apathya_ahara": [
            "Coffee, green tea, energy drinks, colas, pre-workout stimulants",
            "Dry crunchy crackers, cold raw salads at night, pungent hot chilies",
            "Alcoholic binge drinking (causes severe rebound morning panic)"
        ],
        "pathya_vihara": [
            "Abhyanga: Daily self-massage with warm sesame oil before warm shower",
            "Grounding: Walking barefoot on morning grass or soil for 15 minutes",
            "Digital detox: No news or screens after 8 PM"
        ],
        "apathya_vihara": [
            "Engaging in arguments or reading disturbing news late at night",
            "Irregular erratic sleeping hours, suppressing the urge to cry or express emotion"
        ],
        "yoga_pranayama": [
            "Nadi Shodhana Pranayama (Alternate nostril breathing with gentle 1:2 ratio - 15 mins)",
            "Bhramari Pranayama (Humming bee breath to stimulate vagus nerve)",
            "Yoga Nidra (Guided psychophysical deep relaxation)"
        ]
    }
}
