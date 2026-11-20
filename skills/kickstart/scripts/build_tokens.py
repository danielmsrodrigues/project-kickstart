#!/usr/bin/env python3
"""Design tokens: one source file (design/tokens.json), native outputs per platform.

Source format: W3C Design Tokens (DTCG) - nested groups, tokens carry "$value"
and optionally "$type". Aliases look like "{color.palette.ink}".
Extensions this script reads from a token's "$extensions":
  "modes": {"dark": <value>}   dark-mode value (alias or literal)
  "lineHeight": 1.5            on font size tokens: paired line height

Groups named "palette" (e.g. color.palette.*) are primitives: they exist for
aliases. CSS keeps them as variables but gives them no Tailwind utilities;
Swift and TypeScript leave them out. Screens use the semantic tokens.

Colors: hex strings, or DTCG color objects {"colorSpace": "srgb", "components": [r, g, b], "alpha": a}.
Code names: camelCase from the path; a step name like "4x" becomes "x4" (Theme.Spacing.x4).

Usage (Python 3.8+, standard library only):
  python3 design/build_tokens.py build design/tokens.json --css src/styles/tokens.css
  python3 design/build_tokens.py build design/tokens.json --css src/styles/tokens.css --tailwind v4
  python3 design/build_tokens.py build design/tokens.json --css src/styles/tokens.css --tailwind v3 --tailwind-out tailwind.tokens.cjs
  python3 design/build_tokens.py build design/tokens.json --swift Sources/MyApp/DesignSystem/Theme+Generated.swift
  python3 design/build_tokens.py build design/tokens.json --ts src/theme/theme.ts
  python3 design/build_tokens.py diff  design/tokens.json candidate.json
  python3 design/build_tokens.py check src [more paths] [--allow GLOB ...]

Exit codes: 0 ok, 1 check found hardcoded values or diff found changes, 2 bad input.
"""
import argparse
import fnmatch
import json
import os
import re
import sys

HEADER = "Generated from design/tokens.json by design/build_tokens.py. Do not edit by hand."
ALIAS = re.compile(r"^\{([^}]+)\}$")
HEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")

# Top-level group name -> category. Unknown groups are kept as "other".
CATEGORIES = {
    "color": "color", "colors": "color",
    "spacing": "spacing", "space": "spacing",
    "radius": "radius", "radii": "radius",
    "size": "size", "sizes": "size",
    "font": "font", "typography": "font",
    "shadow": "shadow", "shadows": "shadow",
    "motion": "motion", "duration": "motion",
}
PRIMITIVE_GROUPS = {"palette"}


class TokenError(Exception):
    pass


def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise TokenError(f"{path}: {e}")


def flatten(tree, path=(), inherited_type=None, out=None):
    """Return {('color','text','primary'): {'value', 'type', 'dark', 'line_height_of'}}."""
    out = {} if out is None else out
    group_type = tree.get("$type", inherited_type)
    for key, node in tree.items():
        if key.startswith("$") or not isinstance(node, dict):
            continue
        p = path + (key,)
        if "$value" in node:
            ext = node.get("$extensions", {})
            out[p] = {"value": node["$value"], "type": node.get("$type", group_type),
                      "dark": ext.get("modes", {}).get("dark"), "line_height_of": None}
            if "lineHeight" in ext:
                out[p[:-1] + (key + "-line-height",)] = {"value": ext["lineHeight"], "type": "number",
                                                         "dark": None, "line_height_of": p}
        else:
            flatten(node, p, group_type, out)
    return out


def resolve(tokens):
    def follow(value, seen):
        if isinstance(value, str):
            m = ALIAS.match(value)
            if m:
                ref = tuple(m.group(1).split("."))
                if ref in seen:
                    raise TokenError("alias cycle: " + " -> ".join(".".join(s) for s in seen + [ref]))
                if ref not in tokens:
                    raise TokenError(f"unknown alias {value}")
                return follow(tokens[ref]["value"], seen + [ref])
        return value

    def color(value):
        if isinstance(value, dict) and "components" in value:  # DTCG 2025 color object
            if value.get("colorSpace", "srgb") != "srgb":
                raise TokenError(f"only srgb color objects are supported, got {value.get('colorSpace')}")
            r, g, b = (round(max(0.0, min(1.0, c)) * 255) for c in value["components"])
            a = round(max(0.0, min(1.0, value.get("alpha", 1))) * 255)
            return "#%02x%02x%02x" % (r, g, b) + ("" if a == 255 else "%02x" % a)
        if isinstance(value, dict) and "color" in value:  # shadow with a color object or alias inside
            return dict(value, color=color(follow(value["color"], [])))
        if isinstance(value, list):
            return [color(v) for v in value]
        return value

    return {p: dict(t, value=color(follow(t["value"], [p])),
                    dark=color(follow(t["dark"], [p])) if t["dark"] is not None else None)
            for p, t in tokens.items()}


