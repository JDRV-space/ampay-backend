# JSON Schema Design for Political Transparency / Legislative Data

**Research Date:** 2026-01-21
**Confidence Level:** High - Multiple authoritative sources (Popolo, Open Civic Data, Schema.org, OpenStates)

---

## TLDR

Use **Open Civic Data (OCD) standards** as foundation: OCD-IDs for entities, Popolo-based schemas for Person/Organization/Vote, ClaimReview for fact-checking. Design promise tracking as custom extension linking pledges to votes via foreign keys with full audit trails.

---

## 1. Existing Standards & Schemas

### 1.1 Popolo Project (International Legislative Standard)

**Source:** [popoloproject.com/specs](https://www.popoloproject.com/specs/) | [GitHub](https://github.com/popolo-project/popolo-spec)

The foundational standard for legislative data. Core entities:

| Entity | Purpose |
|--------|---------|
| Person | Legislators, officials |
| Organization | Parties, chambers, committees |
| Membership | Person-to-Organization relationships |
| Post | Elected positions |
| Motion | Proposals being voted on |
| VoteEvent | A single voting session |
| Vote | Individual vote cast |
| Area | Geographic/political divisions |

**Key Design Decisions:**
- Uses `snake_case` (not camelCase)
- JSON Schema draft v3 validation
- All entities require `created_at`, `updated_at`, `sources[]`

### 1.2 Open Civic Data (OCD) - US Legislative Standard

**Source:** [open-civic-data.readthedocs.io](https://open-civic-data.readthedocs.io/en/latest/ocdids.html)

Extends Popolo with US-specific conventions. Used by OpenStates (all 50 US states).

**OCD-ID Format:**
```
ocd-{type}/{hierarchical-path}

Examples:
ocd-division/country:us/state:oh/place:cleveland/ward:3
ocd-jurisdiction/country:us/state:ex/place:example/legislature
ocd-person/ebaff054-05df-11e3-a53b-f0def1bd7298
```

**ID Design Pattern:**
- Divisions: Hierarchical, human-readable paths
- Persons/Orgs: UUID-based (uuid1) for uniqueness
- Prefix indicates entity type

### 1.3 OpenStates API Schema

**Source:** [docs.openstates.org/api-v3](https://docs.openstates.org/api-v3/) | [Data Types](https://docs.openstates.org/api-v2/types/)

Production-tested schema for US legislative data (11+ years).

**Person Schema:**
```json
{
  "id": "ocd-person/ebaff054-05df-11e3-a53b-f0def1bd7298",
  "name": "Jane Smith",
  "familyName": "Smith",
  "givenName": "Jane",
  "birthDate": "1975-03-15",
  "image": "https://example.com/photos/jane-smith.jpg",
  "currentMemberships": [
    {
      "organization": {"id": "ocd-organization/...", "name": "State Senate"},
      "role": "Senator",
      "district": "District 5",
      "startDate": "2023-01-01"
    }
  ],
  "contactDetails": [
    {"type": "email", "value": "jane.smith@senate.gov"},
    {"type": "phone", "value": "+1-555-0100"}
  ],
  "sources": [{"url": "https://senate.gov/members/jane-smith"}],
  "createdAt": "2023-01-15T10:30:00Z",
  "updatedAt": "2025-11-20T14:22:00Z"
}
```

**Bill Schema:**
```json
{
  "id": "ocd-bill/abc123",
  "identifier": "HB 264",
  "title": "Education Reform Act",
  "legislativeSession": "2025-regular",
  "fromOrganization": {"id": "ocd-organization/...", "name": "House"},
  "classification": ["bill"],
  "subject": ["education", "funding"],
  "abstracts": [{"note": "Official Summary", "text": "..."}],
  "sponsorships": [
    {
      "name": "Jane Smith",
      "entityType": "person",
      "entityId": "ocd-person/...",
      "primary": true,
      "classification": "author"
    }
  ],
  "actions": [
    {
      "date": "2025-03-15",
      "description": "Introduced",
      "organization": {"name": "House"},
      "classification": ["introduction"]
    }
  ],
  "votes": ["ocd-vote/xyz789"],
  "sources": [{"url": "https://congress.gov/bill/..."}]
}
```

**Vote Schema:**
```json
{
  "id": "ocd-vote/xyz789",
  "identifier": "HV-2025-0342",
  "motionText": "Passage of HB 264",
  "motionClassification": ["passage"],
  "startDate": "2025-04-20",
  "result": "pass",
  "organization": {"id": "ocd-organization/...", "name": "House"},
  "counts": [
    {"option": "yes", "value": 58},
    {"option": "no", "value": 42},
    {"option": "absent", "value": 5}
  ],
  "votes": [
    {
      "voterName": "Jane Smith",
      "voterId": "ocd-person/...",
      "option": "yes"
    }
  ]
}
```

### 1.4 ClaimReview (Fact-Checking Standard)

**Source:** [schema.org/ClaimReview](https://schema.org/ClaimReview) | [Google Implementation](https://developers.google.com/search/docs/appearance/structured-data/factcheck)

W3C standard for fact-checking markup. Used by PolitiFact, Snopes, FactCheck.org.

```json
{
  "@context": "https://schema.org",
  "@type": "ClaimReview",
  "url": "https://factcheck.org/2025/04/promise-analysis-123",
  "datePublished": "2025-04-25",
  "claimReviewed": "I will reduce taxes by 20%",
  "itemReviewed": {
    "@type": "Claim",
    "author": {
      "@type": "Person",
      "name": "Senator Jane Smith"
    },
    "datePublished": "2024-10-15",
    "appearance": {
      "@type": "CreativeWork",
      "url": "https://campaign.example.com/promises"
    }
  },
  "author": {
    "@type": "Organization",
    "name": "FactCheck Peru",
    "url": "https://factcheck.pe"
  },
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": 2,
    "bestRating": 5,
    "worstRating": 1,
    "alternateName": "Partially True"
  }
}
```

---

## 2. Custom Schema: Promise Tracking System

No existing standard covers promise-to-vote linkage. Here's a designed schema:

### 2.1 Promise Entity

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^promise-[a-z]{2}-[0-9]{4}-[0-9]{4}$",
      "description": "Human-readable ID: promise-{country}-{year}-{sequence}",
      "examples": ["promise-pe-2024-0001"]
    },
    "uuid": {
      "type": "string",
      "format": "uuid",
      "description": "Internal UUID for database operations"
    },
    "politician_id": {
      "type": "string",
      "description": "OCD-ID of the politician who made the promise"
    },
    "party_id": {
      "type": "string",
      "description": "OCD-ID of the political party (at time of promise)"
    },
    "text": {
      "type": "object",
      "properties": {
        "es": {"type": "string", "description": "Spanish text"},
        "en": {"type": "string", "description": "English translation"},
        "original_language": {"type": "string", "enum": ["es", "en", "qu"]}
      },
      "required": ["es", "original_language"]
    },
    "category": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": [
          "economy", "education", "health", "security",
          "infrastructure", "environment", "corruption",
          "labor", "taxation", "foreign_policy", "social_programs"
        ]
      },
      "minItems": 1
    },
    "source": {
      "type": "object",
      "properties": {
        "url": {"type": "string", "format": "uri"},
        "type": {
          "type": "string",
          "enum": ["campaign_website", "debate", "interview", "speech", "document", "social_media"]
        },
        "date": {"type": "string", "format": "date"},
        "archived_url": {"type": "string", "format": "uri", "description": "Wayback Machine or similar"},
        "quote_context": {"type": "string", "description": "Surrounding text for context"}
      },
      "required": ["url", "type", "date"]
    },
    "status": {
      "type": "string",
      "enum": ["not_started", "in_progress", "fulfilled", "partially_fulfilled", "broken", "compromised", "stalled"]
    },
    "status_history": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "status": {"type": "string"},
          "changed_at": {"type": "string", "format": "date-time"},
          "changed_by": {"type": "string", "description": "Analyst ID"},
          "reason": {"type": "string"},
          "evidence_ids": {"type": "array", "items": {"type": "string"}}
        }
      }
    },
    "related_votes": {
      "type": "array",
      "items": {"type": "string", "description": "OCD vote IDs"},
      "description": "Votes that are relevant to this promise"
    },
    "related_bills": {
      "type": "array",
      "items": {"type": "string", "description": "OCD bill IDs"}
    },
    "audit": {
      "$ref": "#/$defs/audit_trail"
    }
  },
  "required": ["id", "uuid", "politician_id", "text", "category", "source", "status", "audit"],
  "$defs": {
    "audit_trail": {
      "type": "object",
      "properties": {
        "created_at": {"type": "string", "format": "date-time"},
        "created_by": {"type": "string"},
        "updated_at": {"type": "string", "format": "date-time"},
        "updated_by": {"type": "string"},
        "version": {"type": "integer", "minimum": 1},
        "sources": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "url": {"type": "string", "format": "uri"},
              "accessed_at": {"type": "string", "format": "date-time"},
              "note": {"type": "string"}
            }
          },
          "minItems": 1
        }
      },
      "required": ["created_at", "created_by", "version", "sources"]
    }
  }
}
```

### 2.2 Promise-Vote Linkage Entity

```json
{
  "id": "link-pe-2024-0001-v001",
  "promise_id": "promise-pe-2024-0001",
  "vote_id": "ocd-vote/abc123",
  "relationship": {
    "type": {
      "type": "string",
      "enum": ["supports", "contradicts", "partially_supports", "tangentially_related"]
    },
    "strength": {
      "type": "string",
      "enum": ["direct", "indirect", "weak"]
    },
    "explanation": {
      "type": "object",
      "properties": {
        "es": {"type": "string"},
        "en": {"type": "string"}
      }
    }
  },
  "politician_vote": {
    "option": "yes",
    "expected_based_on_promise": "yes",
    "is_consistent": true
  },
  "analysis": {
    "analyst_id": "analyst-001",
    "analyzed_at": "2025-04-25T14:30:00Z",
    "confidence": "high",
    "notes": "Vote directly implements the promised tax reduction"
  },
  "audit": {
    "created_at": "2025-04-25T14:30:00Z",
    "created_by": "analyst-001",
    "version": 1,
    "sources": [
      {
        "url": "https://congress.pe/vote/abc123",
        "accessed_at": "2025-04-25T14:00:00Z"
      }
    ]
  }
}
```

### 2.3 Politician Entity (Extended from OCD Person)

```json
{
  "id": "ocd-person/pe-congress-2024-smith",
  "uuid": "ebaff054-05df-11e3-a53b-f0def1bd7298",
  "name": {
    "full": "Maria Elena Rodriguez Vargas",
    "display": "Maria Rodriguez",
    "sort": "Rodriguez Vargas, Maria Elena"
  },
  "identifiers": [
    {"scheme": "dni_peru", "identifier": "12345678"},
    {"scheme": "congress_pe", "identifier": "CR-2024-042"}
  ],
  "party_affiliations": [
    {
      "party_id": "ocd-organization/pe-party-app",
      "party_name": "Alianza para el Progreso",
      "start_date": "2020-01-15",
      "end_date": null,
      "is_current": true
    }
  ],
  "terms": [
    {
      "role": "Congresista",
      "organization_id": "ocd-organization/pe-congress",
      "district": "Lima",
      "start_date": "2021-07-28",
      "end_date": "2026-07-27"
    }
  ],
  "promise_stats": {
    "total": 45,
    "fulfilled": 12,
    "partially_fulfilled": 8,
    "broken": 5,
    "in_progress": 15,
    "not_started": 5,
    "last_updated": "2025-12-01T00:00:00Z"
  },
  "vote_stats": {
    "total_votes": 342,
    "attendance_rate": 0.89,
    "party_alignment_rate": 0.76,
    "last_updated": "2025-12-01T00:00:00Z"
  }
}
```

### 2.4 Party Entity

```json
{
  "id": "ocd-organization/pe-party-app",
  "name": {
    "full": "Alianza para el Progreso",
    "short": "APP",
    "display": "Alianza para el Progreso"
  },
  "classification": "political_party",
  "founding_date": "2001-12-10",
  "dissolution_date": null,
  "ideology": {
    "spectrum": "center-right",
    "tags": ["populist", "regionalist"]
  },
  "identifiers": [
    {"scheme": "jne_peru", "identifier": "PARTY-042"},
    {"scheme": "wikidata", "identifier": "Q5663893"}
  ],
  "current_members_count": 23,
  "links": [
    {"url": "https://app.pe", "note": "Official Website"},
    {"url": "https://es.wikipedia.org/wiki/Alianza_para_el_Progreso", "note": "Wikipedia"}
  ]
}
```

---

## 3. Technical Best Practices

### 3.1 ID Schemes

| Use Case | Recommended Format | Example |
|----------|-------------------|---------|
| External API / URLs | Prefixed human-readable | `promise-pe-2024-0001` |
| Internal DB operations | UUID v4 | `ebaff054-05df-11e3...` |
| Cross-system references | OCD-ID | `ocd-person/uuid` |
| Legislative references | Jurisdiction-specific | `HB 264`, `PL-2024-0312` |

**Pattern (Stripe-style prefixes):**
```
promise-{country}-{year}-{sequence}
vote-{country}-{year}-{sequence}
bill-{country}-{session}-{chamber}-{number}
```

**Why both UUID and readable ID:**
- UUID: Database joins, prevents enumeration attacks
- Readable ID: Debugging, logs, user-facing URLs

### 3.2 Date Formats

```json
{
  "date_formats": {
    "full_precision": "2025-04-25T14:30:00Z",
    "date_only": "2025-04-25",
    "partial_date": "2025-04",
    "year_only": "2025"
  }
}
```

**Rule:** Always ISO 8601. Use partial dates when precision unknown (e.g., birth dates).

### 3.3 Audit Trail Schema

```json
{
  "audit": {
    "created_at": "2025-04-20T10:00:00Z",
    "created_by": "analyst-001",
    "updated_at": "2025-04-25T14:30:00Z",
    "updated_by": "analyst-002",
    "version": 3,
    "change_log": [
      {
        "version": 2,
        "changed_at": "2025-04-22T09:15:00Z",
        "changed_by": "analyst-001",
        "changes": {
          "status": {"old": "in_progress", "new": "fulfilled"}
        },
        "reason": "Vote passed implementing the promise"
      }
    ],
    "sources": [
      {
        "url": "https://congress.pe/vote/123",
        "accessed_at": "2025-04-25T14:00:00Z",
        "archived_url": "https://web.archive.org/web/...",
        "note": "Official vote record"
      }
    ]
  }
}
```

### 3.4 Versioning Strategy

**Approach: Event Sourcing Lite**
- Store current state + change log
- Each change creates new version number
- Old values preserved in `change_log`

```json
{
  "version": 3,
  "previous_versions": [
    {"version": 1, "snapshot_url": "https://api.example.com/promises/pe-2024-0001/v1"},
    {"version": 2, "snapshot_url": "https://api.example.com/promises/pe-2024-0001/v2"}
  ]
}
```

### 3.5 Internationalization (i18n)

```json
{
  "text": {
    "es": "Reducir impuestos en un 20%",
    "en": "Reduce taxes by 20%",
    "qu": "Impuestokuna 20% pisiyachisaq",
    "original_language": "es",
    "translations": {
      "en": {
        "translated_by": "human",
        "translator_id": "translator-001",
        "translated_at": "2025-04-21T10:00:00Z"
      },
      "qu": {
        "translated_by": "machine",
        "model": "google-translate-v3",
        "translated_at": "2025-04-21T10:05:00Z",
        "needs_review": true
      }
    }
  }
}
```

### 3.6 Flat vs Nested JSON

**Recommendation: Hybrid**
- Nested for tightly coupled data (contact_details, sources)
- Flat references (IDs) for loosely coupled entities

```json
{
  "promise": {
    "politician_id": "ocd-person/...",
    "politician": {
      "_embedded": true,
      "name": "Maria Rodriguez",
      "party": "APP"
    }
  }
}
```

Use `_embedded` flag or `_links` (HATEOAS) for API responses.

---

## 4. Status Enums

### Promise Status
```json
{
  "enum": [
    "not_started",
    "in_progress",
    "fulfilled",
    "partially_fulfilled",
    "broken",
    "compromised",
    "stalled",
    "expired"
  ]
}
```

### Vote Relationship Type
```json
{
  "enum": [
    "directly_supports",
    "directly_contradicts",
    "partially_supports",
    "partially_contradicts",
    "tangentially_related",
    "unrelated"
  ]
}
```

### Policy Categories (Peru-specific)
```json
{
  "enum": [
    "economia",
    "educacion",
    "salud",
    "seguridad",
    "infraestructura",
    "medio_ambiente",
    "corrupcion",
    "trabajo",
    "impuestos",
    "politica_exterior",
    "programas_sociales",
    "reforma_politica",
    "justicia",
    "agricultura",
    "mineria",
    "tecnologia"
  ]
}
```

---

## 5. Referencias

Para ver todas las referencias academicas y fuentes utilizadas en AMPAY, consulta el documento centralizado:
[Bibliografia y Fuentes](/referencia/fuentes)
