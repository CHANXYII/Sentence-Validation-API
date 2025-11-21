# Daily Vocab - Sentence Validation API

Full-stack app for validating sentences with vocabulary words.
1660901693
Natthanarong Tiangjit

## Quick Start

### 1. Start Database
```bash
docker run --name mysql-daily-vocab \
  -e MYSQL_ROOT_PASSWORD=password \
  -e MYSQL_DATABASE=daily_vocab \
  -p 3306:3306 -d mysql:8.0
```

### 2. Start Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python init_db.py
uvicorn main:app --reload
```
→ Backend: http://localhost:8000  
→ API Docs: http://localhost:8000/docs

### 3. Start Frontend
```bash
cd frontend
npm install
npm run dev
```
→ Frontend: http://localhost:3000

## How to Use

1. Open http://localhost:3000
2. Enter Word ID (1-5)
3. Write a sentence using that word
4. Click "Validate Sentence"
5. See your score and feedback

## Sample Vocabulary

| ID | Word | Level |
|----|------|-------|
| 1 | library | Beginner |
| 2 | magnificent | Intermediate |
| 3 | serendipity | Advanced |
| 4 | study | Beginner |
| 5 | collaborate | Intermediate |

## Test with Postman

**POST** http://localhost:8000/api/validate-sentence

```json
{
  "word_id": 1,
  "sentence": "I went to the library."
}
```

**Response:**
```json
{
  "score": 85.0,
  "level": "Beginner",
  "suggestion": "Great job!",
  "corrected_sentence": "I went to the library."
}
```