def category(path):
    return CATEGORIES.get(path[0].lower(), "other")


def is_primitive(path):
    return len(path) > 1 and path[1].lower() in PRIMITIVE_GROUPS


def kebab(path):
    return "-".join(re.sub(r"[^0-9a-zA-Z]+", "-", s).strip("-").lower() for s in path)


def camel(parts):
    parts = [re.sub(r"^(\d+)x$", r"x\1", s) for s in parts]  # spacing step "4x" -> "x4"
    words = [w for s in parts for w in re.split(r"[^0-9a-zA-Z]+", s) if w]
    name = words[0].lower() + "".join(w[:1].upper() + w[1:] for w in words[1:])
    return "_" + name if name[:1].isdigit() else name


def dim(value):
    if isinstance(value, dict) and "value" in value and "unit" in value:  # DTCG dimension object
        return f"{value['value']}{value['unit']}"
    return str(value)


def css_value(value):
    if isinstance(value, list) and value and isinstance(value[0], dict):  # layered shadow
        return ", ".join(css_value(v) for v in value)
    if isinstance(value, list):  # font family stack
        return ", ".join(f'"{v}"' if " " in str(v) else str(v) for v in value)
    if isinstance(value, dict) and {"offsetX", "offsetY", "color"} <= set(value):  # DTCG shadow
        parts = [dim(value["offsetX"]), dim(value["offsetY"]), dim(value.get("blur", 0)),
                 dim(value.get("spread", 0)), str(value["color"])]
        return ("inset " if value.get("inset") else "") + " ".join(parts)
    if isinstance(value, dict) and "unit" in value:
        return dim(value)
    if isinstance(value, dict):
        raise TokenError(f"composite value not supported: {value}")
    return str(value)


def number(value):
    """Dimension -> number in points/px; None if not a px/pt/unitless number."""
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, dict) and value.get("unit") in ("px", "pt"):
        return value["value"]
    m = re.match(r"^(-?\d+(?:\.\d+)?)(px|pt)?$", str(value).strip())
    return float(m.group(1)) if m else None


def rgba(hex_value):
    h = HEX.match(str(hex_value))
    if not h:
        return None
    s = h.group(1)
    if len(s) in (3, 4):
        s = "".join(c * 2 for c in s)
    if len(s) == 6:
        s += "ff"
    return tuple(int(s[i:i + 2], 16) / 255 for i in range(0, 8, 2))


# ---------- CSS and Tailwind ----------

# Our CSS names already match these Tailwind v4 namespaces (--color-*, --spacing-*, ...).
TAILWIND_V4_NAMESPACES = ("color", "spacing", "radius", "shadow")
# Tailwind v4 also resolves max-w-*/w-* etc. against --spacing-<name>, so these names would
# override its container sizes (max-w-md would become your "md" spacing).
TAILWIND_CONTAINER_NAMES = {"3xs", "2xs", "xs", "sm", "md", "lg", "xl", "2xl", "3xl", "4xl", "5xl", "6xl", "7xl"}


def tailwind_v4_name(p, t):
    """Tailwind v4 theme variable for a token, or None if it gets no utility."""
    if is_primitive(p):
        return None
    cat = category(p)
    if cat in TAILWIND_V4_NAMESPACES:
        return kebab(p)
    if cat == "font":
        if t["line_height_of"]:
            return f"text-{kebab(t['line_height_of'][-1:])}--line-height"
        ns = {"fontFamily": "font", "fontWeight": "font-weight"}.get(t["type"], "text")
        return f"{ns}-{kebab(p[-1:])}"
    return None


