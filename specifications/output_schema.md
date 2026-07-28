# Excellens Output Schemas (`output_schema.md`)

This specification defines the JSON Schemas for all intermediate artifacts exchanged between pipeline prompts (`lesson_spec.json`, `design_decisions.json`, `review_report.json`).

---

## 1. `lesson_spec.json` Schema (Produced by `01_lesson_designer.md`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ExcellensLessonSpecification",
  "type": "OBJECT",
  "properties": {
    "meta": {
      "type": "OBJECT",
      "properties": {
        "topicSlug": { "type": "STRING" },
        "title": { "type": "STRING" },
        "subtitle": { "type": "STRING" },
        "subject": { "type": "STRING" },
        "targetGrade": { "type": "ARRAY", "items": { "type": "STRING" } },
        "estimatedDurationMinutes": { "type": "INTEGER" },
        "totalPossibleXP": { "type": "INTEGER" }
      },
      "required": ["topicSlug", "title", "subject", "targetGrade"]
    },
    "prerequisites": {
      "type": "ARRAY",
      "items": {
        "type": "OBJECT",
        "properties": {
          "id": { "type": "STRING" },
          "question": { "type": "STRING" },
          "options": { "type": "ARRAY", "items": { "type": "STRING" } },
          "correctAnswer": { "type": "STRING" },
          "remediationHint": { "type": "STRING" }
        }
      }
    },
    "stages": {
      "type": "ARRAY",
      "items": {
        "type": "OBJECT",
        "properties": {
          "id": { "type": "STRING" },
          "number": { "type": "INTEGER" },
          "title": { "type": "STRING" },
          "phaseType": { 
            "type": "STRING",
            "enum": [
              "curiosity", "discovery", "intuition", "dual_coding", 
              "formalization", "guided_practice", "autonomous_practice", 
              "mastery", "revision_express", "error_notebook", 
              "feynman", "timed_exam"
            ]
          },
          "pedagogicalGoal": { "type": "STRING" },
          "representationIntent": {
            "type": "OBJECT",
            "properties": {
              "modelType": { "type": "STRING" },
              "reasoning": { "type": "STRING" }
            }
          },
          "content": { "type": "OBJECT" }
        },
        "required": ["id", "number", "title", "phaseType", "pedagogicalGoal"]
      }
    },
    "examConfig": {
      "type": "OBJECT",
      "properties": {
        "timeLimitSeconds": { "type": "INTEGER" },
        "questionCount": { "type": "INTEGER" },
        "questions": { "type": "ARRAY", "items": { "type": "OBJECT" } }
      }
    }
  },
  "required": ["meta", "stages"]
}
```

---

## 2. `design_decisions.json` Schema (Produced by `02_html_generator.md`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ExcellensDesignDecisions",
  "type": "OBJECT",
  "properties": {
    "layoutStrategy": {
      "type": "OBJECT",
      "properties": {
        "sidebarType": { "type": "STRING" },
        "topbarComponents": { "type": "ARRAY", "items": { "type": "STRING" } },
        "reasoning": { "type": "STRING" }
      }
    },
    "interactiveEngines": {
      "type": "ARRAY",
      "items": {
        "type": "OBJECT",
        "properties": {
          "stageId": { "type": "STRING" },
          "engineKind": { "type": "STRING" },
          "implementationType": { "type": "STRING", "enum": ["svg", "canvas", "dom_slider", "input_grid"] },
          "rationale": { "type": "STRING" }
        }
      }
    },
    "accessibilityPlan": {
      "type": "OBJECT",
      "properties": {
        "ariaLiveRegions": { "type": "ARRAY", "items": { "type": "STRING" } },
        "focusManagement": { "type": "STRING" }
      }
    }
  },
  "required": ["layoutStrategy", "interactiveEngines"]
}
```

---

## 3. `review_report.json` Schema (Produced by `03_reviewer.md`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ExcellensReviewReport",
  "type": "OBJECT",
  "properties": {
    "pedagogicalFidelityScore": { "type": "INTEGER", "minimum": 0, "maximum": 100 },
    "wcagComplianceScore": { "type": "INTEGER", "minimum": 0, "maximum": 100 },
    "codeQualityScore": { "type": "INTEGER", "minimum": 0, "maximum": 100 },
    "identifiedIssues": {
      "type": "ARRAY",
      "items": {
        "type": "OBJECT",
        "properties": {
          "category": { "type": "STRING", "enum": ["pedagogy", "ux", "accessibility", "javascript", "css", "performance", "latex"] },
          "severity": { "type": "STRING", "enum": ["critical", "major", "minor"] },
          "description": { "type": "STRING" },
          "location": { "type": "STRING" },
          "remediationAction": { "type": "STRING" }
        },
        "required": ["category", "severity", "description", "remediationAction"]
      }
    },
    "approvalStatus": { "type": "STRING", "enum": ["approved_with_fixes", "requires_reconsideration"] }
  },
  "required": ["pedagogicalFidelityScore", "wcagComplianceScore", "codeQualityScore", "identifiedIssues", "approvalStatus"]
}
```
