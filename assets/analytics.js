const SCPDocsAnalyticsCore = (() => {
  "use strict";

  const MEASUREMENT_ID = "G-5M5Q6SML03";
  const CONSENT_KEY = "scpdocs.analytics-consent";
  const MAX_VALUE_LENGTH = 80;
  const SENSITIVE_INPUT = /(?:https?:\/\/|www\.|[\w.+-]+@[\w.-]+\.[a-z]{2,}|(?:\+?\d[\d\s().-]{7,}\d))/iu;

  function cleanValue(value, limit = MAX_VALUE_LENGTH) {
    return String(value || "").normalize("NFKC").replace(/\s+/g, " ").trim().slice(0, limit);
  }

  function safeSearchTerm(value) {
    const term = cleanValue(value);
    if (!term || SENSITIVE_INPUT.test(term)) return "";
    return term;
  }

  function analyticsPageURL(value) {
    const url = new URL(value);
    url.search = "";
    url.hash = "";
    return url.toString();
  }

  function analyticsPagePath(value) {
    return new URL(value).pathname;
  }

  function isAnalyticsHost(hostname) {
    return hostname === "scpdocs.link" || hostname === "www.scpdocs.link";
  }

  return {
    CONSENT_KEY,
    MEASUREMENT_ID,
    analyticsPagePath,
    analyticsPageURL,
    cleanValue,
    isAnalyticsHost,
    safeSearchTerm,
  };
})();

