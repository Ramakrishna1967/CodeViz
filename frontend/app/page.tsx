import Link from 'next/link'

export default function Home() {
    return (
        <div className="flex min-h-[calc(100vh-4rem)] flex-col items-center justify-center px-4">
            <div className="max-w-3xl text-center">
                <h1 className="mb-6 text-5xl font-bold tracking-tight sm:text-6xl">
                    <span className="text-white">Understand any </span>
                    <span className="bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
                        codebase
                    </span>
                    <span className="text-white"> in minutes</span>
                </h1>

                <p className="mb-10 text-lg text-gray-400 sm:text-xl">
                    AI-powered visualization that turns complex repositories into interactive,
                    explorable graphs. Ask questions, trace dependencies, understand architecture.
                </p>

                <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
                    <Link
                        href="/analyze"
                        className="inline-flex items-center justify-center rounded-lg bg-primary-500 px-8 py-3 text-base font-semibold text-white transition-colors hover:bg-primary-600"
                    >
                        Analyze Repository
                    </Link>
                    <a
                        href="https://github.com"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center justify-center rounded-lg border border-gray-700 px-8 py-3 text-base font-semibold text-gray-300 transition-colors hover:border-gray-600 hover:text-white"
                    >
                        View on GitHub
                    </a>
                </div>
            </div>

            <div className="mt-20 grid max-w-4xl grid-cols-1 gap-6 px-4 sm:grid-cols-3">
                <div className="rounded-lg border border-gray-800 bg-gray-900/50 p-6">
                    <div className="mb-3 text-2xl">Graph</div>
                    <h3 className="mb-2 text-lg font-semibold">Interactive Visualization</h3>
                    <p className="text-sm text-gray-400">
                        Explore code as interactive graphs. Click nodes, trace dependencies, zoom into modules.
                    </p>
                </div>

                <div className="rounded-lg border border-gray-800 bg-gray-900/50 p-6">
                    <div className="mb-3 text-2xl">AI</div>
                    <h3 className="mb-2 text-lg font-semibold">Ask Anything</h3>
                    <p className="text-sm text-gray-400">
                        Chat with AI about the codebase. Get explanations, find patterns, understand logic.
                    </p>
                </div>

                <div className="rounded-lg border border-gray-800 bg-gray-900/50 p-6">
                    <div className="mb-3 text-2xl">Fast</div>
                    <h3 className="mb-2 text-lg font-semibold">Instant Analysis</h3>
                    <p className="text-sm text-gray-400">
                        Parse any GitHub repo in minutes. Tree-sitter powered for accurate understanding.
                    </p>
                </div>
            </div>
        </div>
    )
}
