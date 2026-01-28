# PDF Text Extraction for LLM Processing - Research Report

**Date:** 2026-01-21
**Use Case:** JNE Planes de Gobierno (Peruvian government PDFs)
**Document Types:** Native text PDFs, scanned PDFs, mixed documents

---

## TLDR

**Best pipeline for Peruvian government PDFs:**
1. **Detection:** Use PyMuPDF to check if text extractable (native) or image-heavy (scanned)
2. **Native PDFs:** PyMuPDF or pymupdf4llm (fastest, best for LLM output)
3. **Scanned PDFs:** Tesseract with Spanish language pack (`spa`) + preprocessing
4. **Complex/Mixed:** Claude API direct PDF support (3,000 tokens/page, ~$0.38 per 50 pages)
5. **Chunking:** Page-level chunks with 10-20% overlap for RAG

---

## 1. Python Libraries Comparison

### Winner: PyMuPDF (fitz) / pymupdf4llm

| Library | Speed | Spanish Text | Tables | Best For |
|---------|-------|--------------|--------|----------|
| **PyMuPDF** | 0.12s | Excellent | Good | High-volume extraction |
| **pdfplumber** | 0.10s | Good | **Best** | Table-heavy documents |
| **pypdfium2** | 0.003s | Good | Basic | Raw speed |
| **pypdf** | 0.024s | Good | Basic | Simple extraction |

**pymupdf4llm** - Specifically optimized for LLM applications:
- Clean markdown output with proper headings
- Preserves table formatting
- 0.14s processing time
- Best for RAG/content systems

### Code Examples

```python
# PyMuPDF - Basic extraction
import fitz

def extract_with_pymupdf(pdf_path):
    doc = fitz.open(pdf_path)
    text_by_page = {}
    for page_num, page in enumerate(doc):
        text_by_page[page_num + 1] = page.get_text()
    return text_by_page

# pymupdf4llm - LLM-optimized
import pymupdf4llm

def extract_for_llm(pdf_path):
    md_text = pymupdf4llm.to_markdown(pdf_path)
    return md_text

# pdfplumber - Best for tables
import pdfplumber

def extract_tables(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        tables = []
        for page in pdf.pages:
            page_tables = page.extract_tables()
            tables.extend(page_tables)
    return tables
```

### Licensing Note
PyMuPDF is under AGPL license. Commercial use requires a paid license from Artifex.

---

## 2. Detecting Native vs Scanned PDFs

```python
import fitz

def detect_pdf_type(pdf_path):
    """
    Detect if PDF is native (text-based) or scanned (image-based)
    Returns: 'native', 'scanned', or 'mixed'
    """
    doc = fitz.open(pdf_path)

    native_pages = 0
    scanned_pages = 0

    for page in doc:
        text = page.get_text().strip()
        images = page.get_images()
        page_rect = page.rect

        # Check if images cover most of the page
        image_coverage = 0
        for img in images:
            xref = img[0]
            img_rect = page.get_image_bbox(xref)
            if img_rect:
                img_area = img_rect.width * img_rect.height
                page_area = page_rect.width * page_rect.height
                image_coverage = max(image_coverage, img_area / page_area)

        # Heuristics
        if len(text) > 100:
            native_pages += 1
        elif image_coverage > 0.8:
            scanned_pages += 1
        else:
            # Ambiguous - could be mixed
            if len(text) > 50:
                native_pages += 1
            else:
                scanned_pages += 1

    total = len(doc)
    if scanned_pages == 0:
        return 'native'
    elif native_pages == 0:
        return 'scanned'
    else:
        return 'mixed'
```

---

## 3. OCR Solutions for Scanned PDFs

### Tesseract + pytesseract (FREE, Local)

**Setup:**
```bash
# macOS
brew install tesseract
brew install tesseract-lang  # All languages including Spanish

# Ubuntu
sudo apt install tesseract-ocr tesseract-ocr-spa

# Python
pip install pytesseract pdf2image Pillow
```

**Spanish OCR Code:**
```python
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import cv2
import numpy as np

def preprocess_image(image):
    """Improve OCR accuracy with preprocessing"""
    # Convert PIL to OpenCV
    img = np.array(image)

    # Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Denoise
    denoised = cv2.fastNlMeansDenoising(gray)

    # Threshold (binarization)
    _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return Image.fromarray(binary)

def ocr_scanned_pdf(pdf_path, lang='spa'):
    """
    OCR a scanned PDF with Spanish language
    """
    # Convert PDF pages to images
    images = convert_from_path(pdf_path, dpi=300)

    text_by_page = {}
    custom_config = r'--oem 3 --psm 6'  # LSTM engine, assume uniform block of text

    for page_num, image in enumerate(images):
        # Preprocess for better accuracy
        processed = preprocess_image(image)

        # OCR
        text = pytesseract.image_to_string(
            processed,
            lang=lang,
            config=custom_config
        )
        text_by_page[page_num + 1] = text

    return text_by_page
```

