#!/usr/bin/env python3
"""Generate themes/*/index.html from root index.html (body only). Does not modify index.html."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = (ROOT / "index.html").read_text(encoding="utf-8")
nav_i = SRC.index("<!-- NAV -->")
scroll_i = SRC.index("<!-- SCROLL ANIMATIONS -->")
auto_i = SRC.index("<!-- Auto-refresh")
BODY_RAW = SRC[nav_i:scroll_i]
SCROLL = SRC[scroll_i:auto_i]

LR = """
<script>
(function () {
    var host = location.hostname;
    if (host !== 'localhost' && host !== '127.0.0.1') return;
    var url = location.pathname;
    if (url.endsWith('/')) url += 'index.html';
    var last = null;
    setInterval(function () {
        fetch(url + '?_lr=' + Date.now(), { method: 'HEAD', cache: 'no-store' })
            .then(function (r) { return r.headers.get('last-modified'); })
            .then(function (lm) {
                if (!lm) return;
                if (last === null) { last = lm; return; }
                if (lm !== last) location.reload();
            })
            .catch(function () {});
    }, 700);
})();
</script>
"""

FOOTER_BLOCK = """<footer>
    <p>&copy; 2026 Tejaswini Dondeti. All rights reserved.</p>
</footer>"""


def make_picker() -> str:
    return '<p class="theme-picker"><a href="/">View default theme</a></p>'


def inject_picker(body_raw: str, picker_html: str) -> str:
    return body_raw.replace(
        FOOTER_BLOCK,
        "<footer>\n    <p>&copy; 2026 Tejaswini Dondeti. All rights reserved.</p>\n" + picker_html + "\n</footer>",
    )


def doc(title: str, extra_css: str, body_html: str) -> str:
    base_css = r"""
        *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
        html { scroll-behavior: smooth; }
        section { padding: 5rem 2rem; }
        .section-header { text-align: center; margin-bottom: 3rem; }
        .section-header h2 { font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; }
        .container { max-width: 1120px; margin: 0 auto; }
        .about-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; align-items: center; }
        .about-text h3 { font-size: 1.5rem; margin-bottom: 1rem; }
        .about-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-top: 2rem; }
        .stat { text-align: center; padding: 1.25rem; border-radius: var(--radius); box-shadow: var(--shadow); }
        .stat-number { font-size: 1.8rem; font-weight: 700; color: var(--primary); }
        .stat-label { font-size: 0.8rem; color: var(--text-light); margin-top: 0.25rem; }
        .skills-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem; }
        .skill-card {
            padding: 1.75rem; border: 1px solid var(--border); border-radius: var(--radius);
            transition: all 0.2s; background: var(--card-bg);
        }
        .skill-card:hover { box-shadow: var(--shadow-lg); transform: translateY(-2px); border-color: var(--primary); }
        .skill-icon { font-size: 2rem; margin-bottom: 1rem; }
        .skill-card h3 { font-size: 1.05rem; margin-bottom: 0.5rem; }
        .skill-card p { font-size: 0.9rem; color: var(--text-light); }
        .projects-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 1.5rem; }
        .project-card {
            border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden;
            transition: all 0.25s; background: var(--card-bg);
        }
        .project-card:hover { box-shadow: var(--shadow-lg); transform: translateY(-3px); }
        .project-banner { height: 10px; width: 100%; }
        .project-body { padding: 1.5rem; }
        .project-tag {
            display: inline-block; padding: 0.2rem 0.6rem; border-radius: 4px;
            font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.75rem;
        }
        .project-body h3 { font-size: 1.1rem; margin-bottom: 0.5rem; }
        .project-body p { font-size: 0.88rem; color: var(--text-light); margin-bottom: 1rem; line-height: 1.55; }
        .project-tools { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 1rem; }
        .tool-badge {
            padding: 0.2rem 0.6rem; background: var(--bg-alt); border-radius: 4px;
            font-size: 0.75rem; color: var(--text-light); border: 1px solid var(--border);
        }
        .project-link {
            display: inline-flex; align-items: center; gap: 0.3rem;
            font-size: 0.85rem; font-weight: 600; color: var(--primary); text-decoration: none;
        }
        .project-link:hover { text-decoration: underline; }
        .certs-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem; }
        .cert-card {
            display: flex; align-items: center; gap: 1rem; padding: 1.25rem;
            border: 1px solid var(--border); border-radius: var(--radius); transition: all 0.2s;
            background: var(--card-bg);
        }
        .cert-card:hover { box-shadow: var(--shadow-md); }
        .cert-icon { font-size: 2rem; }
        .cert-info h4 { font-size: 0.95rem; margin-bottom: 0.15rem; }
        .cert-info p { font-size: 0.8rem; color: var(--text-light); }
        .contact-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; }
        .contact-info h3 { font-size: 1.3rem; margin-bottom: 1rem; }
        .contact-info p { color: var(--text-light); margin-bottom: 1.5rem; }
        .contact-item { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem; }
        .contact-item-icon {
            width: 40px; height: 40px; border-radius: 8px; background: var(--primary-light);
            display: flex; align-items: center; justify-content: center; font-size: 1.1rem;
        }
        .contact-item-text a { color: var(--primary); text-decoration: none; font-weight: 500; }
        .contact-item-text span { font-size: 0.8rem; color: var(--text-light); display: block; }
        .contact-form { display: flex; flex-direction: column; gap: 1rem; }
        .contact-form input, .contact-form textarea {
            padding: 0.85rem 1rem; border: 1.5px solid var(--border); border-radius: 8px;
            font-family: inherit; font-size: 0.9rem; background: var(--input-bg); color: var(--text);
            transition: border-color 0.2s;
        }
        .contact-form input:focus, .contact-form textarea:focus { outline: none; border-color: var(--primary); }
        .contact-form textarea { resize: vertical; min-height: 120px; }
        footer { text-align: center; padding: 2rem; border-top: 1px solid var(--border); font-size: 0.85rem; color: var(--text-light); }
        .theme-picker { margin-top: 1.25rem; font-size: 0.78rem; line-height: 1.8; }
        .theme-picker a { color: var(--primary); margin: 0 0.35rem; font-weight: 600; }
        .theme-picker span { color: var(--text-light); margin-right: 0.25rem; }
        .mobile-toggle { display: none; background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--text); }
        .fade-in { opacity: 0; transform: translateY(20px); transition: opacity 0.6s ease, transform 0.6s ease; }
        .fade-in.visible { opacity: 1; transform: translateY(0); }
        @media (max-width: 768px) {
            .nav-links {
                display: none; position: absolute; top: 64px; left: 0; right: 0;
                flex-direction: column; background: var(--mobile-nav-bg); border-bottom: 1px solid var(--border);
                padding: 1rem 2rem; gap: 0.75rem; box-shadow: var(--shadow-md);
            }
            .nav-links.show { display: flex; }
            .mobile-toggle { display: block; }
            .hero h1 { font-size: 2.2rem; }
            .about-grid, .contact-grid { grid-template-columns: 1fr; }
            .about-stats { grid-template-columns: repeat(3, 1fr); }
            .projects-grid { grid-template-columns: 1fr; }
        }
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {extra_css}
    <style>
{base_css}
    </style>
