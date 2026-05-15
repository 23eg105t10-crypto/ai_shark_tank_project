
import os
import re
from datetime import datetime

import streamlit as st

st.set_page_config(page_title="AI Shark Tank", page_icon="🦈", layout="wide")


SHARKS = {
    "Mark Titan": {
        "emoji": "💰",
        "persona": "Aggressive billionaire investor focused on profits and scale.",
        "avatar": "https://ui-avatars.com/api/?name=Mark+Titan&background=ff5a5f&color=ffffff&size=256",
    },
    "Sophia Ventures": {
        "emoji": "🚀",
        "persona": "Tech-focused venture capitalist who values innovation.",
        "avatar": "https://ui-avatars.com/api/?name=Sophia+Ventures&background=6f42c1&color=ffffff&size=256",
    },
    "Raj Growth": {
        "emoji": "📣",
        "persona": "Marketing genius focused on customer acquisition and branding.",
        "avatar": "https://ui-avatars.com/api/?name=Raj+Growth&background=0dcaf0&color=ffffff&size=256",
    },
    "Elena Finance": {
        "emoji": "📊",
        "persona": "Finance expert who carefully analyzes business models and risk.",
        "avatar": "https://ui-avatars.com/api/?name=Elena+Finance&background=198754&color=ffffff&size=256",
    },
}

# Small app/logo image and hero banner (can be overridden by local files in ./assets)
APP_LOGO = "https://ui-avatars.com/api/?name=AI+Shark+Tank&background=0d6efd&color=ffffff&size=280"
HERO_IMAGE = "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=1600&auto=format&fit=crop&ixlib=rb-4.0.3&s=6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d"


def choose_asset(default_url: str, local_candidates: list[str]) -> str:
    """Return the first existing local path from local_candidates (relative to the app), else return default_url."""
    base = os.path.dirname(__file__)
    for rel in local_candidates:
        p = os.path.join(base, rel)
        if os.path.exists(p):
            return p
    return default_url

# Prefer local assets if provided (place your exact images in ./assets/ to use them)
APP_LOGO = choose_asset(APP_LOGO, ["assets/logo.png", "assets/logo.jpg"])
HERO_IMAGE = choose_asset(HERO_IMAGE, ["assets/hero.jpg", "assets/hero.png"])
 
