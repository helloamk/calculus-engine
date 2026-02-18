import streamlit as st
import sympy as sp
from sympy import (
    symbols, diff, integrate, latex, sympify, simplify,
    sin, cos, tan, exp, log, sqrt, Derivative, Integral,
    expand, Symbol, oo, pi, E,
    asin, acos, atan, sinh, cosh, tanh, sec, csc, cot,
    Mul, Add, Pow, Rational, Integer, preorder_traversal
)
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Advanced Calculus Solver - MathWithAmrit",
                   page_icon="📐", layout="wide",
                   initial_sidebar_state="collapsed")

for k, v in [('operation', None), ('show_formula', False), ('show_graph', False),
             ('der_solved', False), ('der_inputs', None),
             ('trp_solved', False), ('trp_inputs', None),
             ('dbl_solved', False), ('dbl_inputs', None),
             ('int_solved', False), ('int_inputs', None)]:
    if k not in st.session_state: st.session_state[k] = v

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  CSS                                                                     ║
# ╚══════════════════════════════════════════════════════════════════════════╝
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

[data-theme="dark"],.stApp[data-theme="dark"]{--bg:#0b0f1a;--surface:#111827;--surface2:#1a2235;--border:#1e293b;--text-head:#f0f6ff;--text-body:#94a3b8;--text-muted:#4b5563;--step-bg:#0f172a;}
[data-theme="light"],.stApp[data-theme="light"]{--bg:#f0f4ff;--surface:#ffffff;--surface2:#f8faff;--border:#dde3f0;--text-head:#0f172a;--text-body:#475569;--text-muted:#94a3b8;--step-bg:#f1f5fb;}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0b0f1a;--surface:#111827;--surface2:#1a2235;--border:#1e293b;--text-head:#f0f6ff;--text-body:#94a3b8;--text-muted:#4b5563;--step-bg:#0f172a;}}
@media(prefers-color-scheme:light){:root:not([data-theme="dark"]){--bg:#f0f4ff;--surface:#ffffff;--surface2:#f8faff;--border:#dde3f0;--text-head:#0f172a;--text-body:#475569;--text-muted:#94a3b8;--step-bg:#f1f5fb;}}
:root{--accent1:#4f8ef7;--accent2:#a78bfa;--accent3:#34d399;--accent4:#fb923c;}

html,body,.stApp{background-color:var(--bg)!important;font-family:'Sora',sans-serif!important;color:var(--text-body)!important;}
#MainMenu,footer,header{visibility:hidden;}
/* ── Hide Streamlit watermark, deploy button & all branding ── */
[data-testid="stToolbar"]{display:none!important;}
[data-testid="stDecoration"]{display:none!important;}
[data-testid="stStatusWidget"]{display:none!important;}
[data-testid="stDeployButton"]{display:none!important;}
.stDeployButton{display:none!important;}
[data-testid="stBottom"]{display:none!important;}
[data-testid="stBottomBlockContainer"]{display:none!important;}
._profileContainer_gzau3_53{display:none!important;}
._container_gzau3_1{display:none!important;}
._profilePreview_gzau3_63{display:none!important;}
div[class*="ProfileContainer"]{display:none!important;}
div[class*="profileContainer"]{display:none!important;}
section[data-testid="stFooter"]{display:none!important;}
.reportview-container .main footer{display:none!important;}
.block-container{padding:1.5rem 2.5rem 3rem!important;max-width:1400px!important;}

/* ── Mobile ── */
@media(max-width:768px){
  .block-container{padding:1rem 0.75rem 2rem!important;}
  [data-testid="column"]{width:100%!important;flex:100%!important;min-width:100%!important;}
  [data-testid="stHorizontalBlock"]{flex-wrap:wrap!important;gap:0!important;}
}

/* ── Hero — minimal ── */
.hero-wrap{text-align:center;padding:2.5rem 1rem 1.5rem;margin-bottom:1.5rem;}
.hero-title{font-size:clamp(1.6rem,4vw,2.8rem);font-weight:800;color:var(--text-head);line-height:1.2;margin-bottom:0.6rem;}
.hero-title span{background:linear-gradient(90deg,var(--accent1),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.hero-sub{color:var(--text-body);font-size:0.95rem;max-width:480px;margin:0 auto;line-height:1.6;}

/* ── Section heading ── */
.section-heading{text-align:center;margin-bottom:1.8rem;}
.section-heading h2{font-size:1.3rem;font-weight:700;color:var(--text-head);margin-bottom:0.3rem;}
.section-heading p{color:var(--text-muted);font-size:0.85rem;}
@media(max-width:768px){.section-heading h2{font-size:1.1rem;}}

/* ── Op-card ── */
.op-card{background:var(--surface);border:1.5px solid var(--border);border-radius:20px 20px 0 0;padding:2rem 1.5rem 1.4rem;text-align:center;position:relative;overflow:hidden;margin-bottom:0;}
.op-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:20px 20px 0 0;background:linear-gradient(90deg,transparent,var(--c),transparent);}
.card-der{--c:#4f8ef7;}.card-int{--c:#a78bfa;}.card-dbl{--c:#34d399;}.card-trp{--c:#fb923c;}
@media(max-width:768px){.op-card{padding:1.4rem 1rem 1rem;border-radius:14px 14px 0 0;}}

.op-symbol-text{font-family:'JetBrains Mono',monospace;font-size:2rem;font-weight:800;color:var(--c);text-shadow:0 2px 12px color-mix(in srgb,var(--c) 40%,transparent);display:flex;align-items:center;justify-content:center;height:80px;margin-bottom:0.75rem;}
@media(max-width:768px){.op-symbol-text{height:58px;font-size:1.6rem;}}

.op-name{font-size:1.05rem;font-weight:700;color:var(--text-head);margin-bottom:0.5rem;}
.op-caption{font-size:0.8rem;color:var(--text-muted);line-height:1.55;min-height:3rem;}
@media(max-width:768px){.op-name{font-size:0.95rem;}.op-caption{font-size:0.75rem;min-height:auto;}}

/* ── Card buttons — solid, high-contrast ── */
div[id^="card-btn-"]{margin-top:0!important;}
div[id^="card-btn-"]>div{margin-top:0!important;}
div[id^="card-btn-"] .stButton{width:100%;}
div[id^="card-btn-"] .stButton>button{width:100%!important;border-radius:0 0 20px 20px!important;font-family:'Sora',sans-serif!important;font-size:1.08rem!important;font-weight:900!important;letter-spacing:0.03em!important;text-transform:none!important;padding:1.25rem 1rem!important;border-width:0!important;border-top:none!important;margin-top:0!important;cursor:pointer!important;transition:all 0.22s ease!important;line-height:1.3!important;}
#card-btn-der .stButton>button{background:linear-gradient(135deg,#3b7ef5,#5b9bff)!important;border-color:#2d6ee8!important;color:#fff!important;box-shadow:0 4px 18px rgba(79,142,247,0.45)!important;}
#card-btn-der .stButton>button:hover{background:linear-gradient(135deg,#2d6ee8,#4f8ef7)!important;box-shadow:0 8px 28px rgba(79,142,247,0.6)!important;transform:translateY(-2px)!important;}
#card-btn-int .stButton>button{background:linear-gradient(135deg,#8b5cf6,#a78bfa)!important;border-color:#7c3aed!important;color:#fff!important;box-shadow:0 4px 18px rgba(167,139,250,0.45)!important;}
#card-btn-int .stButton>button:hover{background:linear-gradient(135deg,#7c3aed,#8b5cf6)!important;box-shadow:0 8px 28px rgba(167,139,250,0.6)!important;transform:translateY(-2px)!important;}
#card-btn-dbl .stButton>button{background:linear-gradient(135deg,#10b981,#34d399)!important;border-color:#059669!important;color:#fff!important;box-shadow:0 4px 18px rgba(52,211,153,0.45)!important;}
#card-btn-dbl .stButton>button:hover{background:linear-gradient(135deg,#059669,#10b981)!important;box-shadow:0 8px 28px rgba(52,211,153,0.6)!important;transform:translateY(-2px)!important;}
#card-btn-trp .stButton>button{background:linear-gradient(135deg,#f97316,#fb923c)!important;border-color:#ea6c0a!important;color:#fff!important;box-shadow:0 4px 18px rgba(251,146,60,0.45)!important;}
#card-btn-trp .stButton>button:hover{background:linear-gradient(135deg,#ea6c0a,#f97316)!important;box-shadow:0 8px 28px rgba(251,146,60,0.6)!important;transform:translateY(-2px)!important;}
@media(max-width:768px){div[id^="card-btn-"] .stButton>button{font-size:0.9rem!important;padding:1rem 0.8rem!important;border-radius:0 0 14px 14px!important;font-weight:900!important;}div[id^="card-btn-"]{margin-bottom:1.2rem!important;}}



/* ── Solver banner ── */
.solver-banner{background:var(--surface);border:1.5px solid var(--border);border-radius:18px;padding:1.5rem 2rem;display:flex;align-items:center;gap:1.2rem;margin-bottom:1.8rem;}
.solver-banner .sb-symbol{min-width:3rem;text-align:center;display:flex;align-items:center;justify-content:center;}
.solver-banner .sb-text h3{font-size:1.25rem;font-weight:700;color:var(--text-head);margin:0 0 0.2rem;}
.solver-banner .sb-text p{font-size:0.85rem;color:var(--text-muted);margin:0;}
@media(max-width:768px){.solver-banner{padding:1rem 1.2rem;gap:0.8rem;border-radius:12px;margin-bottom:1.2rem;}.solver-banner .sb-text h3{font-size:1rem;}.solver-banner .sb-text p{font-size:0.75rem;}}

/* ── Buttons ── */
#back-btn .stButton>button{background:var(--surface)!important;border:1px solid var(--border)!important;color:var(--text-body)!important;border-radius:10px!important;font-family:'Sora',sans-serif!important;font-size:0.85rem!important;font-weight:500!important;padding:0.5rem 1.4rem!important;transition:border-color 0.2s,color 0.2s!important;}
#back-btn .stButton>button:hover{border-color:var(--accent1)!important;color:var(--accent1)!important;}
#solve-btn .stButton>button{background:linear-gradient(135deg,var(--accent1),var(--accent2))!important;border:none!important;color:#fff!important;border-radius:12px!important;font-family:'Sora',sans-serif!important;font-size:1.1rem!important;font-weight:900!important;padding:1rem 2.2rem!important;letter-spacing:0.04em!important;width:100%!important;box-shadow:0 6px 28px rgba(79,142,247,0.5)!important;transition:opacity 0.2s,transform 0.15s!important;}
#solve-btn .stButton>button:hover{opacity:0.88!important;transform:translateY(-2px)!important;}

/* ── Inputs ── */
.stTextInput>div>div>input,.stTextArea>div>div>textarea,.stNumberInput>div>div>input{background:var(--surface2)!important;border:1px solid var(--border)!important;border-radius:10px!important;color:var(--text-head)!important;font-family:'JetBrains Mono',monospace!important;font-size:0.88rem!important;}
.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus,.stNumberInput>div>div>input:focus{border-color:var(--accent1)!important;box-shadow:0 0 0 3px rgba(79,142,247,0.15)!important;}
.stSelectbox>div>div{background:var(--surface2)!important;border:1px solid var(--border)!important;border-radius:10px!important;color:var(--text-head)!important;}
label,.stTextInput label,.stTextArea label,.stNumberInput label,.stSelectbox label,.stCheckbox label{color:var(--text-body)!important;font-size:0.85rem!important;font-weight:500!important;}

/* ── Step / solution cards ── */
.step-card{background:var(--step-bg);border:1px solid var(--border);border-left:3px solid var(--accent1);border-radius:12px;padding:1.25rem 1.5rem;margin-bottom:1rem;}
.formula-card{background:color-mix(in srgb,var(--accent1) 5%,var(--surface));border:1px solid color-mix(in srgb,var(--accent1) 22%,transparent);border-radius:12px;padding:1.25rem 1.5rem;margin-bottom:1rem;}
.formula-rule{background:color-mix(in srgb,var(--accent2) 6%,var(--surface));border:1px solid color-mix(in srgb,var(--accent2) 20%,transparent);border-radius:10px;padding:1rem 1.4rem;margin-bottom:0.75rem;}
.final-card{background:linear-gradient(135deg,color-mix(in srgb,var(--accent3) 8%,var(--surface)),color-mix(in srgb,var(--accent1) 8%,var(--surface)));border:1.5px solid color-mix(in srgb,var(--accent3) 30%,transparent);border-radius:14px;padding:1.5rem 1.8rem;margin-bottom:1rem;}
.tip-box{background:color-mix(in srgb,var(--accent4) 7%,var(--surface));border:1px solid color-mix(in srgb,var(--accent4) 22%,transparent);border-radius:10px;padding:0.85rem 1.2rem;margin-top:0.5rem;font-size:0.83rem;color:var(--text-body);}
@media(max-width:768px){.step-card,.formula-card,.final-card{padding:1rem;border-radius:10px;}}

.input-panel-head,.solution-panel-head{font-size:1rem;font-weight:700;color:var(--text-head);margin-bottom:1rem;padding-bottom:0.6rem;border-bottom:1px solid var(--border);}
.disp-options-head{font-size:0.78rem;font-weight:700;color:var(--text-muted);letter-spacing:0.1em;text-transform:uppercase;margin:1rem 0 0.5rem;}
.step-label{font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--accent1);margin-bottom:0.3rem;}
.step-title{font-size:1rem;font-weight:700;color:var(--text-head);margin-bottom:0.5rem;}
.step-explain{font-size:0.85rem;color:var(--text-body);margin-top:0.5rem;line-height:1.6;}
.rule-tag{display:inline-block;background:color-mix(in srgb,var(--accent2) 15%,transparent);border:1px solid color-mix(in srgb,var(--accent2) 30%,transparent);color:var(--accent2);font-size:0.68rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;padding:0.15rem 0.6rem;border-radius:999px;margin-left:0.5rem;vertical-align:middle;}

.footer-wrap{text-align:center;padding:2rem 0 1rem;color:var(--text-muted);font-size:0.78rem;}
.footer-wrap strong{color:var(--accent1);}
hr{border-color:var(--border)!important;margin:1.5rem 0!important;}
.stAlert{border-radius:10px!important;}
@media(max-width:768px){.stLatex{overflow-x:auto;}}
</style>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SVG INTEGRAL SYMBOLS — pixel-perfect, color-parameterised              ║
# ╚══════════════════════════════════════════════════════════════════════════╝
def _int_svg(n: int, color: str, height: int = 72) -> str:
    """
    Return an HTML string containing n integral signs as a single clean SVG.
    Each ∫ is drawn as a smooth cubic Bezier — tall, slender, mathematically styled.
    n must be 1, 2 or 3.
    """
    # Each glyph occupies 28px width; gap between glyphs = 4px
    glyph_w = 28
    gap     = 2
    total_w = n * glyph_w + (n - 1) * gap
    h       = height

    # Bezier path for a single ∫ centred in a 28-wide column.
    # The shape: top curl (right), tall descending S-curve, bottom curl (left)
    def glyph(ox: float) -> str:
        # ox = x-offset for this glyph
        # Key points (relative to column centre cx):
        cx = ox + glyph_w / 2
        # Top serif arc (left → right)
        t_x1, t_y1 = cx - 4,  4
        t_x2, t_y2 = cx + 2,  2
        t_cx, t_cy = cx + 9, 10   # control
        # Main stem: top-centre to bottom-centre via S-curve
        m_x1, m_y1 = cx + 2,  10          # start (just after top curl)
        m_x2, m_y2 = cx - 2,  h - 10      # end (just before bottom curl)
        m_c1x, m_c1y = cx + 10, h * 0.35  # control 1 (lean right mid-top)
        m_c2x, m_c2y = cx - 10, h * 0.65  # control 2 (lean left mid-bottom)
        # Bottom serif arc (right → left)
        b_x1, b_y1 = cx - 2,   h - 10
        b_x2, b_y2 = cx + 4,   h - 4
        b_cx, b_cy = cx - 9,   h - 10   # control
        return (
            # top curl
            f"M {t_x1},{t_y1} Q {t_cx},{t_cy} {t_x2},{t_y2} "
            # main S-stem
            f"C {m_c1x},{m_c1y} {m_c2x},{m_c2y} {m_x2},{m_y2} "
            # bottom curl
            f"Q {b_cx},{b_cy} {b_x2},{b_y2}"
        )

    paths = ""
    for i in range(n):
        ox = i * (glyph_w + gap)
        paths += f'<path d="{glyph(ox)}" stroke="{color}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>\n'

    shadow_id = f"gs_{color.replace('#','')}"
    svg = f"""<svg width="{total_w}" height="{h}" viewBox="0 0 {total_w} {h}"
     fill="none" xmlns="http://www.w3.org/2000/svg" overflow="visible">
  <defs>
    <filter id="{shadow_id}" x="-40%" y="-20%" width="180%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="{color}" flood-opacity="0.45"/>
    </filter>
  </defs>
  <g filter="url(#{shadow_id})">
    {paths}
  </g>
</svg>"""
    return svg


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  FORMULA DATABASE                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝
# KEY FIX: All multi-integral LaTeX uses \iint / \iiint (single atoms that
# MathJax renders correctly) — NOT \int\int which breaks into floating signs.
FORMULA_DB = {
    # Derivatives
    "limit_def":    {"name":"Limit Definition",        "latex":r"\frac{d}{dx}f(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}",           "explanation":"The foundational limit definition of the derivative.",                                      "tags":["derivative"]},
    "power_rule":   {"name":"Power Rule",              "latex":r"\frac{d}{dx}x^n = n\,x^{n-1}",                                   "explanation":"Multiply by the exponent, then subtract 1 from it.",                                        "tags":["derivative","power"]},
    "const_mult":   {"name":"Constant Multiple",       "latex":r"\frac{d}{dx}\bigl[c\,f(x)\bigr]=c\,f'(x)",                      "explanation":"Constants factor out of derivatives.",                                                      "tags":["derivative"]},
    "sum_rule":     {"name":"Sum / Difference Rule",   "latex":r"\frac{d}{dx}[f\pm g]=f'\pm g'",                                  "explanation":"Differentiate each term separately.",                                                       "tags":["derivative","sum"]},
    "product_rule": {"name":"Product Rule",            "latex":r"\frac{d}{dx}(uv)=u'v+uv'",                                       "explanation":"'First times d(Second) plus Second times d(First).'",                                       "tags":["derivative","product"]},
    "quotient_rule":{"name":"Quotient Rule",           "latex":r"\frac{d}{dx}\!\left(\frac{u}{v}\right)=\frac{u'v-uv'}{v^2}",   "explanation":"'Low D-High minus High D-Low, over the square of what's below.'",                           "tags":["derivative","quotient"]},
    "chain_rule":   {"name":"Chain Rule",              "latex":r"\frac{d}{dx}f(g(x))=f'(g(x))\cdot g'(x)",                       "explanation":"Differentiate the outer, keep inner intact, multiply by derivative of inner.",             "tags":["derivative","chain"]},
    "sin_rule":     {"name":"d/dx sin(x)",             "latex":r"\frac{d}{dx}\sin x=\cos x",                                      "explanation":"The derivative of sine is cosine.",                                                         "tags":["derivative","trig"]},
    "cos_rule":     {"name":"d/dx cos(x)",             "latex":r"\frac{d}{dx}\cos x=-\sin x",                                     "explanation":"The derivative of cosine is negative sine.",                                                "tags":["derivative","trig"]},
    "tan_rule":     {"name":"d/dx tan(x)",             "latex":r"\frac{d}{dx}\tan x=\sec^2 x",                                    "explanation":"The derivative of tangent is secant squared.",                                              "tags":["derivative","trig"]},
    "exp_rule":     {"name":"d/dx eˣ",                 "latex":r"\frac{d}{dx}e^x=e^x",                                            "explanation":"The exponential eˣ is its own derivative.",                                                "tags":["derivative","exp"]},
    "ln_rule":      {"name":"d/dx ln(x)",              "latex":r"\frac{d}{dx}\ln x=\frac{1}{x}",                                  "explanation":"The derivative of the natural logarithm.",                                                  "tags":["derivative","log"]},
    "asin_rule":    {"name":"d/dx arcsin(x)",          "latex":r"\frac{d}{dx}\arcsin x=\frac{1}{\sqrt{1-x^2}}",                  "explanation":"Derivative of the inverse sine function.",                                                  "tags":["derivative","inv_trig"]},
    "acos_rule":    {"name":"d/dx arccos(x)",          "latex":r"\frac{d}{dx}\arccos x=\frac{-1}{\sqrt{1-x^2}}",                 "explanation":"Derivative of the inverse cosine function.",                                                "tags":["derivative","inv_trig"]},
    "atan_rule":    {"name":"d/dx arctan(x)",          "latex":r"\frac{d}{dx}\arctan x=\frac{1}{1+x^2}",                         "explanation":"Derivative of the inverse tangent function.",                                               "tags":["derivative","inv_trig"]},
    "sinh_rule":    {"name":"d/dx sinh(x)",            "latex":r"\frac{d}{dx}\sinh x=\cosh x",                                    "explanation":"Derivative of hyperbolic sine.",                                                            "tags":["derivative","hyp"]},
    "cosh_rule":    {"name":"d/dx cosh(x)",            "latex":r"\frac{d}{dx}\cosh x=\sinh x",                                    "explanation":"Derivative of hyperbolic cosine.",                                                          "tags":["derivative","hyp"]},
    # Single integrals
    "indef_def":    {"name":"Indefinite Integral",     "latex":r"\int f(x)\,dx = F(x)+C",                                         "explanation":"The antiderivative; C is the constant of integration.",                                    "tags":["integral"]},
    "ftoc":         {"name":"Fundamental Theorem",     "latex":r"\int_a^b f(x)\,dx = F(b)-F(a)",                                  "explanation":"Evaluate definite integrals via F(b)−F(a) where F'=f.",                                    "tags":["integral","definite"]},
    "power_int":    {"name":"Power Rule (∫)",          "latex":r"\int x^n\,dx=\frac{x^{n+1}}{n+1}+C,\quad n\neq-1",              "explanation":"Add 1 to exponent, divide by new exponent.",                                               "tags":["integral","power"]},
    "recip_int":    {"name":"Reciprocal Rule",         "latex":r"\int \frac{1}{x}\,dx=\ln|x|+C",                                  "explanation":"The integral of 1/x is the natural log.",                                                  "tags":["integral","log"]},
    "exp_int":      {"name":"∫ eˣ dx",                 "latex":r"\int e^x\,dx=e^x+C",                                             "explanation":"The exponential integrates to itself.",                                                     "tags":["integral","exp"]},
    "sin_int":      {"name":"∫ sin(x) dx",             "latex":r"\int \sin x\,dx=-\cos x+C",                                      "explanation":"Integrating sine gives negative cosine.",                                                   "tags":["integral","trig"]},
    "cos_int":      {"name":"∫ cos(x) dx",             "latex":r"\int \cos x\,dx=\sin x+C",                                       "explanation":"Integrating cosine gives sine.",                                                            "tags":["integral","trig"]},
    "sec2_int":     {"name":"∫ sec²(x) dx",            "latex":r"\int \sec^2 x\,dx=\tan x+C",                                     "explanation":"Integrating sec² gives tangent.",                                                          "tags":["integral","trig"]},
    "sum_int":      {"name":"Sum Rule (∫)",             "latex":r"\int[f+g]\,dx=\int f\,dx+\int g\,dx",                           "explanation":"Integrals distribute over addition.",                                                      "tags":["integral","sum"]},
    "const_int":    {"name":"Constant Multiple (∫)",   "latex":r"\int c\,f(x)\,dx=c\int f(x)\,dx",                               "explanation":"Constants factor out of integrals.",                                                       "tags":["integral"]},
    "usub_int":     {"name":"u-Substitution",          "latex":r"\int f(g(x))\,g'(x)\,dx=\int f(u)\,du,\quad u=g(x)",            "explanation":"Replace inner function with u; du=g'(x)dx.",                                              "tags":["integral","usub"]},
    "parts_int":    {"name":"Integration by Parts",    "latex":r"\int u\,dv=uv-\int v\,du",                                       "explanation":"Use when integrand is a product of two different function types.",                         "tags":["integral","byparts"]},
    "ln_int":       {"name":"∫ ln(x) dx",              "latex":r"\int \ln x\,dx=x\ln x-x+C",                                      "explanation":"Integral of natural log (derived via integration by parts).",                             "tags":["integral","log"]},
    # Double integrals — use \iint (single MathJax atom, renders correctly)
    "dbl_def":      {"name":"Double Integral",
                     "latex":r"\iint_{R} f(x,y)\,dA = \int_c^d\!\int_a^b f(x,y)\,dx\,dy",
                     "explanation":"Integrate f over a 2D region by two successive single integrals.",
                     "tags":["double"]},
    "fubini":       {"name":"Fubini's Theorem",
                     "latex":r"\int_c^d\!\int_a^b f\,dx\,dy = \int_a^b\!\int_c^d f\,dy\,dx",
                     "explanation":"For continuous f on a rectangle, the order of integration can be swapped.",
                     "tags":["double","fubini"]},
    "dbl_polar":    {"name":"Polar Coordinates",
                     "latex":r"\iint_{R} f\,dA = \int_\alpha^\beta\!\int_0^{r(\theta)} f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta",
                     "explanation":"Use polar form when the region is circular or f contains x²+y².",
                     "tags":["double","polar"]},
    # Triple integrals — use \iiint (single atom)
    "trp_def":      {"name":"Triple Integral",
                     "latex":r"\iiint_{V} f(x,y,z)\,dV",
                     "explanation":"Three successive integrations over a 3D region V.",
                     "tags":["triple"]},
    "trp_volume":   {"name":"Volume Formula",
                     "latex":r"V = \iiint_{V} dV",
                     "explanation":"Volume of region V equals the triple integral of 1 over V.",
                     "tags":["triple","volume"]},
    "trp_spherical":{"name":"Spherical Coordinates",
                     "latex":r"\iiint_{V} f\,dV = \int_0^{2\pi}\!\int_0^{\pi}\!\int_0^{R} f\,\rho^2\sin\phi\,d\rho\,d\phi\,d\theta",
                     "explanation":"Use when the region is a sphere or f contains x²+y²+z².",
                     "tags":["triple","spherical"]},
}


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  CACHED ANALYSIS — single traversal, cached by Streamlit                ║
# ╚══════════════════════════════════════════════════════════════════════════╝
@st.cache_data(show_spinner=False)
def analyse_expression(expr_str: str, var_str: str) -> dict:
    var  = symbols(var_str)
    expr = sympify(expr_str)
    nodes = list(preorder_traversal(expr))
    type_set = {type(n) for n in nodes}
    TRIG = {sp.sin,sp.cos,sp.tan,sp.asin,sp.acos,sp.atan}
    HYP  = {sp.sinh,sp.cosh,sp.tanh}
    INV  = {sp.asin,sp.acos,sp.atan}
    ALL_TRIG = TRIG | HYP
    is_quotient = is_composite = False
    for n in nodes:
        if not is_quotient and isinstance(n, Pow):
            e = n.args[1]
            if e == -1 or (isinstance(e, sp.Integer) and e < -1): is_quotient = True
        if not is_composite:
            if type(n) in ALL_TRIG and n.args and n.args[0] != var: is_composite = True
            elif isinstance(n, (sp.exp, sp.log)) and n.args and n.args[0] != var: is_composite = True
        if is_quotient and is_composite: break
    return {
        "is_polynomial":    expr.is_polynomial(var),
        "is_product":       isinstance(expr, Mul) and len([f for f in expr.args if f.free_symbols]) >= 2,
        "is_sum":           isinstance(expr, Add),
        "is_quotient":      is_quotient,
        "is_composite":     is_composite,
        "has_trig":         bool(TRIG & type_set),
        "has_exp":          sp.exp in type_set,
        "has_log":          sp.log in type_set,
        "has_hyperbolic":   bool(HYP & type_set),
        "has_inverse_trig": bool(INV & type_set),
        "terms":            list(expr.args) if isinstance(expr, Add) else [expr],
        "factors":          list(expr.args) if isinstance(expr, Mul) else [expr],
    }


@st.cache_data(show_spinner=False)
def detect_relevant_formulas(expr_str: str, var_str: str, operation: str) -> list:
    var   = symbols(var_str)
    expr  = sympify(expr_str)
    nodes = list(preorder_traversal(expr))
    type_set = {type(n).__name__ for n in nodes}
    def has(*names): return any(n in type_set for n in names)
    rel = []
    if operation == "Derivative":
        rel.append("limit_def")
        if has("Pow"): rel.append("power_rule")
        rel.append("const_mult")
        if has("Add"): rel.append("sum_rule")
        if isinstance(expr, Mul) and len([f for f in expr.args if f.free_symbols]) >= 2:
            rel.append("product_rule")
        for n in nodes:
            if isinstance(n, Pow) and (n.args[1]==-1 or (isinstance(n.args[1],sp.Integer) and n.args[1]<-1)):
                rel.append("quotient_rule"); break
        TRIG_HYP = {sp.sin,sp.cos,sp.tan,sp.asin,sp.acos,sp.atan,sp.sinh,sp.cosh,sp.tanh}
        for n in nodes:
            if (type(n) in TRIG_HYP or isinstance(n,(sp.exp,sp.log))) and n.args and n.args[0]!=var:
                rel.append("chain_rule"); break
        if has("sin"): rel.append("sin_rule")
        if has("cos"): rel.append("cos_rule")
        if has("tan"): rel.append("tan_rule")
        if has("exp"): rel.append("exp_rule")
        if has("log"): rel.append("ln_rule")
        if has("asin"): rel.append("asin_rule")
        if has("acos"): rel.append("acos_rule")
        if has("atan"): rel.append("atan_rule")
        if has("sinh"): rel.append("sinh_rule")
        if has("cosh"): rel.append("cosh_rule")
    elif operation == "Single Integral":
        rel += ["power_int","sum_int","const_int"]
        if has("log"): rel += ["ln_int","recip_int"]
        if has("exp"): rel.append("exp_int")
        if has("sin"): rel.append("sin_int")
        if has("cos"): rel.append("cos_int")
        if has("tan"): rel.append("sec2_int")
        TRIG_EXP = {sp.sin,sp.cos,sp.tan,sp.exp}
        for n in nodes:
            if type(n) in TRIG_EXP and n.args and n.args[0]!=var: rel.append("usub_int"); break
        if isinstance(expr, Mul):
            has_poly = any(var in n.free_symbols for n in nodes if isinstance(n,(Pow,sp.Symbol)))
            if has_poly and (has("sin") or has("cos") or has("exp") or has("log")): rel.append("parts_int")
    elif operation == "Double Integral":
        rel += ["dbl_def","fubini"]
        s = str(expr)
        if "x**2 + y**2" in s or "x**2+y**2" in s: rel.append("dbl_polar")
    elif operation == "Triple Integral":
        rel += ["trp_def","trp_volume"]
        s = str(expr)
        if "x**2 + y**2 + z**2" in s or "x**2+y**2+z**2" in s: rel.append("trp_spherical")
    seen = set(); return [k for k in rel if not (k in seen or seen.add(k))]


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  CACHED HEAVY SYMPY                                                      ║
# ╚══════════════════════════════════════════════════════════════════════════╝
@st.cache_data(show_spinner=False)
def _cached_diff(expr_str, var_str, order):
    var = symbols(var_str); expr = sympify(expr_str)
    r = diff(expr, var, order)
    return str(r), str(simplify(r)), str(expand(r))

@st.cache_data(show_spinner=False)
def _cached_diff_k(expr_str, var_str, k):
    var = symbols(var_str); expr = sympify(expr_str)
    r = diff(expr, var, k); return str(r), str(simplify(r))

@st.cache_data(show_spinner=False)
def _cached_antideriv(expr_str, var_str):
    var = symbols(var_str); expr = sympify(expr_str)
    r = integrate(expr, var); return str(r), str(simplify(r))

@st.cache_data(show_spinner=False)
def _cached_def_int(expr_str, var_str, lo_str, hi_str):
    var = symbols(var_str); expr = sympify(expr_str)
    lo = sympify(lo_str); hi = sympify(hi_str)
    r = integrate(expr, (var, lo, hi)); s = simplify(r)
    try: num = float(s.evalf())
    except: num = None
    return str(r), str(s), num

@st.cache_data(show_spinner=False)
def _cached_critical_pts(expr_str, var_str):
    var = symbols(var_str); expr = sympify(expr_str)
    try:
        pts = sp.solve(expr, var, rational=False)
        return [str(p) for p in pts if p.is_real]
    except: return []


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  CARD HELPERS                                                            ║
# ╚══════════════════════════════════════════════════════════════════════════╝
def step_card(label, title, body_fn, tip="", card_class="step-card"):
    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
    st.markdown(f'<div class="step-label">{label}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="step-title">{title}</div>', unsafe_allow_html=True)
    body_fn()
    if tip: st.markdown(f'<div class="tip-box">  {tip}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def formula_card(keys):
    if not keys: return
    st.markdown('<div class="formula-card">', unsafe_allow_html=True)
    st.markdown("## **Relevant Formulas for This Problem**")
    for k in keys:
        f = FORMULA_DB.get(k)
        if not f: continue
        st.markdown('<div class="formula-rule">', unsafe_allow_html=True)
        st.markdown(f'<span class="rule-tag">{f["name"]}</span>', unsafe_allow_html=True)
        st.latex(f["latex"])   # ← these are all clean single-sign formulas now
        st.markdown(f'<div class="step-explain">{f["explanation"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def final_card(body_fn):
    st.markdown('<div class="final-card">', unsafe_allow_html=True)
    st.markdown("### ✅ Final Answer")
    body_fn()
    st.markdown('</div>', unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  VECTORISED EVALUATORS                                                   ║
# ╚══════════════════════════════════════════════════════════════════════════╝
def safe_eval_array(fn, x_arr, limit=1e6):
    x_arr = np.asarray(x_arr, dtype=float)
    try:
        y = np.asarray(fn(x_arr), dtype=complex)
        if y.shape == ():
            y = np.full(len(x_arr), y, dtype=complex)
        mask = (np.abs(y.imag)<1e-9) & (np.abs(y.real)<limit) & np.isfinite(y.real)
        return np.where(mask, y.real, np.nan)
    except:
        out = np.full(len(x_arr), np.nan, dtype=float)
        for i, xv in enumerate(x_arr):
            try:
                v = complex(fn(float(xv)))
                if abs(v.imag)<1e-9 and abs(v.real)<limit and np.isfinite(v.real):
                    out[i] = v.real
            except:
                pass
        return out

def safe_eval_grid(fn, X, Y, limit=1e6):
    try:
        Z = np.asarray(fn(X, Y), dtype=complex)
        mask = (np.abs(Z.imag)<1e-9) & (np.abs(Z.real)<limit) & np.isfinite(Z.real)
        return np.where(mask, Z.real, np.nan).astype(float)
    except:
        Z = np.full_like(X, np.nan, dtype=float)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                try:
                    v = complex(fn(X[i,j], Y[i,j]))
                    if abs(v.imag)<1e-9 and abs(v.real)<limit: Z[i,j]=v.real
                except: pass
        return Z

def safe_eval_grid3(fn, X, Y, z, limit=1e6):
    try:
        Z = np.asarray(fn(X, Y, z), dtype=complex)
        mask = (np.abs(Z.imag)<1e-9) & (np.abs(Z.real)<limit) & np.isfinite(Z.real)
        return np.where(mask, Z.real, np.nan).astype(float)
    except:
        Z = np.full_like(X, np.nan, dtype=float)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                try:
                    v = complex(fn(X[i,j], Y[i,j], z))
                    if abs(v.imag)<1e-9 and abs(v.real)<limit: Z[i,j]=v.real
                except: pass
        return Z


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  CHART STYLES                                                            ║
# ╚══════════════════════════════════════════════════════════════════════════╝
_BG   = 'rgba(11,15,26,0)'
_PBG  = 'rgba(17,24,39,0)'
_GC   = '#1e293b'; _ZC = '#2d3748'; _TC = '#94a3b8'; _FF = 'Sora,sans-serif'

def _style_2d(fig, title):
    fig.update_layout(title=dict(text=title,font=dict(size=18,color='#f0f6ff',family=_FF)),
        hovermode='x unified', plot_bgcolor=_BG, paper_bgcolor=_PBG,
        font=dict(size=13,color=_TC,family=_FF), showlegend=True,
        legend=dict(bgcolor='rgba(17,24,39,0.85)',bordercolor=_GC,borderwidth=1,font=dict(size=12,color='#e2e8f0')),
        height=460, margin=dict(l=20,r=20,t=60,b=20))
    fig.update_xaxes(showgrid=True,gridwidth=1,gridcolor=_GC,zeroline=True,zerolinewidth=2,zerolinecolor=_ZC,color=_TC)
    fig.update_yaxes(showgrid=True,gridwidth=1,gridcolor=_GC,zeroline=True,zerolinewidth=2,zerolinecolor=_ZC,color=_TC)

def _style_3d(fig, title, xl, yl, zl):
    fig.update_layout(title=dict(text=title,font=dict(size=16,color='#f0f6ff',family=_FF)),
        scene=dict(xaxis_title=xl,yaxis_title=yl,zaxis_title=zl,bgcolor='#0b0f1a',
            camera=dict(eye=dict(x=1.5,y=1.5,z=1.3)),
            xaxis=dict(backgroundcolor='#111827',gridcolor=_GC,color=_TC),
            yaxis=dict(backgroundcolor='#111827',gridcolor=_GC,color=_TC),
            zaxis=dict(backgroundcolor='#111827',gridcolor=_GC,color=_TC)),
        paper_bgcolor='rgba(17,24,39,0)', height=560, margin=dict(l=0,r=0,t=60,b=0))


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  DERIVATIVE SOLVER                                                       ║
# ╚══════════════════════════════════════════════════════════════════════════╝
def solve_derivative(expr, var, order, show_formula, show_graph):
    es, vs = str(expr), str(var)
    info   = analyse_expression(es, vs)
    f_keys = detect_relevant_formulas(es, vs, "Derivative") if show_formula else []
    res_s, simp_s, exp_s = _cached_diff(es, vs, order)
    result = sympify(res_s); simplified = sympify(simp_s); expanded = sympify(exp_s)
    # Pre-compute each diff step
    steps = []
    cur = es
    for k in range(1, order+1):
        r, s = _cached_diff_k(cur, vs, 1); steps.append((cur, r, s)); cur = r
    ord_sfx = {1:"st",2:"nd",3:"rd"}.get(order,"th")

    def _struct():
        parts = []
        if info["is_sum"]:        parts.append(f"**Sum of {len(info['terms'])} terms** → Sum Rule")
        if info["is_product"]:    parts.append("**Product of functions** → Product Rule")
        if info["is_quotient"]:   parts.append("**Quotient of functions** → Quotient Rule")
        if info["is_composite"]:  parts.append("**Composite function** → Chain Rule")
        if info["has_trig"]:      parts.append("Contains **trigonometric** functions")
        if info["has_exp"]:       parts.append("Contains **exponential** function")
        if info["has_log"]:       parts.append("Contains **logarithm**")
        if info["has_hyperbolic"]: parts.append("Contains **hyperbolic** functions")
        if info["has_inverse_trig"]: parts.append("Contains **inverse-trig** functions")
        if not parts: parts.append("**Basic function** → apply direct rule")
        st.latex(f"f(x) = {latex(expr)}")
        for p in parts: st.markdown(f"- {p}")
    step_card("Step 0", "Identify the Structure of f(x)", _struct,
              tip="The structure tells you which rules to apply.")
    def _op():
        if order == 1: st.latex(r"f'(x)=\frac{d}{dx}\Bigl["+latex(expr)+r"\Bigr]")
        else: st.latex(rf"\frac{{d^{order}}}{{dx^{order}}}\Bigl[{latex(expr)}\Bigr]")
        st.markdown(f'<div class="step-explain">Find the <strong>{order}{ord_sfx}-order</strong> derivative w.r.t. {var}.</div>', unsafe_allow_html=True)
    step_card("Step 1", f"Write the {order}{ord_sfx}-Order Derivative Operator", _op)

    if info["is_sum"] and order == 1:
        def _sum():
            terms = [sympify(str(t)) for t in info["terms"]]
            st.latex(r"f'(x)="+"+".join([rf"\frac{{d}}{{dx}}\left[{latex(t)}\right]" for t in terms]))
            st.markdown('<div class="step-explain">By the <strong>Sum Rule</strong> differentiate term-by-term.</div>', unsafe_allow_html=True)
        step_card("Step 2", "Sum Rule — Term-by-Term", _sum)

    if info["is_product"] and order == 1:
        vf = [f for f in info["factors"] if f.free_symbols]
        if len(vf) >= 2:
            u_s, v_s = str(vf[0]), str(sp.Mul(*vf[1:]))
            du_s, _ = _cached_diff_k(u_s, vs, 1); dv_s, _ = _cached_diff_k(v_s, vs, 1)
            def _prod(u=sympify(u_s),v=sympify(v_s),du=sympify(du_s),dv=sympify(dv_s)):
                st.latex(rf"u={latex(u)},\quad v={latex(v)}")
                st.latex(rf"u'={latex(du)},\quad v'={latex(dv)}")
                st.latex(rf"f'(x)=u'v+uv'={latex(du)}\cdot{latex(v)}+{latex(u)}\cdot{latex(dv)}")
            step_card("Step 2", "Product Rule Setup", _prod, tip="'First·d(Second) + Second·d(First)'")

    if info["is_composite"] and order == 1 and not info["is_sum"]:
        TH = {sp.sin,sp.cos,sp.tan,sp.asin,sp.acos,sp.atan,sp.sinh,sp.cosh,sp.tanh}
        for node in preorder_traversal(expr):
            if (type(node) in TH or isinstance(node,(sp.exp,sp.log))) and node.args and node.args[0]!=var:
                inner = node.args[0]; outer = type(node)
                di_s, _ = _cached_diff_k(str(inner), vs, 1); di = sympify(di_s)
                u = symbols('u')
                do_s, _ = _cached_diff_k(str(outer(u)), str(u), 1); do = sympify(do_s)
                def _chain(i=inner,o=outer,di=di,do=do,u=u):
                    st.latex(rf"\text{{Outer: }}f(u)={latex(o(u))},\quad\text{{Inner: }}u={latex(i)}")
                    st.latex(rf"f'=\underbrace{{{latex(do)}}}_{{f'(g(x))}}\Big|_{{u={latex(i)}}}\cdot\underbrace{{{latex(di)}}}_{{g'(x)}}")
                step_card("Step 2", "Chain Rule — Outer/Inner Setup", _chain,
                          tip="Differentiate outside (keep inside intact), multiply by derivative of inside.")
                break

    for k, (prev_s, r_s, s_s) in enumerate(steps, 1):
        pe, re, se = sympify(prev_s), sympify(r_s), sympify(s_s)
        kth = {1:"1st",2:"2nd",3:"3rd"}.get(k,f"{k}th")
        def _dk(k=k,pe=pe,re=re,se=se):
            if k==1: st.latex(rf"f'(x)=\frac{{d}}{{dx}}\left[{latex(pe)}\right]={latex(re)}")
            else:
                pn={2:"f'(x)",3:"f''(x)"}.get(k-1,rf"f^{{({k-1})}}(x)")
                cn={2:"f''(x)",3:"f'''(x)"}.get(k,rf"f^{{({k})}}(x)")
                st.latex(rf"{cn}=\frac{{d}}{{dx}}\left[{latex(pe)}\right]={latex(re)}")
            if str(re)!=str(se): st.markdown("Simplify:"); st.latex(f"= {latex(se)}")
        step_card(f"Step {2+k}", f"Compute the {kth} Derivative", _dk)

    if res_s != simp_s:
        def _simp(): st.markdown("**Simplified:**"); st.latex(latex(simplified))
        step_card(f"Step {3+order}", "Simplify", _simp, tip="Combine like terms and cancel factors.")

    def _interp():
        suf = {1:"'",2:"''",3:"'''"}.get(order,f"^{{({order})}}")
        st.latex(rf"f{suf}(x)={latex(simplified)}")
        if order==1: st.markdown('<div class="step-explain">f\'(x) is the <strong>instantaneous rate of change</strong> — slope of the tangent line.</div>', unsafe_allow_html=True)
        elif order==2: st.markdown('<div class="step-explain">f\'\'(x) describes <strong>concavity</strong>: +ve→concave up, −ve→concave down.</div>', unsafe_allow_html=True)
        else: st.markdown(f'<div class="step-explain">Higher-order derivative — captures curvature, jerk, etc.</div>', unsafe_allow_html=True)
    step_card(f"Step {3+order+(1 if res_s!=simp_s else 0)}", "Interpret", _interp)

    def _ans():
        suf = {1:"'",2:"''",3:"'''"}.get(order,f"^{{({order})}}")
        st.latex(rf"f{suf}(x)={latex(simplified)}")
    final_card(_ans)

    if show_formula and f_keys: formula_card(f_keys)

    if show_graph:
        try:
            st.markdown("---")
            st.markdown("### 📊 Advanced Derivative Explorer")

            # ── build lambdified functions for f, f', f'' ──────────────────
            xs  = np.linspace(-6, 6, 600)
            fl  = sp.lambdify(var, expr,       modules=['numpy'])
            dl  = sp.lambdify(var, simplified, modules=['numpy'])
            yf  = safe_eval_array(fl, xs)
            yd  = safe_eval_array(dl, xs)

            # Compute all derivative orders up to current for overlay
            deriv_traces = []
            colors_d = ['#4f8ef7','#a78bfa','#34d399','#fb923c','#f43f5e']
            cur_expr = expr
            for k in range(1, order+1):
                cur_expr = sp.diff(cur_expr, var)
                lf_k = sp.lambdify(var, sp.simplify(cur_expr), modules=['numpy'])
                yk   = safe_eval_array(lf_k, xs)
                sfx  = {1:"'",2:"''",3:"'''"}.get(k, f"^({k})")
                deriv_traces.append((f"f{sfx}(x)", yk, colors_d[k % len(colors_d)]))

            ps = "'"*order if order<=3 else f"^({order})"

            # ── Tangent-line slider ─────────────────────────────────────────
            x0_key = "der_tangent_x0"
            if x0_key not in st.session_state:
                st.session_state[x0_key] = 0.0
            x0 = st.slider("Tangent point  x₀ :", -5.0, 5.0,
                            float(st.session_state[x0_key]), step=0.05, key=x0_key)

            try:
                y0    = float(fl(x0))
                slope = float(dl(x0))
                tan_y = slope*(xs - x0) + y0
                # Clip tangent to visible window
                yf_clean  = np.array([v if v is not None else np.nan for v in yf], dtype=float)
                ylo, yhi  = np.nanpercentile(yf_clean[np.isfinite(yf_clean)], [2,98]) if np.any(np.isfinite(yf_clean)) else (-10,10)
                pad       = max(abs(yhi-ylo)*0.5, 2)
                tan_y     = np.clip(tan_y, ylo-pad, yhi+pad)
                has_tan   = True
            except:
                has_tan = False

            # ── Build figure ────────────────────────────────────────────────
            fig = go.Figure()

            # f(x) — main function
            fig.add_trace(go.Scatter(
                x=xs, y=yf, mode='lines', name='f(x)',
                line=dict(color='#4f8ef7', width=3),
                hovertemplate='x=%{x:.3f}<br>f(x)=%{y:.4f}<extra>f(x)</extra>'
            ))

            # All derivative layers
            for name, yk, col in deriv_traces:
                fig.add_trace(go.Scatter(
                    x=xs, y=yk, mode='lines', name=name,
                    line=dict(color=col, width=2.2, dash='dash'),
                    hovertemplate=f'x=%{{x:.3f}}<br>{name}=%{{y:.4f}}<extra>{name}</extra>'
                ))

            # Tangent line at x0
            if has_tan:
                fig.add_trace(go.Scatter(
                    x=xs, y=tan_y, mode='lines', name=f'Tangent at x={x0:.2f}',
                    line=dict(color='#fbbf24', width=1.8, dash='dot'),
                    hovertemplate=f'Tangent slope={slope:.4f}<extra></extra>'
                ))
                # Point on curve
                fig.add_trace(go.Scatter(
                    x=[x0], y=[y0], mode='markers',
                    name=f'x₀={x0:.2f}  f={y0:.3f}',
                    marker=dict(color='#fbbf24', size=11, symbol='circle',
                                line=dict(color='#fff', width=2)),
                    hovertemplate=f'x₀={x0:.3f}<br>f(x₀)={y0:.4f}<br>slope={slope:.4f}<extra></extra>'
                ))

            # Critical points (f'=0)
            if order >= 1:
                for cp_s in _cached_critical_pts(simp_s, vs):
                    try:
                        cp = float(sympify(cp_s).evalf())
                        if -6 <= cp <= 6:
                            ycp = float(fl(cp))
                            fig.add_trace(go.Scatter(
                                x=[cp], y=[ycp], mode='markers',
                                name=f"CP x={cp:.2f}",
                                marker=dict(color='#34d399', size=12, symbol='diamond',
                                            line=dict(color='#fff', width=2)),
                                hovertemplate=f'Critical point<br>x={cp:.4f}<br>f={ycp:.4f}<extra></extra>'
                            ))
                    except: pass

            # Inflection points — zeros of f''
            if order >= 1:
                try:
                    d2_expr = sp.diff(expr, var, 2)
                    inf_pts = sp.solve(d2_expr, var, rational=False)
                    for ip in inf_pts:
                        if ip.is_real:
                            ipf = float(ip.evalf())
                            if -6 <= ipf <= 6:
                                yip = float(fl(ipf))
                                fig.add_trace(go.Scatter(
                                    x=[ipf], y=[yip], mode='markers',
                                    name=f"Inflection x={ipf:.2f}",
                                    marker=dict(color='#f43f5e', size=10, symbol='x',
                                                line=dict(color='#fff', width=2)),
                                    hovertemplate=f'Inflection point<br>x={ipf:.4f}<br>f={yip:.4f}<extra></extra>'
                                ))
                except: pass

            # Concavity shading for order==2
            if order == 2:
                try:
                    yd_arr = np.array(yd, dtype=float)
                    # shade concave-up regions (f''>0) light green
                    pos_mask = yd_arr > 0
                    fig.add_trace(go.Scatter(
                        x=np.concatenate([xs[pos_mask], xs[pos_mask][::-1]]),
                        y=np.concatenate([yf_clean[pos_mask],
                                          np.full(pos_mask.sum(), np.nanmin(yf_clean))]),
                        fill='toself', fillcolor='rgba(52,211,153,0.07)',
                        line=dict(color='rgba(0,0,0,0)'),
                        name='Concave Up (f''> 0)', showlegend=True,
                        hoverinfo='skip'
                    ))
                except: pass

            # Zero line
            fig.add_hline(y=0, line=dict(color='#2d3748', width=1, dash='solid'))

            _style_2d(fig, f"f(x) · Derivatives · Tangent at x={x0:.2f}")
            fig.update_layout(
                height=520,
                legend=dict(orientation='v', x=1.01, y=1, font=dict(size=11)),
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)

            # ── Info row ────────────────────────────────────────────────────
            if has_tan:
                ci1, ci2, ci3 = st.columns(3)
                ci1.metric("x₀", f"{x0:.4f}")
                ci2.metric("f(x₀)", f"{y0:.4f}")
                ci3.metric(f"f{ps}(x₀)  [slope]", f"{slope:.4f}")
            if order==1: st.caption("🟢 Diamonds = critical points (f′=0)  ·  🔴 × = inflection points  ·  🟡 dashed = tangent line")
            if order==2: st.caption("🟢 Diamonds = critical points  ·  💚 shading = concave-up regions  ·  🔴 × = inflection points")

        except Exception as e: st.warning(f"⚠️ Graph error: {e}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SINGLE INTEGRAL SOLVER                                                  ║
# ╚══════════════════════════════════════════════════════════════════════════╝
def solve_integral(expr, var, is_def, lower, upper, show_formula, show_graph):
    es, vs = str(expr), str(var)
    info   = analyse_expression(es, vs)
    f_keys = []
    if show_formula:
        f_keys = detect_relevant_formulas(es, vs, "Single Integral")
        f_keys.insert(0, "ftoc" if is_def else "indef_def")
        seen = set()
        f_keys = [k for k in f_keys if not (k in seen or seen.add(k))]

    anti_s, anti_simp_s = _cached_antideriv(es, vs)
    anti_simp = sympify(anti_simp_s)
    if is_def:
        _, res_simp_s, num_val = _cached_def_int(es, vs, str(lower), str(upper))
        res_simp = sympify(res_simp_s)
    # Term integrals pre-computed
    term_ints = []
    if info["is_sum"]:
        for t in info["terms"]:
            ts, _ = _cached_antideriv(str(t), vs); term_ints.append((t, sympify(ts)))

    def _struct():
        st.latex(f"f(x)={latex(expr)}")
        parts = []
        if info["is_sum"]:       parts.append(f"**Sum of {len(info['terms'])} terms** → integrate term-by-term")
        if info["is_product"]:   parts.append("**Product** → may need by-parts or u-sub")
        if info["is_composite"]: parts.append("**Composite** → try u-substitution")
        if info["has_trig"]:     parts.append("Contains **trig** functions")
        if info["has_exp"]:      parts.append("Contains **exponential**")
        if info["has_log"]:      parts.append("Contains **logarithm**")
        if not parts: parts.append("**Basic function** → apply standard rules directly")
        for p in parts: st.markdown(f"- {p}")
    step_card("Step 0", "Identify the Integrand Structure", _struct,
              tip="Structure determines which integration technique to use.")

    def _write():
        # Build LaTeX manually — never pass Integral() to st.latex()
        flt = latex(expr)
        v   = latex(var)
        if is_def:
            lo_lt = latex(lower); hi_lt = latex(upper)
            st.latex(rf"\int_{{{lo_lt}}}^{{{hi_lt}}} {flt}\,d{v}")
            st.markdown(f'<div class="step-explain">Evaluate the <strong>definite integral</strong> from {lo_lt} to {hi_lt} — the <strong>net signed area</strong> under f(x).</div>', unsafe_allow_html=True)
        else:
            st.latex(rf"\int {flt}\,d{v}")
            st.markdown('<div class="step-explain">Find the <strong>general antiderivative</strong> F(x)+C where F\'(x)=f(x).</div>', unsafe_allow_html=True)
    step_card("Step 1", "Write the Integral", _write)

    technique = "Direct Rules"
    if "usub_int"  in f_keys: technique = "u-Substitution"
    if "parts_int" in f_keys: technique = "Integration by Parts"
    TH_MAP = {"u-Substitution":"Look for an inner function whose derivative also appears.",
              "Integration by Parts":"LIATE: Log · Inv-trig · Algebra · Trig · Exp.",
              "Direct Rules":"Power, trig, and exp rules applied directly."}
    def _tech():
        st.markdown(f"**Selected: {technique}**")
        if technique == "u-Substitution":
            TE = {sp.sin,sp.cos,sp.tan,sp.exp}
            for node in preorder_traversal(expr):
                if type(node) in TE and node.args and node.args[0]!=var:
                    inner = node.args[0]
                    di_s, _ = _cached_diff_k(str(inner), vs, 1)
                    st.latex(rf"u={latex(inner)},\quad du={latex(sympify(di_s))}\,d{latex(var)}")
                    st.markdown(f'<div class="step-explain">Substitute u={latex(inner)} to simplify the integrand.</div>', unsafe_allow_html=True)
                    break
        elif technique == "Integration by Parts":
            vf = [f for f in info["factors"] if f.free_symbols]
            if len(vf) >= 2:
                up, dvp = vf[0], vf[1]
                du_s, _ = _cached_diff_k(str(up), vs, 1)
                v_s,  _ = _cached_antideriv(str(dvp), vs)
                st.latex(rf"u={latex(up)},\quad dv={latex(dvp)}\,d{latex(var)}")
                st.latex(rf"du={latex(sympify(du_s))}\,d{latex(var)},\quad v={latex(sympify(v_s))}")
                st.markdown('<div class="step-explain"><strong>LIATE</strong>: choose u as the function that simplifies most when differentiated.</div>', unsafe_allow_html=True)
        else:
            if info["is_sum"]:
                terms = [sympify(str(t)) for t in info["terms"]]
                st.latex(r"\int\left["+"+".join([latex(t) for t in terms])+r"\right]\,dx="+
                         "+".join([rf"\int {latex(t)}\,dx" for t in terms]))
            st.markdown('<div class="step-explain">Apply standard integral rules directly.</div>', unsafe_allow_html=True)
    step_card("Step 2", f"Technique: {technique}", _tech, tip=TH_MAP[technique])

    flt = latex(expr); v = latex(var)
    def _antideriv():
        st.latex(rf"\int {flt}\,d{v} = {latex(anti_simp)}")
        if term_ints:
            st.markdown("**Term-by-term:**")
            for t, ti in term_ints:
                st.latex(rf"\int {latex(t)}\,d{v} = {latex(ti)}")
    step_card("Step 3", "Compute the Antiderivative F(x)", _antideriv,
              tip="Always add +C to an indefinite integral.")

    if is_def:
        lo_lt = latex(lower); hi_lt = latex(upper)
        def _ftoc():
            st.markdown("**Apply the Fundamental Theorem of Calculus:**")
            st.latex(rf"F(x)={latex(anti_simp)}")
            fu = anti_simp.subs(var, upper); fl_ = anti_simp.subs(var, lower)
            st.latex(rf"F({hi_lt})-F({lo_lt}) = {latex(fu)} - \left({latex(fl_)}\right)")
        step_card("Step 4", "Apply the Fundamental Theorem (FToC)", _ftoc)

        def _eval():
            st.latex(rf"\int_{{{lo_lt}}}^{{{hi_lt}}} {flt}\,d{v} = {latex(res_simp)}")
            if num_val is not None:
                st.latex(rf"\approx {num_val:.6f}")
                msg = ("positive → net area <strong>above</strong> the x-axis" if num_val>0
                       else "negative → net area <strong>below</strong> the x-axis" if num_val<0
                       else "zero — areas above and below cancel exactly")
                st.markdown(f'<div class="step-explain">Result is {msg}.</div>', unsafe_allow_html=True)
        step_card("Step 5", "Evaluate and Interpret", _eval)

        def _ans(): st.latex(rf"\int_{{{lo_lt}}}^{{{hi_lt}}} {flt}\,d{v} = {latex(res_simp)}")
        final_card(_ans)
    else:
        def _ans(): st.latex(rf"\int {flt}\,d{v} = {latex(anti_simp)} + C")
        final_card(_ans)
        res_simp = anti_simp; num_val = None

    if show_formula and f_keys: formula_card(f_keys)

    if show_graph:
        try:
            st.markdown("---")
            st.markdown("### 📊 Advanced Integral Explorer")

            fn     = sp.lambdify(var, expr,      modules=['numpy'])
            anti_l = sp.lambdify(var, anti_simp, modules=['numpy'])

            if is_def:
                lof = float(lower.evalf()); hif = float(upper.evalf())
                pad = max(1.2, (hif-lof)*0.5)
                xf  = np.linspace(lof-pad, hif+pad, 600)
                xs  = np.linspace(lof, hif, 400)
            else:
                lof, hif = -3.0, 3.0
                xf = np.linspace(-5, 5, 600)
                xs = np.linspace(-3, 3, 400)

            yf   = safe_eval_array(fn,     xf)
            yant = safe_eval_array(anti_l, xf)

            tab1, tab2, tab3 = st.tabs(["Area & Antiderivative", "Riemann Sums", "Accumulation Function"])

            # ── TAB 1 : f(x), F(x), shaded area ───────────────────────────
            with tab1:
                fig1 = go.Figure()

                yf_arr = np.array(yf, dtype=float)
                ys_arr = safe_eval_array(fn, xs)

                # Positive area (above x-axis)
                pos_x = xs[ys_arr >= 0]; pos_y = ys_arr[ys_arr >= 0]
                if len(pos_x) > 1:
                    fig1.add_trace(go.Scatter(
                        x=np.concatenate([pos_x, pos_x[::-1]]),
                        y=np.concatenate([pos_y, np.zeros(len(pos_y))]),
                        fill='toself', fillcolor='rgba(79,142,247,0.22)',
                        line=dict(color='rgba(0,0,0,0)'), name='+ Area', hoverinfo='skip'
                    ))
                # Negative area (below x-axis)
                neg_x = xs[ys_arr < 0]; neg_y = ys_arr[ys_arr < 0]
                if len(neg_x) > 1:
                    fig1.add_trace(go.Scatter(
                        x=np.concatenate([neg_x, neg_x[::-1]]),
                        y=np.concatenate([neg_y, np.zeros(len(neg_y))]),
                        fill='toself', fillcolor='rgba(244,63,94,0.18)',
                        line=dict(color='rgba(0,0,0,0)'), name='− Area', hoverinfo='skip'
                    ))

                # f(x) curve
                fig1.add_trace(go.Scatter(
                    x=xf, y=yf, mode='lines', name='f(x)',
                    line=dict(color='#4f8ef7', width=3),
                    hovertemplate='x=%{x:.3f}<br>f(x)=%{y:.4f}<extra>f(x)</extra>'
                ))

                # F(x) antiderivative
                fig1.add_trace(go.Scatter(
                    x=xf, y=yant, mode='lines', name='F(x) antiderivative',
                    line=dict(color='#34d399', width=2.2, dash='longdash'),
                    hovertemplate='x=%{x:.3f}<br>F(x)=%{y:.4f}<extra>F(x)</extra>'
                ))

                # Boundary lines & annotations
                if is_def:
                    for bnd, lbl in [(lof, lo_lt),(hif, hi_lt)]:
                        try:
                            yb = float(fn(bnd))
                            fig1.add_vline(x=bnd, line=dict(color='#34d399', width=1.5, dash='dot'))
                            fig1.add_annotation(x=bnd, y=yb, text=f" {lbl}",
                                showarrow=True, arrowhead=2, font=dict(color='#34d399', size=12))
                        except: pass

                fig1.add_hline(y=0, line=dict(color='#2d3748', width=1))
                _style_2d(fig1, "f(x)  ·  F(x)  ·  Signed Area")
                fig1.update_layout(height=480)
                st.plotly_chart(fig1, use_container_width=True)
                if is_def and num_val is not None:
                    ca, cb, cc = st.columns(3)
                    ca.metric("Lower bound a", f"{lof:.4f}")
                    cb.metric("Upper bound b", f"{hif:.4f}")
                    cc.metric("∫f dx  (net area)", f"{num_val:.6f}")
                st.caption("🔵 = f(x)  ·  🟢 dashed = F(x) antiderivative  ·  Blue fill = + area  ·  Red fill = − area")

            # ── TAB 2 : Riemann sums ────────────────────────────────────────
            with tab2:
                if "int_riemann_n" not in st.session_state:
                    st.session_state["int_riemann_n"] = 10
                if "int_riemann_m" not in st.session_state:
                    st.session_state["int_riemann_m"] = "Left"
                n_rect = st.slider("Number of rectangles n:", 2, 80,
                                   int(st.session_state["int_riemann_n"]),
                                   step=1, key="int_riemann_n")
                method = st.radio("Method:", ["Left", "Midpoint", "Right"],
                                  index=["Left","Midpoint","Right"].index(st.session_state["int_riemann_m"]),
                                  horizontal=True, key="int_riemann_m")
                xs_r   = np.linspace(lof, hif, n_rect+1)
                dx     = (hif - lof) / n_rect
                if   method == "Left":     x_sample = xs_r[:-1]
                elif method == "Right":    x_sample = xs_r[1:]
                else:                      x_sample = (xs_r[:-1] + xs_r[1:]) / 2
                y_sample = np.array([float(fn(float(x))) if np.isfinite(float(fn(float(x)))) else 0.0
                                     for x in x_sample])
                riemann_sum = float(np.sum(y_sample * dx))

                fig2 = go.Figure()
                # Rectangles
                for i, (xi, yi) in enumerate(zip(x_sample, y_sample)):
                    col_r = 'rgba(79,142,247,0.35)' if yi >= 0 else 'rgba(244,63,94,0.35)'
                    fig2.add_shape(type='rect', x0=xs_r[i], x1=xs_r[i+1], y0=0, y1=yi,
                        fillcolor=col_r, line=dict(color='rgba(79,142,247,0.7)', width=0.8))
                # f(x) on top
                fig2.add_trace(go.Scatter(
                    x=xf, y=yf, mode='lines', name='f(x)',
                    line=dict(color='#fbbf24', width=2.5),
                    hovertemplate='x=%{x:.3f}<br>f(x)=%{y:.4f}<extra></extra>'
                ))
                fig2.add_hline(y=0, line=dict(color='#2d3748', width=1))
                _style_2d(fig2, f"{method} Riemann Sum  (n={n_rect})")
                fig2.update_layout(height=460)
                st.plotly_chart(fig2, use_container_width=True)
                rc1, rc2, rc3 = st.columns(3)
                rc1.metric("n rectangles", n_rect)
                rc2.metric("Δx width", f"{dx:.4f}")
                rc3.metric(f"{method} Riemann Sum", f"{riemann_sum:.6f}")
                if is_def and num_val is not None:
                    err = abs(riemann_sum - num_val)
                    st.caption(f"Exact value = **{num_val:.6f}**  ·  Error = **{err:.6f}**  →  increase n to reduce error")

            # ── TAB 3 : Accumulation function ───────────────────────────────
            with tab3:
                st.markdown(f'**Accumulation function** $A(x) = \\int_{{{lof:.2f}}}^{{x}} f(t)\\,dt$')
                x_acc   = np.linspace(lof, hif, 300)
                dx_acc  = x_acc[1] - x_acc[0]
                y_acc_f = safe_eval_array(fn, x_acc)
                y_acc   = np.nancumsum(np.where(np.isfinite(y_acc_f), y_acc_f, 0)) * dx_acc

                fig3 = go.Figure()
                fig3.add_trace(go.Scatter(
                    x=x_acc, y=y_acc_f, mode='lines', name='f(t)',
                    line=dict(color='#4f8ef7', width=2.5),
                    hovertemplate='t=%{x:.3f}<br>f(t)=%{y:.4f}<extra>f(t)</extra>'
                ))
                fig3.add_trace(go.Scatter(
                    x=x_acc, y=y_acc, mode='lines', name='A(x) = ∫f dt',
                    line=dict(color='#a78bfa', width=3),
                    fill='toself' if False else None,
                    hovertemplate='x=%{x:.3f}<br>A(x)=%{y:.4f}<extra>A(x)</extra>'
                ))
                fig3.add_hline(y=0, line=dict(color='#2d3748', width=1))
                _style_2d(fig3, "Accumulation Function  A(x) = ∫ₐˣ f(t) dt")
                fig3.update_layout(height=460)
                st.plotly_chart(fig3, use_container_width=True)
                st.caption("🔵 f(t) = integrand  ·  🟣 A(x) = running total area from a to x  ·  A(b) = definite integral value")

        except Exception as e: st.warning(f"⚠️ Graph error: {e}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  DOUBLE INTEGRAL SOLVER                                                  ║
# ╚══════════════════════════════════════════════════════════════════════════╝
def solve_double_integral(expr, v1, v2, lim1, lim2, show_formula, show_graph):
    n1, n2 = str(v1), str(v2)
    f_keys = []
    if show_formula:
        f_keys = detect_relevant_formulas(str(expr), n1, "Double Integral")

    def _struct():
        st.latex(f"f({n1},{n2})={latex(expr)}")
        st.markdown(f'<div class="step-explain">A double integral computes the <strong>volume</strong> under the surface z=f({n1},{n2}) over the 2D region R.</div>', unsafe_allow_html=True)
        if lim1 and lim2:
            st.markdown(f"**Region R:** {n1}∈[{latex(lim1[0])},{latex(lim1[1])}], {n2}∈[{latex(lim2[0])},{latex(lim2[1])}]")
    step_card("Step 0", "Understand the Double Integral Geometry", _struct)

    # Step 1 — write using \iint (NOT \int\int)
    def _write():
        flt = latex(expr)
        if lim1 and lim2:
            st.latex(rf"\iint_R {flt}\,d{n1}\,d{n2} = \int_{{{latex(lim2[0])}}}^{{{latex(lim2[1])}}}\int_{{{latex(lim1[0])}}}^{{{latex(lim1[1])}}} {flt}\,d{n1}\,d{n2}")
        else:
            st.latex(rf"\iint {flt}\,d{n1}\,d{n2}")
        st.markdown(f'<div class="step-explain">By <strong>Fubini\'s theorem</strong>, evaluate the inner integral first (treating {n2} as a constant), then the outer.</div>', unsafe_allow_html=True)
    step_card("Step 1", "Write the Iterated Double Integral", _write)

    # Inner integral
    if lim1: inner = integrate(expr, (v1, lim1[0], lim1[1]))
    else:    inner = integrate(expr, v1)
    inner_s = simplify(inner); inner_e = expand(inner_s)

    def _inner():
        st.markdown(f"**Integrate over {n1}, treating {n2} as constant:**")
        flt = latex(expr)
        if lim1:
            st.latex(rf"\int_{{{latex(lim1[0])}}}^{{{latex(lim1[1])}}} {flt}\,d{n1} = {latex(inner_s)}")
        else:
            st.latex(rf"\int {flt}\,d{n1} = {latex(inner_s)}")
        st.markdown(f'<div class="step-explain">Result is now a function of {n2} only.</div>', unsafe_allow_html=True)
    step_card("Step 2", f"Inner Integral: integrate w.r.t. {n1}", _inner,
              tip=f"Treat {n2} as a fixed parameter.")

    def _outer_integrand():
        st.latex(f"g({n2}) = {latex(inner_e)}")
        st.markdown(f'<div class="step-explain">This single-variable function of {n2} is now integrated.</div>', unsafe_allow_html=True)
    step_card("Step 3", f"Outer Integrand g({n2})", _outer_integrand)

    if lim2: final = integrate(inner_s, (v2, lim2[0], lim2[1]))
    else:    final = integrate(inner_s, v2)
    final_s = simplify(final)

    def _outer():
        st.markdown(f"**Integrate over {n2}:**")
        if lim2:
            st.latex(rf"\int_{{{latex(lim2[0])}}}^{{{latex(lim2[1])}}} {latex(inner_s)}\,d{n2} = {latex(final_s)}")
        else:
            st.latex(rf"\int {latex(inner_s)}\,d{n2} = {latex(final_s)}")
    step_card("Step 4", f"Outer Integral: integrate w.r.t. {n2}", _outer)

    def _simp():
        st.latex(f"\\text{{Result}} = {latex(final_s)}")
        if lim1 and lim2:
            try:
                nv = float(final_s.evalf())
                st.latex(rf"\approx {nv:.6f}")
                st.markdown(f'<div class="step-explain">≈ {nv:.4f} — the <strong>volume</strong> under f({n1},{n2}) over R.</div>', unsafe_allow_html=True)
            except: pass
    step_card("Step 5", "Simplify and Interpret", _simp)

    def _ans():
        if lim1 and lim2:
            st.latex(rf"\int_{{{latex(lim2[0])}}}^{{{latex(lim2[1])}}}\int_{{{latex(lim1[0])}}}^{{{latex(lim1[1])}}} {latex(expr)}\,d{n1}\,d{n2} = {latex(final_s)}")
        else:
            st.latex(rf"\iint {latex(expr)}\,d{n1}\,d{n2} = {latex(final_s)} + C")
    final_card(_ans)

    if show_formula and f_keys: formula_card(f_keys)

    if show_graph:
        try:
            st.markdown("---")
            st.markdown("### 📊 Advanced Double Integral Explorer")

            xr = np.linspace(float(lim1[0].evalf()),float(lim1[1].evalf()),60) if lim1 else np.linspace(-3,3,60)
            yr = np.linspace(float(lim2[0].evalf()),float(lim2[1].evalf()),60) if lim2 else np.linspace(-3,3,60)
            X, Y = np.meshgrid(xr, yr)
            ff   = sp.lambdify((v1, v2), expr, modules=['numpy'])
            Z    = safe_eval_grid(ff, X, Y)

            dtab1, dtab2, dtab3 = st.tabs(["3D Surface", "Contour Map", "Cross-Sections"])

            # ── TAB 1 : 3D Surface with projected contours & integration box ─
            with dtab1:
                fig_s = go.Figure()
                fig_s.add_trace(go.Surface(
                    x=X, y=Y, z=Z,
                    colorscale='Viridis',
                    colorbar=dict(title=f'f({n1},{n2})', tickfont=dict(color=_TC),
                                  thickness=14, len=0.7),
                    contours=dict(
                        z=dict(show=True, usecolormap=True, project_z=True, highlightwidth=2),
                        x=dict(show=True, color='rgba(255,255,255,0.15)'),
                        y=dict(show=True, color='rgba(255,255,255,0.15)')
                    ),
                    hovertemplate=f'{n1}=%{{x:.3f}}<br>{n2}=%{{y:.3f}}<br>f=%{{z:.4f}}<extra></extra>',
                    opacity=0.92
                ))
                # Draw integration region box if definite
                if lim1 and lim2:
                    x1v,x2v = float(lim1[0].evalf()), float(lim1[1].evalf())
                    y1v,y2v = float(lim2[0].evalf()), float(lim2[1].evalf())
                    corners_x = [x1v,x2v,x2v,x1v,x1v]
                    corners_y = [y1v,y1v,y2v,y2v,y1v]
                    z_base    = np.nanmin(Z) - 0.05*abs(np.nanmax(Z)-np.nanmin(Z))
                    fig_s.add_trace(go.Scatter3d(
                        x=corners_x, y=corners_y,
                        z=[z_base]*5,
                        mode='lines', name='Integration Region R',
                        line=dict(color='#fbbf24', width=5)
                    ))
                _style_3d(fig_s, f"Surface  z = f({n1},{n2})", n1, n2, "f")
                fig_s.update_layout(height=580)
                st.plotly_chart(fig_s, use_container_width=True)
                if lim1 and lim2:
                    try: st.caption(f"🟡 Yellow box = integration region R  ·  📦 Volume ≈ **{float(final_s.evalf()):.4f}**")
                    except: st.caption("🟡 Yellow box = integration region R")

            # ── TAB 2 : Contour / Heatmap with region overlay ───────────────
            with dtab2:
                fig_c = go.Figure()
                fig_c.add_trace(go.Contour(
                    x=xr, y=yr, z=Z,
                    colorscale='Viridis',
                    colorbar=dict(title=f'f({n1},{n2})', tickfont=dict(color=_TC)),
                    contours=dict(showlabels=True, labelfont=dict(size=10, color='white')),
                    hovertemplate=f'{n1}=%{{x:.3f}}<br>{n2}=%{{y:.3f}}<br>f=%{{z:.4f}}<extra></extra>'
                ))
                # Draw integration rectangle
                if lim1 and lim2:
                    x1v,x2v = float(lim1[0].evalf()), float(lim1[1].evalf())
                    y1v,y2v = float(lim2[0].evalf()), float(lim2[1].evalf())
                    fig_c.add_shape(type='rect', x0=x1v, x1=x2v, y0=y1v, y1=y2v,
                        line=dict(color='#fbbf24', width=3, dash='dash'),
                        fillcolor='rgba(251,191,36,0.08)')
                    fig_c.add_annotation(x=(x1v+x2v)/2, y=(y1v+y2v)/2,
                        text="R", font=dict(color='#fbbf24', size=18, family='Sora'),
                        showarrow=False)
                fig_c.update_layout(
                    title=dict(text=f"Contour Map  f({n1},{n2})",
                               font=dict(size=16, color='#f0f6ff', family=_FF)),
                    xaxis=dict(title=n1, showgrid=True, gridcolor=_GC, color=_TC),
                    yaxis=dict(title=n2, showgrid=True, gridcolor=_GC, color=_TC),
                    paper_bgcolor=_PBG, plot_bgcolor=_BG,
                    font=dict(color=_TC, family=_FF), height=480,
                    margin=dict(l=20,r=20,t=60,b=20)
                )
                st.plotly_chart(fig_c, use_container_width=True)
                st.caption(f"🟡 Dashed box = integration region R  ·  Contour lines show equal values of f({n1},{n2})")

            # ── TAB 3 : Interactive cross-section sliders ────────────────────
            with dtab3:
                # Sliders first — both above the charts so no rerun confusion
                xs0_default = float(np.mean(xr))
                ys0_default = float(np.mean(yr))

                if "dbl_xslice" not in st.session_state:
                    st.session_state["dbl_xslice"] = xs0_default
                if "dbl_yslice" not in st.session_state:
                    st.session_state["dbl_yslice"] = ys0_default

                sl1, sl2 = st.columns(2)
                with sl1:
                    xs0 = st.slider(f"Fix {n1} =", float(xr[0]), float(xr[-1]),
                                    float(st.session_state["dbl_xslice"]),
                                    step=float((xr[-1]-xr[0])/80),
                                    key="dbl_xslice")
                with sl2:
                    ys0 = st.slider(f"Fix {n2} =", float(yr[0]), float(yr[-1]),
                                    float(st.session_state["dbl_yslice"]),
                                    step=float((yr[-1]-yr[0])/80),
                                    key="dbl_yslice")

                # Evaluate slices using numpy — find closest grid index, extract row/col
                xi_idx = int(np.argmin(np.abs(xr - xs0)))
                yi_idx = int(np.argmin(np.abs(yr - ys0)))

                # f(xs0, y)  — fix x, vary y  → column xi_idx of Z matrix
                zy = Z[:, xi_idx].copy()          # shape (len_yr,)
                # f(x, ys0)  — fix y, vary x  → row yi_idx of Z matrix
                zx = Z[yi_idx, :].copy()          # shape (len_xr,)

                sc1, sc2 = st.columns(2)
                with sc1:
                    figx = go.Figure()
                    figx.add_trace(go.Scatter(
                        x=yr, y=zy, mode='lines',
                        name=f'f({xs0:.3f}, {n2})',
                        line=dict(color='#a78bfa', width=3),
                        fill='tozeroy', fillcolor='rgba(167,139,250,0.18)',
                        hovertemplate=f'{n2}=%{{x:.3f}}<br>f=%{{y:.4f}}<extra></extra>'
                    ))
                    figx.add_vline(x=float(yr[yi_idx]),
                        line=dict(color='#fbbf24', width=1.5, dash='dot'))
                    figx.add_hline(y=0, line=dict(color='#2d3748', width=1))
                    _style_2d(figx, f"f({xs0:.3f},  {n2})")
                    figx.update_layout(height=340,
                        xaxis_title=n2,
                        yaxis_title=f'f({xs0:.3f}, {n2})',
                        margin=dict(l=20,r=20,t=50,b=20))
                    st.plotly_chart(figx, use_container_width=True)
                    zy_clean = zy[np.isfinite(zy)]
                    if len(zy_clean):
                        m1,m2,m3 = st.columns(3)
                        m1.metric("min", f"{zy_clean.min():.4f}")
                        m2.metric("max", f"{zy_clean.max():.4f}")
                        m3.metric("mean", f"{zy_clean.mean():.4f}")

                with sc2:
                    figy = go.Figure()
                    figy.add_trace(go.Scatter(
                        x=xr, y=zx, mode='lines',
                        name=f'f({n1}, {ys0:.3f})',
                        line=dict(color='#34d399', width=3),
                        fill='tozeroy', fillcolor='rgba(52,211,153,0.18)',
                        hovertemplate=f'{n1}=%{{x:.3f}}<br>f=%{{y:.4f}}<extra></extra>'
                    ))
                    figy.add_vline(x=float(xr[xi_idx]),
                        line=dict(color='#fbbf24', width=1.5, dash='dot'))
                    figy.add_hline(y=0, line=dict(color='#2d3748', width=1))
                    _style_2d(figy, f"f({n1},  {ys0:.3f})")
                    figy.update_layout(height=340,
                        xaxis_title=n1,
                        yaxis_title=f'f({n1}, {ys0:.3f})',
                        margin=dict(l=20,r=20,t=50,b=20))
                    st.plotly_chart(figy, use_container_width=True)
                    zx_clean = zx[np.isfinite(zx)]
                    if len(zx_clean):
                        m1,m2,m3 = st.columns(3)
                        m1.metric("min", f"{zx_clean.min():.4f}")
                        m2.metric("max", f"{zx_clean.max():.4f}")
                        m3.metric("mean", f"{zx_clean.mean():.4f}")

                st.caption(f"🟣 Left: {n1}={xs0:.3f} fixed, vary {n2}  ·  🟢 Right: {n2}={ys0:.3f} fixed, vary {n1}  ·  🟡 dotted = current opposite-axis position")

        except Exception as e: st.warning(f"⚠️ 3D error: {e}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  TRIPLE INTEGRAL SOLVER                                                  ║
# ╚══════════════════════════════════════════════════════════════════════════╝
def solve_triple_integral(expr, v1, v2, v3, lim1, lim2, lim3, show_formula, show_graph):
    n1, n2, n3 = str(v1), str(v2), str(v3)
    f_keys = []
    if show_formula:
        f_keys = detect_relevant_formulas(str(expr), n1, "Triple Integral")

    def _struct():
        st.latex(f"f({n1},{n2},{n3})={latex(expr)}")
        st.markdown('<div class="step-explain">A triple integral evaluates over a <strong>3D region V</strong>. Uses: volume, mass, moments.</div>', unsafe_allow_html=True)
        if lim1 and lim2 and lim3:
            st.markdown(f"**Region V:** {n1}∈[{latex(lim1[0])},{latex(lim1[1])}], {n2}∈[{latex(lim2[0])},{latex(lim2[1])}], {n3}∈[{latex(lim3[0])},{latex(lim3[1])}]")
    step_card("Step 0", "Triple Integral Geometry", _struct)

    # Step 1 — always use \iiint
    def _write():
        flt = latex(expr)
        if lim1 and lim2 and lim3:
            st.latex(rf"\iiint_V {flt}\,dV = \int_{{{latex(lim3[0])}}}^{{{latex(lim3[1])}}}\int_{{{latex(lim2[0])}}}^{{{latex(lim2[1])}}}\int_{{{latex(lim1[0])}}}^{{{latex(lim1[1])}}} {flt}\,d{n1}\,d{n2}\,d{n3}")
        else:
            st.latex(rf"\iiint {flt}\,d{n1}\,d{n2}\,d{n3}")
        st.markdown(f'<div class="step-explain">Integrate from the innermost ({n1}) outward ({n3}).</div>', unsafe_allow_html=True)
    step_card("Step 1", "Write the Iterated Triple Integral", _write)

    r1 = integrate(expr, (v1,lim1[0],lim1[1])) if lim1 else integrate(expr, v1)
    r1s = simplify(r1)
    def _r1():
        flt = latex(expr)
        if lim1: st.latex(rf"\int_{{{latex(lim1[0])}}}^{{{latex(lim1[1])}}} {flt}\,d{n1} = {latex(r1s)}")
        else:    st.latex(rf"\int {flt}\,d{n1} = {latex(r1s)}")
        st.markdown(f'<div class="step-explain">Result is now a function of {n2}, {n3} only.</div>', unsafe_allow_html=True)
    step_card("Step 2", f"Inner Integral w.r.t. {n1}", _r1, tip=f"Treat {n2}, {n3} as constants.")

    r2 = integrate(r1s, (v2,lim2[0],lim2[1])) if lim2 else integrate(r1s, v2)
    r2s = simplify(r2)
    def _r2():
        if lim2: st.latex(rf"\int_{{{latex(lim2[0])}}}^{{{latex(lim2[1])}}} \left[{latex(r1s)}\right]\,d{n2} = {latex(r2s)}")
        else:    st.latex(rf"\int \left[{latex(r1s)}\right]\,d{n2} = {latex(r2s)}")
        st.markdown(f'<div class="step-explain">Result depends on {n3} only.</div>', unsafe_allow_html=True)
    step_card("Step 3", f"Middle Integral w.r.t. {n2}", _r2, tip=f"Treat {n3} as a constant.")

    r3 = integrate(r2s, (v3,lim3[0],lim3[1])) if lim3 else integrate(r2s, v3)
    r3s = simplify(r3)
    def _r3():
        if lim3: st.latex(rf"\int_{{{latex(lim3[0])}}}^{{{latex(lim3[1])}}} \left[{latex(r2s)}\right]\,d{n3} = {latex(r3s)}")
        else:    st.latex(rf"\int \left[{latex(r2s)}\right]\,d{n3} = {latex(r3s)}")
    step_card("Step 4", f"Outer Integral w.r.t. {n3}", _r3)

    def _simp():
        st.latex(f"\\text{{Result}} = {latex(r3s)}")
        if lim1 and lim2 and lim3:
            try:
                nv = float(r3s.evalf())
                st.latex(rf"\approx {nv:.6f}")
                st.markdown(f'<div class="step-explain">≈ {nv:.4f} — the integral over the 3D region V (= volume when f=1).</div>', unsafe_allow_html=True)
            except: pass
    step_card("Step 5", "Simplify and Interpret", _simp)

    def _ans():
        flt = latex(expr)
        if lim1 and lim2 and lim3:
            st.latex(rf"\int_{{{latex(lim3[0])}}}^{{{latex(lim3[1])}}}\int_{{{latex(lim2[0])}}}^{{{latex(lim2[1])}}}\int_{{{latex(lim1[0])}}}^{{{latex(lim1[1])}}} {flt}\,d{n1}\,d{n2}\,d{n3} = {latex(r3s)}")
        else:
            st.latex(rf"\iiint {flt}\,d{n1}\,d{n2}\,d{n3} = {latex(r3s)} + C")
    final_card(_ans)

    if show_formula and f_keys: formula_card(f_keys)

    if show_graph:
        try:
            st.markdown("---")
            st.markdown("### 📊 Advanced Triple Integral Explorer")

            xr  = np.linspace(float(lim1[0].evalf()),float(lim1[1].evalf()),55) if lim1 else np.linspace(-2,2,55)
            yr  = np.linspace(float(lim2[0].evalf()),float(lim2[1].evalf()),55) if lim2 else np.linspace(-2,2,55)
            zlo = float(lim3[0].evalf()) if lim3 else -2.0
            zhi = float(lim3[1].evalf()) if lim3 else  2.0
            zr  = np.linspace(zlo, zhi, 55)
            ff  = sp.lambdify((v1, v2, v3), expr, modules=['numpy'])

            ttab1, ttab2, ttab3 = st.tabs([f"{n3}-Slice (XY plane)", f"{n1}-Slice (YZ plane)", f"{n2}-Slice (XZ plane)"])

            def _heatmap_layout(title, xa, ya):
                return dict(
                    title=dict(text=title, font=dict(size=15, color='#f0f6ff', family=_FF)),
                    xaxis=dict(title=xa, showgrid=True, gridcolor=_GC, color=_TC),
                    yaxis=dict(title=ya, showgrid=True, gridcolor=_GC, color=_TC),
                    paper_bgcolor=_PBG, plot_bgcolor=_BG,
                    font=dict(color=_TC, family=_FF),
                    height=430, margin=dict(l=20, r=20, t=60, b=20)
                )

            # ── TAB 1 : XY slice at fixed z ─────────────────────────────────
            with ttab1:
                st.caption(f"🎚️ Fix {n3}, see f({n1},{n2},·) heatmap in the XY plane")
                if "trp_z_slider" not in st.session_state:
                    st.session_state["trp_z_slider"] = float((zlo+zhi)/2)
                zv = st.slider(f"{n3} =", min_value=float(zlo), max_value=float(zhi),
                               value=float(st.session_state["trp_z_slider"]),
                               step=float((zhi-zlo)/80), key="trp_z_slider")
                X, Y = np.meshgrid(xr, yr)
                Zxy  = safe_eval_grid3(ff, X, Y, zv)
                fig1 = go.Figure(data=[go.Heatmap(
                    x=xr, y=yr, z=Zxy, colorscale='Plasma',
                    colorbar=dict(title=f'f  ({n3}={zv:.2f})', tickfont=dict(color=_TC)),
                    hoverongaps=False,
                    hovertemplate=f'{n1}=%{{x:.3f}}<br>{n2}=%{{y:.3f}}<br>f=%{{z:.4f}}<extra></extra>'
                )])
                # Overlay contour lines
                fig1.add_trace(go.Contour(
                    x=xr, y=yr, z=Zxy, showscale=False,
                    colorscale='Greys',
                    contours=dict(showlabels=True, labelfont=dict(size=9, color='white')),
                    line=dict(width=1), opacity=0.55, hoverinfo='skip'
                ))
                fig1.update_layout(**_heatmap_layout(
                    f"XY Cross-section  at  {n3} = {zv:.3f}", n1, n2))
                st.plotly_chart(fig1, use_container_width=True)

                # Value stats row
                Zxy_flat = Zxy[np.isfinite(Zxy)]
                if len(Zxy_flat) > 0:
                    sc1,sc2,sc3,sc4 = st.columns(4)
                    sc1.metric(f"{n3} value", f"{zv:.4f}")
                    sc2.metric("f  min", f"{Zxy_flat.min():.4f}")
                    sc3.metric("f  max", f"{Zxy_flat.max():.4f}")
                    sc4.metric("f  mean", f"{Zxy_flat.mean():.4f}")
                st.caption(f"Heatmap + contour lines of f({n1},{n2},{zv:.3f}) — colour = function value")

            # ── TAB 2 : YZ slice at fixed x ─────────────────────────────────
            with ttab2:
                st.caption(f"🎚️ Fix {n1}, see f(·,{n2},{n3}) heatmap in the YZ plane")
                xlo2, xhi2 = float(xr[0]), float(xr[-1])
                if "trp_x_slider" not in st.session_state:
                    st.session_state["trp_x_slider"] = float((xlo2+xhi2)/2)
                xv = st.slider(f"{n1} =", min_value=xlo2, max_value=xhi2,
                               value=float(st.session_state["trp_x_slider"]),
                               step=float((xhi2-xlo2)/80), key="trp_x_slider")
                Y2, Z2 = np.meshgrid(yr, zr)
                Zyz = np.zeros_like(Y2)
                for i in range(Y2.shape[0]):
                    for j in range(Y2.shape[1]):
                        try:
                            val = float(ff(xv, float(Y2[i,j]), float(Z2[i,j])))
                            Zyz[i,j] = val if np.isfinite(val) else np.nan
                        except: Zyz[i,j] = np.nan
                fig2 = go.Figure(data=[go.Heatmap(
                    x=yr, y=zr, z=Zyz, colorscale='Viridis',
                    colorbar=dict(title=f'f  ({n1}={xv:.2f})', tickfont=dict(color=_TC)),
                    hoverongaps=False,
                    hovertemplate=f'{n2}=%{{x:.3f}}<br>{n3}=%{{y:.3f}}<br>f=%{{z:.4f}}<extra></extra>'
                )])
                fig2.add_trace(go.Contour(
                    x=yr, y=zr, z=Zyz, showscale=False,
                    colorscale='Greys',
                    contours=dict(showlabels=True, labelfont=dict(size=9, color='white')),
                    line=dict(width=1), opacity=0.55, hoverinfo='skip'
                ))
                fig2.update_layout(**_heatmap_layout(
                    f"YZ Cross-section  at  {n1} = {xv:.3f}", n2, n3))
                st.plotly_chart(fig2, use_container_width=True)
                Zyz_flat = Zyz[np.isfinite(Zyz)]
                if len(Zyz_flat) > 0:
                    sc1,sc2,sc3,sc4 = st.columns(4)
                    sc1.metric(f"{n1} value", f"{xv:.4f}")
                    sc2.metric("f  min", f"{Zyz_flat.min():.4f}")
                    sc3.metric("f  max", f"{Zyz_flat.max():.4f}")
                    sc4.metric("f  mean", f"{Zyz_flat.mean():.4f}")
                st.caption(f"Heatmap + contour lines of f({xv:.3f},{n2},{n3}) — colour = function value")

            # ── TAB 3 : XZ slice at fixed y ─────────────────────────────────
            with ttab3:
                st.caption(f"🎚️ Fix {n2}, see f({n1},·,{n3}) heatmap in the XZ plane")
                ylo2, yhi2 = float(yr[0]), float(yr[-1])
                if "trp_y_slider" not in st.session_state:
                    st.session_state["trp_y_slider"] = float((ylo2+yhi2)/2)
                yv = st.slider(f"{n2} =", min_value=ylo2, max_value=yhi2,
                               value=float(st.session_state["trp_y_slider"]),
                               step=float((yhi2-ylo2)/80), key="trp_y_slider")
                X3, Z3 = np.meshgrid(xr, zr)
                Zxz = np.zeros_like(X3)
                for i in range(X3.shape[0]):
                    for j in range(X3.shape[1]):
                        try:
                            val = float(ff(float(X3[i,j]), yv, float(Z3[i,j])))
                            Zxz[i,j] = val if np.isfinite(val) else np.nan
                        except: Zxz[i,j] = np.nan
                fig3 = go.Figure(data=[go.Heatmap(
                    x=xr, y=zr, z=Zxz, colorscale='Cividis',
                    colorbar=dict(title=f'f  ({n2}={yv:.2f})', tickfont=dict(color=_TC)),
                    hoverongaps=False,
                    hovertemplate=f'{n1}=%{{x:.3f}}<br>{n3}=%{{y:.3f}}<br>f=%{{z:.4f}}<extra></extra>'
                )])
                fig3.add_trace(go.Contour(
                    x=xr, y=zr, z=Zxz, showscale=False,
                    colorscale='Greys',
                    contours=dict(showlabels=True, labelfont=dict(size=9, color='white')),
                    line=dict(width=1), opacity=0.55, hoverinfo='skip'
                ))
                fig3.update_layout(**_heatmap_layout(
                    f"XZ Cross-section  at  {n2} = {yv:.3f}", n1, n3))
                st.plotly_chart(fig3, use_container_width=True)
                Zxz_flat = Zxz[np.isfinite(Zxz)]
                if len(Zxz_flat) > 0:
                    sc1,sc2,sc3,sc4 = st.columns(4)
                    sc1.metric(f"{n2} value", f"{yv:.4f}")
                    sc2.metric("f  min", f"{Zxz_flat.min():.4f}")
                    sc3.metric("f  max", f"{Zxz_flat.max():.4f}")
                    sc4.metric("f  mean", f"{Zxz_flat.mean():.4f}")
                st.caption(f"Heatmap + contour lines of f({n1},{yv:.3f},{n3}) — colour = function value")

        except Exception as e: st.warning(f"⚠️ 3D error: {e}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  HELPERS                                                                 ║
# ╚══════════════════════════════════════════════════════════════════════════╝
def _wrap(div_id):  st.markdown(f'<div id="{div_id}">', unsafe_allow_html=True)
def _end():         st.markdown('</div>', unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SYNTAX REFERENCE HTML  — 100 % inline styles, no CSS classes needed    ║
# ╚══════════════════════════════════════════════════════════════════════════╝
def _row(math_label, code_text, code_color, bg_color, border_color):
    """Single table row: math symbol label → code badge."""
    return (
        f'<tr style="border-bottom:1px solid #f1f5f9;">'
        f'<td style="padding:8px 12px 8px 0;color:#475569;font-size:13px;">{math_label}</td>'
        f'<td style="padding:8px 8px;color:#94a3b8;font-size:12px;">→</td>'
        f'<td style="padding:8px 0;">'
        f'<span style="background:{bg_color};border:1px solid {border_color};color:{code_color};'
        f'font-family:\'JetBrains Mono\',\'Courier New\',monospace;font-size:13px;font-weight:700;'
        f'padding:4px 10px;border-radius:7px;white-space:nowrap;">{code_text}</span>'
        f'</td>'
        f'</tr>'
    )

def _card(icon, accent, title, rows_html):
    """Syntax card with coloured top border."""
    return (
        f'<div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:14px;'
        f'overflow:hidden;flex:1;min-width:220px;">'
        f'<div style="height:4px;background:{accent};"></div>'
        f'<div style="padding:18px 20px 22px;">'
        f'<div style="font-size:11px;font-weight:800;letter-spacing:0.12em;text-transform:uppercase;'
        f'color:{accent};margin-bottom:16px;">{icon}&nbsp; {title}</div>'
        f'<table style="border-collapse:collapse;width:100%;">{rows_html}</table>'
        f'</div></div>'
    )

# ── math labels use Unicode superscripts / math symbols — no plain English ──
_basic = (
    _row("x²",        "x**2",        "#2563eb","#eff6ff","#bfdbfe") +
    _row("x³",        "x**3",        "#2563eb","#eff6ff","#bfdbfe") +
    _row("xⁿ",        "x**n",        "#2563eb","#eff6ff","#bfdbfe") +
    _row("x·y",       "x*y",         "#2563eb","#eff6ff","#bfdbfe") +
    _row("x/y",       "x/y",         "#2563eb","#eff6ff","#bfdbfe") +
    _row("√x",        "sqrt(x)",     "#2563eb","#eff6ff","#bfdbfe") +
    _row("1/(x²+1)",  "1/(x**2+1)",  "#2563eb","#eff6ff","#bfdbfe")
)

_trig = (
    _row("sin x",    "sin(x)",      "#7c3aed","#f5f3ff","#ddd6fe") +
    _row("cos x",    "cos(x)",      "#7c3aed","#f5f3ff","#ddd6fe") +
    _row("tan x",    "tan(x)",      "#7c3aed","#f5f3ff","#ddd6fe") +
    _row("sin⁻¹x",   "asin(x)",     "#7c3aed","#f5f3ff","#ddd6fe") +
    _row("cos⁻¹x",   "acos(x)",     "#7c3aed","#f5f3ff","#ddd6fe") +
    _row("tan⁻¹x",   "atan(x)",     "#7c3aed","#f5f3ff","#ddd6fe") +
    _row("sin²x",    "sin(x)**2",   "#7c3aed","#f5f3ff","#ddd6fe")
)

_explog = (
    _row("eˣ",       "exp(x)",      "#059669","#ecfdf5","#6ee7b7") +
    _row("e^(x²)",   "exp(x**2)",   "#059669","#ecfdf5","#6ee7b7") +
    _row("ln(x)",    "log(x)",      "#059669","#ecfdf5","#6ee7b7") +
    _row("log₁₀(x)", "log(x,10)",   "#059669","#ecfdf5","#6ee7b7") +
    _row("sinh x",   "sinh(x)",     "#059669","#ecfdf5","#6ee7b7") +
    _row("cosh x",   "cosh(x)",     "#059669","#ecfdf5","#6ee7b7") +
    _row("tanh x",   "tanh(x)",     "#059669","#ecfdf5","#6ee7b7")
)

_special = (
    _row("∞",        "oo",               "#d97706","#fffbeb","#fde68a") +
    _row("π",        "pi",               "#d97706","#fffbeb","#fde68a") +
    _row("e",        "E",                "#d97706","#fffbeb","#fde68a") +
    _row("|x|",      "Abs(x)",           "#d97706","#fffbeb","#fde68a") +
    _row("x·sin(x²)","x*sin(x**2)",      "#d97706","#fffbeb","#fde68a") +
    _row("ln(sin x)","log(sin(x))",      "#d97706","#fffbeb","#fde68a") +
    _row("−∞",       "-oo",              "#d97706","#fffbeb","#fde68a")
)

def _c(t):  # inline code badge helper for the key-rules line
    return (f'<span style="background:#eff6ff;border:1px solid #bfdbfe;color:#2563eb;'
            f'font-family:\'JetBrains Mono\',monospace;font-size:12px;font-weight:600;'
            f'padding:2px 7px;border-radius:4px;">{t}</span>')

_HOW_TO_USE_HTML = (
    '<div style="margin:2.5rem 0 1rem;">'

    # subtitle only — no step cards
    '<div style="text-align:center;font-size:13px;color:#94a3b8;margin-bottom:18px;">'
    'Use the syntax below when entering your function</div>'

    # 4 syntax cards
    '<div style="display:flex;gap:14px;flex-wrap:wrap;">'
    + _card("1.","#2563eb","Basic Operations",      _basic)
    + _card("2.","#7c3aed","Trig &amp; Inverse Trig", _trig)
    + _card("3.","#059669","Exponential &amp; Log",  _explog)
    + _card("4.","#d97706","Special Values &amp; Tips", _special)
    + '</div>'

    # key rules bar
    + '<div style="margin-top:16px;padding:12px 16px;background:#f8faff;'
    'border-left:3px solid #4f8ef7;border-radius:0 8px 8px 0;'
    'font-size:12.5px;color:#64748b;line-height:1.8;">'
    + '  <strong style="color:#475569;">Key rules:</strong> &nbsp;'
    + f'Use {_c("**")} for powers, not {_c("^")} &nbsp;·&nbsp; '
    + f'Use {_c("*")} for multiplication — write {_c("2*x")} not {_c("2x")} &nbsp;·&nbsp; '
    + f'Functions need brackets: {_c("sin(x)")} not {_c("sinx")}'
    + '</div>'

    '</div>'
)

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  MAIN APP                                                                ║
# ╚══════════════════════════════════════════════════════════════════════════╝
if st.session_state.operation is None:

    # Title
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-title">Advanced <span>Calculus Solver</span></div>
        <div class="hero-sub">Step-by-step solutions with interactive visualizations.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-heading">
        <h2>Choose Your Operation</h2>
        <p>Click a card below to start solving</p>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="op-card card-der">
            <div class="op-symbol-text">d/dx</div>
            <div class="op-name">Derivative</div>
            <div class="op-caption">Rate of change — polynomials to trig. Up to 5th-order with full rule detection.</div>
        </div>""", unsafe_allow_html=True)
        _wrap("card-btn-der")
        if st.button("Click here to solve Derivative", key="der", use_container_width=True):
            st.session_state.operation = "Derivative"; st.rerun()
        _end()

    with c2:
        st.markdown(f"""
        <div class="op-card card-int">
            <div class="op-symbol-text" style="font-size:3.2rem;background:linear-gradient(135deg,#a78bfa,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-shadow:none;filter:drop-shadow(0 2px 10px rgba(167,139,250,0.5));">∫</div>
            <div class="op-name">Single Integral</div>
            <div class="op-caption">Definite &amp; indefinite integrals — u-sub, by-parts, direct rules &amp; area visualisation.</div>
        </div>""", unsafe_allow_html=True)
        _wrap("card-btn-int")
        if st.button("Click here to solve Integral", key="int", use_container_width=True):
            st.session_state.operation = "Single Integral"; st.rerun()
        _end()

    with c3:
        st.markdown(f"""
        <div class="op-card card-dbl">
            <div class="op-symbol-text" style="font-size:2.8rem;background:linear-gradient(135deg,#34d399,#059669);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-shadow:none;filter:drop-shadow(0 2px 10px rgba(52,211,153,0.5));">∬</div>
            <div class="op-name">Double Integral</div>
            <div class="op-caption">2D region integrals — Fubini's theorem step-by-step with 3D surface plot.</div>
        </div>""", unsafe_allow_html=True)
        _wrap("card-btn-dbl")
        if st.button("Click here to solve Double Integral", key="dbl", use_container_width=True):
            st.session_state.operation = "Double Integral"; st.rerun()
        _end()

    with c4:
        st.markdown(f"""
        <div class="op-card card-trp">
            <div class="op-symbol-text" style="font-size:2.6rem;background:linear-gradient(135deg,#fb923c,#f97316);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-shadow:none;filter:drop-shadow(0 2px 10px rgba(251,146,60,0.5));">∭</div>
            <div class="op-name">Triple Integral</div>
            <div class="op-caption">3D volume integrals with interactive Z-slice cross-section explorer.</div>
        </div>""", unsafe_allow_html=True)
        _wrap("card-btn-trp")
        if st.button("Click here to solve Triple Integral", key="trp", use_container_width=True):
            st.session_state.operation = "Triple Integral"; st.rerun()
        _end()

    # ── How To Use ──────────────────────────────────────────────────────────
    st.markdown(_HOW_TO_USE_HTML, unsafe_allow_html=True)

else:
    operation = st.session_state.operation

    # Banner symbols — all Unicode, no SVG
    def _banner_svg(op):
        m = {
            "Derivative":     '<span style="font-family:\'JetBrains Mono\',monospace;font-size:1.8rem;font-weight:800;background:linear-gradient(135deg,#4f8ef7,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">d/dx</span>',
            "Single Integral":'<span style="font-size:2.4rem;font-weight:900;background:linear-gradient(135deg,#a78bfa,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;filter:drop-shadow(0 2px 8px rgba(167,139,250,0.55));line-height:1;">∫</span>',
            "Double Integral":'<span style="font-size:2.2rem;font-weight:900;background:linear-gradient(135deg,#34d399,#059669);-webkit-background-clip:text;-webkit-text-fill-color:transparent;filter:drop-shadow(0 2px 8px rgba(52,211,153,0.55));line-height:1;">∬</span>',
            "Triple Integral":'<span style="font-size:2.0rem;font-weight:900;background:linear-gradient(135deg,#fb923c,#f97316);-webkit-background-clip:text;-webkit-text-fill-color:transparent;filter:drop-shadow(0 2px 8px rgba(251,146,60,0.55));line-height:1;">∭</span>',
        }
        return m.get(op,"")

    BMETA = {
        "Derivative":      ("Derivative Solver",      "Intelligent rule detection · step-by-step · critical points"),
        "Single Integral": ("Single Integral Solver",  "Auto-detects u-sub / by-parts · FToC · area visualisation"),
        "Double Integral": ("Double Integral Solver",  "Fubini's theorem · iterated integration · 3D surface"),
        "Triple Integral": ("Triple Integral Solver",  "Iterated 3D integration · Z-slice surface explorer"),
    }
    title, subtitle = BMETA[operation]
    st.markdown(f"""
    <div class="solver-banner">
        <div class="sb-symbol">{_banner_svg(operation)}</div>
        <div class="sb-text"><h3>{title}</h3><p>{subtitle}</p></div>
    </div>""", unsafe_allow_html=True)

    _wrap("back-btn")
    if st.button("← Back to Menu"): st.session_state.operation = None; st.rerun()
    _end()

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('<div class="input-panel-head">Input Parameters</div>', unsafe_allow_html=True)
        EX = {
            "Derivative":      {"x²":"x**2","sin(x)·cos(x)":"sin(x)*cos(x)","(ln x)²":"log(x)**2","eˣ²":"exp(x**2)","x·eˣ":"x*exp(x)","1/(x²+1)":"1/(x**2+1)","x³·sin(x)":"x**3*sin(x)","ln(sin(x))":"log(sin(x))"},
            "Single Integral": {"x²":"x**2","sin(x)":"sin(x)","eˣ":"exp(x)","x·eˣ":"x*exp(x)","1/(x²+1)":"1/(x**2+1)","x·sin(x)":"x*sin(x)","ln(x)":"log(x)"},
            "Double Integral": {"x·y":"x*y","x²·y":"x**2*y","eˣ⁺ʸ":"exp(x+y)","sin(x+y)":"sin(x+y)"},
            "Triple Integral": {"x·y·z":"x*y*z","x²+y²+z²":"x**2+y**2+z**2"},
        }
        ex = EX.get(operation, {})
        sel = st.selectbox("Quick Examples:", ["Custom"]+list(ex.keys()))
        default = ex.get(sel,"x*y*z" if "Triple" in operation else ("x*y" if "Double" in operation else "x**2")) if sel!="Custom" else ("x*y*z" if "Triple" in operation else ("x*y" if "Double" in operation else "x**2"))
        func_in = st.text_area("**Function:**", value=default, height=90)

        st.markdown('<div class="disp-options-head">Display Options</div>', unsafe_allow_html=True)
        show_formula = st.checkbox("Show Relevant Formulas", value=st.session_state.show_formula, key="cb_f")
        show_graph   = st.checkbox("Show Graph", value=st.session_state.show_graph, key="cb_g")

        # If checkbox changed while a solution is already rendered, update stored inputs live
        if show_formula != st.session_state.show_formula or show_graph != st.session_state.show_graph:
            st.session_state.show_formula = show_formula
            st.session_state.show_graph   = show_graph
            for _key in ('der_inputs','int_inputs','dbl_inputs','trp_inputs'):
                if st.session_state.get(_key):
                    st.session_state[_key]['show_formula'] = show_formula
                    st.session_state[_key]['show_graph']   = show_graph
        else:
            st.session_state.show_formula = show_formula
            st.session_state.show_graph   = show_graph

        st.markdown("---")

        # Variable & limit inputs
        if operation == "Double Integral":
            vc1,vc2 = st.columns(2)
            with vc1: var1 = st.text_input("Inner var:", value="x")
            with vc2: var2 = st.text_input("Outer var:", value="y")
        elif operation == "Triple Integral":
            vc1,vc2,vc3 = st.columns(3)
            with vc1: var1 = st.text_input("Inner:", value="x")
            with vc2: var2 = st.text_input("Mid:",   value="y")
            with vc3: var3 = st.text_input("Outer:", value="z")
        else:
            variable = st.text_input("**Variable:**", value="x")

        if operation == "Derivative":
            order = st.number_input("Derivative Order:", 1, 5, 1)

        elif operation == "Single Integral":
            definite = st.checkbox("✓ Definite integral?")
            if definite:
                st.info("  Use `oo` for ∞")
                la,lb = st.columns(2)
                with la: lo_in = st.text_input("Lower:", value="0")
                with lb: hi_in = st.text_input("Upper:", value="1")

        elif operation == "Double Integral":
            definite = st.checkbox("✓ Definite?")
            if definite:
                la1,lb1 = st.columns(2)
                with la1: lo1 = st.text_input(f"{var1} Lower:", value="0", key="l1")
                with lb1: hi1 = st.text_input(f"{var1} Upper:", value="1", key="u1")
                la2,lb2 = st.columns(2)
                with la2: lo2 = st.text_input(f"{var2} Lower:", value="0", key="l2")
                with lb2: hi2 = st.text_input(f"{var2} Upper:", value="1", key="u2")

        elif operation == "Triple Integral":
            definite = st.checkbox("✓ Definite?")
            if definite:
                la1,lb1 = st.columns(2)
                with la1: lo1 = st.text_input(f"{var1} L:", value="0", key="l1")
                with lb1: hi1 = st.text_input(f"{var1} U:", value="1", key="u1")
                la2,lb2 = st.columns(2)
                with la2: lo2 = st.text_input(f"{var2} L:", value="0", key="l2")
                with lb2: hi2 = st.text_input(f"{var2} U:", value="1", key="u2")
                la3,lb3 = st.columns(2)
                with la3: lo3 = st.text_input(f"{var3} L:", value="0", key="l3")
                with lb3: hi3 = st.text_input(f"{var3} U:", value="1", key="u3")

        st.markdown("---")
        _wrap("solve-btn")
        solve_btn = st.button("Click here to Solve Now", type="primary", use_container_width=True)
        _end()

    with col2:
        st.markdown('<div class="solution-panel-head">Step-by-Step Solution</div>', unsafe_allow_html=True)

        # When operation changes, clear stored solutions
        if st.session_state.get('der_solved') and st.session_state.get('der_inputs', {}).get('operation') != operation:
            st.session_state.der_solved = False
            st.session_state.der_inputs = None
        if st.session_state.get('trp_solved') and st.session_state.get('trp_inputs', {}).get('operation') != operation:
            st.session_state.trp_solved = False
            st.session_state.trp_inputs = None
        if st.session_state.get('dbl_solved') and st.session_state.get('dbl_inputs', {}).get('operation') != operation:
            st.session_state.dbl_solved = False
            st.session_state.dbl_inputs = None
        if st.session_state.get('int_solved') and st.session_state.get('int_inputs', {}).get('operation') != operation:
            st.session_state.int_solved = False
            st.session_state.int_inputs = None

        # Determine whether to render
        # Also re-render when a checkbox is toggled while a solution is stored
        _checkbox_changed = (show_formula != st.session_state.get('_prev_sf', show_formula) or
                             show_graph   != st.session_state.get('_prev_sg', show_graph))
        st.session_state['_prev_sf'] = show_formula
        st.session_state['_prev_sg'] = show_graph

        render_solution = solve_btn
        if not render_solution and operation == "Derivative" and st.session_state.der_solved:
            render_solution = True
        if not render_solution and operation == "Triple Integral" and st.session_state.trp_solved:
            render_solution = True
        if not render_solution and operation == "Double Integral" and st.session_state.dbl_solved:
            render_solution = True
        if not render_solution and operation == "Single Integral" and st.session_state.int_solved:
            render_solution = True
        # Re-render on checkbox toggle if any solver has a stored solution
        if not render_solution and _checkbox_changed:
            if (st.session_state.der_solved or
                st.session_state.int_solved or
                st.session_state.dbl_solved or
                st.session_state.trp_solved):
                render_solution = True

        if solve_btn and operation == "Derivative":
            st.session_state.der_solved = True
            st.session_state.der_inputs = {
                'operation': operation,
                'func_in': func_in,
                'variable': variable,
                'order': order,
                'show_formula': show_formula, 'show_graph': show_graph,
            }
        elif solve_btn and operation == "Single Integral":
            st.session_state.int_solved = True
            st.session_state.int_inputs = {
                'operation': operation,
                'func_in': func_in,
                'variable': variable,
                'definite': definite,
                'lo_in': lo_in if definite else '0',
                'hi_in': hi_in if definite else '1',
                'show_formula': show_formula, 'show_graph': show_graph,
            }
        elif solve_btn and operation == "Triple Integral":
            st.session_state.trp_solved = True
            st.session_state.trp_inputs = {
                'operation': operation,
                'func_in': func_in,
                'var1': var1, 'var2': var2, 'var3': var3,
                'definite': definite,
                'lo1': lo1 if definite else '0', 'hi1': hi1 if definite else '1',
                'lo2': lo2 if definite else '0', 'hi2': hi2 if definite else '1',
                'lo3': lo3 if definite else '0', 'hi3': hi3 if definite else '1',
                'show_formula': show_formula, 'show_graph': show_graph,
            }
        elif solve_btn and operation == "Double Integral":
            st.session_state.dbl_solved = True
            st.session_state.dbl_inputs = {
                'operation': operation,
                'func_in': func_in,
                'var1': var1, 'var2': var2,
                'definite': definite,
                'lo1': lo1 if definite else '0', 'hi1': hi1 if definite else '1',
                'lo2': lo2 if definite else '0', 'hi2': hi2 if definite else '1',
                'show_formula': show_formula, 'show_graph': show_graph,
            }
        elif solve_btn:
            st.session_state.der_solved = False
            st.session_state.der_inputs = None
            st.session_state.trp_solved = False
            st.session_state.trp_inputs = None
            st.session_state.dbl_solved = False
            st.session_state.dbl_inputs = None
            st.session_state.int_solved = False
            st.session_state.int_inputs = None

        if render_solution:
            # Restore inputs for derivative slider reruns
            if not solve_btn and operation == "Derivative" and st.session_state.der_inputs:
                di = st.session_state.der_inputs
                func_in      = di['func_in']
                variable     = di['variable']
                order        = di['order']
                show_formula = di['show_formula']
                show_graph   = di['show_graph']
            # Restore inputs for triple integral slider reruns
            if not solve_btn and operation == "Triple Integral" and st.session_state.trp_inputs:
                ti = st.session_state.trp_inputs
                func_in      = ti['func_in']
                var1,var2,var3 = ti['var1'],ti['var2'],ti['var3']
                definite     = ti['definite']
                lo1,hi1      = ti['lo1'],ti['hi1']
                lo2,hi2      = ti['lo2'],ti['hi2']
                lo3,hi3      = ti['lo3'],ti['hi3']
                show_formula = ti['show_formula']
                show_graph   = ti['show_graph']
            # Restore inputs for double integral slider reruns
            if not solve_btn and operation == "Double Integral" and st.session_state.dbl_inputs:
                di = st.session_state.dbl_inputs
                func_in      = di['func_in']
                var1,var2    = di['var1'],di['var2']
                definite     = di['definite']
                lo1,hi1      = di['lo1'],di['hi1']
                lo2,hi2      = di['lo2'],di['hi2']
                show_formula = di['show_formula']
                show_graph   = di['show_graph']
            # Restore inputs for single integral slider/radio reruns
            if not solve_btn and operation == "Single Integral" and st.session_state.int_inputs:
                ii = st.session_state.int_inputs
                func_in      = ii['func_in']
                variable     = ii['variable']
                definite     = ii['definite']
                lo_in        = ii['lo_in']
                hi_in        = ii['hi_in']
                show_formula = ii['show_formula']
                show_graph   = ii['show_graph']
            try:
                if operation == "Derivative":
                    var = symbols(variable); expr = sympify(func_in)
                    st.markdown("### f(x)"); st.latex(f"f(x)={latex(expr)}"); st.markdown("---")
                    solve_derivative(expr, var, order, show_formula, show_graph)

                elif operation == "Single Integral":
                    var = symbols(variable); expr = sympify(func_in)
                    st.markdown("### f(x)"); st.latex(f"f(x)={latex(expr)}"); st.markdown("---")
                    if definite:
                        solve_integral(expr, var, True, sympify(lo_in), sympify(hi_in), show_formula, show_graph)
                    else:
                        solve_integral(expr, var, False, None, None, show_formula, show_graph)

                elif operation == "Double Integral":
                    v1=symbols(var1); v2=symbols(var2); expr=sympify(func_in)
                    st.markdown(f"### f({var1},{var2})"); st.latex(f"f({var1},{var2})={latex(expr)}"); st.markdown("---")
                    if definite:
                        solve_double_integral(expr,v1,v2,(sympify(lo1),sympify(hi1)),(sympify(lo2),sympify(hi2)),show_formula,show_graph)
                    else:
                        solve_double_integral(expr,v1,v2,None,None,show_formula,show_graph)

                elif operation == "Triple Integral":
                    v1=symbols(var1); v2=symbols(var2); v3=symbols(var3); expr=sympify(func_in)
                    st.markdown(f"### f({var1},{var2},{var3})"); st.latex(f"f({var1},{var2},{var3})={latex(expr)}"); st.markdown("---")
                    if definite:
                        solve_triple_integral(expr,v1,v2,v3,(sympify(lo1),sympify(hi1)),(sympify(lo2),sympify(hi2)),(sympify(lo3),sympify(hi3)),show_formula,show_graph)
                    else:
                        solve_triple_integral(expr,v1,v2,v3,None,None,None,show_formula,show_graph)

            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.info("  Syntax: `log(x)` for ln · `oo` for ∞ · `**2` for squared")

st.markdown("---")
st.markdown("""
<div class="footer-wrap">
    <strong>MathWithAmrit</strong> ·Calculus Solver ·<br>
    Built for mathematics learners · 
</div>""", unsafe_allow_html=True)