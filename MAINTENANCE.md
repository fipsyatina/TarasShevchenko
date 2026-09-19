# Profile maintenance

The SVGs and generator are original work inspired by the layout of [Andrew6rant/Andrew6rant](https://github.com/Andrew6rant/Andrew6rant). No source code or portrait from that repository is included. The portrait is text sampled from a transparent cutout of Taras's supplied photo. The cutout is included as `assets/portrait-cutout.png`; the original photos are not stored in this repository.

The background was removed with the built-in image generation tool. Prompt: remove buildings, sky, poles and wires; preserve the person's face, expression, hair, glasses, headphones and clothing; output a centered photographic head-and-shoulders cutout with a genuinely transparent background, without text or stylization. To resample the portrait, install Pillow and run `python scripts/extract_portrait.py`, then rebuild the cards.

## Updates

`.github/workflows/update-profile.yml` runs daily at 02:17 UTC, on relevant pushes, or manually in Actions. Scheduling can be delayed by GitHub. In inactive public repositories GitHub may disable scheduled workflows after 60 days; re-enable the workflow in Actions if needed.

The generator uses Python 3.12 and the standard library on Linux. For Windows, install `tzdata` if IANA time zones are unavailable. No personal access token is needed: the workflow uses its repository-scoped `GITHUB_TOKEN`.

```sh
python scripts/update_profile.py
# Rebuild deterministically from the saved snapshot without API requests:
python scripts/update_profile.py --offline
```

Edit personal information in `profile.json`. The SVG layout is in `scripts/update_profile.py`; update the README text version when changing personal information. Spoken language descriptions are self-reported, not CEFR certifications.

Public repository count includes owned forks. Stars and forks are sums for public, owned, non-fork repositories. Followers come from the public GitHub user endpoint. Private repositories, commit counts and lines of code are not represented. API failures fail the update and retain the previous published cards instead of substituting zeroes.

Uptime is actual elapsed time from `2006-12-23 04:36 Europe/Kyiv` (`2006-12-23 02:36 UTC`), computed in UTC so daylight-saving transitions do not change elapsed time. It is a daily snapshot, not a live second-by-second counter.

The university's English name follows its [official engineering page](https://wab.edu.pl/en/engineering-degree/).

## Show this on the GitHub profile

This repository has the requested name `TarasShevchenko`. GitHub displays a profile README only from a public repository named exactly like the account: `fipsyatina/fipsyatina`. To display this card there, embed the following in that repository's root README. Updates will continue to come from this repository.

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/fipsyatina/TarasShevchenko/main/dark_mode.svg">
  <img alt="Taras Shevchenko — GitHub profile" src="https://raw.githubusercontent.com/fipsyatina/TarasShevchenko/main/light_mode.svg" width="1200">
</picture>
```

See [GitHub's profile README requirements](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme).