</head>
<body>
{body_html}
{SCROLL}
{LR}
</body>
</html>
"""


WARM_SHELL = """    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: {primary};
            --primary-light: {primary_light};
            --text: {text};
            --text-light: {text_light};
            --bg: {bg};
            --bg-alt: {bg_alt};
            --card-bg: {card_bg};
            --input-bg: {input_bg};
            --border: {border};
            --mobile-nav-bg: {mobile_nav_bg};
            --shadow: {shadow};
            --shadow-md: {shadow_md};
            --shadow-lg: {shadow_lg};
            --radius: {radius};
        }}
        body {{ font-family: 'DM Sans', system-ui, sans-serif; color: var(--text); background: var(--bg); line-height: 1.65; }}
        .section-header h2 {{ font-family: 'Fraunces', Georgia, serif; font-weight: 700; }}
        .section-header p {{ color: var(--text-light); font-size: 1.05rem; }}
        .about-text h3 {{ font-family: 'Fraunces', Georgia, serif; }}
        .about-text p {{ color: var(--text-light); margin-bottom: 1rem; }}
        nav {{
            position: fixed; top: 0; width: 100%; z-index: 100;
            background: {nav_bg}; backdrop-filter: blur(10px);
            border-top: {nav_border_top};
            border-bottom: {nav_border_bottom};
            box-shadow: {nav_shadow};
            padding: 0 2rem;
        }}
        .nav-inner {{ max-width: 1120px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; height: 64px; position: relative; }}
        .nav-logo {{ font-family: 'Fraunces', Georgia, serif; font-weight: 700; font-size: 1.15rem; color: var(--text); text-decoration: none; }}
        .nav-logo span {{ color: var(--primary); }}
        .nav-links {{ display: flex; gap: 2rem; list-style: none; }}
        .nav-links a {{ text-decoration: none; color: var(--text-light); font-size: 0.9rem; font-weight: 600; }}
        .nav-links a:hover {{ color: var(--primary); }}
        .hero {{
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
            text-align: center; padding: 6rem 2rem 4rem;
            background: {hero_bg};
        }}
        .hero-content {{ max-width: 700px; }}
        .hero-badge {{
            display: inline-block; padding: 0.3rem 0.9rem; border-radius: {badge_radius};
            background: var(--primary-light); color: var(--primary); font-size: 0.72rem; font-weight: 700;
            margin-bottom: 1.5rem; letter-spacing: 0.14em; text-transform: uppercase;
        }}
        .hero h1 {{ font-family: 'Fraunces', Georgia, serif; font-size: 3.1rem; font-weight: 700; line-height: 1.12; margin-bottom: 1rem; }}
        .hero h1 span {{ color: var(--primary); font-style: {h1_span_style}; }}
        .hero p {{ font-size: 1.12rem; color: var(--text-light); margin-bottom: 2rem; max-width: 560px; margin-left: auto; margin-right: auto; }}
        .hero-buttons {{ display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }}
        .btn {{
            display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.7rem 1.6rem;
            border-radius: {btn_radius}; font-size: 0.92rem; font-weight: 600; text-decoration: none;
            cursor: pointer; border: none; transition: all 0.2s;
        }}
        .btn-primary {{ background: var(--primary); color: {btn_primary_color}; }}
        .btn-primary:hover {{ background: {btn_primary_hover}; }}
        .btn-outline {{ background: transparent; color: var(--text); border: {btn_outline_width} solid var(--border); }}
        .btn-outline:hover {{ border-color: var(--primary); color: var(--primary); }}
        .about-section {{ background: var(--bg-alt); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); }}
        .stat {{ background: var(--card-bg); border: 1px solid var(--border); }}
        .projects-section {{ background: var(--bg); }}
        .contact-section {{ background: var(--bg-alt); }}
        .skill-card {{ box-shadow: var(--shadow); }}
        .project-card {{ box-shadow: var(--shadow); }}
        {extra_rules}
    </style>
