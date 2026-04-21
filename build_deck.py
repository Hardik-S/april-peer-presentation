from __future__ import annotations

import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parent
DECK_DIR = ROOT / "deck"
PNG_DIR = DECK_DIR / "slides_png"
REVIEW_DIR = ROOT / "review"
OUTPUT_PPTX = DECK_DIR / "April_peer_presentation.pptx"
OUTPUT_SCRIPT = DECK_DIR / "April_peer_presentation_script.md"
CONTACT_SHEET = REVIEW_DIR / "contact_sheet.png"
STRUCTURE_MAP = REVIEW_DIR / "adam_structure_mapping.md"
REVIEW_MEMO = REVIEW_DIR / "review_memo.md"
REVIEW_CHECKLIST = REVIEW_DIR / "review_checklist.md"
ADAM_DIR = ROOT / "sources" / "adam_structure"

SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)
WORDS_PER_MINUTE = 130

NAVY = RGBColor(16, 38, 68)
INK = RGBColor(30, 37, 46)
SLATE = RGBColor(78, 91, 108)
TEAL = RGBColor(33, 132, 142)
TEAL_SOFT = RGBColor(222, 241, 241)
GOLD = RGBColor(223, 169, 59)
GOLD_SOFT = RGBColor(250, 239, 209)
RED = RGBColor(177, 70, 64)
RED_SOFT = RGBColor(248, 229, 225)
GREEN = RGBColor(57, 140, 101)
GREEN_SOFT = RGBColor(230, 244, 235)
BLUE_SOFT = RGBColor(232, 239, 249)
BG = RGBColor(248, 246, 239)
WHITE = RGBColor(255, 255, 255)

TITLE_FONT = "Bahnschrift"
BODY_FONT = "Aptos"
MONO_FONT = "Consolas"


def color(name: str) -> RGBColor:
    return {
        "navy": NAVY,
        "ink": INK,
        "slate": SLATE,
        "teal": TEAL,
        "teal_soft": TEAL_SOFT,
        "gold": GOLD,
        "gold_soft": GOLD_SOFT,
        "red": RED,
        "red_soft": RED_SOFT,
        "green": GREEN,
        "green_soft": GREEN_SOFT,
        "blue_soft": BLUE_SOFT,
        "bg": BG,
        "white": WHITE,
    }[name]


def add_text_box(slide, left, top, width, height, paragraphs, *, margin=0.05, vertical_anchor=None):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Inches(margin)
    frame.margin_right = Inches(margin)
    frame.margin_top = Inches(margin)
    frame.margin_bottom = Inches(margin)
    if vertical_anchor is not None:
        frame.vertical_anchor = vertical_anchor
    for idx, spec in enumerate(paragraphs):
        p = frame.paragraphs[0] if idx == 0 else frame.add_paragraph()
        p.text = spec["text"]
        p.alignment = spec.get("align", PP_ALIGN.LEFT)
        p.level = spec.get("level", 0)
        p.font.name = spec.get("font", BODY_FONT)
        p.font.size = Pt(spec.get("size", 18))
        p.font.bold = spec.get("bold", False)
        p.font.color.rgb = color(spec.get("color", "ink"))
        p.space_after = Pt(spec.get("space_after", 5))
    return box


def add_card(slide, left, top, width, height, fill_name, *, line_name=None, rounded=True):
    shape_type = MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE if rounded else MSO_AUTO_SHAPE_TYPE.RECTANGLE
    shape = slide.shapes.add_shape(shape_type, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color(fill_name)
    shape.line.color.rgb = color(line_name or fill_name)
    shape.line.width = Pt(1.1)
    return shape


def add_chip(slide, text, left, top, width, fill_name="navy", *, text_name="white", font_size=10):
    add_card(slide, left, top, width, 0.34, fill_name)
    add_text_box(
        slide,
        left + 0.08,
        top + 0.08,
        width - 0.16,
        0.16,
        [{"text": text, "size": font_size, "bold": True, "color": text_name, "align": PP_ALIGN.CENTER}],
        margin=0.0,
        vertical_anchor=MSO_ANCHOR.MIDDLE,
    )


def add_background(slide):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = BG
    rail = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, Inches(0.18), SLIDE_HEIGHT)
    rail.fill.solid()
    rail.fill.fore_color.rgb = NAVY
    rail.line.fill.background()
    accent = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, Inches(0.18), 0, Inches(0.08), SLIDE_HEIGHT)
    accent.fill.solid()
    accent.fill.fore_color.rgb = GOLD
    accent.line.fill.background()


def add_headline(slide, title, label):
    add_text_box(slide, 0.72, 0.58, 9.8, 0.72, [{"text": title, "size": 28, "bold": True, "color": "navy"}], margin=0.0)
    add_chip(slide, label, 10.68, 0.74, 1.95, "teal", font_size=9)


def add_takeaway(slide, text, *, fill_name="gold_soft", line_name="gold"):
    add_card(slide, 0.78, 6.13, 11.85, 0.6, fill_name, line_name=line_name)
    add_text_box(
        slide,
        1.0,
        6.31,
        11.4,
        0.18,
        [{"text": text, "size": 14, "bold": True, "color": "navy", "align": PP_ALIGN.CENTER}],
        margin=0.0,
        vertical_anchor=MSO_ANCHOR.MIDDLE,
    )


def add_footer(slide, number):
    line = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, Inches(0.72), Inches(6.92), Inches(11.8), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = TEAL
    line.line.fill.background()
    add_text_box(slide, 11.8, 6.98, 0.75, 0.2, [{"text": f"{number:02d}", "size": 9, "color": "slate", "align": PP_ALIGN.RIGHT}], margin=0.0)


def add_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def bullet_paragraphs(items, *, size=18, color_name="ink"):
    return [{"text": item, "size": size, "color": color_name, "space_after": 8} for item in items]