SAMPLE_PITCHES = {
    # Food & Bev samples (5)
    "GreenWrap — Sustainable Packaging": {
        "industry": "Food & Bev",
        "text": (
            "Problem: Single-use plastic packaging creates waste and regulatory risk for food service.\n\n"
            "Solution: GreenWrap makes compostable food packaging with comparable cost and performance for restaurants.\n\n"
            "Traction: 30 cafe pilots; positive unit economics; conversion to paid pilots.\n\n"
            "Business model: B2B wholesale, subscription for branded disposables.\n\n"
            "Ask: $250,000 for 15% to scale manufacturing and sales."
        ),
    },
    "QuickBite — Ghost Kitchen Network": {
        "industry": "Food & Bev",
        "text": (
            "Problem: High fixed costs prevent restaurant expansion.\n\n"
            "Solution: QuickBite operates lean ghost kitchens with white-label brands to test demand.\n\n"
            "Traction: 12 kitchens, strong unit economics.\n\n"
            "Business model: revenue share + franchise.\n\n"
            "Ask: $900,000 for 8% to expand to 50 cities."
        ),
    },
    "SipSmart — Beverage Analytics": {
        "industry": "Food & Bev",
        "text": (
            "Problem: Beverage brands lack real-time shelf insights.\n\n"
            "Solution: SipSmart provides IoT sensors and analytics for fridge-level inventory optimization.\n\n"
            "Traction: pilots with 20 retailers.\n\n"
            "Business model: hardware + SaaS.\n\n"
            "Ask: $420,000 for 12% to ramp manufacturing and sales."
        ),
    },
    "Farm2Table — Local Produce D2C": {
        "industry": "Food & Bev",
        "text": (
            "Problem: Consumers want fresh local produce delivered but logistics are complex.\n\n"
            "Solution: Farm2Table aggregates local farms and offers refrigerated delivery.\n\n"
            "Traction: 4k subscribers in pilot city; strong retention.\n\n"
            "Business model: subscription + marketplace fees.\n\n"
            "Ask: $350,000 for 10% to expand to 3 more cities."
        ),
    },

    # AgTech samples (5)
    "FarmSense — Agri IoT": {
        "industry": "AgTech",
        "text": (
            "Problem: Farmers lack affordable, real-time insights to optimize water and fertilizer use.\n\n"
            "Solution: FarmSense provides low-cost soil sensors + AI-driven recommendations to boost yield and reduce inputs.\n\n"
            "Traction: 180 farm pilots; avg yield +12%; input cost -18%.\n\n"
            "Business model: hardware + SaaS; revenue share with distributors.\n\n"
            "Ask: $600,000 for 10% to scale manufacturing and sales."
        ),
    },
    "AgriLens — Crop Analytics": {
        "industry": "AgTech",
        "text": (
            "Problem: Crop disease detection is slow and manual.\n\n"
            "Solution: AgriLens uses drone imagery + ML to flag disease and nutrient stress.\n\n"
            "Traction: pilot with 25 farms; high detection accuracy.\n\n"
            "Business model: per-hectare licensing + custom services.\n\n"
            "Ask: $480,000 for 9% to expand data ops and partnerships."
        ),
    },
    "Irrigo — Smart Irrigation Controllers": {
        "industry": "AgTech",
        "text": (
            "Problem: Water waste in agriculture is costly and unsustainable.\n\n"
            "Solution: Irrigo optimizes irrigation schedules using soil + weather data.\n\n"
            "Traction: 40 large-farm pilots; avg water savings 22%.\n\n"
            "Business model: hardware + subscription; channel partnerships.\n\n"
            "Ask: $520,000 for 10% to scale manufacturing and sales."
        ),
    },
    "Seedly — Precision Seeding Analytics": {
        "industry": "AgTech",
        "text": (
            "Problem: Seed placement inefficiencies lower yields.\n\n"
            "Solution: Seedly optimizes seed placement via machine vision and robotics.\n\n"
            "Traction: demo with two equipment OEMs; promising yield improvements.\n\n"
            "Business model: OEM licensing + SaaS.\n\n"
            "Ask: $640,000 for 9% to build production prototypes."
        ),
    },
    # --- SaaS samples
    "CloudPilot — DevOps Automation": {
        "industry": "SaaS",
        "text": (
            "Problem: Developers spend too much time on repetitive infra tasks.\n\n"
            "Solution: CloudPilot automates CI/CD and infra provisioning with simple policy templates.\n\n"
            "Traction: 120 teams onboarded in private beta; clear time savings on deployments.\n\n"
            "Business model: seats + premium integrations.\n\n"
            "Ask: $400,000 for 8% to accelerate product-market fit and enterprise sales."
        ),
    },
    "TeamFlow — Remote Collaboration": {
        "industry": "SaaS",
        "text": (
            "Problem: Remote teams lose context across tools.\n\n"
            "Solution: TeamFlow unifies docs, async video notes, and task workflows in one lightweight workspace.\n\n"
            "Traction: 2.5k MAU, $35k MRR from SMB customers.\n\n"
            "Business model: freemium -> paid teams.\n\n"
            "Ask: $300,000 for 10% to expand integrations and marketing."
        ),
    },
    "DataPulse — Analytics-as-a-Service": {
        "industry": "SaaS",
        "text": (
            "Problem: Small companies can't hire data teams to extract growth signals.\n\n"
            "Solution: DataPulse provides managed analytics and action dashboards for non-technical teams.\n\n"
            "Traction: $60k ARR, 10 pilot customers with measurable uplift.\n\n"
            "Business model: subscription + professional services.\n\n"
            "Ask: $250,000 for 12% to productize onboarding and scale sales."
        ),
    },

    # --- Consumer samples
    "GlowHome — Smart Lighting": {
        "industry": "Consumer",
        "text": (
            "Problem: Consumers want easy, beautiful smart lighting without complex apps.\n\n"
            "Solution: GlowHome offers plug-and-play smart bulbs with scene-first controls and retail packaging.\n\n"
            "Traction: 6k units sold in pilots; strong repeat purchases.\n\n"
            "Business model: direct-to-consumer + retail partnerships.\n\n"
            "Ask: $200,000 for 10% to expand manufacturing and retail distribution."
        ),
    },
    "PackMate — Subscription Food Kits": {
        "industry": "Consumer",
        "text": (
            "Problem: Busy consumers need healthy cooking solutions with minimal planning.\n\n"
            "Solution: PackMate delivers curated meal kits tailored to dietary preferences with minimal prep.\n\n"
            "Traction: 4k subs in metro market; 45% month-over-month growth.\n\n"
            "Business model: subscription; partnerships with ingredient brands.\n\n"
            "Ask: $350,000 for 9% to expand to three new cities."
        ),
    },
    "FitLoop — Home Fitness App": {
        "industry": "Consumer",
        "text": (
            "Problem: Home fitness apps have low long-term retention.\n\n"
            "Solution: FitLoop uses micro-challenges and social teams to keep users engaged daily.\n\n"
            "Traction: 50k downloads; 6% conversion to paid.\n\n"
            "Business model: subscriptions + brand sponsorships.\n\n"
            "Ask: $180,000 for 12% to improve retention features and partnerships."
        ),
    },

    # --- HealthTech samples
    "MediConnect — Telehealth Platform": {
        "industry": "HealthTech",
        "text": (
            "Problem: Patients in rural areas lack timely specialist access.\n\n"
            "Solution: MediConnect routes primary care cases to vetted specialists via teleconsultation and referrals.\n\n"
            "Traction: pilots with 6 clinics; positive patient satisfaction scores.\n\n"
            "Business model: per-visit revenue share with clinics.\n\n"
            "Ask: $500,000 for 8% to expand clinical integrations and compliance."
        ),
    },
    "CardioSense — Wearable ECG": {
        "industry": "HealthTech",
        "text": (
            "Problem: Early cardiac events are often missed by periodic checkups.\n\n"
            "Solution: CardioSense provides a low-cost wearable ECG and cloud analytics for early detection.\n\n"
            "Traction: clinical pilot with 120 patients; positive signal detection.\n\n"
            "Business model: device + subscription analytics.\n\n"
            "Ask: $750,000 for 10% to finish regulatory pathway and scale pilots."
        ),
    },
    "TheraTrack — Rehab Telemetry": {
        "industry": "HealthTech",
        "text": (
            "Problem: Rehab adherence and outcome tracking are poor.\n\n"
            "Solution: TheraTrack pairs simple wearables with therapist dashboards to measure exercises and outcomes.\n\n"
            "Traction: adopted by two outpatient networks; measurable adherence improvements.\n\n"
            "Business model: hardware + SaaS.\n\n"
            "Ask: $420,000 for 12% to scale manufacturing and sales."
        ),
    },

    # --- FinTech samples
    "Ledgerly — SMB Accounting AI": {
        "industry": "FinTech",
        "text": (
            "Problem: Small businesses struggle to reconcile finances cheaply.\n\n"
            "Solution: Ledgerly automates bookkeeping with AI and tax-ready reports.\n\n"
            "Traction: $28k ARR, pilot partnerships with small accounting firms.\n\n"
            "Business model: subscription + onboarding services.\n\n"
            "Ask: $300,000 for 10% to improve accuracy and distribution."
        ),
    },
    "MicroLoanX — Small Business Lending": {
        "industry": "FinTech",
        "text": (
            "Problem: Micro businesses lack access to fast, affordable capital.\n\n"
            "Solution: MicroLoanX uses alternative underwriting to offer short-term loans with transparent terms.\n\n"
            "Traction: $1.2M in originations with low default in pilot.\n\n"
            "Business model: lending margin + servicing.\n\n"
            "Ask: $1,000,000 for 7% to expand credit lines and underwriting."
        ),
    },
    "PayStream — Instant Payroll": {
        "industry": "FinTech",
        "text": (
            "Problem: Small employers face cashflow instability with rigid payroll cycles.\n\n"
            "Solution: PayStream enables on-demand pay and simplified payroll compliance.\n\n"
            "Traction: pilot with 250 employees; strong satisfaction.\n\n"
            "Business model: per-employee fee.\n\n"
            "Ask: $450,000 for 9% to scale HR integrations."
        ),
    },

    # --- Hardware samples
    "NanoCharge — Fast Charging Tech": {
        "industry": "Hardware",
        "text": (
            "Problem: Charging infrastructure is slow for modern devices.\n\n"
            "Solution: NanoCharge provides a novel power delivery module that reduces charge time by 40%.\n\n"
            "Traction: prototype and partner interest from 2 OEMs.\n\n"
            "Business model: component sales + licensing.\n\n"
            "Ask: $650,000 for 10% to finalize prototypes and start low-volume manufacturing."
        ),
    },
    "ClearSight — AR Glasses for Workers": {
        "industry": "Hardware",
        "text": (
            "Problem: Field technicians need hands-free access to instructions and measurements.\n\n"
            "Solution: ClearSight provides rugged AR glasses with enterprise workflow integration.\n\n"
            "Traction: successful pilot with logistics provider; improved task speed.\n\n"
            "Business model: device + SaaS.\n\n"
            "Ask: $1,200,000 for 12% to start production and certifications."
        ),
    },
    "HomeGuard — IoT Security Hub": {
        "industry": "Hardware",
        "text": (
            "Problem: Consumer home security is fragmented and expensive.\n\n"
            "Solution: HomeGuard integrates sensors, cameras, and monitoring into a single affordable hub.\n\n"
            "Traction: pre-orders from 800 households.\n\n"
            "Business model: hardware + subscription monitoring.\n\n"
            "Ask: $480,000 for 10% to scale manufacturing and support."
        ),
    },

    # --- EdTech samples
    "EduMind — Adaptive Learning": {
        "industry": "EdTech",
        "text": (
            "Problem: Students learn at different paces; classrooms can't personalize effectively.\n\n"
            "Solution: EduMind adapts lessons to each student's pace and provides teachers with actionable dashboards.\n\n"
            "Traction: pilot in 8 schools; improved test scores in pilot cohorts.\n\n"
            "Business model: school licensing + professional services.\n\n"
            "Ask: $350,000 for 10% to expand content and integrations."
        ),
    },
    "CourseCraft — Microcourse Platform": {
        "industry": "EdTech",
        "text": (
            "Problem: Professionals need bite-sized, job-relevant training.\n\n"
            "Solution: CourseCraft offers verified microcourses created with industry partners.\n\n"
            "Traction: partnerships with 3 industry bodies and pilot revenue.\n\n"
            "Business model: B2B licensing + per-learner fees.\n\n"
            "Ask: $220,000 for 12% to expand course catalog and sales."
        ),
    },
    "TutorLink — Peer Tutoring Marketplace": {
        "industry": "EdTech",
        "text": (
            "Problem: Students need affordable, flexible tutoring with vetted helpers.\n\n"
            "Solution: TutorLink matches vetted peer tutors with students and handles scheduling/payments.\n\n"
            "Traction: 3k signups, healthy match rates in pilot campus.\n\n"
            "Business model: commission per session.\n\n"
            "Ask: $150,000 for 12% to expand to new campuses."
        ),
    },

    # --- Other / Impact samples
    "CleanCity — Urban Waste Robotics": {
        "industry": "Other",
        "text": (
            "Problem: Urban waste collection is inefficient and costly.\n\n"
            "Solution: CleanCity deploys small autonomous robots for sidewalk and park cleanups, reducing manual costs.\n\n"
            "Traction: municipal pilot with daily routes; reduced litter metrics.\n\n"
            "Business model: municipal contracts + service fees.\n\n"
            "Ask: $900,000 for 10% to scale fleets and operations."
        ),
    },
    "GreenEnergy — Community Solar": {
        "industry": "Other",
        "text": (
            "Problem: Homeowners in dense areas can't access rooftop solar easily.\n\n"
            "Solution: GreenEnergy builds community solar arrays with subscription access for neighbors.\n\n"
            "Traction: one community launched with 120 subscribers.\n\n"
            "Business model: subscription + power purchase agreements.\n\n"
            "Ask: $1,100,000 for 8% to fund additional arrays and grid interconnects."
        ),
    },
    "EventPulse — Live Event Analytics": {
        "industry": "Other",
        "text": (
            "Problem: Event organizers lack real-time metrics to improve attendee experience.\n\n"
            "Solution: EventPulse aggregates sensor and app data to provide heatmaps, dwell time, and engagement metrics.\n\n"
            "Traction: pilot with 3 festivals; strong organizer interest.\n\n"
            "Business model: per-event licensing + analytics.\n\n"
            "Ask: $275,000 for 12% to productize sensors and dashboards."
        ),
    },
}

