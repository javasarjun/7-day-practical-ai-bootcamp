# Day 4 RAG Lab - Demo Guide

## 📄 Sample Document

A sample PDF has been created at: `sample_documents/climate_change_guide.pdf`

**Document Title:** Climate Change: A Comprehensive Guide
**Content:** 6 sections covering causes, effects, solutions, and international agreements

---

## 🚀 Quick Start

```bash
# Navigate to the directory
cd day4-pdf-chat-rag

# Activate virtual environment
source venv/bin/activate

# Ensure .env file exists with your OpenAI API key
echo "OPENAI_API_KEY=your_key_here" > .env

# Run the Streamlit app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📋 Demo Scenarios & Sample Questions

### **Scenario 1: Direct Factual Questions**
*Best for testing accurate retrieval and grounding in document*

**Upload:** `climate_change_guide.pdf`

**Questions:**
1. "What are the main causes of climate change?"
   - ✅ Expected: Should mention burning fossil fuels, deforestation, industrial processes, agriculture, waste
   
2. "How much has global CO2 increased?"
   - ✅ Expected: "increased by 50% since pre-industrial times, rising from 280 ppm to over 420 ppm"
   
3. "What is the Paris Agreement and what are its key provisions?"
   - ✅ Expected: Mentions 195 countries, 2°C/1.5°C limit, NDCs, $100 billion financing, 5-year reviews

4. "How much has the global average temperature increased?"
   - ✅ Expected: "approximately 1.1°C since the pre-industrial era"

---

### **Scenario 2: Synthesis Questions**
*Tests ability to combine information from multiple sections*

**Questions:**
1. "What are the main effects of climate change and how do they relate to the causes?"
   - ✅ Expected: Should connect causes (emissions) → effects (temperature, sea level, weather)

2. "What renewable energy sources are mentioned and how much do they currently contribute?"
   - ✅ Expected: Solar, wind, hydroelectric; solar provides 4% of global electricity

3. "Name three individual actions someone can take to help with climate change"
   - ✅ Expected: Should list from the "What Can Individuals Do" section

---

### **Scenario 3: Specific Details & Examples**
*Tests fine-grained retrieval of concrete examples*

**Questions:**
1. "Which coastal cities are experiencing flooding due to climate change?"
   - ✅ Expected: Venice and Miami mentioned as examples of "sunny day" flooding

2. "What animals are vulnerable to climate change?"
   - ✅ Expected: Polar bears, sea turtles, coral reefs

3. "What did India do with trees in 2017?"
   - ✅ Expected: Planted 66 million trees in 12 hours

4. "Name two countries or regions affected by climate-related disasters mentioned in the document"
   - ✅ Expected: Australia (bushfires), Pakistan (floods), Africa (droughts), Asia (floods)

---

### **Scenario 4: Numerical & Statistics Questions**
*Tests precise information extraction*

**Questions:**
1. "How many species are we losing and at what rate?"
   - ✅ Expected: "137 species every single day due to rainforest destruction"

2. "What percentage of global electricity does solar currently provide?"
   - ✅ Expected: "4% of global electricity"

3. "How many countries signed the Paris Agreement?"
   - ✅ Expected: "195 countries"

4. "What temperature targets did the Paris Agreement set?"
   - ✅ Expected: "well below 2°C, preferably to 1.5°C"

---

### **Scenario 5: Edge Cases & Robustness Testing**

**Out-of-scope question:**
```
Q: "What is the capital of France?"
Expected: "I don't see information about this in the provided document..."
```

**Vague question:**
```
Q: "Tell me everything"
Expected: Should return top 4 most relevant chunks (may be section headings)
```

**Follow-up question:**
```
Q: "What are the causes?"
A: [Gets answer about causes]
Q: "Which one has the biggest impact?"
Expected: Should still work, retrieving relevant context
```

**Partially relevant:**
```
Q: "How can we solve climate change?"
Expected: Should retrieve solutions section with renewable energy, efficiency, EVs, etc.
```

---

## 🧪 Testing Checklist

- [ ] **Upload & Processing**
  - [ ] File uploads successfully
  - [ ] "Process PDF" button works
  - [ ] Shows correct chunk count (should be ~7-10 chunks)
  - [ ] Success message appears

- [ ] **Retrieval Quality**
  - [ ] Questions retrieve relevant sections
  - [ ] Top 4 chunks are related to the question
  - [ ] Metadata shows correct page numbers

- [ ] **Answer Quality**
  - [ ] Answers are grounded in document
  - [ ] No hallucinations (facts made up)
  - [ ] Clear and well-formatted
  - [ ] Includes specific examples when relevant

- [ ] **Chat Features**
  - [ ] Chat history shows user Q & AI A
  - [ ] "View Retrieved Context" expander works
  - [ ] Shows chunk indices and page numbers
  - [ ] Clear Chat button resets conversation

- [ ] **UI/UX**
  - [ ] Loading spinners appear during processing
  - [ ] Error messages are clear
  - [ ] Layout is readable and organized

---

## 📊 What You're Testing

1. **Text Extraction:** PDF → text conversion accuracy
2. **Chunking:** How the document is split into manageable pieces
3. **Embedding:** Semantic understanding via embeddings
4. **Retrieval:** How well ChromaDB finds relevant chunks
5. **Grounding:** How well the LLM uses retrieved context
6. **RAG Flow:** End-to-end pipeline correctness

---

## 💡 Advanced Testing

### Test with Your Own PDF
1. Download any PDF (research paper, manual, documentation)
2. Click "Upload a PDF document"
3. Select your file and click "Process PDF"
4. Ask specific questions about your document
5. Verify answers are grounded in your content

### Test Multiple Documents
1. Process climate PDF
2. Ask questions → verify answers
3. Process a different PDF (replace climate one)
4. Ask questions about new PDF → should get different answers
5. Verifies collection is properly cleared

### Test Embedding Quality
- Ask very similar questions → same chunks retrieved
- Ask opposite questions → different chunks retrieved
- Ask specific vs. general questions → relevance varies

---

## 🔍 What to Look For (Indicators of Success)

✅ **Good Signs:**
- Answers include specific quotes from the document
- Retrieved chunks clearly relate to the question
- No information appears that isn't in the PDF
- Follow-up questions work naturally
- Response time is reasonable (< 5 seconds usually)

❌ **Red Flags:**
- Answers contradict the document
- Retrieved chunks seem unrelated
- Making up facts not in the document
- Consistently retrieving wrong sections
- Crashes or errors on certain questions

---

## 📝 Notes

- First question may take 5-10 seconds (model initialization)
- Subsequent questions are typically faster (2-3 seconds)
- ChromaDB stores data persistently in `chroma_db/` directory
- Each PDF upload clears the previous collection and stores new chunks
- The LLM system message: "Answer only using the retrieved document context"

**Happy testing! 🎉**