"""


DEFAULT_TAGS = """        .tag-risk { background: #fef2f2; color: #b91c1c; }
        .tag-compliance { background: #f0fdf4; color: #15803d; }
        .tag-governance { background: #eff6ff; color: #1d4ed8; }
        .tag-audit { background: #fefce8; color: #a16207; }
        .tag-security { background: #faf5ff; color: #7e22ce; }
        .tag-policy { background: #fff7ed; color: #c2410c; }"""


def warm_css(**kw: str) -> str:
    defaults = {
        "extra_rules": DEFAULT_TAGS,
        "h1_span_style": "italic",
        "btn_primary_color": "#fff",
        "btn_outline_width": "2px",
        "badge_radius": "4px",
        "btn_radius": "4px",
        "nav_border_top": "4px solid transparent",
        "nav_border_bottom": "1px solid var(--border)",
        "nav_shadow": "none",
    }
    defaults.update(kw)
    return WARM_SHELL.format(**defaults)


SHADOW_WARM = (
    "0 2px 8px rgba(41,37,36,0.06)",
    "0 6px 20px rgba(41,37,36,0.08)",
    "0 16px 48px rgba(41,37,36,0.1)",
)

THEMES = {
    "warm": {
        "title": "Tejaswini Dondeti | GRC Portfolio (Warm)",
        "css": warm_css(
            primary="#c2410c",
            primary_light="#ffedd5",
            text="#292524",
            text_light="#78716c",
            bg="#faf7f2",
            bg_alt="#f3eee8",
            card_bg="#fffefb",
            input_bg="#fffefb",
            border="#e7e5e4",
            mobile_nav_bg="#f5efe6",
            shadow=SHADOW_WARM[0],
            shadow_md=SHADOW_WARM[1],
            shadow_lg=SHADOW_WARM[2],
            radius="6px",
            nav_bg="rgba(241, 232, 220, 0.97)",
            nav_border_top="4px solid #4a4538",
            nav_border_bottom="2px solid #a89885",
            nav_shadow="0 6px 18px rgba(41, 37, 36, 0.09)",
            hero_bg="linear-gradient(170deg, #fff7ed 0%, #faf7f2 40%, #fef3c7 100%)",
            btn_primary_hover="#9a3412",
        ),
    },
}


def main() -> None:
    picker = make_picker()
    body = inject_picker(BODY_RAW, picker)
    for slug, cfg in THEMES.items():
        out_dir = ROOT / "themes" / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        html = doc(cfg["title"], cfg["css"], body)
        (out_dir / "index.html").write_text(html, encoding="utf-8")
        print("Wrote", out_dir / "index.html")


if __name__ == "__main__":
    main()