STRUCTURED_FORMAT = """
VERDICT: IN or OUT
SCORE: <number 1-10>
OFFER: <dollar amount or None>
EQUITY: <percent or N/A>
OPINION: <2-3 sentences>
STRENGTH: <one sentence>
CONCERN: <one sentence>
"""

if "pitch_history" not in st.session_state:
    st.session_state.pitch_history = []
if "last_session" not in st.session_state:
    st.session_state.last_session = None
if "negotiation" not in st.session_state:
    st.session_state.negotiation = {"shark": None, "messages": []}
if "accepted_deals" not in st.session_state:
    st.session_state.accepted_deals = set()
if "shark_vote" not in st.session_state:
    st.session_state.shark_vote = None
# removed auto-pitch/demo state to keep app professional and key-free


def parse_shark_response(text: str) -> dict:
    def grab(label: str, default: str = "") -> str:
        m = re.search(rf"{label}:\s*(.+?)(?=\n[A-Z]+:|\Z)", text, re.IGNORECASE | re.DOTALL)
        return m.group(1).strip() if m else default

    score_m = re.search(r"SCORE:\s*(\d+(?:\.\d+)?)", text, re.IGNORECASE)
    score = float(score_m.group(1)) if score_m else 5.0

    return {
        "raw": text,
        "verdict": "IN" if re.search(r"VERDICT:\s*IN\b", text, re.IGNORECASE) else "OUT",
        "score": max(1.0, min(10.0, score)),
        "offer": grab("OFFER", "None"),
        "equity": grab("EQUITY", "N/A"),
        "opinion": grab("OPINION", text[:280]),
        "strength": grab("STRENGTH"),
        "concern": grab("CONCERN"),
    }


