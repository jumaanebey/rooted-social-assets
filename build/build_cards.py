#!/usr/bin/env python3
"""Render the 16 new Rooted feed cards (1080x1350, 4:5) from CALENDAR.md copy.
  python3 build_cards.py        -> cards/<date>-<slug>.jpg  (+ html/ for each)
Light teal system only (BRAND-SYSTEM.md): cream, teal, ink; no dark or orange backgrounds."""
import base64, html, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "cards")
HTML = os.path.join(HERE, "html")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FF = os.path.expanduser("~/projects/jay-bey-social/hyperframes/bin/ffmpeg")
LOGO = base64.b64encode(open(os.path.join(HERE, "logo-icon.svg"), "rb").read()).decode()


def shot(name):
    return "data:image/png;base64," + base64.b64encode(open(f"{HERE}/shots/{name}.png", "rb").read()).decode()


CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Playfair+Display:wght@600;700;800&display=swap');
:root{--cream:#fbfaf7;--teal:#0f766e;--teal2:#0d9488;--mint:#e6f4f1;--ink:#241c16;--mute:#6b625a;--line:#e4dfd6}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;background:var(--cream);font-family:'DM Sans',sans-serif;color:var(--ink);position:relative;overflow:hidden}
.bar{position:absolute;top:0;left:0;width:100%;height:14px;background:var(--teal)}
.brand{position:absolute;top:58px;left:80px;display:flex;align-items:center;gap:16px;font:700 34px 'Playfair Display',serif}
.brand img{width:52px;height:52px;border-radius:12px}
.eyebrow{position:absolute;top:60px;right:80px;font:700 24px 'DM Sans';letter-spacing:.16em;color:var(--teal);text-transform:uppercase}
.main{position:absolute;left:80px;right:80px;top:170px;bottom:170px;display:flex;flex-direction:column}
h1{font:800 84px/1.04 'Playfair Display',serif;letter-spacing:-.01em}
h1 em{color:var(--teal);font-style:normal}
.sub{font:500 36px/1.35 'DM Sans';color:var(--mute);margin-top:26px}
.foot{position:absolute;left:80px;right:80px;bottom:62px;display:flex;justify-content:space-between;align-items:center;font:700 30px 'DM Sans';color:var(--teal)}
.foot span:last-child{color:var(--mute);font-weight:500;font-size:26px}
.list{margin-top:44px;display:flex;flex-direction:column;gap:20px}
.item{display:flex;gap:26px;align-items:center;background:#fff;border:2px solid var(--line);border-radius:26px;padding:26px 32px;font:500 35px/1.25 'DM Sans'}
.num{flex:none;width:62px;height:62px;border-radius:50%;background:var(--teal);color:#fff;font:700 32px/62px 'DM Sans';text-align:center}
.panel{border-radius:30px;padding:46px 50px}
.myth{background:#f1eee8;border:2px solid var(--line)}
.fact{background:var(--teal);color:#fff;margin-top:26px}
.tag{font:700 24px 'DM Sans';letter-spacing:.18em;text-transform:uppercase;margin-bottom:16px}
.myth .tag{color:var(--mute)} .fact .tag{color:#bdeee6}
.panel p{font:600 48px/1.2 'Playfair Display',serif}
.big{font:800 300px/1 'Playfair Display',serif;color:var(--teal);margin-top:30px;margin-bottom:30px}
.pill{display:inline-block;background:var(--mint);color:var(--teal);border-radius:999px;padding:12px 26px;font:700 28px 'DM Sans';margin-top:28px;align-self:flex-start}
.shot{margin-top:34px;border-radius:30px;border:2px solid var(--line);box-shadow:0 18px 50px rgba(36,28,22,.12);width:100%;height:640px;object-fit:cover;object-position:top}
.q{font:700 52px/1.15 'Playfair Display',serif;margin-top:6px}
.a{font:500 46px/1.4 'DM Sans';color:var(--ink);margin-top:44px}
.quote{justify-content:center;text-align:left}
.quote h1{font-size:112px;line-height:1.05}
.mark{width:140px;height:14px;background:var(--teal);border-radius:8px;margin-bottom:46px}
"""


def page(eyebrow, body, foot_l, foot_r="Link in bio"):
    return f"""<!doctype html><meta charset=utf-8><style>{CSS}</style><body>
<div class=bar></div><div class=brand><img src="data:image/svg+xml;base64,{LOGO}">Rooted</div>
<div class=eyebrow>{html.escape(eyebrow)}</div>
<div class=main>{body}</div>
<div class=foot><span>{html.escape(foot_l)}</span><span>{html.escape(foot_r)}</span></div>"""


def checklist(eyebrow, title, items, sub=None, foot="rootedcoliving.com/find"):
    li = "".join(f'<div class=item><div class=num>{i+1}</div><div>{html.escape(t)}</div></div>' for i, t in enumerate(items))
    s = f'<div class=sub>{html.escape(sub)}</div>' if sub else ""
    return page(eyebrow, f"<h1>{title}</h1>{s}<div class=list>{li}</div>", foot)


def myth(eyebrow, title, m, f, foot="rootedcoliving.com"):
    return page(eyebrow, f"<h1>{title}</h1><div style='height:44px'></div>"
                f"<div class='panel myth'><div class=tag>Myth</div><p>{html.escape(m)}</p></div>"
                f"<div class='panel fact'><div class=tag>Fact</div><p>{html.escape(f)}</p></div>", foot)


def city(name, slug, n):
    return page("City spotlight",
                f"<h1>Recovery housing in <em>{html.escape(name)}</em></h1><div class=big>{n}</div>"
                f"<div class=sub style='margin-top:0'>homes from the public recovery-residence registry are listed in {html.escape(name)}, CA.</div>"
                f"<div class=pill>None reviewed on Rooted yet</div>", f"rootedcoliving.com/find/{slug}")


def whatsnew(title, sub, img, foot):
    return page("What's new", f"<h1>{title}</h1><div class=sub>{html.escape(sub)}</div><img class=shot src='{shot(img)}'>", foot)


def faq(q, a, foot="rootedcoliving.com"):
    return page("Quick answer", f"<div class=mark></div><div class=q style='font-size:88px;line-height:1.08;margin-top:110px'>{html.escape(q)}</div><div class=a>{html.escape(a)}</div>", foot)


def quote(line):
    return page("Rooted", f"<div class='quote' style='display:flex;flex-direction:column;justify-content:center;height:100%'><div class=mark></div><h1>{line}</h1></div>", "rootedcoliving.com")


CARDS = [
    ("2026-10-18-checklist-moving-in", checklist("Checklist", "5 questions to ask <em>before you move in</em>", [
        "What does rent include?", "How are house rules set, and who explains them?",
        "What happens if a guest needs to leave?", "How does the application work?", "Who do you call with a question?"])),
    ("2026-10-20-city-riverside", city("Riverside", "riverside-ca", 18)),
    ("2026-10-22-myth-referral", myth("Myth vs fact", "A referral does <em>not</em> reserve a bed", "A referral holds a bed.",
        "A referral starts a conversation. The operator confirms the next step.")),
    ("2026-10-23-new-bed-alerts", whatsnew("Bed alerts for your <em>city</em>", "Case managers get an email when a home nearby marks a bed available.", "bed-alerts", "rootedcoliving.com/cm")),
    ("2026-10-25-checklist-listing", checklist("For operators", "What case managers need <em>from a listing</em>", [
        "Photos, room by room", "Who the home serves", "Hours and how fast you reply",
        "How to reach the house manager", "A way to apply online"], foot="rootedcoliving.com/list-your-home")),
    ("2026-10-27-city-los-angeles", city("Los Angeles", "los-angeles-ca", 13)),
    ("2026-10-29-myth-reviewed", myth("Myth vs fact", "“Reviewed” is not <em>“endorsed”</em>", "Reviewed means inspected, licensed and endorsed.",
        "A person at Rooted reviewed one document and checked the operator's ID. That is all it means.")),
    ("2026-10-30-new-claim", whatsnew("Your home may <em>already be listed</em>", "Claim it for free to add beds, photos and costs, and take referrals online.", "claim", "rootedcoliving.com/claim")),
    ("2026-11-01-quote-front-door", quote("A fresh start needs <em>a front door.</em>")),
    ("2026-11-03-city-san-bernardino", city("San Bernardino", "san-bernardino-ca", 3)),
    ("2026-11-05-faq-free", faq("Do I need to pay to list my home?", "No. A free listing gives your home its own page and an application inbox. Add more whenever you are ready.", "rootedcoliving.com/list-your-home")),
    ("2026-11-06-new-waitlist", whatsnew("When you’re full, <em>they can wait</em>", "Guests join a waitlist from your listing. The longest wait is listed first.", "waitlist", "rootedcoliving.com/for-operators")),
    ("2026-11-08-checklist-families", checklist("For families", "Questions families <em>ask first</em>", [
        "Can we visit, and when?", "What are the house rules?", "What does rent include?",
        "Who is the house manager, and how do we reach them?", "What happens if plans change?"])),
    ("2026-11-10-city-long-beach", city("Long Beach", "long-beach-ca", 10)),
    ("2026-11-12-faq-24h", faq("How fast should a home reply to a referral?", "Within 24 hours. If a home doesn’t answer, the referral goes back to the pool.", "rootedcoliving.com/refer")),
    ("2026-11-13-quote-next-step", quote("Home is where <em>the next step</em> starts.")),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); os.makedirs(HTML, exist_ok=True)
    only = sys.argv[1:]
    for slug, doc in CARDS:
        if only and not any(o in slug for o in only):
            continue
        hp, pp, jp = f"{HTML}/{slug}.html", f"{HTML}/{slug}.png", f"{OUT}/{slug}.jpg"
        open(hp, "w").write(doc)
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        "--window-size=1080,1350", "--virtual-time-budget=8000", f"--screenshot={pp}", f"file://{hp}"],
                       capture_output=True)
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", pp, "-q:v", "2", jp], check=True)
        print(slug, os.path.getsize(jp) // 1024, "KB")
