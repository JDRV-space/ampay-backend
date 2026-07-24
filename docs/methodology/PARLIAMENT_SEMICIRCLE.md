# Parliament Semicircle Algorithm

**Version:** 1.0
**Date:** 2026-02-27
**Status:** ACTIVE

---

## Executive Summary

Visualization of congressional votes as a hemicycle, representing each individual vote as a colored circular seat based on its vote type.

---

## 1. Purpose

The ParliamentSemicircle component renders congressional vote results as a hemicycle (half circle), mimicking the physical layout of the hemicycle of the Congress of the Republic of Peru. Each individual vote is represented as a circular dot, colored by vote type.

### 1.1 Visualization Objective

- **Immediate comprehension:** The user identifies vote proportions at a glance
- **Visual familiarity:** The hemicycle shape is universally recognized as parliamentary representation
- **Individual granularity:** Each circle represents exactly one vote, not a percentage

---

## 2. Vote Aggregation

The first step is to sum all party votes to obtain global totals. The data comes from the voteByParty object containing votes broken down by party.

### 2.1 Aggregation Process

```javascript
let totalSi = 0, totalNo = 0, totalAbs = 0, totalAus = 0;

Object.values(voteByParty.parties).forEach((data) => {
  totalSi  += data.si;
  totalNo  += data.no;
  totalAbs += data.abstencion;
  totalAus += data.ausente;
});
```

### 2.2 Vote Categories

| Category | Variable | Description |
|---|---|---|
| **YES** | `totalSi` | Votes in favor of the motion |
| **NO** | `totalNo` | Votes against the motion |
| **ABSTENTION** | `totalAbs` | Present congress members who abstained |
| **ABSENT** | `totalAus` | Congress members who were not present |

---

## 3. Seat Assignment

A seats array is created where each element represents an individual vote. Seats are sorted by vote type to visually group colors in the hemicycle.

### 3.1 Seat Ordering

Seats are ordered in the following fixed order:

```
1. SI        (#22c55e)  // First - votes in favor
2. NO        (#ef4444)  // Second - votes against
3. ABSTENCION (#eab308)  // Third - abstentions
4. AUSENTE   (#6b7280)  // Fourth - absent
```

### 3.2 Colors by Vote Type

| Vote Type | Color | Hex Code |
|---|---|---|
| **YES** | Green | `#22c55e` |
| **NO** | Red | `#ef4444` |
| **ABSTENTION** | Yellow | `#eab308` |
| **ABSENT** | Gray | `#6b7280` |

### 3.3 Array Generation

```javascript
const seats: { color: string }[] = [];

// SI seats
for (let i = 0; i < totalSi; i++)
  seats.push({ color: '#22c55e' });

// NO seats
for (let i = 0; i < totalNo; i++)
  seats.push({ color: '#ef4444' });

// ABSTENCION seats
for (let i = 0; i < totalAbs; i++)
  seats.push({ color: '#eab308' });

// AUSENTE seats
for (let i = 0; i < totalAus; i++)
  seats.push({ color: '#6b7280' });
```

---

## 4. Semicircle Geometry

The algorithm distributes seats across 5 concentric rows forming a semicircle. Each row has a larger radius and more seats than the previous one.

### 4.1 Row Parameters

| Row | Radius (px) | Base Seats | Formula |
|---|---|---|---|
| 0 | 60 | `seatsPerRow + 0` | `60 + 0 * 25` |
| 1 | 85 | `seatsPerRow + 2` | `60 + 1 * 25` |
| 2 | 110 | `seatsPerRow + 4` | `60 + 2 * 25` |
| 3 | 135 | `seatsPerRow + 6` | `60 + 3 * 25` |
| 4 | 160 | `seatsPerRow + 8` | `60 + 4 * 25` |

```javascript
const rows = 5;
const seatsPerRow = Math.ceil(seats.length / rows);

for (let row = 0; row < rows; row++) {
  const radius = 60 + row * 25;
  const seatsInThisRow = Math.min(
    seatsPerRow + row * 2,
    seats.length - seatIndex
  );
}
```

### 4.2 Angular Distribution

Seats are distributed evenly along each row arc. The angle goes from PI (left) to 0 (right):

```javascript
const startAngle = Math.PI;  // PI radians = 180 degrees (left)
const endAngle   = 0;        // 0 radians = 0 degrees (right)

// For each seat i in a row with N seats:
const angle = startAngle - (i / (N - 1 || 1)) * (startAngle - endAngle);

// Simplified:
// angle = PI - (i / (N - 1)) * PI
// angle = PI * (1 - i / (N - 1))
```

### 4.3 Polar to Cartesian Conversion

Each seat is positioned by converting polar coordinates (angle, radius) to Cartesian coordinates (x, y):

```javascript
// Polar to Cartesian conversion:
// x = centerX + radius * cos(angle)
// y = centerY - radius * sin(angle)

const centerX = 200;
const centerY = 180;

const x = centerX + radius * Math.cos(angle);
const y = centerY - radius * Math.sin(angle);

// Note: y uses subtraction because SVG y-axis is inverted
// (0,0) is top-left, y increases downward
```

---

## 5. SVG Parameters

The hemicycle is rendered inside an SVG element with fixed dimensions and parameters.

### 5.1 Canvas Dimensions

| Parameter | Value |
|---|---|
| `viewBox` | `0 0 400 200` |
| Center X | `200` |
| Center Y | `180` |
| Seat radius | `6px` |
| Base radius (row 0) | `60px` |
| Max radius (row 4) | `160px` |

### 5.2 Base Arc

The base arc (lower curved line) is drawn as a separate SVG path to provide visual context to the hemicycle:

```jsx
<svg viewBox="0 0 400 200">
  {/* Base arc path */}
  <path
    d="M 20,180 A 180,180 0 0,1 380,180"
    fill="none"
    stroke="rgba(255,255,255,0.1)"
    strokeWidth="1"
  />

  {/* Seat circles */}
  {seats.map((seat, index) => (
    <circle
      key={index}
      cx={seat.x}
      cy={seat.y}
      r={6}
      fill={seat.color}
    />
  ))}
</svg>
```

---

## 6. Result Determination

The vote result is determined by simple majority comparing YES votes against NO votes. Abstentions and absences do not affect the result.

### 6.1 Decision Logic

| Condition | Result | Display |
|---|---|---|
| `YES > NO` | **APPROVED** | Green text |
| `NO > YES` | **REJECTED** | Red text |
| `YES = NO` | **TIE** | Yellow text |

### 6.2 Implementation

```javascript
const result =
  totalSi > totalNo
    ? "APROBADO"
    : totalNo > totalSi
      ? "RECHAZADO"
      : "EMPATE";
```

---

## 7. Limitations

- **Fixed rows:** The 5-row layout is fixed. With few votes (<20) the hemicycle looks sparse; with many votes (>200) circles may overlap
- **No party grouping:** Seats are grouped by vote type, not by party. It is not possible to identify which party cast each individual vote
- **Fixed seat size:** The 6px radius does not adjust to the total vote count, which can cause visual overlap in large votes
- **No interactivity:** Individual circles have no tooltip or hover state. Detailed information is only available in the side legend

---

## 8. Related Files

| File | Content |
|---|---|
| `ParliamentSemicircle.tsx` | React component implementing the visualization algorithm |
| `votaciones_por_partido.json` | Source data with votes broken down by party and type |

---

## References

For all academic references and sources used in AMPAY, see the centralized document:
[Bibliography and Sources](../reference/SOURCES_BIBLIOGRAPHY.md)

---

*Last updated: 2026-02-27*