def build_css(tokens, tailwind=None):
    """CSS custom properties on :root, dark overrides by media query and [data-theme].
    Tailwind v4: tokens whose variable name already is the Tailwind name are declared in
    @theme (utilities are generated from them); the rest get @theme inline aliases.
    Tailwind's default color palette is cleared so only tokens produce color utilities."""
    decl = lambda p, v: f"  --{kebab(p)}: {css_value(v)};"
    tw_names = {}
    if tailwind == "v4":
        seen = {}
        for p, t in tokens.items():
            name = tailwind_v4_name(p, t)
            if not name:
                continue
            if name in seen:
                raise TokenError(f"Tailwind name --{name} comes from both {'.'.join(seen[name])} and {'.'.join(p)}; rename one")
            if category(p) == "spacing" and kebab(p[1:]) in TAILWIND_CONTAINER_NAMES:
                raise TokenError(f"spacing.{'.'.join(p[1:])}: the name collides with Tailwind's container sizes "
                                 f"(max-w-{kebab(p[1:])} would use it). Use step names like 1x, 2x, 4x")
            if category(p) == "font" and t["type"] in ("fontFamily", "fontWeight"):
                utility = "font-" + kebab(p[-1:])  # family and weight share the font-<name> utility
                if utility in seen:
                    raise TokenError(f"{'.'.join(seen[utility])} and {'.'.join(p)} would both be the {utility} "
                                     "utility; give the weight or the family another name")
                seen[utility] = p
            seen[name] = p
            tw_names[p] = name
    in_theme = lambda p: tw_names.get(p) == kebab(p)
    theme = [decl(p, t["value"]) for p, t in tokens.items() if in_theme(p)]
    root = [decl(p, t["value"]) for p, t in tokens.items() if not in_theme(p)]
    dark = [decl(p, t["dark"]) for p, t in tokens.items() if t["dark"] is not None]
    css = [f"/* {HEADER} */"]
    if tailwind == "v4":
        css += ['/* Import this file right after @import "tailwindcss" in the app\'s CSS entry. */',
                "@theme {", "  --color-*: initial;", *theme, "}", ""]
    css += [":root {", *root, "}"]
    aliases = [f"  --{n}: var(--{kebab(p)});" for p, n in tw_names.items() if not in_theme(p)]
    if aliases:
        css += ["", "@theme inline {", *aliases, "}"]
    if dark:
        css += ["", "@media (prefers-color-scheme: dark) {", '  :root:not([data-theme="light"]) {',
                *["  " + d for d in dark], "  }", "}", "", ':root[data-theme="dark"] {', *dark, "}"]
    css = "\n".join(css) + "\n"

    tw = None
    if tailwind == "v3":
        groups = {}
        keys = {"color": "colors", "spacing": "spacing", "radius": "borderRadius", "shadow": "boxShadow"}
        for p, t in tokens.items():
            cat = category(p)
            if is_primitive(p) or t["line_height_of"]:
                continue
            if cat in keys:
                groups.setdefault(keys[cat], {})[kebab(p[1:])] = f"var(--{kebab(p)})"
            elif cat == "font":
                key = {"fontFamily": "fontFamily", "fontWeight": "fontWeight"}.get(t["type"], "fontSize")
                groups.setdefault(key, {})[kebab(p[-1:])] = f"var(--{kebab(p)})"
        tw = (f"// {HEADER}\n// Spread into theme.extend in tailwind.config (or theme, to drop Tailwind's defaults).\n"
              "module.exports = " + json.dumps(groups, indent=2) + ";\n")
    return css, tw


# ---------- SwiftUI ----------

SWIFT_WEIGHTS = {100: ".ultraLight", 200: ".thin", 300: ".light", 400: ".regular", 500: ".medium",
                 600: ".semibold", 700: ".bold", 800: ".heavy", 900: ".black"}


def swift_color(value):
    c = rgba(value)
    if not c:
        raise TokenError(f"Swift output needs hex colors, got {value}")
    return "SwiftUI.Color(rgba: 0x%02x%02x%02x%02x)" % tuple(round(x * 255) for x in c)


def swift_literal(t, value, size_of=None):
    """Return (type annotation or None, Swift expression)."""
    cat, typ = t["cat"], t["type"]
    if cat == "color" or typ == "color":
        return None, swift_color(value)
    if typ == "fontFamily":
        return None, json.dumps(value[0] if isinstance(value, list) else value)
    if typ == "fontWeight":
        return None, "Font.Weight" + SWIFT_WEIGHTS.get(int(value), ".regular")
    if typ == "duration":
        return "TimeInterval", "%g" % (float(str(value).rstrip("ms")) / 1000)  # seconds
    if t["line_height_of"]:  # ratio -> extra points between lines, what .lineSpacing() takes
        return "CGFloat", "%g" % round(number(size_of) * (float(value) - 1), 2)
    n = number(value)
    if n is None:
        raise TokenError(f"Swift output cannot convert {value!r} ({typ})")
    return "CGFloat", "%g" % n


