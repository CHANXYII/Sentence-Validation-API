'use client'

import { useState } from react

interface ValidationResult {
  score: number
  level: string
  suggestion: string
  corrected_sentence: string
}

export default function Home() {
  const [wordId, setWordId] = useState<number>(1)
  const [sentence, setSentence] = useState<string>('')
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [result, setResult] = useState<ValidationResult | null>(null)
  const [error, setError] = useState<string>('')

  // Handle textarea change
  const handleSentenceChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setSentence(e.target.value)
    setError('')
  }

  // Handle word ID change
  const handleWordIdChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setWordId(Number(e.target.value))
    setError('')
  }

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // Validation
    if (!sentence.trim()) {
      setError('Please enter a sentence')
      return
    }

    if (!wordId || wordId < 1) {
      setError('Please enter a valid word ID')
      return
    }

    setIsLoading(true)
    setError('')
    setResult(null)

    try {
      // Call the backend API
      const response = await fetch('http://localhost:8000/api/validate-sentence', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          word_id: wordId,
          sentence: sentence,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to validate sentence')
      }

      const data: ValidationResult = await response.json()
      setResult(data)
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      console.error('Error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  // Get score color based on value
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  // Get score background color
  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-green-100'
    if (score >= 60) return 'bg-yellow-100'
    return 'bg-red-100'
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            📚 Daily Vocab
          </h1>
          <p className="text-lg text-gray-600">
            Practice your vocabulary with AI-powered sentence validation
          </p>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-lg shadow-xl p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Word ID Input */}
            <div>
              <label htmlFor="wordId" className="block text-sm font-medium text-gray-700 mb-2">
                Word ID
              </label>
              <input
                type="number"
                id="wordId"
                value={wordId}
                onChange={handleWordIdChange}
                min="1"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter word ID (e.g., 1)"
              />
              <p className="mt-1 text-sm text-gray-500">
                Available IDs: 1 (library), 2 (magnificent), 3 (serendipity), 4 (study), 5 (collaborate)
              </p>
            </div>

            {/* Sentence Textarea */}
            <div>
              <label htmlFor="sentence" className="block text-sm font-medium text-gray-700 mb-2">
                Your Sentence
              </label>
              <textarea
                id="sentence"
                value={sentence}
                onChange={handleSentenceChange}
                rows={4}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                placeholder="Write a sentence using the vocabulary word..."
              />
            </div>

            {/* Error Message */}
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                {error}
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-200 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Validating...' : 'Validate Sentence'}
            </button>
          </form>

          {/* Results Section */}
          {result && (
            <div className="mt-8 space-y-4 animate-fadeIn">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">
                Validation Results
              </h2>

              {/* Score Card */}
              <div className={`${getScoreBgColor(result.score)} rounded-lg p-6 border-2 ${result.score >= 80 ? 'border-green-300' : result.score >= 60 ? 'border-yellow-300' : 'border-red-300'}`}>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Your Score</p>
                    <p className={`text-5xl font-bold ${getScoreColor(result.score)}`}>
                      {result.score}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-600">Level</p>
                    <p className="text-2xl font-semibold text-gray-800">
                      {result.level}
                    </p>
                  </div>
                </div>
              </div>

              {/* Suggestion */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h3 className="font-semibold text-blue-900 mb-2">💡 Suggestion</h3>
                <p className="text-blue-800">{result.suggestion}</p>
              </div>

              {/* Corrected Sentence */}
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                <h3 className="font-semibold text-gray-900 mb-2">✏️ Corrected Sentence</h3>
                <p className="text-gray-800 italic">{result.corrected_sentence}</p>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-gray-600">
          <p className="text-sm">
            Built with FastAPI & Next.js | API Docs: <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">localhost:8000/docs</a>
          </p>
        </div>
      </div>
    </main>
  )
}