def chat_completion(messages: list[dict]) -> str:
    # Local deterministic simulator with persona-aware responses.
    # Determine system persona (shark) if provided
    system_role = None
    for m in messages:
        if m.get("role") == "system":
            system_role = m.get("content", "")
            break

    # If this appears to be a negotiation (messages contain both assistant and user),
    # produce a short in-character conversational reply.
    roles = {m.get("role") for m in messages}
    if "assistant" in roles and "user" in roles and system_role:
        # negotiation reply (short, persona-specific)
        shark_name = re.search(r"You are (.+?),", system_role)
        shark = shark_name.group(1) if shark_name else "The Shark"
        persona = ""
        # attempt to map shark to persona from SHARKS
        for name, meta in SHARKS.items():
            if name in system_role:
                persona = meta.get("persona", "")
                break

        # craft a punchy persona reply
        user_msg = "".join([m.get("content", "") for m in messages if m.get("role") == "user"]).strip()
        if re.search(r"reduce|lower|cheaper|discount", user_msg, re.IGNORECASE):
            reply = f"{shark}: I'm intrigued, but I want better margins. Cut costs or I'll walk. Offer me a pilot deal first."
        elif re.search(r"equity|counter|less%|more%", user_msg, re.IGNORECASE):
            reply = f"{shark}: You're asking for a lot. I can offer capital plus distribution support — 50% of the ask for half your requested equity."
        else:
            # persona-flavored default
            if "Aggressive" in persona:
                reply = f"{shark}: Bold idea. I like scale and margins — show me unit economics and I'll write a cheque."
            elif "Tech-focused" in persona:
                reply = f"{shark}: Tech is promising. How defensible is the model? I back teams that can out-execute."
            elif "Marketing" in persona:
                reply = f"{shark}: Growth looks repeatable. Show me CAC payback and I'll consider a pilot."
            elif "Finance" in persona:
                reply = f"{shark}: Numbers look noisy; I need clean forecasts and runway plans."
            else:
                reply = f"{shark}: Interesting — I'd like to dig into the metrics before committing."

        return reply

    # Otherwise treat as an evaluation prompt and return structured fields
    user_content = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            user_content = m.get("content", "")
            break

    pitch_text = ""
    if "Pitch:" in user_content:
        pitch_text = user_content.split("\n\nPitch:\n")[-1]
    else:
        pitch_text = user_content

    # Heuristic scoring with persona flavor
    length = len(pitch_text)
    base = min(9.0, max(3.0, 3.0 + (length / 150)))
    bonus = 0
    if re.search(r"\b(users|MRR|revenue|traction|paid|sold|units)\b", pitch_text, re.IGNORECASE):
        bonus += 1.0
    score = round(min(10.0, base + bonus), 1)

    verdict = "IN" if score >= 5.5 or re.search(r"\b(pilot|paying|MRR|users|sold)\b", pitch_text, re.IGNORECASE) else "OUT"

    ask_m = re.search(r"\$(\d[\d,]*)", user_content)
    ask = int(ask_m.group(1).replace(",", "")) if ask_m else 250000
    equity_m = re.search(r"(\d+)%", user_content)
    equity = int(equity_m.group(1)) if equity_m else 10

    # persona-influenced offer
    shark_name = None
    if system_role:
        m = re.search(r"You are (.+?),", system_role)
        shark_name = m.group(1) if m else None

    if verdict == "IN":
        # base offer scales with ask and persona
        multiplier = 0.4
        if shark_name and "Mark" in shark_name:
            multiplier = 0.6
        if shark_name and "Elena" in shark_name:
            multiplier = 0.35
        offer_amount = max(10000, int(ask * multiplier))
        offer_str = f"${offer_amount:,}"
        equity_str = f"{min(50, max(1, int(equity * (1.0 + (multiplier - 0.3))))) }%"
    else:
        offer_str = "None"
        equity_str = "N/A"

    # Create a more creative opinion and lines tuned by persona
    opinion = ""
    if shark_name and "Sophia" in (shark_name or ""):
        opinion = "A bold tech play — defensibility and roadmap will decide this. Delight me with product moat." 
    elif shark_name and "Raj" in (shark_name or ""):
        opinion = "Great growth hooks — amplify the channel that already works and tighten acquisition costs."
    elif shark_name and "Elena" in (shark_name or ""):
        opinion = "Careful on margins; show me 24-month forecasts and the unit economics."
    else:
        opinion = "Interesting opportunity; solid traction will convert curiosity into checks."

    strength = "Clear problem-solution fit" if re.search(r"\b(problem|solution|traction|users|MRR)\b", pitch_text, re.IGNORECASE) else "Compelling concept"
    concern = "Needs unit economics and growth playbook" if score < 6 else "Watch dilution at current ask"

    return (
        f"VERDICT: {verdict}\n"
        f"SCORE: {score}\n"
        f"OFFER: {offer_str}\n"
        f"EQUITY: {equity_str}\n"
        f"OPINION: {opinion}\n"
        f"STRENGTH: {strength}\n"
        f"CONCERN: {concern}\n"
    )


