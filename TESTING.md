# Testing Guide for SyncType

## Quick Test Checklist

### ✅ Backend Tests

#### 1. Health Check
```bash
curl http://localhost:8000/health
```
Expected: `{"status":"healthy"}`

#### 2. Original Translation Endpoint
```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "som sok sabay", "mode": "hybrid"}'
```
Expected: `{"result":"សុំសុខសប្បាយ","mode":"hybrid"}`

#### 3. New Translation Endpoint
```bash
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "som sok sabay"}'
```
Expected: 
```json
{
  "translation": "សុំសុខសប្បាយ",
  "confidence": 0.95,
  "matched_roman": "som"
}
```

#### 4. Suggestions Endpoint
```bash
curl -X POST http://localhost:8000/api/suggest \
  -H "Content-Type: application/json" \
  -d '{"text": "som", "max_results": 5}'
```
Expected: Array of suggestions with roman, khmer, and confidence

---

### ✅ Frontend Tests

#### 1. Basic Translation
1. Open http://localhost:5173
2. Type "som sok sabay" in the input box
3. Click "Translate" or press Ctrl+Enter
4. Verify:
   - ✓ Output shows Khmer script
   - ✓ Confidence meter appears
   - ✓ Matched pattern displays

#### 2. Real-time Suggestions
1. Start typing "som" slowly
2. After 400ms, suggestions dropdown should appear
3. Click on a suggestion
4. Verify it's added to the output

#### 3. Theme Toggle
1. Click the sun/moon icon in top-right
2. Verify smooth transition between light/dark mode
3. Refresh page - theme should persist

#### 4. Example Pills
1. Click on any example pill (e.g., "eng tv na?")
2. Verify it auto-fills the input and translates

#### 5. Clear Functionality
1. Enter some text and translate
2. Click "Clear all"
3. Verify all fields are reset

---

### 🧪 Edge Cases to Test

#### Empty Input
- Input: (empty)
- Expected: Translate button disabled

#### Very Long Input
- Input: Multiple sentences of romanized Khmer
- Expected: Should handle gracefully

#### Unknown Words
- Input: "xyz123abc"
- Expected: Model attempts translation, shows lower confidence

#### Special Characters
- Input: "som! sok? sabay."
- Expected: Should handle punctuation

#### Mixed Case
- Input: "SoM sOk SaBaY"
- Expected: Should normalize and translate correctly

---

### 🔍 Visual Testing

#### Desktop (1920x1080)
- [ ] Hero section displays properly
- [ ] Translation interface centered
- [ ] Features cards in 3-column grid
- [ ] Footer elements aligned

#### Tablet (768x1024)
- [ ] Responsive layout adjusts
- [ ] Features stack appropriately
- [ ] Text remains readable

#### Mobile (375x667)
- [ ] Single column layout
- [ ] Touch-friendly buttons
- [ ] Input area expandable
- [ ] Navigation works

---

### 🎨 Animation Tests

- [ ] Logo breathing animation works
- [ ] Floating icons animate smoothly
- [ ] Gradient text shifts colors
- [ ] Output slide-up animation plays
- [ ] Hover effects on cards work
- [ ] Theme transition is smooth

---

### 🐛 Common Issues

#### "API offline" in header
- **Cause**: Backend not running or wrong port
- **Fix**: Start backend on port 8000

#### "Failed to fetch" error
- **Cause**: CORS issue or backend unreachable
- **Fix**: Check CORS settings in backend main.py

#### No suggestions appearing
- **Cause**: Endpoint not responding or empty dictionary
- **Fix**: Verify CSV file loaded and /api/suggest works

#### Theme not persisting
- **Cause**: localStorage blocked
- **Fix**: Check browser privacy settings

---

### 📊 Performance Benchmarks

Target metrics:
- Translation request: < 200ms
- Suggestion request: < 100ms
- Page load: < 2s
- Theme toggle: < 100ms

---

### ✨ Success Criteria

All tests pass when:
1. ✅ Backend returns correct responses
2. ✅ Frontend displays Khmer script correctly
3. ✅ Confidence scores calculate properly
4. ✅ Suggestions appear in real-time
5. ✅ Theme persists across refreshes
6. ✅ All animations run smoothly
7. ✅ Responsive on all screen sizes
8. ✅ No console errors

---

## Automated Testing (Future)

### Backend Tests
```bash
# Install pytest
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/
```

### Frontend Tests
```bash
# Install testing libraries
npm install --save-dev @testing-library/react vitest

# Run tests
npm run test
```

---

Happy Testing! 🧪
