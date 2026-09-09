// Forge Classic neo has UI text that changes dynamically (for example,
// "Brush Width (25)"). Its native localization only performs exact lookups.
// Support the same @@regex keys used by the bundled bilingual translator.
(function () {
  let regexTranslations = [];

  function buildRegexTranslations() {
    regexTranslations = [];
    const localization = window.localization;
    if (!localization) return;

    for (const [key, value] of Object.entries(localization)) {
      if (!key.startsWith("@@")) continue;
      try {
        regexTranslations.push([new RegExp(key.slice(2)), value]);
      } catch (error) {
        console.warn(`[ja_JP] Invalid localization regex: ${key}`, error);
      }
    }
  }

  function translateString(source) {
    if (!source) return source;
    const trimmed = source.trim();
    if (!trimmed) return source;

    for (const [regex, replacement] of regexTranslations) {
      regex.lastIndex = 0;
      if (!regex.test(trimmed)) continue;
      regex.lastIndex = 0;
      const translated = trimmed.replace(regex, replacement);
      return source.replace(trimmed, translated);
    }

    return source;
  }

  function processNode(node) {
    if (!node) return;

    if (node.nodeType === Node.TEXT_NODE) {
      const translated = translateString(node.textContent);
      if (translated !== node.textContent) node.textContent = translated;
      return;
    }

    if (node.nodeType !== Node.ELEMENT_NODE && node.nodeType !== Node.DOCUMENT_FRAGMENT_NODE) return;

    if (node.nodeType === Node.ELEMENT_NODE) {
      if (node.title) {
        const translatedTitle = translateString(node.title);
        if (translatedTitle !== node.title) node.title = translatedTitle;
      }
      if (node.placeholder) {
        const translatedPlaceholder = translateString(node.placeholder);
        if (translatedPlaceholder !== node.placeholder) node.placeholder = translatedPlaceholder;
      }
    }

    const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT);
    let textNode;
    while ((textNode = walker.nextNode())) processNode(textNode);
  }

  document.addEventListener("DOMContentLoaded", function () {
    buildRegexTranslations();
    if (regexTranslations.length === 0) return;

    const app = typeof gradioApp === "function" ? gradioApp() : document;
    processNode(app);

    if (typeof onUiUpdate === "function") {
      onUiUpdate(function (mutations) {
        for (const mutation of mutations) {
          for (const node of mutation.addedNodes) processNode(node);
        }
      });
    }
  });
})();