def render_title(prs, number, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = NAVY
    bar = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, SLIDE_WIDTH, Inches(0.2))
    bar.fill.solid()
    bar.fill.fore_color.rgb = GOLD
    bar.line.fill.background()
    add_text_box(slide, 0.78, 1.15, 10.9, 1.15, [{"text": spec["title"], "size": 35, "bold": True, "color": "white"}], margin=0.0)
    add_text_box(slide, 0.8, 2.55, 8.8, 0.52, [{"text": spec["subtitle"], "size": 17, "color": "gold_soft"}], margin=0.0)
    add_card(slide, 0.82, 4.0, 5.4, 1.1, "teal")
    add_text_box(slide, 1.08, 4.28, 4.88, 0.42, [{"text": spec["claim"], "size": 18, "bold": True, "color": "white", "align": PP_ALIGN.CENTER}], margin=0.0, vertical_anchor=MSO_ANCHOR.MIDDLE)
    add_chip(slide, "Adam's structure + Hardik's Maple content", 7.2, 4.25, 4.8, "white", text_name="navy", font_size=12)
    add_notes(slide, spec["script"])
    add_footer(slide, number)


def render_roadmap(prs, number, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide)
    add_headline(slide, spec["title"], "Talk Map")
    for idx, step in enumerate(spec["steps"]):
        left = 0.82 + idx * 3.1
        add_card(slide, left, 2.0, 2.72, 2.75, step["fill"], line_name=step["line"])
        add_text_box(slide, left + 0.22, 2.28, 2.28, 0.42, [{"text": step["name"], "size": 18, "bold": True, "color": "navy", "align": PP_ALIGN.CENTER}], margin=0.0)
        add_text_box(slide, left + 0.23, 3.02, 2.25, 0.82, [{"text": step["detail"], "size": 13, "color": "ink", "align": PP_ALIGN.CENTER}], margin=0.0)
        add_chip(slide, step["tag"], left + 0.3, 4.12, 2.1, "navy", font_size=9)
    add_takeaway(slide, spec["takeaway"])
    add_notes(slide, spec["script"])
    add_footer(slide, number)


def render_two_column(prs, number, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide)
    add_headline(slide, spec["title"], spec.get("label", "Technical Core"))
    add_card(slide, 0.86, 1.72, 5.78, 3.78, spec.get("left_fill", "white"), line_name=spec.get("left_line", "navy"))
    add_card(slide, 6.95, 1.72, 5.64, 3.78, spec.get("right_fill", "teal_soft"), line_name=spec.get("right_line", "teal"))
    add_text_box(slide, 1.15, 1.98, 5.18, 0.35, [{"text": spec["left_title"], "size": 18, "bold": True, "color": "navy"}], margin=0.0)
    add_text_box(slide, 7.23, 1.98, 5.08, 0.35, [{"text": spec["right_title"], "size": 18, "bold": True, "color": "navy"}], margin=0.0)
    add_text_box(slide, 1.14, 2.55, 5.1, 2.25, bullet_paragraphs(spec["left"], size=15), margin=0.0)
    add_text_box(slide, 7.22, 2.55, 5.05, 2.25, bullet_paragraphs(spec["right"], size=15), margin=0.0)
    if spec.get("chip"):
        add_chip(slide, spec["chip"], 4.35, 5.42, 4.6, "gold", font_size=10)
    add_takeaway(slide, spec["takeaway"], fill_name=spec.get("takeaway_fill", "gold_soft"))
    add_notes(slide, spec["script"])
    add_footer(slide, number)


def render_pipeline(prs, number, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide)
    add_headline(slide, spec["title"], "Pipeline")
    for idx, node in enumerate(spec["nodes"]):
        left = 0.78 + idx * 2.45
        add_card(slide, left, 2.35, 1.78, 1.08, node["fill"], line_name=node["line"])
        add_text_box(slide, left + 0.13, 2.68, 1.52, 0.28, [{"text": node["name"], "size": 13, "bold": True, "color": "navy", "align": PP_ALIGN.CENTER}], margin=0.0, vertical_anchor=MSO_ANCHOR.MIDDLE)
        if idx < len(spec["nodes"]) - 1:
            add_text_box(slide, left + 1.88, 2.72, 0.42, 0.2, [{"text": "->", "size": 18, "bold": True, "color": "teal", "align": PP_ALIGN.CENTER}], margin=0.0)
    add_card(slide, 1.06, 4.35, 11.0, 0.8, "white", line_name="navy")
    add_text_box(slide, 1.33, 4.58, 10.45, 0.24, [{"text": spec["detail"], "size": 15, "bold": True, "color": "ink", "align": PP_ALIGN.CENTER}], margin=0.0)
    add_takeaway(slide, spec["takeaway"])
    add_notes(slide, spec["script"])
    add_footer(slide, number)


def render_code(prs, number, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide)
    add_headline(slide, spec["title"], spec.get("label", "Pseudocode"))
    add_card(slide, 0.9, 1.72, 7.2, 3.96, "blue_soft", line_name="navy", rounded=False)
    add_text_box(slide, 1.12, 1.98, 6.72, 3.42, [{"text": spec["code"], "size": spec.get("code_size", 14), "font": MONO_FONT, "color": "ink", "space_after": 0}], margin=0.0)
    add_card(slide, 8.46, 1.72, 3.98, 3.96, "white", line_name="teal")
    add_text_box(slide, 8.74, 2.0, 3.42, 0.34, [{"text": spec["side_title"], "size": 17, "bold": True, "color": "navy"}], margin=0.0)
    add_text_box(slide, 8.72, 2.55, 3.45, 2.0, bullet_paragraphs(spec["side"], size=14), margin=0.0)
    add_takeaway(slide, spec["takeaway"])
    add_notes(slide, spec["script"])
    add_footer(slide, number)


