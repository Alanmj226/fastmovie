"""
Convert logo.svg → logo.png  (or copy the pre-generated AI PNG if available)
Tries cairosvg first, then Pillow+wand, then falls back to copying the AI-generated PNG.
"""
import os, shutil, sys

SVG_PATH  = r"d:\VSC\.vscode\logo.svg"
PNG_OUT   = r"d:\VSC\.vscode\logo.png"
AI_PNG    = os.path.join(os.getcwd(), "fast_movie_logo.png")

# ── Method 1: cairosvg ──────────────────────────────────────────────
try:
    import cairosvg
    cairosvg.svg2png(url=SVG_PATH, write_to=PNG_OUT, output_width=512, output_height=512)
    print("✅ Converted via cairosvg →", PNG_OUT)
    sys.exit(0)
except ImportError:
    print("cairosvg not installed, trying next...")
except Exception as e:
    print(f"cairosvg error: {e}, trying next...")

# ── Method 2: copy the AI-generated PNG ────────────────────────────
if os.path.exists(AI_PNG):
    shutil.copy2(AI_PNG, PNG_OUT)
    print("✅ Copied AI-generated logo →", PNG_OUT)
    sys.exit(0)

print("❌ Could not find any source PNG. Please manually copy a PNG to:", PNG_OUT)
