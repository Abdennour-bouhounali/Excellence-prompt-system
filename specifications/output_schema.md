# Excellens Output Schemas (`output_schema.md`)

This specification defines the strict JSON Schemas for all intermediate artifacts exchanged between compiler pipeline agents (`knowledge_graph.json`, `content_spec.json`, `experience_spec.json`, `design_decisions.json`, `quality_report.json`, `student_model.json`, `interaction_events.json`).

---

## 1. Global Artifact Metadata Schema Header

Every JSON artifact emitted in the Excellens pipeline MUST include this top-level header:

```json
{
  "meta": {
    "artifactVersion": "1.0",
    "pipelineVersion": "2026.07",
    "agentName": "01_learning_architect",
    "agentVersion": "1.0",
    "generatedAt": "2026-07-28T18:59:00Z",
    "topicSlug": "simplifier-racines-carrees",
    "title": "Simplifier l'écriture d'une racine carrée",
    "subject": "Mathematics",
    "targetGrade": ["3e"]
  }
}
```

---

## 2. `knowledge_graph.json` Schema (Emitted by `01_learning_architect.md`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ExcellensKnowledgeGraph",
  "type": "object",
  "properties": {
    "meta": { "type": "object" },
    "prerequisites": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "concept": { "type": "string" },
          "diagnosticQuestion": { "type": "string" },
          "options": { "type": "array", "items": { "type": "string" } },
          "correctAnswer": { "type": "string" },
          "remediationHint": { "type": "string" }
        },
        "required": ["id", "concept", "diagnosticQuestion", "correctAnswer"]
      }
    },
    "cognitiveFrictionPoints": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "obstacleDescription": { "type": "string" },
          "commonStudentMisconception": { "type": "string" },
          "rootCauseAnalysis": { "type": "string" }
        },
        "required": ["id", "obstacleDescription", "commonStudentMisconception"]
      }
    },
    "learningGoals": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "goal": { "type": "string" },
          "bloomTaxonomyLevel": { "type": "string", "enum": ["remember", "understand", "apply", "analyze", "evaluate"] }
        },
        "required": ["id", "goal", "bloomTaxonomyLevel"]
      }
    }
  },
  "required": ["meta", "prerequisites", "cognitiveFrictionPoints", "learningGoals"]
}
```

---

## 3. `content_spec.json` Schema (Emitted by `02_content_architect.md`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ExcellensContentSpec",
  "type": "object",
  "properties": {
    "meta": { "type": "object" },
    "difficultyProfile": {
      "type": "object",
      "properties": {
        "conceptualDifficulty": { "type": "integer", "minimum": 1, "maximum": 5 },
        "calculationDifficulty": { "type": "integer", "minimum": 1, "maximum": 5 },
        "abstractionLevel": { "type": "integer", "minimum": 1, "maximum": 5 },
        "prerequisiteLoad": { "type": "integer", "minimum": 1, "maximum": 5 }
      },
      "required": ["conceptualDifficulty", "calculationDifficulty", "abstractionLevel", "prerequisiteLoad"]
    },
    "stages": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "stageNumber": { "type": "integer" },
          "stageType": {
            "type": "string",
            "enum": [
              "activate_prior", "discovery", "formalization", 
              "guided_practice", "misconception_repair", "mastery", "reflection", "exam_test"
            ]
          },
          "title": { "type": "string" },
          "pedagogicalObjective": { "type": "string" },
          "narrativeText": { "type": "string" },
          "microRuleTakeaway": { "type": "string" },
          "workedExamples": { "type": "array" }
        },
        "required": ["id", "stageNumber", "stageType", "title", "pedagogicalObjective"]
      }
    },
    "exercises": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "taxonomyLevel": { "type": "integer", "minimum": 1, "maximum": 5 },
          "levelName": { "type": "string", "enum": ["Recognition", "Transformation", "Multi-Step Application", "Brevet Standard", "Transfer"] },
          "skillTarget": { "type": "string" },
          "cognitiveOperation": { "type": "string" },
          "commonErrorTarget": { "type": "string" },
          "questionText": { "type": "string" },
          "expectedAnswerSchema": {
            "type": "object",
            "properties": {
              "type": { "type": "string", "enum": ["qcm", "atomic_components", "numeric_input"] },
              "components": { "type": "array", "items": { "type": "string" } },
              "targetValues": { "type": "object" }
            },
            "required": ["type"]
          },
          "hintStrategy": { "type": "array", "items": { "type": "string" } },
          "masteryRequirement": { "type": "integer" }
        },
        "required": ["id", "taxonomyLevel", "levelName", "skillTarget", "questionText", "expectedAnswerSchema"]
      }
    }
  },
  "required": ["meta", "difficultyProfile", "stages", "exercises"]
}
```