def render_metrics(prs, number, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide)
    add_headline(slide, spec["title"], "Evidence")
    for idx, metric in enumerate(spec["metrics"]):
        left = 0.92 + idx * 3.9
        add_card(slide, left, 2.08, 3.34, 1.62, metric["fill"], line_name=metric["line"])
        add_text_box(slide, left + 0.18, 2.36, 2.98, 0.42, [{"text": metric["value"], "size": 24, "bold": True, "color": "navy", "align": PP_ALIGN.CENTER}], margin=0.0)
        add_text_box(slide, left + 0.24, 3.04, 2.86, 0.28, [{"text": metric["label"], "size": 12, "color": "ink", "align": PP_ALIGN.CENTER}], margin=0.0)
    add_card(slide, 1.0, 4.35, 11.1, 0.8, "white", line_name="navy")
    add_text_box(slide, 1.28, 4.58, 10.55, 0.24, [{"text": spec["detail"], "size": 15, "bold": True, "color": "ink", "align": PP_ALIGN.CENTER}], margin=0.0)
    add_takeaway(slide, spec["takeaway"])
    add_notes(slide, spec["script"])
    add_footer(slide, number)


def render_close(prs, number, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = NAVY
    bar = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, SLIDE_WIDTH, Inches(0.2))
    bar.fill.solid()
    bar.fill.fore_color.rgb = GOLD
    bar.line.fill.background()
    add_text_box(slide, 0.78, 1.05, 11.2, 0.8, [{"text": spec["title"], "size": 33, "bold": True, "color": "white"}], margin=0.0)
    add_text_box(slide, 0.82, 2.2, 10.6, 0.8, [{"text": spec["claim"], "size": 21, "bold": True, "color": "gold_soft"}], margin=0.0)
    for idx, chip in enumerate(spec["chips"]):
        add_chip(slide, chip, 1.0 + idx * 3.95, 4.25, 3.35, "white", text_name="navy", font_size=11)
    add_text_box(slide, 0.82, 6.08, 3.0, 0.3, [{"text": "Thank you.", "size": 18, "bold": True, "color": "white"}], margin=0.0)
    add_notes(slide, spec["script"])
    add_footer(slide, number)


