"""Public product copy for released 6.0.2 (2026-10-10).

17 UI/site locales; ASC's 19 regional metadata entries are not 19 UI languages.
Source: released app 7396d99, ArticleRepository/GlobalSearchEntitlementPolicy,
Sharing contract and 6.0.2 public release notes. Never use a dirty future app tree.
"""
import json
from html import escape
from pathlib import Path

COPY = json.loads(Path(__file__).with_name('released_product_copy.json').read_text())


def install(g):
    """Reuse the site's layout, hero, brand, screenshots and language routing."""
    for lang in g['LANGS']:
        title, free, premium, share_title, share, scope = COPY[lang]
        f = escape
        current = f'''<section aria-labelledby="released-title" style="margin-top:48px;">
          <p class="section-label">SCP docs · 6.0.2 · 2026-10-10</p>
          <h2 id="released-title" class="section-title-lg">{f(title)}</h2>
          <div class="grid-2">
            <article class="card"><h3>Free</h3><p>{f(free)}</p></article>
            <article class="card"><h3>Premium</h3><p>{f(premium)}</p></article>
          </div>
          <div class="card" style="margin-top:24px;"><h3>{f(share_title)}</h3><p>{f(share)}</p></div>
          <p>{f(scope)}</p>
          <a class="btn-primary" href="{g['APP_STORE_URL']}" target="_blank" rel="noopener noreferrer">App Store · iPhone / iPad · iOS 17+</a>
        </section>'''
        old = g['INDEX'][lang]['body']
        # Keep the existing search console in JA and existing hero in other locales.
        hero = old[:old.index('</section>') + len('</section>')]
        hero = hero.replace('13+', '16+')
        promo = '' if lang == 'ja' else g['reading_home_promo'](lang)
        g['INDEX'][lang]['body'] = hero + promo + current + '</main>'
        if lang in g['FEATURES']:
            screens = '\n'.join(f'<figure class="screen-frame"><img src="{g["screenshot_path"](lang, kind)}" alt="SCP docs · {kind}" loading="lazy" /><figcaption>{kind}</figcaption></figure>' for kind in ['home','catalog','library'])
            g['FEATURES'][lang]['body'] = '<main class="main-pad">' + current + f'<section style="margin-top:48px;"><p class="section-label">Reader / Catalog / Library</p><div class="feature-shot-grid">{screens}</div></section></main>'
        data = g['SUPPORT_TEXT'][lang]
        old_faqs = data['faqs']
        data['faqs'] = [old_faqs[0],old_faqs[1],(title,free),('Premium',premium),(share_title,share)]
        # Avoid implying every branch has the same content or that UI locale = article translation.
        g['SEARCH_SUPPORT_COPY'][lang] = (premium, premium)
    for lang, cmp in g['FEATURE_CMP'].items():
        cmp['rows'][6] = (cmp['rows'][6][0], 'no', 'yes')