**Tesseract Accuracy:** ~80% on real-world documents. Significantly better with preprocessing.

### Cloud OCR Comparison

| Service | Accuracy | Spanish | Cost | Best For |
|---------|----------|---------|------|----------|
| **AWS Textract** | 82% | Good | ~$10/1000 pages | Tables, forms |
| **Google Document AI** | 82% | Excellent | ~$10/1000 pages | Handwritten, custom training |
| **Azure Doc Intelligence** | 85%+ | Good | ~$10/1000 pages | Overall quality |

**Recommendation:** For government PDFs in Spanish, Google Document AI has edge for handwritten portions. AWS Textract better for structured forms/tables.

---

## 4. LLM-Based PDF Extraction (Claude)

### Claude PDF Support (Current)

**Capabilities:**
- Native PDF processing via API (since late 2024)
- Multimodal: reads text + analyzes charts/images
- Full vision processing up to 100 pages
- Pages beyond 100: text-only extraction

**Limitations:**
- 32 MB max file size
- 100 page limit for full vision
- No encrypted/password-protected PDFs

**Cost Analysis:**
- ~1,500-3,000 tokens per page
- Sonnet 4: $3/million image tokens, $0.30/million text tokens
- **50-page report: ~$0.38**

**When to Use Claude Direct:**
- Complex layouts that confuse traditional parsers
- Need to understand charts/diagrams
- Mixed content (text + images + tables)
- Small batch of important documents

**API Code:**
```python
import anthropic
import base64

def extract_with_claude(pdf_path, query="Extract all text from this document"):
    client = anthropic.Anthropic()

    with open(pdf_path, "rb") as f:
        pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": query
                    }
                ],
            }
        ],
    )
    return message.content[0].text
```

---

## 5. Chunking Strategies for LLM/RAG

### Best Strategy: Page-Level Chunking

NVIDIA 2024 benchmarks found page-level chunking achieved **0.648 accuracy** with lowest variance across document types.

**Why it works for government PDFs:**
- Legal/official documents organized by pages
- Natural semantic boundaries
- Easy citation (page numbers)
- Consistent chunk sizes

### Implementation

```python
def chunk_document(text_by_page, overlap_pages=0, include_page_numbers=True):
    """
    Chunk document by pages with optional overlap
    """
    chunks = []
    pages = list(text_by_page.keys())

    for i, page_num in enumerate(pages):
        chunk_text = ""

        # Add page number for citation
        if include_page_numbers:
            chunk_text = f"[Page {page_num}]\n\n"

        chunk_text += text_by_page[page_num]

        # Add overlap from next page
        if overlap_pages > 0 and i < len(pages) - 1:
            next_page = pages[i + 1]
            next_text = text_by_page[next_page]
            # Take first 20% of next page as overlap
            overlap_chars = int(len(next_text) * 0.2)
            chunk_text += f"\n\n[Continues: Page {next_page}]\n{next_text[:overlap_chars]}..."

        chunks.append({
            'page': page_num,
            'text': chunk_text,
            'char_count': len(chunk_text)
        })

    return chunks

# For RAG with semantic search
def chunk_for_rag(text_by_page, target_tokens=512):
    """
    Adaptive chunking targeting specific token count
    """
    chunks = []
    current_chunk = ""
    current_pages = []

    for page_num, text in text_by_page.items():
        # Estimate tokens (rough: 1 token ~ 4 chars for Spanish)
        estimated_tokens = len(text) / 4
        current_tokens = len(current_chunk) / 4

        if current_tokens + estimated_tokens > target_tokens and current_chunk:
            chunks.append({
                'pages': current_pages.copy(),
                'text': current_chunk,
                'tokens_est': int(len(current_chunk) / 4)
            })
            current_chunk = ""
            current_pages = []

        current_chunk += f"\n\n[Page {page_num}]\n{text}"
        current_pages.append(page_num)

    # Don't forget last chunk
    if current_chunk:
        chunks.append({
            'pages': current_pages,
            'text': current_chunk,
            'tokens_est': int(len(current_chunk) / 4)
        })

    return chunks
```

### Chunk Size Guidelines

| Query Type | Optimal Chunk Size | Reason |
|------------|-------------------|--------|
| Factoid (specific facts) | 256-512 tokens | Precise retrieval |
| Analytical (summaries) | 1024+ tokens | Needs context |
| Multi-concept | Variable | Keep related data together |

---

## 6. Complete Pipeline for JNE PDFs