def build_slides() -> list[dict]:
    slides = [
        {
            "layout": "title",
            "title": "Exact Loop-Level Parallelization in Maple",
            "subtitle": "April peer presentation, rebuilt with Adam's technical walkthrough structure",
            "claim": "Integer feasibility is the decision layer.",
            "script": "This is a fresh April version of the talk. I am using Adam's presentation as the model for structure rather than content: start with context, introduce the representation, walk through the algorithm, then show evidence and limits. The content here is my Maple thesis work. The contribution is a command, IsParallelizable, that keeps Maple's existing loop-analysis front end but changes the final loop-level decision so it is based on integer feasibility instead of rational over-approximation alone.",
        },
        {
            "layout": "roadmap",
            "title": "The talk follows a technical walkthrough",
            "steps": [
                {"name": "Setup", "detail": "What dependence analysis must decide for loop nests.", "tag": "problem", "fill": "white", "line": "navy"},
                {"name": "Model", "detail": "How Maple represents loops, accesses, and constraints.", "tag": "representation", "fill": "teal_soft", "line": "teal"},
                {"name": "Algorithm", "detail": "How IsParallelizable tests one loop level at a time.", "tag": "decision", "fill": "white", "line": "navy"},
                {"name": "Evidence", "detail": "Where integer reasoning improves the rational baseline.", "tag": "validation", "fill": "gold_soft", "line": "gold"},
            ],
            "takeaway": "Adam's structure keeps the talk grounded: model first, algorithm second, evidence last.",
            "script": "The structure is deliberately close to Adam's rhythm. I first give the high-level setup, then the data representation, then the algorithmic walkthrough, and only then the performance-style evidence and limitations. The difference is the content. Instead of hypergraph transversals, the object here is dependence analysis for Maple loop nests and the exact question of which loop levels can be safely parallelized.",
        },
        {
            "layout": "two_column",
            "title": "The parallelization question is level-specific",
            "label": "Setup",
            "left_title": "What Maple already knows",
            "right_title": "What the thesis decides",
            "left": ["The loop nest has legal integer iterations.", "Array references identify which memory cells are read or written.", "DependenceCone summarizes possible dependences over rational space."],
            "right": ["A loop level is blocked only by a real integer witness.", "The first different index must occur at that level.", "The answer should be safe variables, not only a cone summary."],
            "chip": "From dependence summary to loop-level decision",
            "takeaway": "The thesis contribution is the last decision step, not a replacement front end.",
            "script": "The core issue is that loop parallelization is not just asking whether some dependence exists. It is asking whether a specific loop level is blocked by an actual pair of iterations. Maple already has the front half of the analysis: it can normalize a loop, describe the legal iteration space, and collect array references. The thesis adds the exact decision layer that asks whether a blocking witness exists in integer iteration space for the level under test.",
        },
        {
            "layout": "two_column",
            "title": "Marc's dependence definition gives the test shape",
            "label": "Definition",
            "left_title": "Dependence ingredients",
            "right_title": "Constraint ingredients",
            "left": ["Two statement instances touch the same memory location.", "At least one side writes.", "There is a legal execution path from source to target."],
            "right": ["Source legality constraints.", "Target legality constraints.", "Equal-access equations plus the level blocker."],
            "chip": "Same-memory + one write + legal order",
            "takeaway": "The slide-level definition becomes a concrete integer feasibility query.",
            "script": "Marc's formal dependence definition is the bridge into the algorithm. A data dependence needs same memory, at least one write, and a legal execution path. In the implementation, those become source legality, target legality, equal-access equations, and a condition that fixes where the first loop-index difference occurs. This is why the talk can stay technical without drifting into implementation detail too early.",
        },
        {
            "layout": "pipeline",
            "title": "Maple supplies the front half of the analysis",
            "nodes": [
                {"name": "procedure", "fill": "white", "line": "navy"},
                {"name": "CreateLoop", "fill": "teal_soft", "line": "teal"},
                {"name": "ForLoop", "fill": "white", "line": "navy"},
                {"name": "IterationSpace", "fill": "teal_soft", "line": "teal"},
                {"name": "ArrayReferences", "fill": "white", "line": "navy"},
            ],
            "detail": "IsParallelizable reuses this pipeline and adds the exact integer decision layer after it.",
            "takeaway": "The command extends Maple's existing representation rather than inventing a new one.",
            "script": "This is the representation slide in Adam's sense: what data structures are actually being passed around. Maple normalizes a procedure into a ForLoop object. From there, IterationSpace gives the affine legality conditions, and ArrayReferences gives the reads and writes. IsParallelizable is intentionally conservative about scope: it uses these existing objects and focuses on the final question of whether an integer blocking witness exists for each loop level.",
        },
        {
            "layout": "two_column",
            "title": "The model is a two-iteration system",
            "label": "Model",
            "left_title": "Variables",
            "right_title": "Families of constraints",
            "left": ["Source loop indices.", "Target loop indices.", "Distance variables where useful.", "Initialization parameters after substitution."],
            "right": ["Both iterations must be legal.", "The accesses must address the same cell.", "The source-target order must be legal.", "The selected level must be the first blocker."],
            "chip": "One pair, one level, one feasibility query",
            "takeaway": "Every decision is reduced to whether this system has an integer point.",
            "script": "For one source-target reference pair and one loop level, the command builds a two-iteration system. One copy of the loop variables describes the source instance, another describes the target instance, and the constraints force both to be legal and to touch the same memory cell. The level-specific blocker then says that this is the first loop level where the target is ordered after the source in a way that prevents parallel execution.",
        },
        {
            "layout": "code",
            "title": "Decision rule for one loop level",
            "code": "for level in loop_levels:\n    blocked = false\n    for source, target in relevant_access_pairs:\n        system = legality(source) + legality(target)\n        system += same_memory(source, target)\n        system += first_difference_at(level)\n        if has_integer_point(system):\n            blocked = true\n            break\n    report level as safe iff not blocked",
            "side_title": "Important boundary",
            "side": ["The query is existential.", "One real witness blocks the level.", "No integer witness means this pair does not block it."],
            "takeaway": "The criterion is exact for the affine integer system being tested.",
            "script": "This is the core algorithm in compact form. For each loop level, the command checks every relevant source-target access pair. It builds the legality constraints, the equal-access constraints, and the first-difference condition for the level. Then it asks a single yes-or-no question: does this system have an integer point? If yes, that loop level is blocked by a real execution witness. If no pair produces a witness, the level is reported safe.",
        },
        {
            "layout": "two_column",
            "title": "Reference pairs are filtered before solving",
            "label": "Implementation",
            "left_title": "Pairs that matter",
            "right_title": "Pairs that do not matter",
            "left": ["Read/write pairs.", "Write/read pairs.", "Write/write pairs.", "Pairs inside the affine loop scope."],
            "right": ["Read/read pairs do not create dependence.", "Unsupported nonlinear forms stay outside the claim.", "Cases outside the validated surface are not oversold."],
            "chip": "Keep the solver work tied to dependence semantics",
            "takeaway": "The command is precise because it asks the right smaller set of questions.",
            "script": "Before the backend query, the implementation keeps only access pairs that can create a dependence. A read-read pair is not a dependence because neither side writes. The command also keeps the claim inside the supported affine loop surface. That scope control matters for the talk: the result is not that every Maple program is now solved, but that this class of loop-level dependence decisions is handled exactly over integer iteration space.",
        },
        {
            "layout": "pipeline",
            "title": "ZPolyhedralSets is the integer backend",
            "nodes": [
                {"name": "constraints", "fill": "white", "line": "navy"},
                {"name": "normalize", "fill": "teal_soft", "line": "teal"},
                {"name": "ZPolyhedralSet", "fill": "white", "line": "navy"},
                {"name": "IntegerPoint", "fill": "teal_soft", "line": "teal"},
                {"name": "safe?", "fill": "gold_soft", "line": "gold"},
            ],
            "detail": "The semantic domain is integer loop iterations, so the backend must answer integer-point existence.",
            "takeaway": "The backend matches the mathematics of loop execution.",
            "script": "Marc specifically asked for the role of ZPolyhedralSets, and this is the cleanest way to present it. Loop iterations are integer points. The blocker system is a system of affine constraints over those integer variables. So Maple builds a ZPolyhedralSet and asks whether any integer point remains. The command is not inventing a solver; it is connecting Maple's loop-analysis representation to the backend whose domain matches the question.",
        },
        {
            "layout": "two_column",
            "title": "DependenceCone is useful but rational",
            "label": "Comparison",
            "left_title": "Rational summary",
            "right_title": "Integer decision",
            "left": ["Summarizes possible dependence distances.", "Can preserve fractional witnesses.", "Good for broad dependence information."],
            "right": ["Asks whether real iteration pairs exist.", "Rejects fractional artifacts.", "Returns loop variables that are safe to parallelize."],
            "chip": "The gap appears at the final decision step",
            "takeaway": "A rational witness is not automatically an executable loop witness.",
            "script": "This is the main contrast. DependenceCone is useful, but its output is rational. That is appropriate for a cone summary, but it is not the same thing as proving that a real pair of integer loop iterations blocks a level. In the parity-style cases, the rational analysis can keep a fractional distance that cannot be an actual iteration distance. IsParallelizable resolves that final question by checking the integer system.",
        },
        {
            "layout": "code",
            "title": "The parity mechanism explains the improvement",
            "label": "Mechanism",
            "code": "rational projection:\n    distance = 3/2\n    looks like a blocker\n\ninteger feasibility:\n    source index, target index in Z\n    target - source = 3/2\n    no integer solution\n\nresult:\n    rational blocker is rejected",
            "code_size": 15,
            "side_title": "What changes",
            "side": ["The same constraints are interpreted over integers.", "The false blocker disappears.", "The loop-level answer becomes less pessimistic."],
            "takeaway": "The thesis novelty is rejecting blockers that no execution can realize.",
            "script": "The parity case is the simplest way to explain why the backend matters. A rational projection can preserve a distance like three halves. As a rational object, that is perfectly legal. As a loop distance between two integer iterations, it is impossible. When the integer feasibility query is empty, the command rejects the blocker. That is the strict improvement over treating the rational summary as the final answer.",
        },
        {
            "layout": "two_column",
            "title": "Worked example: heat_eq starts from Maple objects",
            "label": "Example",
            "left_title": "Input surface",
            "right_title": "Analysis surface",
            "left": ["A concrete loop nest normalized by Maple.", "Array accesses extracted from the ForLoop.", "Affine legality constraints from IterationSpace."],
            "right": ["Reference pairs are checked one by one.", "Outer and inner loop levels are tested separately.", "Outputs are compared against the validated bundle."],
            "chip": "Example first, general claim second",
            "takeaway": "The example shows the whole pipeline rather than only the final answer.",
            "script": "For the worked example, the current defense deck uses heat_eq because it walks through the full pipeline. The point of the slide is not only the final safe loop variable. It is that Maple starts from the same ForLoop representation, extracts accesses, builds the pairwise systems, and then makes a separate decision for each loop level. That makes the implementation easier to defend because the example lines up with the algorithm.",
        },
        {
            "layout": "two_column",
            "title": "The blocker is level-specific in heat_eq",
            "label": "Walkthrough",
            "left_title": "Outer level",
            "right_title": "Inner level",
            "left": ["The blocker system can contain a real integer witness.", "That witness prevents parallel execution at the tested level.", "The level is reported blocked."],
            "right": ["The corresponding integer witness may be absent.", "A rational summary alone can be too coarse.", "The level can remain safe."],
            "chip": "Same loop nest, different level decision",
            "takeaway": "Parallelizability is a per-level property, not a single global label.",
            "script": "The key teaching point in heat_eq is that loop levels must be tested separately. One level can be blocked because there is a real source-target pair that creates a dependence witness. Another level can be safe because no such integer witness exists under the first-difference condition for that level. This is why the command returns safe variables rather than only saying whether the loop nest has any dependence at all.",
        },
        {
            "layout": "code",
            "title": "What IsParallelizable returns",
            "label": "Interface",
            "code": "IsParallelizable(loop_or_procedure)\n\ninput:\n    ForLoop object, or procedure normalized by CreateLoop\n\noutput:\n    safe loop variables from outermost to innermost\n\nmeaning:\n    listed levels have no integer blocking witness\n    inside the supported affine analysis surface",
            "side_title": "User-facing result",
            "side": ["The command is callable, not worksheet-only.", "It preserves Maple's existing objects.", "The output is directly about parallelization."],
            "takeaway": "The public interface exposes the exact decision, not backend machinery.",
            "script": "The user-facing part is intentionally simple. The command accepts either a ForLoop or a procedure that Maple can normalize through CreateLoop. It returns the loop variables that are safe, ordered from outermost to innermost. The backend details are important for the defense, but the command surface is about the practical question a Maple user asks: which loop levels can I parallelize?",
        },
        {
            "layout": "metrics",
            "title": "Validation stays tied to the frozen bundle",
            "metrics": [
                {"value": "23", "label": "frozen cases", "fill": "white", "line": "navy"},
                {"value": "PASS", "label": "dated rerun surface", "fill": "green_soft", "line": "green"},
                {"value": "0", "label": "validated cases where the rational baseline is less pessimistic", "fill": "gold_soft", "line": "gold"},
            ],
            "detail": "The evidence claim is bounded to the validated bundle and examples in the current technical defense.",
            "takeaway": "The deck should make a strong claim only where the evidence is frozen.",
            "script": "The evidence slide needs to be careful. The current technical defense ties the claim to a frozen 23-case bundle and a dated pass rerun. Within that surface, there is no validated case where DependenceCone is less pessimistic than IsParallelizable, and there are strict-improvement cases where integer reasoning rejects a false rational blocker. That is the claim the April deck should make, without turning it into an unsupported universal theorem.",
        },
        {
            "layout": "two_column",
            "title": "The strict-improvement cases are the headline evidence",
            "label": "Results",
            "left_title": "Agreement cases",
            "right_title": "Strict-improvement cases",
            "left": ["The command preserves standard dependence answers.", "Control cases stay blocked when real witnesses exist.", "The new layer does not erase real dependences."],
            "right": ["Bucket C cases expose rational pessimism.", "Fractional witnesses are rejected over integers.", "Safe loop levels become visible."],
            "chip": "Preserve correctness, remove false blockers",
            "takeaway": "The improvement is useful because it is bounded by control cases.",
            "script": "The evidence should be presented in two parts. First, agreement cases show that the command preserves standard answers and does not incorrectly remove real dependences. Second, the strict-improvement cases show where rational pessimism is too strong. This makes the result credible: the command is not simply more optimistic everywhere, it is more precise where the integer feasibility question rules out a false blocker.",
        },
        {
            "layout": "two_column",
            "title": "Optimizations and precision have tradeoffs",
            "label": "Lessons",
            "left_title": "What became clearer",
            "right_title": "What remains bounded",
            "left": ["Exactness belongs at the final decision point.", "Integer feasibility changes the answer only when the witness set is empty.", "Backend choice affects semantic precision."],
            "right": ["The current claim is affine.", "The current evidence is the frozen bundle.", "Unsupported program shapes need separate treatment."],
            "chip": "Adam-style lesson slide: what worked and why",
            "takeaway": "The talk should explain the boundary as part of the contribution.",
            "script": "Adam's talk included lessons about optimizations that did not always behave the same way across cases. The equivalent lesson here is about precision. Integer feasibility is the right semantic test for loop iterations, but the claim is still bounded by the supported affine surface and the validated examples. That boundary is not a weakness to hide. It is what keeps the technical claim defensible.",
        },
        {
            "layout": "two_column",
            "title": "Scope control keeps the claim defensible",
            "label": "Limits",
            "left_title": "Inside this deck",
            "right_title": "Outside this deck",
            "left": ["Affine loop bounds and affine array accesses.", "Maple ForLoop normalization.", "ZPolyhedralSets integer-point queries.", "Validated bundle examples."],
            "right": ["Nonlinear indexing claims.", "Arbitrary side effects.", "A universal theorem over all Maple programs.", "Performance claims beyond the available evidence."],
            "chip": "Precise does not mean unlimited",
            "takeaway": "The April version should be technically confident and scope-aware.",
            "script": "This slide prevents overclaiming. Inside the deck are affine loops, Maple's ForLoop representation, array-reference constraints, and ZPolyhedralSets integer feasibility. Outside the deck are nonlinear indexing, arbitrary side effects, and performance or correctness claims that have not been validated. That lets the presentation be strong without being brittle.",
        },
        {
            "layout": "two_column",
            "title": "Future work follows from the same architecture",
            "label": "Future Work",
            "left_title": "Short-term extensions",
            "right_title": "Longer-term direction",
            "left": ["Broaden the validated example bundle.", "Improve diagnostics for blocked levels.", "Add clearer traces for the generated witness systems."],
            "right": ["Handle more program shapes.", "Explore integration with broader Maple parallelization tools.", "Use exact feasibility as a reusable decision layer."],
            "chip": "Same pipeline, wider surface",
            "takeaway": "The architecture is useful because the exact decision layer is separable.",
            "script": "The future work follows naturally from the architecture. The front end can stay Maple's loop representation, and the exact integer decision can be improved independently. The near-term direction is better validation, clearer diagnostics, and better traces for why a level is blocked. The longer-term direction is expanding the supported program surface and connecting the command more directly to parallelization workflows.",
        },
        {
            "layout": "close",
            "title": "Closing claim",
            "claim": "IsParallelizable turns Maple's dependence information into an exact loop-level decision over integer iteration space.",
            "chips": ["Adam's structure", "Hardik's content", "Maple-ready final step"],
            "script": "The closing claim is deliberately compact. Maple already has useful dependence infrastructure. The thesis contribution is to turn that into an exact loop-level parallelization decision by asking the right integer feasibility question. For the April version, Adam's structure gives the talk a clear technical arc, but the content stays anchored in the current Maple technical defense and the frozen validation surface.",
        },
    ]
    timing_expansions = [
        "I would also say explicitly that this version is not trying to imitate Adam's topic. The useful thing from Adam is the discipline of explaining one technical object at a time. That means the audience should always know what role the current slide plays: representation, algorithm step, evidence, or limitation.",
        "This roadmap also sets expectations about depth. I am not going to race through every theorem and every implementation detail from the defense deck. Instead, I am choosing the same kind of paced technical story Adam used: enough background to make the algorithm meaningful, then one concrete path through the implementation, then evidence.",
        "This distinction is important because a dependence summary can be true and still not answer the question a programmer cares about. The programmer wants to know whether a specific loop index can run in parallel. That makes the unit of analysis a loop level, not the entire nest and not the whole dependence cone.",
        "I should keep this slide connected to Marc's lecture language. The formal definition is not decoration. It tells us exactly what the generated constraint system has to encode. If any of same memory, one write, or legal ordering is missing, then the solver is answering the wrong question.",
        "The reason to show the pipeline is to avoid making the thesis sound larger or vaguer than it is. Maple already has machinery for parsing and representing loop nests. The new work starts after that machinery has produced the objects needed to ask the exact loop-level question.",
        "In the talk I would slow down here and make the two copies of the loop variables concrete. One copy is the earlier or source execution instance and one copy is the later or target execution instance. The equal-access constraints tie them together by forcing the two array subscripts to name the same cell.",
        "This pseudocode is the center of the talk. The nested loops over levels and reference pairs are deliberately simple. The complexity is hidden in building the correct system and in asking the backend over integers. That simplicity is useful because it makes the correctness argument easier to explain.",
        "The filtering step also explains why the command is not just throwing every possible pair at a solver. It uses the dependence semantics first, then uses integer feasibility second. That order matters for performance and for clarity, because the backend query should only be asked for pairs that could actually change the answer.",
        "This is where I would connect the command back to Maple rather than presenting ZPolyhedralSets as a separate mathematical tool. The backend is already in the ecosystem, and the thesis uses it because loop iterations are integer points. That makes the integration feel natural instead of bolted on.",
        "The comparison should be respectful to DependenceCone. It is not wrong for doing its job. The point is that its job is a rational dependence summary, while IsParallelizable has a different job: a final safety decision for loop levels. The difference in domain is what creates the improvement.",
        "This mechanism is the cleanest explanation of the false-blocker issue. A fractional value can survive rational reasoning, but the loop program will never execute at a fractional iteration. Once the audience accepts that, the need for an integer backend becomes intuitive rather than merely formal.",
        "The example section should feel like Adam's algorithm walkthrough: we do not only state that the command works, we show how the input travels through the analysis. The audience sees the representation, the pairwise constraints, and the separate decisions, so the final output is earned.",
        "I would emphasize that the same loop nest can produce different answers at different levels. That is the practical reason for returning safe variables. A single yes-or-no answer for the whole nest would lose useful information, especially when an inner level remains parallelizable after an outer level is blocked.",
        "This interface slide keeps the result concrete. It tells the audience what they would call, what kind of input is accepted, and how to read the output. The implementation can be mathematically detailed, but the command has to land as a usable Maple feature.",
        "The validation slide should be delivered with restraint. The right claim is strong but bounded: on the frozen evidence surface, the integer method preserves validated answers and exposes strict improvements over rational pessimism. I should avoid implying that untested program classes have already been handled.",
        "The important balance is that strict improvement is not just optimism. The agreement and control cases show that real dependences remain real dependences. The improvement cases matter because they are paired with that control surface, so the story is precision rather than wishful parallelization.",
        "This lesson slide mirrors Adam's habit of explaining what the experiments taught, not only what the algorithm does. Here the lesson is that exactness belongs at the semantic boundary where Maple decides safety. Earlier rational summaries are useful, but they should not be forced to answer an integer execution question.",
        "The limits should stay visible because they protect the contribution. It is better to say clearly that the current deck covers affine loop nests and validated examples than to imply a broader result. That gives reviewers a precise target for technical criticism and keeps the final thesis claim defensible.",
        "The future-work slide should not introduce a new thesis. It should show that the current architecture has room to grow. Better diagnostics, broader examples, and more program shapes all build on the same separation between Maple's front-end representation and the exact integer decision layer.",
        "The closing should return to the three-part story: Adam supplied the presentation structure, the Maple defense supplied the content, and this fresh repo keeps the April work isolated until review. The final import back into Maple should happen only after the deck is reviewed and explicitly approved.",
    ]
    for slide, extra in zip(slides, timing_expansions):
        slide["script"] = f"{slide['script']} {extra}"
    delivery_notes = [
        "I will frame this as a reset from the previous direction: the deck is now about the thesis contribution, presented with a cleaner peer-talk structure.",
        "I will use this slide to promise the audience a path through the talk, so they know each later technical slide has a specific job.",
        "I will give a small verbal example here: two loop iterations can both exist, but only one level may be responsible for the ordering problem.",
        "I will say that this is why the implementation checks read-write, write-read, and write-write cases, rather than treating all pairs uniformly.",
        "I will pause on each pipeline box long enough to show that the command is reusing Maple's native analysis objects.",
        "I will describe the two-iteration system as a witness search: if the witness exists, the level is blocked; otherwise it is not blocked by that pair.",
        "I will walk through the pseudocode line by line, because this is the easiest place for the audience to verify the algorithmic shape.",
        "I will connect this filtering to both correctness and cost: it avoids irrelevant queries and keeps the evidence tied to dependence semantics.",
        "I will emphasize that the backend question is existence, not enumeration; the command only needs to know whether at least one integer point remains.",
        "I will avoid making DependenceCone sound like a failed tool. It is the right baseline, but not the final safety oracle.",
        "I will make the fractional-distance example slow and concrete, because it is the shortest route to the intuition behind the thesis.",
        "I will use heat_eq as the running example that turns the abstract constraint language into something visibly produced by Maple.",
        "I will stress that different levels can have different answers, which is why the command returns a set of safe variables.",
        "I will keep the interface slide practical and avoid exposing more backend notation than a Maple user needs to use the command.",
        "I will state the validation date and bundle idea as process evidence: this deck should be auditable, not just persuasive.",
        "I will say that strict improvement means fewer false blocks, not a willingness to ignore true dependence witnesses.",
        "I will use this slide to show what I learned from the April reset: the narrative must make the exact decision layer obvious.",
        "I will present the limits before questions, so scope concerns are answered by the deck itself rather than patched on afterward.",
        "I will keep future work tied to the existing architecture instead of proposing disconnected research directions.",
        "I will close by reminding the audience that the repo isolation is also part of the process: review first, Maple import later.",
    ]
    for slide, note in zip(slides, delivery_notes):
        slide["script"] = f"{slide['script']} {note}"
    return slides


