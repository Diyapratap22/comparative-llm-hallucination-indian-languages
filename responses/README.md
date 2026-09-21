# Responses

Home for model responses collected during the experiment.

## `raw_responses/`

Planned layout (subject to change once the pipeline is implemented):

```
responses/raw_responses/
├── {run_id}__manifest.json         # metadata for one experiment run
└── {run_id}/
    ├── {model_id}__{question_id}__en.json
    └── {model_id}__{question_id}__hi.json
```

Each response file records:

- **run metadata:** `run_id`, timestamp, experiment config snapshot;
- **prompt metadata:** `question_id`, `language`, full prompt text;
- **output:** the raw model response, unmodified;
- **decoding settings:** temperature, max tokens, etc. (exact fields TBD).

**Status: empty.** No API calls have been made and no responses exist.

## Rules

- Raw responses are saved **unmodified**; any post-processing happens later in
  the analysis step.
- Field names and schemas are preliminary and will be finalized and documented
  here once the model list and pipeline are implemented.