def build_eval_prompt(name: str, persona: str, pitch: str, context: dict) -> str:
    return f"""You are {name} on Shark Tank.
Personality: {persona}

Startup: {context['startup_name']}
Industry: {context['industry']}
Founder asks: ${context['funding_ask']:,} for {context['equity_offered']}% equity
Tone intensity: {context['intensity']}/10 (10 = blunt TV drama)

Pitch:
{pitch}

Respond in EXACTLY this format (one line per field):
{STRUCTURED_FORMAT}
"""


# No external API handling is necessary for the local simulator.


# (Removed demo header and explanatory text to keep the sidebar minimal.)

# --- Sidebar: Pitch settings ---
st.sidebar.header("🎤 Your pitch")
# Show Startup name first, then Industry
startup_name = st.sidebar.text_input("Startup name", value="My Startup")
industry = st.sidebar.selectbox(
    "Industry",
    ["SaaS", "Consumer", "HealthTech", "FinTech", "Hardware", "Food & Bev", "EdTech", "AgTech", "Other"],
    index=0,
)
funding_ask = st.sidebar.slider("Funding ask ($)", 10_000, 2_000_000, 250_000, 10_000)
equity_offered = st.sidebar.slider("Equity offered (%)", 1, 50, 10)
intensity = st.sidebar.slider("Shark intensity 🎭", 1, 10, 7)
selected_sharks = st.sidebar.multiselect(
    "Sharks in the tank",
    list(SHARKS.keys()),
    default=list(SHARKS.keys()),
)