def swift_shadow(value):
    layers = value if isinstance(value, list) else [value]
    v = layers[0]  # SwiftUI .shadow takes one layer; extra layers need stacked modifiers
    blur = number(v.get("blur", 0)) or 0
    return ("Theme.Shadow(color: %s, radius: %g, x: %g, y: %g)"
            % (swift_color(v["color"]), blur / 2, number(v["offsetX"]) or 0, number(v["offsetY"]) or 0))


def build_swift(tokens):
    enums = {"color": "Colors", "spacing": "Spacing", "radius": "Radius", "size": "Size",
             "font": "Typography", "shadow": "Shadows", "motion": "Motion", "other": "Other"}
    by_enum = {}
    for p, t in tokens.items():
        if is_primitive(p):
            continue
        cat = category(p)
        t = dict(t, cat=cat)
        name = camel(p[1:])
        if cat == "shadow":
            decl = f"        public static let {name} = {swift_shadow(t['value'])}"
        else:
            size_of = tokens[t["line_height_of"]]["value"] if t["line_height_of"] else None
            if t["line_height_of"]:
                name = camel(p[1:-1] + (t["line_height_of"][-1] + "-line-spacing",))
            typ, literal = swift_literal(t, t["value"], size_of)
            if t["dark"] is not None:
                literal = f"SwiftUI.Color(light: {literal}, dark: {swift_literal(t, t['dark'])[1]})"
            decl = f"        public static let {name}{': ' + typ if typ else ''} = {literal}"
        by_enum.setdefault(enums[cat], []).append(decl)
    out = [f"// {HEADER}", "// swiftlint:disable all", "import SwiftUI", "", "public enum Theme {}", ""]
    for name, lines in by_enum.items():
        out += ["public extension Theme {", f"    enum {name} {{", *lines, "    }", "}", ""]
    if "Shadows" in by_enum:
        out += ["public extension Theme {",
                "    struct Shadow: Sendable {",
                "        public let color: SwiftUI.Color",
                "        public let radius: CGFloat",
                "        public let x: CGFloat",
                "        public let y: CGFloat",
                "    }",
                "}",
                "",
                "public extension View {",
                "    /// Applies a shadow token: `.themeShadow(Theme.Shadows.raised)`.",
                "    func themeShadow(_ shadow: Theme.Shadow) -> some View {",
                "        self.shadow(color: shadow.color, radius: shadow.radius, x: shadow.x, y: shadow.y)",
                "    }",
                "}",
                ""]
    out += ["extension SwiftUI.Color {",
            "    init(rgba: UInt32) {",
            "        self.init(.sRGB,",
            "                  red: Double((rgba >> 24) & 0xff) / 255,",
            "                  green: Double((rgba >> 16) & 0xff) / 255,",
            "                  blue: Double((rgba >> 8) & 0xff) / 255,",
            "                  opacity: Double(rgba & 0xff) / 255)",
            "    }",
            ""]
    if any(t["dark"] is not None for t in tokens.values()):
        out += ["    init(light: SwiftUI.Color, dark: SwiftUI.Color) {",
                "        #if canImport(UIKit)",
                "        self.init(UIColor { traits in",
                "            traits.userInterfaceStyle == .dark ? UIColor(dark) : UIColor(light)",
                "        })",
                "        #elseif canImport(AppKit)",
                "        self.init(NSColor(name: nil) { appearance in",
                "            appearance.bestMatch(from: [.darkAqua, .aqua]) == .darkAqua ? NSColor(dark) : NSColor(light)",
                "        })",
                "        #else",
                "        self = light",
                "        #endif",
                "    }"]
    out += ["}", ""]
    return "\n".join(out)


# ---------- TypeScript (React Native) ----------

