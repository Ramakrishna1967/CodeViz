import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
    title: 'CodeViz AI - Codebase Visualization',
    description: 'AI-powered codebase visualization and understanding platform',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body className="min-h-screen bg-[#0a0a0a] text-white antialiased">
                <nav className="fixed top-0 left-0 right-0 z-50 border-b border-gray-800 bg-[#0a0a0a]/80 backdrop-blur-sm">
                    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                        <div className="flex h-16 items-center justify-between">
                            <a href="/" className="flex items-center space-x-2">
                                <span className="text-xl font-bold text-primary-400">CodeViz</span>
                                <span className="rounded bg-primary-500/20 px-2 py-0.5 text-xs text-primary-400">AI</span>
                            </a>
                            <div className="flex items-center space-x-4">
                                <a href="/analyze" className="text-sm text-gray-400 hover:text-white transition-colors">
                                    Analyze
                                </a>
                            </div>
                        </div>
                    </div>
                </nav>
                <main className="pt-16">
                    {children}
                </main>
            </body>
        </html>
    )
}
