import flet as ft
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import re

# ===== TEAM BRANDING - YOUR BRAND! =====
TEAM_NAME = "Team SafeRand — Keep Your Rand Safe"
TEAM_SLOGAN = "Keep Your Rand Safe - Anywhere in SA!"
SAFERAND_BLUE = "#003366"
SAFERAND_LIGHT_BLUE = "#00A9CE"
SAFERAND_BLUE2 = "#1976D2"
DISCLAIMER = "SafeRand is independent, not affiliated with any bank. Supports all SA banks."

BANKS = {"SafeRand":"0800 123 4567","Capitec":"0860 10 20 43","Absa":"0860 557 557","Standard Bank":"0800 020 600","Nedbank":"0800 110 929","TymeBank":"0860 999 119","SASSA":"0800 60 10 11"}
USERS = {"test@test.com": {"full_name":"Test User","email":"test@test.com","phone":"0821234567","id_number":"8001015009087","bank":"SafeRand","password":"123456","location":"Gauteng"}}
CURRENT_USER = {"email": None}

SCAMMERS = [
    {"number": "087 230 1234", "type": "SMS", "subtype": "Bank Fake SMS", "location": "Local Mall", "area": "Your Area", "distance": "0.3km", "reports": 18, "risk": "HIGH"},
    {"number": "079 123 4567", "type": "Call", "subtype": "OTP Scam", "location": "Taxi Rank", "area": "Your Area", "distance": "0.6km", "reports": 11, "risk": "HIGH"},
    {"number": "060 987 6543", "type": "Loan", "subtype": "Mashonisa Loan Shark", "location": "Near Shops", "area": "Your Area", "distance": "0.5km", "reports": 25, "risk": "HIGH"},
    {"number": "081 555 9999", "type": "Job", "subtype": "Fake Job Offer", "location": "Shopping Centre", "area": "Nearby", "distance": "1.2km", "reports": 9, "risk": "MEDIUM"},
    {"number": "073 222 3333", "type": "SMS", "subtype": "Prize Win Scam", "location": "Local Area", "area": "Nearby", "distance": "1.5km", "reports": 15, "risk": "MEDIUM"},
    {"number": "082 111 2222", "type": "SMS", "subtype": "SASSA Fake SMS", "location": "Community", "area": "Nearby", "distance": "2.0km", "reports": 30, "risk": "HIGH"},
]

SAFE_PLACES = [
    {"name": "SafeRand Verified Safe Branch", "type": "Bank", "area": "Your Area", "distance": "0.4km"},
    {"name": "Bank Branch - Nearest", "type": "Bank", "area": "Your Area", "distance": "0.8km"},
    {"name": "SAPS - Police Station", "type": "Police", "area": "Your Area", "distance": "1.1km"},
    {"name": "Shoprite / Pick n Pay - Verified Safe", "type": "Shop", "area": "Your Area", "distance": "0.5km"},
    {"name": "Clinic / Hospital - Safe Zone", "type": "Clinic", "area": "Nearby", "distance": "1.3km"},
]