def build_ts(tokens):
    def tree(mode):
        root = {}
        for p, t in tokens.items():
            if is_primitive(p):
                continue
            value = t["dark"] if mode == "dark" and t["dark"] is not None else t["value"]
            numeric = category(p) in ("spacing", "radius", "size") or t["type"] in ("dimension", "number")
            n = number(value) if numeric else None
            node = root
            for key in [camel([s]) for s in p[:-1]]:
                node = node.setdefault(key, {})
            node[camel([p[-1]])] = n if n is not None else css_value(value)
        return root

    return (f"// {HEADER}\n"
            f"export const lightTheme = {json.dumps(tree('light'), indent=2)} as const;\n\n"
            f"export const darkTheme: Theme = {json.dumps(tree('dark'), indent=2)};\n\n"
            "export type Theme = Widen<typeof lightTheme>;\n"
            "type Widen<T> = { [K in keyof T]: T[K] extends string ? string : T[K] extends number ? number : Widen<T[K]> };\n")


# ---------- diff ----------

def diff(old_path, new_path):
    old_raw, new_raw = flatten(load(old_path)), flatten(load(new_path))
    old, new = resolve(old_raw), resolve(new_raw)
    show = lambda t, r: (f"{r['value']}" if r["value"] == t["value"] else f"{r['value']} = {t['value']}") + \
        (f" (dark {t['dark']})" if t["dark"] is not None else "")
    lines = []
    for p in sorted(set(old) | set(new)):
        name = ".".join(p)
        css = f"--{kebab(p)} | {camel(p[1:])}"
        if p not in new:
            lines.append(f"- {name} [{css}]: {show(old[p], old_raw[p])}")
        elif p not in old:
            lines.append(f"+ {name} [{css}]: {show(new[p], new_raw[p])}")
        elif (old_raw[p]["value"], old_raw[p]["dark"]) != (new_raw[p]["value"], new_raw[p]["dark"]):
            lines.append(f"~ {name} [{css}]: {show(old[p], old_raw[p])} -> {show(new[p], new_raw[p])}")
        elif (old[p]["value"], old[p]["dark"]) != (new[p]["value"], new[p]["dark"]):
            res = lambda t: str(t["value"]) + (f" (dark {t['dark']})" if t["dark"] is not None else "")
            lines.append(f"  {name} [{css}]: follows alias {new_raw[p]['value']}: {res(old[p])} -> {res(new[p])}")
    print("\n".join(lines) if lines else "No token changes.")
    return 1 if lines else 0


# ---------- check ----------

TW_COLORS = ("slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|"
             "blue|indigo|violet|purple|fuchsia|pink|rose")
SWIFT_COLORS = "red|orange|yellow|green|mint|teal|cyan|blue|indigo|purple|pink|brown|gray|black|white"
HARDCODED = [
    ("hex color", re.compile(r"(?<![\w&])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b")),
    ("rgb/hsl color", re.compile(r"\b(?:rgba?|hsla?)\(\s*\d")),
    ("primitive token used directly", re.compile(r"--color-palette-|\bpalette\.[a-z]")),
    ("Tailwind arbitrary value", re.compile(r"\b[a-z][\w:-]*-\[(?:#|-?\d+(?:\.\d+)?(?:px|rem|em)\b)")),
    ("Tailwind default palette", re.compile(rf"\b[a-z]+-(?:{TW_COLORS})-\d{{2,3}}\b")),
    ("CSS length literal", re.compile(r"\b(?:margin|padding|gap|row-gap|column-gap|border-radius|font-size|"
                                      r"line-height|width|height|max-width|min-height|inset|top|left|right|bottom)"
                                      r"(?:-[a-z]+)?\s*:\s*[^;{}]*?(?<![\w.-])[1-9]\d*(?:\.\d+)?(?:px|rem|em)\b")),
    ("style length literal", re.compile(r"\b(?:margin|padding|gap|borderRadius|fontSize|lineHeight)\w*\s*:\s*['\"]?[1-9]\d*")),
]
SWIFT_HARDCODED = [
    ("SwiftUI color literal", re.compile(rf"Color\(\s*(?:\.sRGB\s*,\s*)?(?:red|hue|white):|#colorLiteral\(|Color\(\s*\"|"
                                         rf"Color\.(?:{SWIFT_COLORS})\b|(?<![\w.])\.(?:{SWIFT_COLORS})\.opacity\(")),
    ("SwiftUI length literal", re.compile(r"\.padding\([^)]*?(?<![\w.])[1-9]\d*(?:\.\d+)?\s*\)|EdgeInsets\([^)]*:\s*[1-9]|"
                                          r"\.frame\([^)]*\b(?:width|height|minWidth|minHeight|maxWidth|maxHeight):\s*[1-9]|"
                                          r"\bspacing:\s*[1-9]|cornerRadius(?::|\()\s*[1-9]|lineWidth:\s*[1-9]|"
                                          r"\.border\([^)]*width:\s*[1-9]|\.lineSpacing\(\s*[1-9]|\.shadow\([^)]*radius:\s*[1-9]|"
                                          r"\bpadding:\s*[1-9]")),
    ("SwiftUI font literal", re.compile(r"\bsize:\s*[1-9]|\.font\(\s*\.(?:largeTitle|title|title2|title3|headline|"
                                        r"subheadline|body|callout|footnote|caption|caption2)\b")),
]
SCAN_EXT = {".css", ".scss", ".less", ".html", ".jsx", ".tsx", ".js", ".ts", ".vue", ".svelte",
            ".astro", ".razor", ".cshtml", ".swift", ".dart", ".kt"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".build", "bin", "obj", "DerivedData", ".next"}
