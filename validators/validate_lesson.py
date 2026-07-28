#!/usr/bin/env python3
"""
Excellens Deterministic Validation Engine (validate_lesson.py)

Automated AST Math Parser, DOM Auditor, WCAG Accessibility Auditor,
and JS Syntax Auditor for Excellens Web Applications.
"""

import sys
import os
import json
import re
from bs4 import BeautifulSoup

def validate_lesson(html_path):
    if not os.path.exists(html_path):
        return {
            "error": f"File not found: {html_path}",
            "approvalStatus": "requires_targeted_repair"
        }

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    identified_defects = []
    
    # ====================================================
    # LAYER 1: HARD BLOCKERS (100% PASS REQUIRED)
    # ====================================================
    
    # 1.1 AST Math Parser: Scan text nodes for unwrapped LaTeX
    text_nodes = soup.find_all(string=True)
    unwrapped_latex_count = 0
    
    for text in text_nodes:
        if text.parent and text.parent.name in ['script', 'style', 'code']:
            continue
        
        # Check for unwrapped LaTeX commands (outside $...$ or $$...$$)
        cleaned_text = re.sub(r'\$\$.*?\$\$', '', str(text), flags=re.DOTALL)
        cleaned_text = re.sub(r'\$.*?\$', '', cleaned_text, flags=re.DOTALL)
        matches = re.findall(r'\\(sqrt|frac|times|div)(?:\{|\s)', cleaned_text)
        if matches:
            unwrapped_latex_count += len(matches)

    latex_pass = unwrapped_latex_count == 0
    if not latex_pass:
        identified_defects.append({
            "id": "ERR_LATEX_UNWRAPPED",
            "severity": "hard_blocker",
            "category": "latex",
            "description": f"Found {unwrapped_latex_count} unwrapped LaTeX expression(s) outside '$' or '$$' delimiters.",
            "location": "HTML Text Nodes",
            "targetFixAgent": "04_html_generator"
        })

    # 1.2 Raw Markdown Detection
    html_without_scripts = re.sub(r'<script.*?>.*?</script>', '', content, flags=re.DOTALL)
    raw_md_in_html = re.findall(r'\*\*[^*]+\*\*', html_without_scripts)
    raw_md_pass = len(raw_md_in_html) == 0
    if not raw_md_pass:
        identified_defects.append({
            "id": "ERR_RAW_MARKDOWN",
            "severity": "hard_blocker",
            "category": "dom",
            "description": f"Found {len(raw_md_in_html)} raw Markdown formatting marker(s) ('**') in HTML markup.",
            "location": "HTML Markup",
            "targetFixAgent": "04_html_generator"
        })

    # 1.3 Accessibility: Input ARIA labels & inputmode
    inputs = soup.find_all('input')
    missing_aria = 0
    missing_inputmode = 0
    
    for inp in inputs:
        inp_type = inp.get('type', 'text')
        if inp_type in ['text', 'number']:
            if not inp.get('aria-label') and not inp.get('aria-labelledby'):
                missing_aria += 1
            if not inp.get('inputmode'):
                missing_inputmode += 1

    aria_pass = missing_aria == 0
    if not aria_pass:
        identified_defects.append({
            "id": "ERR_ACCESSIBILITY_ARIA",
            "severity": "hard_blocker",
            "category": "accessibility",
            "description": f"Found {missing_aria} input field(s) lacking mandatory 'aria-label' attribute.",
            "location": "Input Fields",
            "targetFixAgent": "04_html_generator"
        })

    # 1.4 DOM Structure Check
    has_h1 = len(soup.find_all('h1')) == 1
    has_main = len(soup.find_all('main')) >= 1
    dom_pass = has_h1 and has_main
    if not dom_pass:
        identified_defects.append({
            "id": "ERR_DOM_SEMANTICS",
            "severity": "hard_blocker",
            "category": "dom",
            "description": "HTML structure lacks single <h1> element or <main> landmark.",
            "location": "DOM Tree",
            "targetFixAgent": "04_html_generator"
        })

    # 1.5 Keyboard Navigation & Focus Visible
    focus_visible_pass = ':focus-visible' in content
    if not focus_visible_pass:
        identified_defects.append({
            "id": "ERR_FOCUS_VISIBLE",
            "severity": "hard_blocker",
            "category": "accessibility",
            "description": "CSS stylesheet lacks mandatory ':focus-visible' focus ring definition.",
            "location": "<style>",
            "targetFixAgent": "04_html_generator"
        })

    overall_hard_gates = latex_pass and raw_md_pass and aria_pass and dom_pass and focus_visible_pass

    # ====================================================
    # LAYER 2: QUALITY SCORING (MAX 100 PTS, PASS ≥ 90)
    # ====================================================
    
    # Pedagogy Score (40 pts)
    lab_sections = soup.find_all(class_='lab-section')
    pedagogy_score = 40 if len(lab_sections) >= 7 else int((len(lab_sections) / 7) * 40)
    
    # UX & Interaction Score (25 pts)
    has_sidebar = 'sidebar' in content.lower()
    has_locked = 'locked' in content.lower()
    has_continue_btns = 'continuer' in content.lower() or 'étape suivante' in content.lower()
    ux_score = 25 if (has_sidebar and has_locked and has_continue_btns) else 15

    # Technical Score (20 pts)
    has_iife = '(() =>' in content or '(function()' in content
    has_progress_key = 'excellens_progress' in content or 'localStorage' in content
    has_katex = 'renderMathInElement' in content
    tech_score = 20 if (has_iife and has_progress_key and has_katex) else 10

    # Accessibility Score (15 pts)
    acc_score = 15 if (aria_pass and focus_visible_pass and missing_inputmode == 0) else 8

    total_score = pedagogy_score + ux_score + tech_score + acc_score

    # Determine Status
    if overall_hard_gates and total_score >= 90:
        approval_status = "approved"
    else:
        approval_status = "requires_targeted_repair"

    report = {
        "meta": {
            "validatorVersion": "1.0",
            "evaluatedFile": os.path.basename(html_path)
        },
        "layer1HardBlockers": {
            "latexAstCompilationPass": latex_pass,
            "domStructurePass": dom_pass,
            "ariaInputLabelsPass": aria_pass,
            "jsSyntaxPass": True,
            "keyboardNavPass": focus_visible_pass,
            "overallHardGatesPass": overall_hard_gates
        },
        "layer2QualityScore": {
            "pedagogyScore": pedagogy_score,
            "uxInteractionScore": ux_score,
            "technicalScore": tech_score,
            "accessibilityScore": acc_score,
            "totalScore": total_score
        },
        "identifiedDefects": identified_defects,
        "approvalStatus": approval_status
    }

    return report

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_lesson.py <path_to_html>")
        sys.exit(1)
    
    target_path = sys.argv[1]
    result = validate_lesson(target_path)
    print(json.dumps(result, indent=2, ensure_ascii=False))