```python
import fitz
import pytesseract
from pdf2image import convert_from_path
import os

class PlanDeGobiernoExtractor:
    """
    Complete pipeline for extracting Peruvian government PDFs
    """

    def __init__(self, tesseract_lang='spa'):
        self.lang = tesseract_lang

    def process(self, pdf_path):
        """
        Main entry point - auto-detects and processes PDF
        """
        # Step 1: Detect PDF type
        pdf_type = self._detect_type(pdf_path)
        print(f"Detected PDF type: {pdf_type}")

        # Step 2: Extract based on type
        if pdf_type == 'native':
            text_by_page = self._extract_native(pdf_path)
        elif pdf_type == 'scanned':
            text_by_page = self._extract_scanned(pdf_path)
        else:  # mixed
            text_by_page = self._extract_mixed(pdf_path)

        # Step 3: Validate extraction quality
        quality_score = self._validate_quality(text_by_page)

        # Step 4: Chunk for LLM
        chunks = self._chunk_for_llm(text_by_page)

        return {
            'pdf_type': pdf_type,
            'pages': len(text_by_page),
            'quality_score': quality_score,
            'text_by_page': text_by_page,
            'chunks': chunks
        }

    def _detect_type(self, pdf_path):
        doc = fitz.open(pdf_path)
        scanned_count = 0

        for page in doc:
            text = page.get_text().strip()
            if len(text) < 50:  # Very little text
                scanned_count += 1

        ratio = scanned_count / len(doc)
        if ratio == 0:
            return 'native'
        elif ratio == 1:
            return 'scanned'
        else:
            return 'mixed'

    def _extract_native(self, pdf_path):
        doc = fitz.open(pdf_path)
        return {i+1: page.get_text() for i, page in enumerate(doc)}

    def _extract_scanned(self, pdf_path):
        images = convert_from_path(pdf_path, dpi=300)
        text_by_page = {}

        for i, img in enumerate(images):
            text = pytesseract.image_to_string(img, lang=self.lang)
            text_by_page[i+1] = text

        return text_by_page

    def _extract_mixed(self, pdf_path):
        doc = fitz.open(pdf_path)
        images = convert_from_path(pdf_path, dpi=300)
        text_by_page = {}

        for i, page in enumerate(doc):
            text = page.get_text().strip()

            if len(text) < 50:  # Likely scanned
                text = pytesseract.image_to_string(images[i], lang=self.lang)

            text_by_page[i+1] = text

        return text_by_page

    def _validate_quality(self, text_by_page):
        """
        Simple quality score based on text characteristics
        """
        total_chars = sum(len(t) for t in text_by_page.values())
        total_pages = len(text_by_page)

        if total_pages == 0:
            return 0

        avg_chars_per_page = total_chars / total_pages

        # Government docs typically have 1500-3000 chars per page
        if avg_chars_per_page < 500:
            return 0.3  # Poor extraction
        elif avg_chars_per_page < 1000:
            return 0.6  # Moderate
        else:
            return 0.9  # Good

    def _chunk_for_llm(self, text_by_page, target_tokens=512):
        chunks = []
        for page_num, text in text_by_page.items():
            chunks.append({
                'page': page_num,
                'text': f"[Page {page_num}]\n\n{text}",
                'tokens_est': len(text) // 4
            })
        return chunks


# Usage
if __name__ == "__main__":
    extractor = PlanDeGobiernoExtractor()
    result = extractor.process("plan_de_gobierno.pdf")

    print(f"Extracted {result['pages']} pages")
    print(f"Quality score: {result['quality_score']}")
    print(f"Generated {len(result['chunks'])} chunks")
```

---

## 7. Recommendations Summary

### For JNE Planes de Gobierno:

1. **Start with PyMuPDF** - Fast, handles most native PDFs
2. **Auto-detect scanned pages** - Use heuristic above
3. **OCR fallback** - Tesseract with `spa` language + preprocessing
4. **Quality validation** - Check chars/page ratio
5. **Page-level chunks** - Best for legal/government docs
6. **Claude fallback** - For complex layouts or when accuracy critical

### Cost Optimization:
- **Free tier:** PyMuPDF + Tesseract (local)
- **Low cost:** AWS Textract for batch scanned docs (~$10/1000 pages)
- **Quality critical:** Claude API (~$0.38/50 pages)

### Dependencies to Install:
```bash
pip install PyMuPDF pymupdf4llm pdfplumber pytesseract pdf2image Pillow opencv-python
brew install tesseract tesseract-lang poppler
```

---

## Referencias

Para ver todas las referencias academicas y fuentes utilizadas en AMPAY, consulta el documento centralizado:
[Bibliografia y Fuentes](/referencia/fuentes)
