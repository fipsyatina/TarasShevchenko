"""Generate both GitHub profile themes from verified public API data."""
import argparse
import calendar
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import urllib.request
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]


def api(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "TarasShevchenko-profile", "X-GitHub-Api-Version": "2022-11-28"}
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request("https://api.github.com/" + path, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_stats(username, now):
    user = api(f"users/{username}")
    repos = []
    page = 1
    while True:
        batch = api(f"users/{username}/repos?type=owner&per_page=100&page={page}")
        repos.extend(r for r in batch if not r.get("private", False))
        if len(batch) < 100:
            break
        page += 1
    original = [r for r in repos if not r["fork"]]
    return {"public_repos": len(repos), "stars": sum(r["stargazers_count"] for r in original),
            "followers": user["followers"], "forks": sum(r["forks_count"] for r in original),
            "updated_at": now.isoformat()}


def uptime(profile, now):
    born = datetime.fromisoformat(profile["birth_local"]).replace(tzinfo=ZoneInfo(profile["birth_timezone"]))
    local_now = now.astimezone(born.tzinfo)
    if local_now < born:
        raise ValueError("Update timestamp precedes birth")
    months = (local_now.year - born.year) * 12 + local_now.month - born.month

    def anniversary(offset):
        year, month = divmod(born.year * 12 + born.month - 1 + offset, 12)
        month += 1
        return born.replace(year=year, month=month, day=min(born.day, calendar.monthrange(year, month)[1]))

    if local_now < anniversary(months):
        months -= 1
    days = (local_now - anniversary(months)).days
    years, months = divmod(months, 12)
    return ", ".join(f"{value} {unit}{'' if value == 1 else 's'}" for value, unit in ((years, "year"), (months, "month"), (days, "day")))


def render(profile, stats, now, dark):
    colors = {"bg": "#161b22", "fg": "#c9d1d9", "key": "#ffa657", "value": "#a5d6ff", "muted": "#8492a6", "green": "#7ee787", "line": "#30363d"} if dark else {"bg": "#f6f8fa", "fg": "#24292f", "key": "#953800", "value": "#0550ae", "muted": "#596579", "green": "#116329", "line": "#d0d7de"}
    c = colors
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="790" viewBox="0 0 1200 790" role="img" aria-labelledby="title desc">',
           '<title id="title">Taras Shevchenko — GitHub profile</title>',
           '<desc id="desc">ASCII portrait, C++ and AI development, education, languages, contacts and public GitHub statistics.</desc>',
           f'<rect width="1200" height="790" rx="16" fill="{c["bg"]}"/>',
           '<style>text{font-family:Consolas,"Liberation Mono",Menlo,monospace;font-size:15px} .portrait{font-size:11px} text{white-space:pre}</style>']

    def text(x, y, value, color="fg", extra=""):
        svg.append(f'<text x="{x}" y="{y}" fill="{c[color]}" {extra}>{escape(str(value))}</text>')

    def field(y, key, value, value_color="value"):
        text(530, y, key, "key")
        text(530 + (len(key) + 1) * 9, y, " " + "." * max(1, 16 - len(key)) + " ", "muted")
        text(701, y, value, value_color)

    def heading(y, title):
        text(530, y, title)
        start = 530 + (len(title) + 2) * 9
        svg.append(f'<path d="M{start} {y-5} H1170" stroke="{c["line"]}"/>')

    text(28, 38, "taras@fipsyatina:~$ whoami", "green")
    lines = (ROOT / "assets/portrait.txt").read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        text(28, 110 + i * 13.5, line.ljust(64), extra='class="portrait" xml:space="preserve" textLength="460" lengthAdjust="spacingAndGlyphs"')
    text(28, 714, "TARAS SHEVCHENKO", "value")
    text(28, 739, "C++ / AI DEVELOPMENT", "key")
    text(28, 764, "[ open to work ]", "green")
    svg.append(f'<path d="M502 65 V764" stroke="{c["line"]}"/>')
    heading(38, "taras@shevchenko")
    field(76, "Name", profile["name"])
    field(100, "Focus", profile["focus"])
    field(124, "Status", "Open to work · C++ / AI", "green")
    field(148, "Location", profile["location"])
    field(172, "Born in", profile["birthplace"])
    field(196, "Uptime", uptime(profile, now))
    heading(238, "- Education")
    field(264, "University", "Wroclaw Business University")
    text(701, 288, "of Applied Sciences", "value")
    field(312, "Studying", profile["degree"])
    heading(354, "- Languages & hobbies")
    field(380, "Ukrainian", "Native")
    field(404, "Polish", "Advanced")
    field(428, "Russian", "Advanced")
    field(452, "English", "Intermediate")
    text(701, 475, "Comprehension > speaking", "muted")
    field(499, "Hobby", profile["hobby"])
    heading(541, "- Contact")
    field(567, "Email", profile["email"])
    field(591, "Discord", profile["discord"])
    field(615, "LinkedIn", "taras-shevchenko-a62643279")
    heading(657, "- GitHub stats · public")
    field(683, "Repositories", f'{stats["public_repos"]:,}       Stars: {stats["stars"]:,}')
    field(707, "Followers", f'{stats["followers"]:,}       Forks: {stats["forks"]:,}')
    text(530, 746, f'Updated {now:%Y-%m-%d %H:%M} UTC · daily snapshot', "muted")
    text(530, 768, "Stars & forks: owned, non-fork repositories", "muted")
    svg.append("</svg>")
    return "\n".join(svg) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true", help="Render using the saved public snapshot")
    args = parser.parse_args()
    profile = json.loads((ROOT / "profile.json").read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    cache = ROOT / "assets/stats.json"
    if args.offline:
        stats = json.loads(cache.read_text(encoding="utf-8"))
        now = datetime.fromisoformat(stats["updated_at"])
    else:
        stats = fetch_stats(profile["username"], now)
        cache.write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
    for theme in ("dark", "light"):
        (ROOT / f"{theme}_mode.svg").write_text(render(profile, stats, now, theme == "dark"), encoding="utf-8")
        (ROOT / f"profile-{theme}.svg").write_text(render(profile, stats, now, theme == "dark"), encoding="utf-8")
    print(f'Generated both themes: {stats["public_repos"]} public repositories; updated {now.isoformat()}')


if __name__ == "__main__":
    main()