def build_script_markdown(slides: list[dict]) -> str:
    counts = [len(re.findall(r"\b[\w:-]+\b", slide["script"])) for slide in slides]
    total_words = sum(counts)
    lines = [
        "# April Peer Presentation Script",
        "",
        f"Target rate: {WORDS_PER_MINUTE} wpm",
        f"Estimated words: {total_words}",
        f"Estimated time: {round(total_words / WORDS_PER_MINUTE, 1)} minutes",
        "",
    ]
    for idx, (slide, count) in enumerate(zip(slides, counts), start=1):
        lines.extend(
            [
                f"## Slide {idx}. {slide['title']}",
                f"Estimated words: {count}",
                f"Estimated time: {round(count / WORDS_PER_MINUTE * 60)} seconds",
                "",
                slide["script"],
                "",
            ]
        )
    return "\n".join(lines)


def render_slides(prs: Presentation, slides: list[dict]) -> None:
    renderers = {
        "title": render_title,
        "roadmap": render_roadmap,
        "two_column": render_two_column,
        "pipeline": render_pipeline,
        "code": render_code,
        "metrics": render_metrics,
        "close": render_close,
    }
    for number, slide in enumerate(slides, start=1):
        renderers[slide["layout"]](prs, number, slide)


def export_slide_pngs(pptx_path: Path, output_dir: Path) -> bool:
    output_dir.mkdir(parents=True, exist_ok=True)
    for old in output_dir.glob("Slide*.PNG"):
        old.unlink()
    ps = f"""
$ErrorActionPreference = 'Stop'
$ppt = Resolve-Path '{pptx_path}'
$out = '{output_dir}'
$pp = New-Object -ComObject PowerPoint.Application
$msoTrue = -1
$msoFalse = 0
$pres = $pp.Presentations.Open($ppt.Path, $msoTrue, $msoFalse, $msoFalse)
try {{
    $pres.Export($out, 'PNG', 1600, 900)
}} finally {{
    $pres.Close()
    $pp.Quit()
}}
"""
    try:
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps], check=True, cwd=ROOT)
        return True
    except Exception as exc:
        print(f"PNG_EXPORT_SKIPPED: {exc}")
        return False