if (typeof window !== "undefined" && typeof document !== "undefined") {
  (() => {
    "use strict";

    const COPY = {
      en: {
        title: "Help improve SCP Docs",
        body: "With your permission, Google Analytics measures page views and feature use. It is not loaded until you accept.",
        accept: "Allow analytics",
        decline: "Not now",
        settings: "Analytics settings",
        privacy: "Privacy details",
      },
      ja: {
        title: "サイト改善のためのアクセス解析",
        body: "同意した場合のみ、Google Analyticsでページ閲覧や機能の利用状況を計測します。同意するまで解析機能は読み込まれません。",
        accept: "アクセス解析を許可",
        decline: "許可しない",
        settings: "アクセス解析の設定",
        privacy: "詳しい取扱い",
      },
      fr: { title: "Aidez-nous à améliorer SCP Docs", body: "Avec votre accord, Google Analytics mesure les pages consultées et l’utilisation des fonctions. Il n’est chargé qu’après votre consentement.", accept: "Autoriser l’analyse", decline: "Pas maintenant", settings: "Paramètres d’analyse", privacy: "Détails de confidentialité" },
      ru: { title: "Помогите улучшить SCP Docs", body: "С вашего согласия Google Analytics измеряет просмотры страниц и использование функций. Он не загружается до вашего согласия.", accept: "Разрешить аналитику", decline: "Не сейчас", settings: "Настройки аналитики", privacy: "О конфиденциальности" },
      ko: { title: "SCP Docs 개선에 도움을 주세요", body: "동의한 경우에만 Google Analytics로 페이지 조회와 기능 사용을 측정합니다. 동의 전에는 분석 기능을 불러오지 않습니다.", accept: "분석 허용", decline: "허용하지 않음", settings: "분석 설정", privacy: "개인정보 안내" },
      es: { title: "Ayuda a mejorar SCP Docs", body: "Con tu permiso, Google Analytics mide las páginas vistas y el uso de funciones. No se carga hasta que aceptas.", accept: "Permitir analítica", decline: "Ahora no", settings: "Ajustes de analítica", privacy: "Detalles de privacidad" },
      pl: { title: "Pomóż ulepszać SCP Docs", body: "Za Twoją zgodą Google Analytics mierzy wyświetlenia stron i użycie funkcji. Nie jest ładowany przed wyrażeniem zgody.", accept: "Zezwól na analitykę", decline: "Nie teraz", settings: "Ustawienia analityki", privacy: "Informacje o prywatności" },
      cs: { title: "Pomozte zlepšovat SCP Docs", body: "S vaším souhlasem Google Analytics měří zobrazení stránek a používání funkcí. Před udělením souhlasu se nenačítá.", accept: "Povolit analytiku", decline: "Nyní ne", settings: "Nastavení analytiky", privacy: "Podrobnosti o soukromí" },
      de: { title: "Hilf, SCP Docs zu verbessern", body: "Mit deiner Zustimmung misst Google Analytics Seitenaufrufe und die Nutzung von Funktionen. Es wird erst nach deiner Zustimmung geladen.", accept: "Analyse erlauben", decline: "Jetzt nicht", settings: "Analyse-Einstellungen", privacy: "Datenschutzdetails" },
      id: { title: "Bantu tingkatkan SCP Docs", body: "Dengan persetujuan Anda, Google Analytics mengukur tampilan halaman dan penggunaan fitur. Analitik tidak dimuat sebelum Anda menyetujuinya.", accept: "Izinkan analitik", decline: "Jangan sekarang", settings: "Pengaturan analitik", privacy: "Detail privasi" },
      it: { title: "Aiutaci a migliorare SCP Docs", body: "Con il tuo consenso, Google Analytics misura le visualizzazioni e l’uso delle funzioni. Non viene caricato prima del consenso.", accept: "Consenti analisi", decline: "Non ora", settings: "Impostazioni analisi", privacy: "Dettagli sulla privacy" },
      "pt-br": { title: "Ajude a melhorar o SCP Docs", body: "Com sua permissão, o Google Analytics mede visualizações de página e uso de recursos. Ele não é carregado antes do seu consentimento.", accept: "Permitir análise", decline: "Agora não", settings: "Configurações de análise", privacy: "Detalhes de privacidade" },
      th: { title: "ช่วยปรับปรุง SCP Docs", body: "เมื่อคุณยินยอม Google Analytics จะวัดการเข้าชมหน้าและการใช้ฟีเจอร์ โดยจะไม่โหลดก่อนที่คุณจะอนุญาต", accept: "อนุญาตการวิเคราะห์", decline: "ไม่ใช่ตอนนี้", settings: "การตั้งค่าการวิเคราะห์", privacy: "รายละเอียดความเป็นส่วนตัว" },
      tr: { title: "SCP Docs'u geliştirmemize yardımcı olun", body: "İzninizle Google Analytics sayfa görüntülemelerini ve özellik kullanımını ölçer. Siz kabul edene kadar yüklenmez.", accept: "Analitiğe izin ver", decline: "Şimdi değil", settings: "Analitik ayarları", privacy: "Gizlilik ayrıntıları" },
      vi: { title: "Giúp cải thiện SCP Docs", body: "Khi bạn đồng ý, Google Analytics sẽ đo lượt xem trang và mức sử dụng tính năng. Công cụ này không được tải trước khi bạn chấp thuận.", accept: "Cho phép phân tích", decline: "Để sau", settings: "Cài đặt phân tích", privacy: "Chi tiết quyền riêng tư" },
      "zh-hans": { title: "帮助改进 SCP Docs", body: "仅在您同意后，我们才会使用 Google Analytics 衡量页面浏览量和功能使用情况。您同意前不会加载分析功能。", accept: "允许分析", decline: "暂不允许", settings: "分析设置", privacy: "隐私详情" },
      "zh-hant": { title: "協助改進 SCP Docs", body: "只有在您同意後，我們才會使用 Google Analytics 衡量頁面瀏覽量與功能使用情況。您同意前不會載入分析功能。", accept: "允許分析", decline: "暫不允許", settings: "分析設定", privacy: "隱私詳情" },
    };

    const state = { ready: false, granted: false, queued: [] };

    function localeCode() {
      const lang = String(document.documentElement.lang || "en").toLowerCase();
      if (lang === "pt" || lang.startsWith("pt-")) return "pt-br";
      if (lang === "zh-cn" || lang === "zh-sg" || lang === "zh-hans") return "zh-hans";
      if (lang.startsWith("zh")) return "zh-hant";
      return COPY[lang] ? lang : lang.split("-")[0];
    }

    function copy() {
      return COPY[localeCode()] || COPY.en;
    }

    function privacyHref() {
      const path = window.location.pathname;
      const filename = path.split("/").pop() || "index.html";
      const match = filename.match(/-(cs|de|es|fr|id|it|ja|ko|pl|pt-br|ru|th|tr|vi|zh-hans|zh-hant)\.html$/);
      return match ? `privacy-${match[1]}.html` : "privacy.html";
    }

    function readConsent() {
      try {
        return window.localStorage.getItem(SCPDocsAnalyticsCore.CONSENT_KEY);
      } catch (_) {
        return null;
      }
    }

    function writeConsent(value) {
      try {
        window.localStorage.setItem(SCPDocsAnalyticsCore.CONSENT_KEY, value);
      } catch (_) {
        // Analytics can still run for the current page if storage is unavailable.
      }
    }

    function gtag() {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push(arguments);
    }

    function track(name, parameters = {}) {
      if (!state.granted) return;
      const safeParameters = Object.fromEntries(
        Object.entries(parameters)
          .filter(([, value]) => value !== undefined && value !== null && value !== "")
          .map(([key, value]) => [key, typeof value === "string" ? SCPDocsAnalyticsCore.cleanValue(value) : value]),
      );
      if (!state.ready) {
        state.queued.push([name, safeParameters]);
        return;
      }
      gtag("event", name, safeParameters);
    }

    function loadAnalytics() {
      if (state.granted) return;
      state.granted = true;
      if (!SCPDocsAnalyticsCore.isAnalyticsHost(window.location.hostname)) return;
      window.dataLayer = window.dataLayer || [];
      gtag("consent", "default", { analytics_storage: "denied" });
      gtag("consent", "update", { analytics_storage: "granted" });
      gtag("js", new Date());
      gtag("config", SCPDocsAnalyticsCore.MEASUREMENT_ID, {
        allow_ad_personalization_signals: false,
        allow_google_signals: false,
        cookie_expires: 31536000,
        cookie_update: false,
        send_page_view: false,
      });

      const script = document.createElement("script");
      script.async = true;
      script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(SCPDocsAnalyticsCore.MEASUREMENT_ID)}`;
      script.addEventListener("load", () => {
        state.ready = true;
        gtag("event", "page_view", {
          page_location: SCPDocsAnalyticsCore.analyticsPageURL(window.location.href),
          page_path: SCPDocsAnalyticsCore.analyticsPagePath(window.location.href),
          page_title: document.title,
        });
        for (const [name, parameters] of state.queued.splice(0)) gtag("event", name, parameters);
      });
      document.head.append(script);
    }

    function removePrompt() {
      document.querySelector("#analytics-consent")?.remove();
    }

    function chooseConsent(value) {
      writeConsent(value);
      removePrompt();
      if (value === "granted") loadAnalytics();
    }

    function showPrompt() {
      removePrompt();
      const strings = copy();
      const prompt = document.createElement("aside");
      prompt.id = "analytics-consent";
      prompt.className = "analytics-consent";
      prompt.setAttribute("role", "dialog");
      prompt.setAttribute("aria-labelledby", "analytics-consent-title");

      const text = document.createElement("div");
      const title = document.createElement("h2");
      title.id = "analytics-consent-title";
      title.textContent = strings.title;
      const body = document.createElement("p");
      body.textContent = strings.body;
      const privacy = document.createElement("a");
      privacy.href = privacyHref();
      privacy.textContent = strings.privacy;
      text.append(title, body, privacy);

      const actions = document.createElement("div");
      const accept = document.createElement("button");
      accept.type = "button";
      accept.className = "analytics-consent-accept";
      accept.textContent = strings.accept;
      accept.addEventListener("click", () => chooseConsent("granted"));
      const decline = document.createElement("button");
      decline.type = "button";
      decline.textContent = strings.decline;
      decline.addEventListener("click", () => chooseConsent("denied"));
      actions.append(accept, decline);
      prompt.append(text, actions);
      document.body.append(prompt);
    }

    function addSettingsControl() {
      const footer = document.querySelector(".site-footer-inner > div:last-child") || document.querySelector(".site-footer");
      if (!footer || footer.querySelector("[data-analytics-settings]")) return;
      const button = document.createElement("button");
      button.type = "button";
      button.className = "analytics-settings";
      button.dataset.analyticsSettings = "";
      button.textContent = copy().settings;
      button.addEventListener("click", showPrompt);
      footer.append(document.createElement("br"), button);
    }

    function eventValue(element, attribute, fallback = "") {
      return element?.getAttribute(attribute) || fallback;
    }

    document.addEventListener("submit", event => {
      const form = event.target.closest?.("#catalog-search, .hero-catalog-search");
      if (!form) return;
      const term = SCPDocsAnalyticsCore.safeSearchTerm(new FormData(form).get("q"));
      track("search", {
        search_term: term,
        search_has_term: Boolean(term),
        search_source: form.id === "catalog-search" ? "catalog" : "home",
      });
    });

    document.addEventListener("change", event => {
      const control = event.target.closest?.("#filter-kind, #filter-object-class, #filter-length, #filter-score, #filter-sort");
      if (!control) return;
      track("search_filter", { filter_name: control.id.replace("filter-", ""), filter_value: control.value || "all" });
    });

    document.addEventListener("click", event => {
      const target = event.target.closest?.("a, button");
      if (!target) return;

      if (target.matches("[data-reading-theme]")) {
        track("reading_theme_select", { theme_id: eventValue(target, "data-reading-theme") });
        return;
      }
      if (target.matches("[data-search-preset]")) {
        track("search_preset_select", { preset: eventValue(target, "data-search-preset") });
        return;
      }
      if (target.matches(".tag-directory-chip, .discovery-tags button")) {
        track("search_tag_select", { tag: target.textContent });
        return;
      }
      if (!(target instanceof HTMLAnchorElement)) return;

      const href = target.getAttribute("href") || "";
      if (href.startsWith("scpdocs://")) {
        track("open_in_app", { source_page: SCPDocsAnalyticsCore.analyticsPagePath(window.location.href) });
        return;
      }

      let url;
      try {
        url = new URL(target.href, window.location.href);
      } catch (_) {
        return;
      }
      if (url.hostname === "apps.apple.com") {
        track("app_store_click", { source_page: SCPDocsAnalyticsCore.analyticsPagePath(window.location.href) });
      } else if (url.hostname.endsWith("wikidot.com")) {
        track("article_click", { article_host: url.hostname, article_path: url.pathname });
      } else if (/^\/reading(?:-|\.html)/.test(url.pathname) || url.pathname.includes("reading-")) {
        track("reading_lists_open", { destination: url.pathname });
      }
    });

    window.SCPDocsAnalytics = { showSettings: showPrompt, track };

    document.addEventListener("DOMContentLoaded", () => {
      addSettingsControl();
      const consent = readConsent();
      if (consent === "granted") loadAnalytics();
      else if (consent !== "denied") showPrompt();
    }, { once: true });
  })();
}
