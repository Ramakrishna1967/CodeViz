'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { analyzeRepository } from '@/lib/api'
import AnalysisProgress from '@/components/AnalysisProgress'

export default function AnalyzePage() {
    const router = useRouter()
    const [url, setUrl] = useState('')
    const [isAnalyzing, setIsAnalyzing] = useState(false)
    const [progress, setProgress] = useState({ step: '', percent: 0 })
    const [error, setError] = useState('')

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()

        if (!url.trim()) {
            setError('Please enter a GitHub URL')
            return
        }

        if (!url.includes('github.com')) {
            setError('Please enter a valid GitHub repository URL')
            return
        }

        setError('')
        setIsAnalyzing(true)
        setProgress({ step: 'Cloning repository...', percent: 10 })

        try {
            setProgress({ step: 'Parsing files...', percent: 30 })
            const result = await analyzeRepository(url)

            setProgress({ step: 'Building graph...', percent: 70 })
            await new Promise(resolve => setTimeout(resolve, 500))

            setProgress({ step: 'Complete!', percent: 100 })
            await new Promise(resolve => setTimeout(resolve, 300))

            router.push(`/graph/${result.repo_id}`)
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Analysis failed')
            setIsAnalyzing(false)
        }
    }

    return (
        <div className="flex min-h-[calc(100vh-4rem)] flex-col items-center justify-center px-4">
            <div className="w-full max-w-xl">
                <h1 className="mb-2 text-center text-3xl font-bold">Analyze Repository</h1>
                <p className="mb-8 text-center text-gray-400">
                    Paste a GitHub repository URL to generate an interactive visualization
                </p>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <input
                            type="text"
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                            placeholder="https://github.com/username/repository"
                            disabled={isAnalyzing}
                            className="w-full rounded-lg border border-gray-700 bg-gray-900 px-4 py-3 text-white placeholder-gray-500 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20 disabled:opacity-50"
                        />
                    </div>

                    {error && (
                        <div className="rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-400">
                            {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={isAnalyzing}
                        className="w-full rounded-lg bg-primary-500 py-3 font-semibold text-white transition-colors hover:bg-primary-600 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        {isAnalyzing ? 'Analyzing...' : 'Analyze Repository'}
                    </button>
                </form>

                {isAnalyzing && (
                    <div className="mt-8">
                        <AnalysisProgress step={progress.step} percent={progress.percent} />
                    </div>
                )}

                <div className="mt-12 rounded-lg border border-gray-800 bg-gray-900/50 p-6">
                    <h3 className="mb-3 font-semibold">Supported Languages</h3>
                    <div className="flex flex-wrap gap-2">
                        {['Python', 'JavaScript', 'TypeScript'].map((lang) => (
                            <span
                                key={lang}
                                className="rounded-full bg-gray-800 px-3 py-1 text-sm text-gray-300"
                            >
                                {lang}
                            </span>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}