def build_contact_sheet(slides_dir: Path, output_path: Path) -> bool:
    images = sorted(slides_dir.glob("Slide*.PNG"), key=lambda p: int(p.stem.replace("Slide", "")))
    if not images:
        return False
    thumbs = []
    for path in images:
        img = Image.open(path).convert("RGB")
        img.thumbnail((320, 180))
        canvas = Image.new("RGB", (340, 224), "white")
        canvas.paste(img, ((340 - img.width) // 2, 14))
        draw = ImageDraw.Draw(canvas)
        draw.text((14, 198), path.stem, fill=(30, 37, 46))
        thumbs.append(canvas)
    cols = 3
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 340, rows * 224), (248, 246, 239))
    for idx, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((idx % cols) * 340, (idx // cols) * 224))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path)
    return True


def write_review_docs(slides: list[dict], exported_pngs: bool, contact_sheet: bool) -> None:
    adam_screens = sorted(p.name for p in ADAM_DIR.glob("*.png"))
    mapping = [
        "# Adam Structure Mapping",
        "",
        "Adam is used for presentation architecture only. Hardik's Maple technical defense is the content source.",
        "",
        "| Adam-style role | April deck slides | Hardik content mapped into that role |",
        "| --- | --- | --- |",
        "| High-level setup | 1-4 | Dependence analysis problem, formal dependence definition, loop-level decision. |",
        "| Core representation/model | 5-6 | Maple ForLoop, IterationSpace, ArrayReferences, constraint families. |",
        "| Algorithm walkthrough | 7-9 | IsParallelizable pair/level loop and ZPolyhedralSets backend. |",
        "| Comparison and mechanism | 10-11 | DependenceCone rational baseline and integer feasibility improvement. |",
        "| Worked example | 12-14 | heat_eq and public command surface from the technical defense. |",
        "| Evidence | 15-16 | Frozen bundle, strict-improvement cases, control cases. |",
        "| Lessons, limits, future work | 17-20 | Scope boundaries, lessons, extensions, closing claim. |",
        "",
        f"Usable Adam screenshots copied: {len(adam_screens)}",
        "Excluded corrupt screenshot: `Screenshot 2026-04-17 094616.png`",
    ]
    STRUCTURE_MAP.write_text("\n".join(mapping), encoding="utf-8")

    total_words = sum(len(re.findall(r"\b[\w:-]+\b", slide["script"])) for slide in slides)
    estimated_time = total_words / WORDS_PER_MINUTE
    memo = [
        "# Review Memo",
        "",
        "## What changed",
        "",
        "- Created a fresh April peer deck outside the Maple repo.",
        "- Used Adam's work for structure, pacing, and slide rhythm only.",
        "- Used Hardik's current technical defense content as the authoritative Maple source.",
        "- Generated editable PowerPoint slides rather than screenshot-only slides.",
        "",
        "## Timing",
        "",
        f"- Slide count: {len(slides)}",
        f"- Script words: {total_words}",
        f"- Estimated speaking time at {WORDS_PER_MINUTE} wpm: {round(estimated_time, 1)} minutes",
        "",
        "## Generated artifacts",
        "",
        f"- PowerPoint: `{OUTPUT_PPTX}`",
        f"- Script: `{OUTPUT_SCRIPT}`",
        f"- PNG export: {'complete' if exported_pngs else 'skipped'}",
        f"- Contact sheet: {'complete' if contact_sheet else 'skipped'}",
        "",
        "## Boundary",
        "",
        "The Maple repo was not modified. Final import into Maple remains out of scope until explicit approval.",
    ]
    REVIEW_MEMO.write_text("\n".join(memo), encoding="utf-8")

    checklist = [
        "# Review Checklist",
        "",
        "- [x] Adam is used for structure, not content.",
        "- [x] Hardik's technical defense content is the authoritative substance.",
        "- [x] Omar's work is not used as deck basis.",
        "- [x] Adam's corrupt zero-byte screenshot is excluded.",
        "- [x] Slides are editable PowerPoint objects.",
        "- [x] Claims stay inside the validated Maple evidence described in the technical defense.",
        f"- [{'x' if 20 <= estimated_time <= 25 else ' '}] Talk fits roughly 20-25 minutes at normal speaking pace.",
        f"- [{'x' if exported_pngs else ' '}] Exported PNGs were generated.",
        f"- [{'x' if contact_sheet else ' '}] Contact sheet was generated for visual review.",
        "- [ ] Human review confirms slide readability and technical accuracy.",
        "- [ ] Human approval is given before importing final artifacts into Maple.",
    ]
    REVIEW_CHECKLIST.write_text("\n".join(checklist), encoding="utf-8")


def main() -> None:
    DECK_DIR.mkdir(exist_ok=True)
    REVIEW_DIR.mkdir(exist_ok=True)
    slides = build_slides()
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    render_slides(prs, slides)
    prs.save(OUTPUT_PPTX)
    OUTPUT_SCRIPT.write_text(build_script_markdown(slides), encoding="utf-8")
    exported = export_slide_pngs(OUTPUT_PPTX, PNG_DIR)
    contact = build_contact_sheet(PNG_DIR, CONTACT_SHEET)
    write_review_docs(slides, exported, contact)
    print(f"WROTE {OUTPUT_PPTX}")
    print(f"WROTE {OUTPUT_SCRIPT}")
    print(f"WROTE {STRUCTURE_MAP}")
    print(f"WROTE {REVIEW_MEMO}")
    print(f"WROTE {REVIEW_CHECKLIST}")
    print(f"WROTE {CONTACT_SHEET}" if contact else "CONTACT_SHEET_SKIPPED")


if __name__ == "__main__":
    main()