with st.sidebar.expander("📋 Sample pitches"):
    # Visual gallery: filter samples strictly by selected industry
    filtered = [k for k, v in SAMPLE_PITCHES.items() if v.get("industry") == industry]
    display_list = filtered
    if not display_list:
        st.info("No sample pitches available for the selected industry.")
    else:
        # Arrange two per row
        for i in range(0, len(display_list), 2):
            cols = st.columns(2)
            for j, name in enumerate(display_list[i : i + 2]):
                with cols[j]:
                    # compact text-only card (no images)
                    st.markdown(f"**{name}**")
                    st.caption(SAMPLE_PITCHES[name].get("industry", ""))
                    if st.button("Use", key=f"use_{name}"):
                        st.session_state.sample_pitch = SAMPLE_PITCHES[name]
                        st.session_state.sample_choice = name
                        st.rerun()
    st.markdown("---")
    if st.button("Use my own pitch"):
        st.session_state.sample_pitch = None
        st.session_state.sample_choice = None
        st.rerun()

    # removed one-click demo to keep the interface professional

# Title (hero removed to avoid images and deprecation warnings)
st.title("🦈 AI Shark Tank")
st.caption("Pitch · get scored · negotiate deals · climb the leaderboard")

tab_pitch, tab_results, tab_negotiate, tab_history = st.tabs(
    ["🎤 Pitch", "📊 Results", "💬 Negotiate", "📜 History"]
)

