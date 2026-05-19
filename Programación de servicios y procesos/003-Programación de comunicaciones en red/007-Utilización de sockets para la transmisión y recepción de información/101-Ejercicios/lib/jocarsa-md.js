/* jocarsa-md.js
   Tiny Markdown -> HTML (no deps)
   Usage:
     import { mdToHtml } from "./jocarsa-md.js";
     el.innerHTML = mdToHtml(markdownString);
*/

export function mdToHtml(markdown, opts = {}) {
  const options = {
    sanitize: opts.sanitize !== false, // default true
  };

  const src = String(markdown ?? "").replace(/\r\n?/g, "\n");

  // --- helpers ---
  const escapeHTML = (s) =>
    String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");

  const escapeAttr = (s) => {
    const v = String(s).replace(/"/g, "&quot;").trim();
    if (/^\s*javascript:/i.test(v)) return "#";
    return v;
  };

  // --- extract fenced code blocks ---
  const codeBlocks = [];
  let text = src.replace(/```([a-zA-Z0-9_-]+)?\n([\s\S]*?)```/g, (_m, lang, code) => {
    const i = codeBlocks.length;
    codeBlocks.push({
      lang: (lang || "").trim(),
      code: (code || "").replace(/\n$/, ""),
    });
    return `\n@@JOCARSA_CODEBLOCK_${i}@@\n`;
  });

  const lines = text.split("\n");
  const out = [];

  let inUL = false;
  let inOL = false;
  let inBQ = false;
  let paragraph = [];

  const closeLists = () => {
    if (inUL) { out.push("</ul>"); inUL = false; }
    if (inOL) { out.push("</ol>"); inOL = false; }
  };

  const closeBQ = () => {
    if (inBQ) { out.push("</blockquote>"); inBQ = false; }
  };

  const renderInline = (s) => {
    let x = escapeHTML(s);

    // links: [text](url)
    x = x.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_m, txt, url) => {
      return `<a href="${escapeAttr(url)}">${txt}</a>`;
    });

    // inline code: `code`
    x = x.replace(/`([^`]+)`/g, (_m, code) => `<code>${escapeHTML(code)}</code>`);

    // bold / italic
    x = x.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    x = x.replace(/\*([^*]+)\*/g, "<em>$1</em>");

    // hard line breaks inside paragraphs
    x = x.replace(/\n/g, "<br>");

    return x;
  };

  const flushParagraph = () => {
    if (!paragraph.length) return;
    const p = paragraph.join("\n").trim();
    paragraph = [];
    if (!p) return;
    out.push(`<p>${renderInline(p)}</p>`);
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // code block placeholder as standalone line
    const cbm = line.match(/^@@JOCARSA_CODEBLOCK_(\d+)@@$/);
    if (cbm) {
      flushParagraph();
      closeLists();
      closeBQ();

      const cb = codeBlocks[Number(cbm[1])];
      const langClass = cb.lang ? ` class="language-${escapeHTML(cb.lang)}"` : "";
      out.push(`<pre><code${langClass}>${escapeHTML(cb.code)}</code></pre>`);
      continue;
    }

    // hr
    if (/^\s*((---)|(\*\*\*)|(___))\s*$/.test(line)) {
      flushParagraph();
      closeLists();
      closeBQ();
      out.push("<hr>");
      continue;
    }

    // heading
    const h = line.match(/^(#{1,6})\s+(.*)$/);
    if (h) {
      flushParagraph();
      closeLists();
      closeBQ();
      const level = h[1].length;
      out.push(`<h${level}>${renderInline(h[2].trim())}</h${level}>`);
      continue;
    }

    // blockquote
    const bq = line.match(/^\s*>\s?(.*)$/);
    if (bq) {
      flushParagraph();
      closeLists();
      if (!inBQ) { out.push("<blockquote>"); inBQ = true; }
      const content = bq[1].trim();
      out.push(content ? `${renderInline(content)}<br>` : "<br>");
      continue;
    } else {
      closeBQ();
    }

    // unordered list
    const ul = line.match(/^\s*[-*+]\s+(.*)$/);
    if (ul) {
      flushParagraph();
      if (inOL) { out.push("</ol>"); inOL = false; }
      if (!inUL) { out.push("<ul>"); inUL = true; }
      out.push(`<li>${renderInline(ul[1].trim())}</li>`);
      continue;
    }

    // ordered list
    const ol = line.match(/^\s*\d+\.\s+(.*)$/);
    if (ol) {
      flushParagraph();
      if (inUL) { out.push("</ul>"); inUL = false; }
      if (!inOL) { out.push("<ol>"); inOL = true; }
      out.push(`<li>${renderInline(ol[1].trim())}</li>`);
      continue;
    }

    // blank line
    if (/^\s*$/.test(line)) {
      flushParagraph();
      closeLists();
      continue;
    }

    // normal text
    closeLists();
    paragraph.push(line);
  }

  flushParagraph();
  closeLists();
  closeBQ();

  const html = out.join("\n");
  return options.sanitize ? sanitize(html) : html;

  // Minimal sanitizer (small allowlist). For untrusted input, prefer DOMPurify.
  function sanitize(htmlStr) {
    const tpl = document.createElement("template");
    tpl.innerHTML = String(htmlStr);

    const ALLOWED = new Set([
      "A","P","BR","HR",
      "H1","H2","H3","H4","H5","H6",
      "UL","OL","LI",
      "BLOCKQUOTE",
      "PRE","CODE",
      "EM","STRONG",
    ]);

    const ALLOWED_ATTR = {
      "A": new Set(["href"]),
      "CODE": new Set(["class"]),
    };

    const walk = (node) => {
      if (node.nodeType === Node.COMMENT_NODE) {
        node.remove();
        return;
      }

      if (node.nodeType === Node.ELEMENT_NODE) {
        const tag = node.tagName.toUpperCase();

        if (!ALLOWED.has(tag)) {
          node.replaceWith(document.createTextNode(node.textContent || ""));
          return;
        }

        for (const attr of Array.from(node.attributes)) {
          const allowedForTag = ALLOWED_ATTR[tag] || new Set();
          if (!allowedForTag.has(attr.name)) node.removeAttribute(attr.name);
        }

        if (tag === "A") {
          const href = node.getAttribute("href") || "";
          if (/^\s*javascript:/i.test(href)) node.setAttribute("href", "#");
        }
      }

      for (const child of Array.from(node.childNodes)) walk(child);
    };

    walk(tpl.content);
    return tpl.innerHTML;
  }
}