LINE_COMMENT = re.compile(r"(?:^|\s)//.*$")  # whitespace before // keeps https:// intact


def check(paths, allow):
    allow = list(allow) + ["*tokens*", "*Theme+Generated*", "*.min.*", "*/theme/theme.ts", "*/build_tokens.py"]
    missing = [p for p in paths if not os.path.exists(p)]
    if missing:
        raise TokenError("path not found: " + ", ".join(missing))
    hits = 0
    for root in paths:
        walk = os.walk(root) if os.path.isdir(root) else [(os.path.dirname(root) or ".", [], [os.path.basename(root)])]
        for dirpath, dirs, files in walk:
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for fn in files:
                path = os.path.join(dirpath, fn)
                ext = os.path.splitext(fn)[1]
                if ext not in SCAN_EXT or any(fnmatch.fnmatch(path, g) for g in allow):
                    continue
                rules = HARDCODED + (SWIFT_HARDCODED if ext == ".swift" else [])
                with open(path, encoding="utf-8", errors="ignore") as f:
                    for no, line in enumerate(f, 1):
                        code = line.strip()
                        if code.startswith(("//", "/*", "*", "<!--")):
                            continue
                        if ext not in (".css", ".scss", ".less", ".html"):
                            code = LINE_COMMENT.sub("", code)
                        for label, rx in rules:
                            if rx.search(code):
                                print(f"{path}:{no}: {label}: {line.strip()[:120]}")
                                hits += 1
                                break
    if hits:
        print(f"\n{hits} line(s) with hardcoded values. Use a token from design/tokens.json instead "
              "(or --allow GLOB for files that must hold literals).", file=sys.stderr)
    return 1 if hits else 0


# ---------- CLI ----------

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("source")
    b.add_argument("--css")
    b.add_argument("--tailwind", choices=["v3", "v4"])
    b.add_argument("--tailwind-out")
    b.add_argument("--swift")
    b.add_argument("--ts")
    d = sub.add_parser("diff")
    d.add_argument("old")
    d.add_argument("new")
    c = sub.add_parser("check")
    c.add_argument("paths", nargs="+")
    c.add_argument("--allow", nargs="*", default=[])
    a = ap.parse_args(argv)
    try:
        if a.cmd == "diff":
            return diff(a.old, a.new)
        if a.cmd == "check":
            return check(a.paths, a.allow)
        tokens = resolve(flatten(load(a.source)))
        if not tokens:
            raise TokenError(f"{a.source}: no tokens found (tokens need a \"$value\")")
        if not (a.css or a.swift or a.ts):
            raise TokenError("pick at least one output: --css, --swift or --ts")
        if a.tailwind and not a.css:
            raise TokenError("--tailwind needs --css")
        if a.tailwind == "v3" and not a.tailwind_out:
            raise TokenError("--tailwind v3 needs --tailwind-out")
        outputs = []
        if a.css:
            css, tw = build_css(tokens, a.tailwind)
            outputs += [(a.css, css)] + ([(a.tailwind_out, tw)] if tw else [])
        if a.swift:
            outputs.append((a.swift, build_swift(tokens)))
        if a.ts:
            outputs.append((a.ts, build_ts(tokens)))
        for path, text in outputs:  # write only after every output built without errors
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
        print(f"{len(tokens)} tokens -> " + ", ".join(p for p, _ in outputs))
        return 0
    except TokenError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
