'use client'

interface AnalysisProgressProps {
    step: string
    percent: number
}

export default function AnalysisProgress({ step, percent }: AnalysisProgressProps) {
    return (
        <div className="rounded-lg border border-gray-800 bg-gray-900/50 p-6">
            <div className="mb-4 flex items-center justify-between">
                <span className="text-sm text-gray-400">{step}</span>
                <span className="text-sm font-medium text-primary-400">{percent}%</span>
            </div>

            <div className="h-2 overflow-hidden rounded-full bg-gray-800">
                <div
                    className="h-full rounded-full bg-gradient-to-r from-primary-500 to-primary-400 transition-all duration-300"
                    style={{ width: `${percent}%` }}
                />
            </div>

            <div className="mt-4 flex items-center space-x-2">
                <div className="h-2 w-2 animate-pulse rounded-full bg-primary-400" />
                <span className="text-xs text-gray-500">Processing...</span>
            </div>
        </div>
    )
}