pitch_context = {
    "startup_name": startup_name,
    "industry": industry,
    "funding_ask": funding_ask,
    "equity_offered": equity_offered,
    "intensity": intensity,
}

default_pitch = st.session_state.get("sample_pitch", "")
metrics_cols = st.columns(4)
metrics_cols[0].metric("Ask", f"${funding_ask:,}")
metrics_cols[1].metric("Equity", f"{equity_offered}%")
metrics_cols[2].metric("Implied val.", f"${funding_ask * 100 // max(equity_offered, 1):,}")
metrics_cols[3].metric("Sharks", len(selected_sharks))

with tab_pitch:
    # If a sample was loaded, populate the pitch box
    sample_loaded = st.session_state.get("sample_pitch")
    if sample_loaded and isinstance(sample_loaded, dict):
        txt = sample_loaded.get("text", "")
        pitch = st.text_area(
            "Your pitch",
            value=txt,
            height=220,
            placeholder="Problem, solution, traction, business model, and what you're asking for...",
        )
    else:
        pitch = st.text_area(
            "Your pitch",
            value=default_pitch,
            height=180,
            placeholder="Problem, solution, traction, business model, and what you're asking for...",
        )

    col_go, col_clear = st.columns([1, 1])
    pitch_now = col_go.button("🦈 Pitch to the Sharks", type="primary", use_container_width=True)
    if col_clear.button("Clear session", use_container_width=True):
        st.session_state.last_session = None
        st.session_state.accepted_deals = set()
        st.session_state.shark_vote = None
        st.session_state.negotiation = {"shark": None, "messages": []}
        st.rerun()

    if pitch_now:
        if not pitch.strip():
            st.error("Write your pitch first.")
        elif not selected_sharks:
            st.error("Select at least one shark in the sidebar.")
        else:
            results = {}
            progress = st.progress(0, text="Sharks are deliberating...")
            status = st.empty()

            for i, name in enumerate(selected_sharks):
                meta = SHARKS[name]
                status.markdown(f"**{meta['emoji']} {name}** is reviewing your pitch...")
                prompt = build_eval_prompt(name, meta["persona"], pitch, pitch_context)
                try:
                    raw = chat_completion([
                        {"role": "system", "content": f"You are {name}, a Shark Tank investor."},
                        {"role": "user", "content": prompt},
                    ])
                    parsed = parse_shark_response(raw)
                except Exception as exc:
                    st.error(f"Evaluation failed: {exc}")
                    st.stop()

                results[name] = {**parsed, "emoji": meta["emoji"]}
                progress.progress((i + 1) / len(selected_sharks), text=f"{i + 1}/{len(selected_sharks)} sharks responded")

            status.empty()
            progress.empty()

            investors = [n for n, r in results.items() if r["verdict"] == "IN"]
            avg_score = sum(r["score"] for r in results.values()) / len(results)

            session = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "startup": startup_name,
                "pitch": pitch,
                "context": pitch_context,
                "results": results,
                "investors": investors,
                "avg_score": avg_score,
            }
            st.session_state.last_session = session
            st.session_state.accepted_deals = set()
            st.session_state.shark_vote = None
            st.session_state.pitch_history.insert(0, session)
            st.session_state.pitch_history = st.session_state.pitch_history[:10]

            if investors:
                st.balloons()
            st.success(f"Session complete — {len(investors)}/{len(selected_sharks)} sharks want in!")
            st.rerun()