---

## 4. `experience_spec.json` & `design_decisions.json` Schema (Emitted by `03_experience_architect.md`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ExcellensExperienceSpec",
  "type": "object",
  "properties": {
    "meta": { "type": "object" },
    "mentalModelMapping": {
      "type": "object",
      "properties": {
        "modelKind": { "type": "string" },
        "rationale": { "type": "string" },
        "visualRepresentationType": { "type": "string" }
      },
      "required": ["modelKind", "rationale", "visualRepresentationType"]
    },
    "selectedEngines": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "stageId": { "type": "string" },
          "engineKind": { "type": "string", "enum": ["visualization_engine", "algebra_manipulation_engine", "proof_simulation_engine", "exam_engine"] },
          "implementationPattern": { "type": "string", "enum": ["svg", "canvas", "dom_slider", "input_grid"] },
          "rationale": { "type": "string" }
        },
        "required": ["stageId", "engineKind", "implementationPattern", "rationale"]
      }
    },
    "layoutStrategy": {
      "type": "object",
      "properties": {
        "sidebarType": { "type": "string", "enum": ["sticky_bounded"] },
        "topbarComponents": { "type": "array", "items": { "type": "string" } },
        "responsiveBreakpoints": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["sidebarType", "topbarComponents"]
    }
  },
  "required": ["meta", "mentalModelMapping", "selectedEngines", "layoutStrategy"]
}
```

---

## 5. `quality_report.json` Schema (Emitted by `05_quality_engineer.md`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ExcellensQualityReport",
  "type": "object",
  "properties": {
    "meta": { "type": "object" },
    "layer1HardBlockers": {
      "type": "object",
      "properties": {
        "latexAstCompilationPass": { "type": "boolean" },
        "domStructurePass": { "type": "boolean" },
        "ariaInputLabelsPass": { "type": "boolean" },
        "jsSyntaxPass": { "type": "boolean" },
        "keyboardNavPass": { "type": "boolean" },
        "overallHardGatesPass": { "type": "boolean" }
      },
      "required": ["latexAstCompilationPass", "domStructurePass", "ariaInputLabelsPass", "jsSyntaxPass", "keyboardNavPass", "overallHardGatesPass"]
    },
    "layer2QualityScore": {
      "type": "object",
      "properties": {
        "pedagogyScore": { "type": "integer", "minimum": 0, "maximum": 40 },
        "uxInteractionScore": { "type": "integer", "minimum": 0, "maximum": 25 },
        "technicalScore": { "type": "integer", "minimum": 0, "maximum": 20 },
        "accessibilityScore": { "type": "integer", "minimum": 0, "maximum": 15 },
        "totalScore": { "type": "integer", "minimum": 0, "maximum": 100 }
      },
      "required": ["pedagogyScore", "uxInteractionScore", "technicalScore", "accessibilityScore", "totalScore"]
    },
    "identifiedDefects": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "severity": { "type": "string", "enum": ["hard_blocker", "major_quality", "minor"] },
          "category": { "type": "string", "enum": ["latex", "dom", "accessibility", "pedagogy", "ux", "javascript"] },
          "description": { "type": "string" },
          "location": { "type": "string" },
          "targetFixAgent": { "type": "string", "enum": ["04_html_generator", "02_content_architect", "01_learning_architect"] }
        },
        "required": ["id", "severity", "category", "description", "targetFixAgent"]
      }
    },
    "approvalStatus": { "type": "string", "enum": ["approved", "requires_targeted_repair", "human_review_required"] }
  },
  "required": ["meta", "layer1HardBlockers", "layer2QualityScore", "identifiedDefects", "approvalStatus"]
}
```

---

## 6. `student_model.json` & `interaction_events.json` Telemetry Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ExcellensStudentTelemetry",
  "type": "object",
  "properties": {
    "studentId": { "type": "string" },
    "lessonId": { "type": "string" },
    "skillsMastery": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "masteryScore": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
          "attemptsCount": { "type": "integer" },
          "identifiedMisconceptions": { "type": "array", "items": { "type": "string" } },
          "lastAttemptedAt": { "type": "string" }
        }
      }
    },
    "interactionEvents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "eventId": { "type": "string" },
          "eventType": { "type": "string", "enum": ["stage_unlocked", "exercise_attempted", "exercise_failed", "hint_requested", "feynman_submitted"] },
          "stageId": { "type": "string" },
          "timestamp": { "type": "string" },
          "payload": { "type": "object" }
        },
        "required": ["eventId", "eventType", "timestamp"]
      }
    }
  },
  "required": ["studentId", "lessonId", "skillsMastery", "interactionEvents"]
}
```
