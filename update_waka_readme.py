import os
import requests
from pathlib import Path

API_KEY = os.environ["WAKATIME_API_KEY"]
README = Path("README.md")

START = "<!--START_SECTION:waka-custom-->"
END = "<!--END_SECTION:waka-custom-->"

def fetch():
    r = requests.get(
        "https://wakatime.com/api/v1/users/current/summaries",
        params={"range": "last_7_days"},
        auth=(API_KEY, "")
    )
    r.raise_for_status()
    return r.json()["data"][0]

def bar(pct, width=20):
    blocks = "░▒▓█"
    filled = int(pct / 100 * width)
    return blocks[-1] * filled + blocks[0] * (width - filled)

def render(title, items, key="name", pct="percent", limit=5):
    out = [f"**{title}:**"]
    for i in items[:limit]:
        out.append(
            f"{i[key]:<12} {bar(i[pct])} {i[pct]:5.1f} %"
        )
    return "\n".join(out)

def main():
    data = fetch()

    sections = [
        render("💻 OS", data["operating_systems"], limit=3),
        render("🧑‍💻 Editors", data["editors"], limit=3),
        render("📦 Projects", data["projects"], limit=5),
        render("🧠 Languages", data["languages"], limit=5),
    ]

    content = "```\n" + "\n\n".join(sections) + "\n```"

    text = README.read_text()
    before, _ , after = text.partition(START)
    _, _, tail = after.partition(END)

    README.write_text(
        before + START + "\n" + content + "\n" + END + tail
    )

if __name__ == "__main__":
    main()