def main(page: ft.Page):
    page.title = f"SafeRand - {TEAM_NAME}"
    page.padding = 12
    page.bgcolor = "#E3F2FD"
    page.scroll = ft.ScrollMode.AUTO

    # Login fields
    login_email = ft.TextField(label="📧 Email", width=340, border_color=SAFERAND_BLUE)
    login_pass = ft.TextField(label="🔒 Password", width=340, password=True, can_reveal_password=True, border_color=SAFERAND_BLUE)
    login_msg = ft.Text("", color="red", size=11)

    # Register fields
    reg_name = ft.TextField(label="👤 Full Name", width=340, border_color=SAFERAND_BLUE)
    reg_email = ft.TextField(label="📧 Email", width=340, border_color=SAFERAND_BLUE)
    reg_phone = ft.TextField(label="📱 Phone", width=340, border_color=SAFERAND_BLUE)
    reg_id = ft.TextField(label="🆔 SA ID (13 digits)", width=340, keyboard_type=ft.KeyboardType.NUMBER, max_length=13, border_color=SAFERAND_BLUE)
    reg_location = ft.Dropdown(label="📍 Province / City", value="Gauteng", width=340, border_color=SAFERAND_BLUE, options=[ft.dropdown.Option("Gauteng"), ft.dropdown.Option("KwaZulu-Natal"), ft.dropdown.Option("Western Cape"), ft.dropdown.Option("Eastern Cape"), ft.dropdown.Option("Limpopo"), ft.dropdown.Option("Mpumalanga"), ft.dropdown.Option("North West"), ft.dropdown.Option("Free State"), ft.dropdown.Option("Northern Cape")])
    reg_bank = ft.Dropdown(label="🏦 Your Bank", value="SafeRand", width=340, border_color=SAFERAND_BLUE, options=[ft.dropdown.Option(k) for k in BANKS.keys()])
    reg_pass = ft.TextField(label="🔒 Password", width=340, password=True, can_reveal_password=True, border_color=SAFERAND_BLUE)
    reg_pass2 = ft.TextField(label="🔒 Confirm Password", width=340, password=True, can_reveal_password=True, border_color=SAFERAND_BLUE)
    reg_msg = ft.Text("", color="red", size=11)

    content = ft.Column([], expand=True)

    def build_app():
        user = USERS.get(CURRENT_USER["email"], {})
        user_area = user.get("location", "Gauteng")

        # ===== HEADER - SAFERAND BLUE - NO FNB =====
        header = ft.Container(
            padding=14,
            border_radius=16,
            bgcolor=SAFERAND_BLUE,
            content=ft.Column([
                ft.Row([
                    ft.Container(padding=8, border_radius=20, bgcolor="white", content=ft.Text("🛡️", size=24)),
                    ft.Column([
                        ft.Text("SafeRand ULTIMATE", size=18, weight="bold", color="white"),
                        ft.Text(TEAM_NAME, size=11, weight="bold", color=SAFERAND_LIGHT_BLUE),
                        ft.Text(f"{TEAM_SLOGAN} | SafeRand Blue", size=8, color="#BBDEFB"),
                    ], spacing=1),
                    ft.Container(padding=6, border_radius=20, bgcolor=SAFERAND_LIGHT_BLUE, content=ft.Text("SafeRand", size=10, weight="bold", color="white"))
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(padding=6, border_radius=8, bgcolor="#0D47A1", content=ft.Text(f"👤 {user.get('full_name','')} | 📍 {user_area} | 🆔 {user.get('id_number','')[:6]}*** | 🛡️ Protected", size=9, color="white")),
            ])
        )

        # ===== 1. CHECKER - COMPLETE =====
        checker_bank = ft.Dropdown(label="My Bank", value=user.get("bank","SafeRand"), width=340, border_color=SAFERAND_BLUE, options=[ft.dropdown.Option(k) for k in BANKS.keys()])
        checker_fraud = ft.Text(f"Fraud: {BANKS[checker_bank.value]}", color="#E91E63", weight="bold", size=12)
        def upd_fraud(e): checker_fraud.value = f"Fraud: {BANKS[checker_bank.value]}"; page.update()
        checker_bank.on_change = upd_fraud
        sms_input = ft.TextField(label="Paste SMS or suspicious number", width=340, multiline=True, border_color=SAFERAND_BLUE)
        result = ft.Container(padding=14, border_radius=12, bgcolor="#BBDEFB", content=ft.Text(f"Welcome {user.get('full_name','')}! ID verified: {user.get('id_number','')[:6]}*** | {user_area} | SafeRand Blue protects you!", size=11, color=SAFERAND_BLUE))
        def do_check(e):
            txt = sms_input.value.lower()
            if not txt: result.bgcolor="#FFF9C4"; result.content=ft.Text("Paste SMS first!", size=11)
            elif any(w in txt for w in ["click","http","otp","prize","blocked","won","verify","urgent","sassa"]):
                result.bgcolor="#FFCDD2"; result.content=ft.Column([ft.Text("🚨 SCAM DETECTED! - SafeRand Blue", color="red", weight="bold", size=13), ft.Text(f"Don't click! Call {BANKS[checker_bank.value]} now! Broad SA protection!", color="red", size=11), ft.FilledButton(f"Call {checker_bank.value}: {BANKS[checker_bank.value]}", bgcolor="#D32F2F", color="white", width=300)])
            elif len(re.sub(r'[^0-9]','',txt))>=10 and len(txt)<20:
                if "0872301234" in txt.replace(" ",""): result.bgcolor="#FFCDD2"; result.content=ft.Text(f"🚨 SCAMMER NUMBER! {txt} - 18 reports near you! SafeRand Blue blocked!", color="red", weight="bold")
                else: result.bgcolor="#FFF9C4"; result.content=ft.Text(f"⚠️ Unknown {txt} - Be careful! Keep Your Rand Safe! SafeRand Blue!", size=11)
            else: result.bgcolor="#BBDEFB"; result.content=ft.Text("✅ Looks Safe! No scam words! SafeRand Blue - Keep Your Rand Safe!", color=SAFERAND_BLUE, weight="bold")
            page.update()
        def panic(e):
            u = USERS[CURRENT_USER["email"]]; result.bgcolor="#B71C1C"; result.content=ft.Column([ft.Text("🚨 PANIC MODE - ID VERIFIED - SafeRand Blue!", color="white", weight="bold", size=13), ft.Text(f"👤 {u['full_name']} | 🆔 {u['id_number']} | 📍 {u['location']}", color="white", size=11), ft.Text(f"🏦 {u['bank']} Fraud: {BANKS[u['bank']]}", color="white", weight="bold"), ft.Text("✅ Bank can verify you instantly! SafeRand Blue - Anywhere SA!", color="yellow", weight="bold"), ft.FilledButton(f"CALL {u['bank']} NOW: {BANKS[u['bank']]}", bgcolor="white", color="red", width=300)]); page.update()
        checker_page = ft.Column([ft.Row([ft.Icon(ft.Icons.SHIELD, color=SAFERAND_BLUE, size=28), ft.Text(f"SafeRand Checker - {user.get('full_name','')}", weight="bold", color=SAFERAND_BLUE)]), checker_bank, checker_fraud, sms_input, ft.Row([ft.FilledButton("CHECK NOW - SafeRand!", icon=ft.Icons.SEARCH, bgcolor=SAFERAND_BLUE, color="white", width=170, height=45, on_click=do_check), ft.FilledButton("📷 SCAN", bgcolor=SAFERAND_LIGHT_BLUE, color="white", width=90, on_click=lambda e: do_check(e))], wrap=True), ft.FilledButton("🚨 SHAKE PANIC - USES ID - SafeRand Blue!", icon=ft.Icons.WARNING, bgcolor="#E91E63", color="white", width=340, height=45, on_click=panic), result, ft.Container(padding=10, border_radius=12, bgcolor="white", content=ft.Column([ft.Text("💡 SafeRand Blue - How to check:", weight="bold", size=11, color=SAFERAND_BLUE), ft.Text("1. Paste SMS\n2. Or paste unknown number\n3. Click CHECK\n4. Uses 0872301234 test scammer\n5. Panic uses your ID for verification\nWorks anywhere SA - Broad SA!", size=10)]))], scroll=ft.ScrollMode.AUTO)

        # ===== 2. LEARN - COMPLETE =====
        learn_result = ft.Container(padding=12, border_radius=12, bgcolor="#E3F2FD", content=ft.Text("Select scam type to learn - SafeRand Blue - Anywhere SA!", size=11, color=SAFERAND_BLUE))
        def show_learn(t):
            d = {"Phishing":"📧 PHISHING - SafeRand Blue\n\nWhat: Fake bank SMS 'Click link blocked!'\nExample: 'Bank: blocked, click secure-bank.co.za'\n\nSpot: Link not real bank, urgent, asks OTP\n\nDo: NEVER click! Call bank from app! Delete! Report on SafeRand Map!", "Vishing":"📞 VISHING - SafeRand Blue\n\nWhat: Caller 'I'm from bank fraud, give OTP!'\n\nSpot: Bank NEVER asks OTP phone!\n\nDo: Hang up! Call fraud line yourself! SafeRand Blue!", "SIM Swap":"📱 SIM SWAP - SafeRand Blue\n\nWhat: Scammer gets new SIM your number\nSign: Phone 'No Service'\n\nDo: Call network, call bank stop, go branch with ID - anywhere SA! SafeRand Blue!", "Smishing":"💬 JOB/PRIZE - SafeRand Blue\n\nWhat: 'You WON R50k! Pay R200 fee!' or 'Job pay R500!'\n\nSpot: Asks fee upfront, too good\n\nDo: Real jobs NEVER ask fee! Report! SafeRand Blue - Keep Rand Safe!"}
            learn_result.content=ft.Text(d.get(t,""), size=11); page.update()
        learn_page = ft.Column([ft.Text("📚 Learn Scams - SafeRand Blue - Broad SA", size=18, weight="bold", color=SAFERAND_BLUE), ft.Row([ft.FilledButton("📧 Phishing", bgcolor="#D32F2F", color="white", width=75, on_click=lambda e: show_learn("Phishing")), ft.FilledButton("📞 Vishing", bgcolor=SAFERAND_BLUE, color="white", width=75, on_click=lambda e: show_learn("Vishing")), ft.FilledButton("📱 SIM Swap", bgcolor="#FF9800", color="white", width=75, on_click=lambda e: show_learn("SIM Swap")), ft.FilledButton("💬 Job/Prize", bgcolor=SAFERAND_LIGHT_BLUE, color="white", width=75, on_click=lambda e: show_learn("Smishing"))], wrap=True), learn_result, ft.Container(padding=12, border_radius=12, bgcolor="#BBDEFB", content=ft.Column([ft.Text("🛡️ Golden Rules - SafeRand Blue:", weight="bold", size=12, color=SAFERAND_BLUE), ft.Text("1. Bank NEVER asks OTP/PIN phone/SMS\n2. Never click link - go to bank app\n3. If 'You WON!' = SCAM!\n4. Check number on SafeRand Map\n5. Works anywhere SA - SafeRand Blue!", size=11, color=SAFERAND_BLUE)]))], scroll=ft.ScrollMode.AUTO)

        # ===== 3. HELP - COMPLETE =====
        help_bank = ft.Dropdown(label="Choose Bank", value=user.get("bank","SafeRand"), width=340, border_color=SAFERAND_BLUE, options=[ft.dropdown.Option(k) for k in BANKS.keys()])
        help_num = ft.Text(BANKS[help_bank.value], size=32, weight="bold", color="white")
        help_name = ft.Text(f"{help_bank.value} Fraud Line - SafeRand Blue", size=12, color="white")
        help_box = ft.Container(ft.Column([ft.Text("🚨 CALL FRAUD NOW - 24hrs - SafeRand Blue - Anywhere SA:", size=11, color="white"), help_name, help_num]), bgcolor=SAFERAND_BLUE, padding=15, border_radius=12, width=340)
        def upd_h(e): help_num.value=BANKS[help_bank.value]; help_name.value=f"{help_bank.value} Fraud Line - SafeRand Blue"; page.update()
        help_bank.on_change = upd_h
        help_page = ft.Column([ft.Text("🆘 Emergency Help - SafeRand Blue - Broad SA", size=18, weight="bold", color=SAFERAND_BLUE), help_bank, ft.FilledButton("SHOW NUMBER - SafeRand Blue", bgcolor=SAFERAND_BLUE, color="white", width=340, on_click=upd_h), help_box, ft.Container(padding=12, border_radius=12, bgcolor="#BBDEFB", content=ft.Column([ft.Text("Other Emergency - SafeRand Blue - Anywhere SA:", weight="bold", size=12, color=SAFERAND_BLUE), ft.Text(f"👮 SAPS: 10111\n🚑 Ambulance: 10177\n📱 MTN: 083 123\n📱 Vodacom: 082 135\n🛡️ SafeRand: {BANKS['SafeRand']}\nWorks anywhere SA - SafeRand Blue!", size=11, color=SAFERAND_BLUE)]))], scroll=ft.ScrollMode.AUTO)

        # ===== 4. AI - COMPLETE =====
        ai_input = ft.TextField(label="Ask AI: e.g. Is 087 230 1234 scam? - SafeRand Blue", width=340, border_color=SAFERAND_BLUE)
        ai_result = ft.Container(padding=12, border_radius=12, bgcolor="#E3F2FD", content=ft.Text("🤖 SafeRand Blue AI ready! Broad SA! Ask English, Zulu, Sotho! Anywhere SA!", size=11, color=SAFERAND_BLUE))
        def ask_ai(e):
            q=ai_input.value.lower()
            if not q: ai_result.content=ft.Text("Type question first!", size=11); page.update(); return
            if "087 230" in q or "scam" in q: ans="🚨 087 230 1234 is SCAM! 18 reports near you! SafeRand Blue! Don't answer! Block! Call fraud line!"
            elif "sassa" in q and "otp" in q: ans="⚠️ SASSA NEVER asks OTP! If 'SASSA blocked give OTP' = SCAM! Real SASSA: 0800 60 10 11. Delete! SafeRand Blue!"
            elif "job" in q: ans="💼 Job scam: Real bank NEVER asks R200 fee! If 'Pay R500 training' = SCAM! SafeRand Blue - Keep Rand Safe!"
            else: ans=f"🤖 SafeRand Blue AI: You asked '{ai_input.value}'. Check Map. If SMS with link, DON'T click! Call bank official! Works anywhere SA! Keep Rand Safe! SafeRand Blue!"
            ai_result.content=ft.Text(ans, size=11, color=SAFERAND_BLUE); page.update()
        ai_page = ft.Column([ft.Text("🤖 AI Assistant - SafeRand Blue Expert - Broad SA", size=16, weight="bold", color=SAFERAND_BLUE), ai_input, ft.FilledButton("Ask AI - SafeRand Blue", bgcolor=SAFERAND_BLUE, color="white", width=340, on_click=ask_ai), ai_result], scroll=ft.ScrollMode.AUTO)

        # ===== 5. BUDGET - COMPLETE - CLEAN CARDS =====
        selected_job = {"value": "SASSA Grant Only"}
        income = ft.TextField(label="💰 Monthly Income", width=160, value="3500", border_color=SAFERAND_BLUE, keyboard_type=ft.KeyboardType.NUMBER)
        expenses = ft.TextField(label="💸 Monthly Expenses", width=160, value="2500", border_color=SAFERAND_BLUE, keyboard_type=ft.KeyboardType.NUMBER)
        saved = ft.TextField(label="💎 Already Saved", width=160, value="0", border_color=SAFERAND_BLUE, keyboard_type=ft.KeyboardType.NUMBER)
        goal = ft.TextField(label="🎯 Savings Goal", width=160, value="5000", border_color=SAFERAND_BLUE, keyboard_type=ft.KeyboardType.NUMBER)
        job_cards = ft.Column([])
        result_box = ft.Container(padding=14, border_radius=16, bgcolor="#BBDEFB", visible=False)
        advice_box = ft.Container(padding=14, border_radius=16, bgcolor="#E8F5E9", visible=False)
        def select_job(job_name):
            selected_job["value"]=job_name
            for card in job_cards.controls: card.bgcolor="#BBDEFB" if card.data==job_name else "#FFFFFF"
            page.update()
        def make_job_card(emoji,title,subtitle):
            bg="#BBDEFB" if selected_job["value"]==title else "#FFFFFF"
            return ft.Container(data=title, padding=12, border_radius=12, bgcolor=bg, content=ft.Row([ft.Text(emoji,size=24), ft.Column([ft.Text(title,weight="bold",size=12,color=SAFERAND_BLUE), ft.Text(subtitle,size=10,color="grey")])]), on_click=lambda e,t=title: select_job(t))
        job_cards.controls=[make_job_card("👵","SASSA Grant Only","3500 grant - SafeRand Blue"), make_job_card("🚕","Taxi Driver - Paying Owner","Paying owner - SafeRand Blue"), make_job_card("🚕","Taxi Driver - Own Taxi","Own taxi - SafeRand Blue"), make_job_card("💼","Formal Worker - Salary","Salary - SafeRand Blue"), make_job_card("🛒","Trader / Hawker","Sales - SafeRand Blue"), make_job_card("🎓","Student / Unemployed","NSFAS - SafeRand Blue")]
        def calculate(e):
            try:
                inc=float(income.value or 0); exp=float(expenses.value or 0); sav=float(saved.value or 0); g=float(goal.value or 0); remain=inc-exp; pct=(sav/g*100) if g>0 else 0; bar="█"*int(pct/10)+"░"*(10-int(pct/10)); result_box.visible=True; result_box.bgcolor="#BBDEFB" if remain>=0 else "#FFCDD2"; result_box.content=ft.Column([ft.Text(f"📊 {selected_job['value']} - SafeRand Blue", weight="bold", size=13, color=SAFERAND_BLUE), ft.Text(f"💰 Income R{inc:.0f} | Expenses R{exp:.0f} | Left R{remain:.0f}", size=11, color=SAFERAND_BLUE), ft.Text(f"💎 Saved R{sav:.0f} / Goal R{g:.0f} = {pct:.0f}% [{bar}] - SafeRand Blue!", weight="bold", color=SAFERAND_BLUE)]); advice_box.visible=True; advice_box.content=ft.Column([ft.Text(f"🎯 SafeRand Blue: Save R{remain*0.3:.0f} monthly! 50/30/20 rule: Needs R{inc*0.5:.0f} Wants R{inc*0.3:.0f} Save R{inc*0.2:.0f} - Broad SA!", size=11, color=SAFERAND_BLUE)]); page.update()
            except: pass
        budget_page = ft.Column([ft.Text("💙 Smart Budget - SafeRand Blue - Keep Rand Safe Anywhere", size=18, weight="bold", color=SAFERAND_BLUE), ft.Container(padding=12, border_radius=16, bgcolor="white", content=ft.Column([ft.Text("STEP 1: What do you do? - SafeRand Blue", weight="bold", color=SAFERAND_BLUE), job_cards])), ft.Container(padding=12, border_radius=16, bgcolor="white", content=ft.Column([ft.Text("STEP 2: Your Money - SafeRand Blue", weight="bold", color=SAFERAND_BLUE), ft.Row([income, expenses], wrap=True), ft.Row([saved, goal], wrap=True)])), ft.FilledButton("💎 CALCULATE MY PLAN - SafeRand Blue", bgcolor=SAFERAND_BLUE, color="white", width=340, height=48, on_click=calculate), result_box, advice_box], scroll=ft.ScrollMode.AUTO)

        # ===== 6. MAP - COMPLETE - BROAD SA =====
        location_on = {"value": False}
        current_area = {"value": user_area}
        area_dropdown = ft.Dropdown(label="📍 Filter", value="Your Area", width=150, border_color=SAFERAND_BLUE, options=[ft.dropdown.Option("Your Area"), ft.dropdown.Option("Nearby"), ft.dropdown.Option("All Areas")])
        location_text = ft.Text(f"📍 Location: OFF - Turn ON for {user_area} - SafeRand Blue!", size=11, color="grey", weight="bold")
        location_switch = ft.Switch(label="Location ON/OFF - SafeRand Blue - Broad SA", value=False, active_color=SAFERAND_BLUE)
        search_status = ft.Text("", size=11, color=SAFERAND_BLUE)
        map_visual = ft.Container(padding=10, border_radius=16, bgcolor="#BBDEFB", height=180, content=ft.Column([ft.Row([ft.Icon(ft.Icons.MAP, color=SAFERAND_BLUE), ft.Text(f"SafeRand Blue Map - {current_area['value']} - Broad SA", weight="bold", size=12, color=SAFERAND_BLUE)]), ft.Text(f"📍 You: {current_area['value']} - SafeRand Blue Protection Anywhere SA", size=11, weight="bold", color=SAFERAND_BLUE), ft.Row([ft.Container(padding=5, border_radius=20, bgcolor="#D32F2F", content=ft.Text("🔴 HIGH: 3 scams 0.3km", size=8, color="white")), ft.Container(padding=5, border_radius=20, bgcolor="#4CAF50", content=ft.Text("🟢 SAFE: Branch/SAPS near", size=8, color="white"))], wrap=True), ft.Text("Broad SA: Works all provinces! SafeRand Blue - Keep Rand Safe!", size=9, color=SAFERAND_BLUE, weight="bold")]))
        from_dd = ft.Dropdown(label="📍 From", value="Your Location", width=165, border_color=SAFERAND_BLUE, options=[ft.dropdown.Option("Your Location"), ft.dropdown.Option("Home"), ft.dropdown.Option("Work"), ft.dropdown.Option("Mall")])
        to_dd = ft.Dropdown(label="🏁 To", value="SafeRand Verified Safe Branch", width=165, border_color=SAFERAND_BLUE, options=[ft.dropdown.Option(p["name"]) for p in SAFE_PLACES])
        route_result = ft.Container(padding=12, border_radius=16, bgcolor="#FFF9C4", visible=False)
        def calculate_safe_route(e):
            if not location_on["value"]: route_result.visible=True; route_result.content=ft.Text("❌ Turn Location ON - SafeRand Blue!", color="red", weight="bold"); page.update(); return
            route_result.visible=True; route_result.bgcolor="#BBDEFB"; route_result.content=ft.Column([ft.Text("✅ SAFE ROUTE - SafeRand Blue - Keep Rand Safe!", weight="bold", size=12, color=SAFERAND_BLUE), ft.Text(f"{from_dd.value} → {to_dd.value} | 0.8km | 95% SAFE | SafeRand Blue!", size=11, color=SAFERAND_BLUE), ft.Text("1. Main road (avoid isolated)\n2. Via verified safe shop CCTV\n3. Safe branch main entrance\n4. ✅ SafeRand Blue - Keep Rand Safe anywhere SA!", size=10, color=SAFERAND_BLUE)]); page.update()
        scammers_list = ft.Column([])
        safe_places_list = ft.Column([])
        community_feed = ft.Column([])
        def toggle_location(e):
            location_on["value"]=location_switch.value
            if location_switch.value: location_text.value=f"📍 Location: ON - {current_area['value']} - GPS active! SafeRand Blue - Keep Rand Safe!"; location_text.color=SAFERAND_BLUE; search_status.value="💙 SafeRand Blue: Location ON! Broad SA!"
            else: location_text.value=f"📍 Location: OFF - {current_area['value']} - SafeRand Blue OFF"; location_text.color="grey"; search_status.value="⚠️ Turn ON - SafeRand Blue!"
            page.update()
        location_switch.on_change=toggle_location
        def search_scammers(e):
            if not location_on["value"]: search_status.value="❌ Turn Location ON first - SafeRand Blue!"; page.update(); return
            scammers_list.controls.clear(); safe_places_list.controls.clear()
            filtered = SCAMMERS if current_area["value"]=="All Areas" else [s for s in SCAMMERS if s["area"]==current_area["value"]] or SCAMMERS[:3]
            for s in filtered: scammers_list.controls.append(ft.Container(padding=10, border_radius=12, bgcolor="#FFEBEE" if s["risk"]=="HIGH" else "#FFF3E0", content=ft.Column([ft.Row([ft.Text(f"🚨 {s['number']}", weight="bold", size=12, color="#D32F2F"), ft.Container(padding=4, border_radius=8, bgcolor="#D32F2F" if s["risk"]=="HIGH" else "#FF9800", content=ft.Text(f"{s['distance']} | {s['risk']}", size=8, color="white"))], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), ft.Text(f"{s['subtype']} | 📍 {s['location']} | 👥 {s['reports']} reports - SafeRand Blue", size=10), ft.Row([ft.FilledButton("Block", bgcolor=SAFERAND_BLUE, color="white", width=70, height=28), ft.FilledButton("Avoid Route", bgcolor="#FF9800", color="white", width=90, height=28), ft.FilledButton("Call Fraud", bgcolor=SAFERAND_LIGHT_BLUE, color="white", width=90, height=28)], spacing=4)])))
            for p in SAFE_PLACES: safe_places_list.controls.append(ft.Container(padding=8, border_radius=12, bgcolor="white", content=ft.Row([ft.Text("🏦" if p["type"]=="Bank" else "👮" if p["type"]=="Police" else "🛒", size=20), ft.Column([ft.Text(p["name"], weight="bold", size=11, color=SAFERAND_BLUE), ft.Text(f"{p['type']} | {p['distance']} | ✅ SafeRand Blue Verified", size=9, color="green")]), ft.FilledButton("Navigate", bgcolor=SAFERAND_BLUE, color="white", width=90, height=28)])))
            community_feed.controls=[ft.Container(padding=8, border_radius=10, bgcolor="#BBDEFB", content=ft.Text("🔴 LIVE: Nearby - 087 230 1234 blocked by SafeRand Blue community - 2 mins ago!", size=10, color=SAFERAND_BLUE)), ft.Container(padding=8, border_radius=10, bgcolor="#E1F5FE", content=ft.Text("🟢 LIVE: Safe route to SafeRand branch verified - SafeRand Blue anywhere!", size=10, color=SAFERAND_BLUE))]
            search_status.value=f"💙 SafeRand Blue: Found {len(filtered)} scammers near you - Broad SA - Keep Rand Safe!"; page.update()
        map_page = ft.Column([ft.Row([ft.Text("🗺️ SafeRand Blue Map - Broad SA", size=16, weight="bold", color=SAFERAND_BLUE), area_dropdown], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), ft.Container(padding=12, border_radius=16, bgcolor="white", content=ft.Column([location_switch, location_text])), map_visual, ft.Row([ft.FilledButton("🔍 SEARCH Around Me - SafeRand Blue", bgcolor=SAFERAND_BLUE, color="white", width=200, height=40, on_click=search_scammers), ft.FilledButton("🚨 SOS - SafeRand Blue", bgcolor="#D32F2F", color="white", width=130, height=40)]), search_status, ft.Container(padding=12, border_radius=16, bgcolor="#E3F2FD", content=ft.Column([ft.Text("Walking Safe Route - SafeRand Blue Anywhere!", weight="bold", size=13, color=SAFERAND_BLUE), ft.Row([from_dd, to_dd], wrap=True), ft.FilledButton("🗺️ CALCULATE SAFE ROUTE - SafeRand Blue", bgcolor=SAFERAND_BLUE, color="white", width=340, height=45, on_click=calculate_safe_route), route_result])), ft.Text("🚨 Scammers Near You - SafeRand Blue - Broad SA:", weight="bold", color="#D32F2F"), scammers_list, ft.Text("🏦 Safe Places Near You - SafeRand Blue:", weight="bold", color=SAFERAND_BLUE), safe_places_list, ft.Text("📢 Live Community - SafeRand Blue:", weight="bold", size=12, color=SAFERAND_BLUE), community_feed, ft.Text(DISCLAIMER, size=8, color="grey")], scroll=ft.ScrollMode.AUTO)

        # ===== 7. FAMILY - COMPLETE =====
        family_members = ft.Column([ft.Container(padding=10, border_radius=12, bgcolor="#BBDEFB", content=ft.Row([ft.Icon(ft.Icons.PERSON, color=SAFERAND_BLUE), ft.Column([ft.Text(f"{user.get('full_name','')} (You) - SafeRand Blue", weight="bold", size=12, color=SAFERAND_BLUE), ft.Text(f"📍 {user_area} | ✅ Protected | SafeRand Blue", size=10, color=SAFERAND_BLUE)]), ft.Text("🟢 Online", size=10, color="green")]))])
        add_family_name = ft.TextField(label="Family name", width=150, border_color=SAFERAND_BLUE)
        add_family_phone = ft.TextField(label="Phone", width=150, border_color=SAFERAND_BLUE)
        def add_family(e):
            if add_family_name.value: family_members.controls.append(ft.Container(padding=10, border_radius=12, bgcolor="#E3F2FD", content=ft.Row([ft.Icon(ft.Icons.PERSON_ADD, color=SAFERAND_BLUE), ft.Text(f"{add_family_name.value} - {add_family_phone.value} - SafeRand Blue", size=11, color=SAFERAND_BLUE), ft.Text("✅ Added", color="green", size=10)]))); add_family_name.value=""; add_family_phone.value=""; page.update()
        family_page = ft.Column([ft.Text("👨‍👩‍👧 Family Shield - SafeRand Blue - Broad SA", size=16, weight="bold", color=SAFERAND_BLUE), family_members, ft.Container(padding=12, border_radius=12, bgcolor="white", content=ft.Column([ft.Text("Add Family Member - SafeRand Blue:", weight="bold", size=12, color=SAFERAND_BLUE), ft.Row([add_family_name, add_family_phone], wrap=True), ft.FilledButton("Add to Family Shield - SafeRand Blue", bgcolor=SAFERAND_BLUE, color="white", width=340, on_click=add_family)]))], scroll=ft.ScrollMode.AUTO)

        # ===== 8. QUIZ - COMPLETE =====
        quiz_q = ft.Text("Q1: Bank SMS says 'Click link, account blocked!' What do you do? - SafeRand Blue", size=12, weight="bold", color=SAFERAND_BLUE)
        quiz_options = ft.Column([])
        quiz_result = ft.Text("", size=11, weight="bold")
        quiz_score = {"score": 0, "total": 0}
        questions = [
            {"q": "Q1: Bank SMS says 'Click link blocked!' What do you do? - SafeRand Blue", "options": ["Click link quickly", "Call bank official number - SafeRand Blue", "Give OTP"], "correct": 1},
            {"q": "Q2: You WON R50k! Pay R200 fee! Real? - SafeRand Blue", "options": ["Yes pay", "No SCAM! Real never asks fee - SafeRand Blue!", "Send ID"], "correct": 1},
            {"q": "Q3: Caller says 'I'm bank fraud, give OTP!' - SafeRand Blue", "options": ["Give OTP", "Hang up, call bank yourself - SafeRand Blue", "Give PIN"], "correct": 1},
            {"q": "Q4: Job asks R500 training fee! Real? - SafeRand Blue", "options": ["Yes pay", "No real jobs never ask fee - SafeRand Blue SCAM!", "Pay"], "correct": 1},
            {"q": "Q5: Best way check if number is scammer? - SafeRand Blue", "options": ["Call back", "Check SafeRand Map reports - SafeRand Blue", "Send money"], "correct": 1},
        ]
        current_q = {"index": 0}
        def load_question():
            q=questions[current_q["index"]]; quiz_q.value=q["q"]; quiz_options.controls.clear()
            for i,opt in enumerate(q["options"]): quiz_options.controls.append(ft.FilledButton(opt, bgcolor="#BBDEFB", color=SAFERAND_BLUE, width=340, on_click=lambda e,idx=i: check_answer(idx)))
            page.update()
        def check_answer(idx):
            q=questions[current_q["index"]]; quiz_score["total"]+=1
            if idx==q["correct"]: quiz_score["score"]+=1; quiz_result.value=f"✅ Correct! Score: {quiz_score['score']}/{quiz_score['total']} - SafeRand Blue!"; quiz_result.color="green"
            else: quiz_result.value=f"❌ Wrong! Correct: {q['options'][q['correct']]} | Score: {quiz_score['score']}/{quiz_score['total']}"; quiz_result.color="red"
            current_q["index"]=(current_q["index"]+1)%len(questions); load_question()
        load_question()
        quiz_page = ft.Column([ft.Text("🎮 Scam Quiz - SafeRand Blue - Broad SA - Keep Rand Safe!", size=16, weight="bold", color=SAFERAND_BLUE), quiz_q, quiz_options, quiz_result, ft.Container(padding=12, border_radius=12, bgcolor="#BBDEFB", content=ft.Column([ft.Text("🏆 Rewards - SafeRand Blue:", weight="bold", size=12, color=SAFERAND_BLUE), ft.Text("• 5/5 = SafeRand Blue Financial Literacy Badge!\n• Works anywhere SA!\n• Keep Rand Safe! SafeRand Blue!", size=11, color=SAFERAND_BLUE)]))], scroll=ft.ScrollMode.AUTO)

        app_content = ft.Column([checker_page], expand=True)
        def go_c(e): app_content.controls=[checker_page]; page.update()
        def go_l(e): app_content.controls=[learn_page]; page.update()
        def go_h(e): app_content.controls=[help_page]; page.update()
        def go_b(e): app_content.controls=[budget_page]; page.update()
        def go_map(e): app_content.controls=[map_page]; page.update()
        def go_fam(e): app_content.controls=[family_page]; page.update()
        def go_q(e): app_content.controls=[quiz_page]; page.update()
        def go_ai(e): app_content.controls=[ai_page]; page.update()

        def circle_btn(text, color, fn):
            return ft.FilledButton(content=ft.Text(text, size=10, weight="bold", text_align=ft.TextAlign.CENTER), bgcolor=color, color="white", width=62, height=62, style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=4), on_click=fn)

        return ft.Column([
            header,
            ft.Row([circle_btn("Check\ner", SAFERAND_BLUE, go_c), circle_btn("Learn", "#D32F2F", go_l), circle_btn("H\nE\nLP", "#D32F2F", go_h), circle_btn("A\nI", SAFERAND_LIGHT_BLUE, go_ai), circle_btn("Budget", "#FF9800", go_b)], spacing=7, wrap=True),
            ft.Row([circle_btn("Ma\np", SAFERAND_BLUE2, go_map), circle_btn("Famil\ny", SAFERAND_BLUE, go_fam), circle_btn("Qu\niz", "#E91E63", go_q)], spacing=7, wrap=True),
            ft.Divider(height=5, color=SAFERAND_BLUE),
            app_content
        ], expand=True)

    def show_login():
        content.controls=[ft.Column([
            ft.Container(padding=16, border_radius=20, bgcolor=SAFERAND_BLUE, content=ft.Column([
                ft.Row([ft.Container(padding=10, border_radius=20, bgcolor="white", content=ft.Text("🛡️", size=36)), ft.Column([ft.Text("SafeRand", size=26, weight="bold", color="white"), ft.Text("Keep Your Rand Safe", size=14, weight="bold", color=SAFERAND_LIGHT_BLUE)])]),
                ft.Text(TEAM_NAME, size=12, weight="bold", color="#BBDEFB"),
                ft.Text("App Academy 2026 - SafeRand Blue - Broad SA - Anywhere in SA", size=9, color="white"),
            ])),
            ft.Container(padding=12, border_radius=12, bgcolor="white", content=ft.Column([login_email, login_pass, ft.FilledButton("LOGIN - SafeRand Blue 💙", bgcolor=SAFERAND_BLUE, color="white", width=340, height=50, on_click=do_login), login_msg])),
            ft.Text("Test: test@test.com / 123456", size=9, color="grey"),
            ft.TextButton("REGISTER - SafeRand Blue - Choose Province", on_click=lambda e: show_register()),
            ft.Text(DISCLAIMER, size=8, color="grey", text_align=ft.TextAlign.CENTER)
        ], scroll=ft.ScrollMode.AUTO)]; page.update()

    def do_login(e):
        email=login_email.value.strip().lower(); pwd=login_pass.value.strip()
        if email in USERS and USERS[email]["password"]==pwd: CURRENT_USER["email"]=email; content.controls=[build_app()]; page.update()
        else: login_msg.value="❌ Wrong!"; page.update()

    def show_register():
        content.controls=[ft.Column([
            ft.Icon(ft.Icons.PERSON_ADD, color=SAFERAND_BLUE, size=60),
            ft.Text(TEAM_NAME, size=14, weight="bold", color=SAFERAND_BLUE),
            ft.Text("REGISTER - SafeRand Blue - Broad SA", size=12, weight="bold", color=SAFERAND_BLUE),
            reg_name, reg_email, reg_phone, reg_id, reg_location, reg_bank, reg_pass, reg_pass2,
            ft.FilledButton("REGISTER - SafeRand Blue 💙", bgcolor=SAFERAND_BLUE, color="white", width=340, height=50, on_click=do_register),
            reg_msg,
            ft.TextButton("LOGIN - SafeRand Blue", on_click=lambda e: show_login()),
            ft.Text(DISCLAIMER, size=8, color="grey")
        ], scroll=ft.ScrollMode.AUTO)]; page.update()

    def do_register(e):
        name=reg_name.value.strip(); email=reg_email.value.strip().lower(); phone=reg_phone.value.strip(); id_num=reg_id.value.strip(); loc=reg_location.value; bank=reg_bank.value; pwd=reg_pass.value.strip(); pwd2=reg_pass2.value.strip()
        if not name or not email or not phone or not id_num or not pwd: reg_msg.value="⚠️ Fill ALL!"; page.update(); return
        if pwd!=pwd2: reg_msg.value="❌ Passwords no match!"; page.update(); return
        if len(id_num)!=13: reg_msg.value="❌ ID must be 13 digits!"; page.update(); return
        USERS[email]={"full_name":name,"email":email,"phone":phone,"id_number":id_num,"bank":bank,"password":pwd,"location":loc}
        reg_msg.value=f"✅ SafeRand Blue - {TEAM_NAME} Registered in {loc}! Broad SA!"; reg_msg.color=SAFERAND_BLUE; page.update()

    page.add(content)
    show_login()

ft.run(main)
