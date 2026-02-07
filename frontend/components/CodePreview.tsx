'use client'

interface CodePreviewProps {
    fileName: string
    code: string
    startLine?: number
    endLine?: number
    explanation?: string
    onClose?: () => void
}

export default function CodePreview({
    fileName,
    code,
    startLine,
    endLine,
    explanation,
    onClose,
}: CodePreviewProps) {
    const lines = code.split('\n')
    const displayStartLine = startLine || 1

    return (
        <div className="flex h-full flex-col overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
            <div className="flex items-center justify-between border-b border-gray-700 px-4 py-2">
                <div className="flex items-center space-x-2">
                    <span className="text-sm font-medium text-white">{fileName}</span>
                    {startLine && endLine && (
                        <span className="text-xs text-gray-500">
                            Lines {startLine}-{endLine}
                        </span>
                    )}
                </div>
                {onClose && (
                    <button
                        onClick={onClose}
                        className="text-gray-400 hover:text-white"
                    >
                        X
                    </button>
                )}
            </div>

            <div className="flex-1 overflow-auto">
                <pre className="p-4">
                    <code className="text-sm">
                        {lines.map((line, index) => (
                            <div key={index} className="flex">
                                <span className="mr-4 select-none text-gray-600">
                                    {displayStartLine + index}
                                </span>
                                <span className="text-gray-200">{line}</span>
                            </div>
                        ))}
                    </code>
                </pre>
            </div>

            {explanation && (
                <div className="border-t border-gray-700 bg-gray-800/50 p-4">
                    <h4 className="mb-2 text-sm font-medium text-primary-400">AI Explanation</h4>
                    <p className="text-sm text-gray-300">{explanation}</p>
                </div>
            )}
        </div>
    )
}