with tab_results:
    session = st.session_state.last_session
    if not session:
        st.info("Pitch first on the **🎤 Pitch** tab to see results here.")
    else:
        results = session["results"]
        investors = session["investors"]
        n = len(results)

        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Avg. score", f"{session['avg_score']:.1f}/10")
        s2.metric("Offers", len(investors))
        s3.metric("Passes", n - len(investors))
        s4.metric("Startup", session["startup"])

        st.subheader("Who's in?")
        for name, data in results.items():
            verdict_icon = "✅" if data["verdict"] == "IN" else "❌"
            # Creative card header
            header = f"{data['emoji']} {name} — {verdict_icon} {data['verdict']} · Score {data['score']:.0f}/10"
            with st.expander(header):
                cols = st.columns([1, 3])
                with cols[0]:
                    st.markdown(f"### {data['emoji']} {name}")
                    st.metric("Score", f"{data['score']:.1f}/10")
                with cols[1]:
                    st.markdown(f"**Offer:** {data['offer']}  •  **Equity:** {data['equity']}")
                    st.markdown(f"**Quick take:** {data['opinion']}")
                    if data["strength"]:
                        st.success(f"💪 Strength: {data['strength']}")
                    if data["concern"]:
                        st.warning(f"⚠️ Concern: {data['concern']}")

                # Accept checkbox
                if data["verdict"] == "IN":
                    accepted = st.checkbox(
                        f"Accept {name}'s deal",
                        value=name in st.session_state.accepted_deals,
                        key=f"accept_{name}",
                    )
                    if accepted:
                        st.session_state.accepted_deals.add(name)
                    else:
                        st.session_state.accepted_deals.discard(name)

                # creative full response area
                st.markdown("**Full response (raw):**")
                st.code(data["raw"][:1000])

        if st.session_state.accepted_deals:
            st.divider()
            st.subheader("🤝 Deals you accepted")
            for name in st.session_state.accepted_deals:
                d = results[name]
                st.markdown(f"- **{name}**: {d['offer']} for {d['equity']}")

        st.divider()
        st.subheader("🏆 Vote: best shark feedback")
        vote_cols = st.columns(len(results))
        for col, name in zip(vote_cols, results.keys()):
            if col.button(name, key=f"vote_{name}", use_container_width=True):
                st.session_state.shark_vote = name
        if st.session_state.shark_vote:
            st.caption(f"You voted for **{st.session_state.shark_vote}**")

with tab_negotiate:
    session = st.session_state.last_session
    if not session:
        st.info("Complete a pitch first, then negotiate with sharks who said **IN**.")
    else:
        investors = session["investors"]
        if not investors:
            st.warning("No sharks offered a deal — refine your pitch and try again.")
        else:
            shark_pick = st.selectbox("Negotiate with", investors)
            if st.session_state.negotiation.get("shark") != shark_pick:
                st.session_state.negotiation = {
                    "shark": shark_pick,
                    "messages": [
                        {
                            "role": "assistant",
                            "content": session["results"][shark_pick]["raw"],
                        }
                    ],
                }
            # display negotiation messages in chat-like bubbles with timestamps
            for msg in st.session_state.negotiation["messages"]:
                who = "Shark" if msg["role"] == "assistant" else "You"
                ts = datetime.now().strftime("%H:%M")
                if msg["role"] == "assistant":
                    st.info(f"{who} ({ts}):  \n\n{msg['content']}")
                else:
                    st.write(f"**{who} ({ts}):** {msg['content']}")

            counter = st.chat_input(f"Counter-offer to {shark_pick}...")
            if counter:
                st.session_state.negotiation["messages"].append({"role": "user", "content": counter})
                persona = SHARKS[shark_pick]["persona"]
                history = [
                    {
                        "role": "system",
                        "content": (
                            f"You are {shark_pick} on Shark Tank. {persona} "
                            f"Stay in character. You already evaluated {session['startup']}. "
                            "Negotiate deal terms — be tough but fair. Keep replies under 140 words."
                        ),
                    },
                ]
                for m in st.session_state.negotiation["messages"]:
                    role = "assistant" if m["role"] == "assistant" else "user"
                    history.append({"role": role, "content": m["content"]})
                try:
                    reply = chat_completion(history)
                except Exception as exc:
                    st.error(f"Negotiation failed: {exc}")
                    st.stop()
                # append with persona flair
                st.session_state.negotiation["messages"].append({"role": "assistant", "content": reply})
                st.rerun()

with tab_history:
    history = st.session_state.pitch_history
    if not history:
        st.info("Your last 10 pitches will appear here.")
    else:
        for i, entry in enumerate(history):
            inv = len(entry["investors"])
            total = len(entry["results"])
            with st.expander(
                f"{entry['time']} — {entry['startup']} ({inv}/{total} offers · {entry['avg_score']:.1f}/10)"
            ):
                st.caption(entry["pitch"][:300] + ("..." if len(entry["pitch"]) > 300 else ""))
                if st.button("Reload this pitch", key=f"reload_{i}"):
                    st.session_state.sample_pitch = entry["pitch"]
                    st.session_state.last_session = entry
                    st.rerun()
