'use client'

import { useState, useRef, useEffect } from 'react'
import { chatWithCodebase } from '@/lib/api'

interface Message {
    id: string
    role: 'user' | 'assistant'
    content: string
    references?: Array<{
        file: string
        start_line: number
        end_line: number
    }>
}

interface ChatPanelProps {
    repoId: string
    onReferenceClick?: (file: string, startLine: number, endLine: number) => void
}

export default function ChatPanel({ repoId, onReferenceClick }: ChatPanelProps) {
    const [messages, setMessages] = useState<Message[]>([
        {
            id: '1',
            role: 'assistant',
            content: 'Hello! I can help you understand this codebase. Ask me anything about its structure, functions, or architecture.',
        },
    ])
    const [input, setInput] = useState('')
    const [isLoading, setIsLoading] = useState(false)
    const messagesEndRef = useRef<HTMLDivElement>(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()

        if (!input.trim() || isLoading) return

        const userMessage: Message = {
            id: Date.now().toString(),
            role: 'user',
            content: input,
        }

        setMessages((prev) => {
            const newMessages = [...prev, userMessage]
            return newMessages.slice(-50)
        })
        setInput('')
        setIsLoading(true)

        try {
            const response = await chatWithCodebase(repoId, input)

            const assistantMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: response.response,
                references: response.references,
            }

            setMessages((prev) => {
                const newMessages = [...prev, assistantMessage]
                return newMessages.slice(-50)
            })
        } catch (error) {
            const errorMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: `Sorry, I encountered an error: ${error instanceof Error ? error.message : 'Please try again.'}`,
            }
            setMessages((prev) => {
                const newMessages = [...prev, errorMessage]
                return newMessages.slice(-50)
            })
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="flex h-full flex-col">
            <div className="border-b border-gray-800 px-4 py-3">
                <h3 className="font-semibold">Chat with AI</h3>
                <p className="text-xs text-gray-500">Ask questions about the codebase</p>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((message) => (
                    <div
                        key={message.id}
                        className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div
                            className={`max-w-[85%] rounded-lg px-4 py-3 ${message.role === 'user'
                                ? 'bg-primary-500 text-white'
                                : 'bg-gray-800 text-gray-100'
                                }`}
                        >
                            <p className="text-sm whitespace-pre-wrap">{message.content}</p>

                            {message.references && message.references.length > 0 && (
                                <div className="mt-3 flex flex-wrap gap-2">
                                    {message.references.map((ref, index) => (
                                        <button
                                            key={index}
                                            onClick={() => onReferenceClick?.(ref.file, ref.start_line, ref.end_line)}
                                            className="rounded bg-gray-700 px-2 py-1 text-xs text-gray-300 hover:bg-gray-600"
                                        >
                                            {ref.file}:{ref.start_line}-{ref.end_line}
                                        </button>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                ))}

                {isLoading && (
                    <div className="flex justify-start">
                        <div className="rounded-lg bg-gray-800 px-4 py-3">
                            <div className="flex space-x-2">
                                <div className="h-2 w-2 animate-bounce rounded-full bg-gray-500" />
                                <div className="h-2 w-2 animate-bounce rounded-full bg-gray-500" style={{ animationDelay: '0.2s' }} />
                                <div className="h-2 w-2 animate-bounce rounded-full bg-gray-500" style={{ animationDelay: '0.4s' }} />
                            </div>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            <form onSubmit={handleSubmit} className="border-t border-gray-800 p-4">
                <div className="flex space-x-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask about the codebase..."
                        disabled={isLoading}
                        className="flex-1 rounded-lg border border-gray-700 bg-gray-900 px-4 py-2 text-sm text-white placeholder-gray-500 focus:border-primary-500 focus:outline-none disabled:opacity-50"
                    />
                    <button
                        type="submit"
                        disabled={isLoading || !input.trim()}
                        className="rounded-lg bg-primary-500 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-primary-600 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        Send
                    </button>
                </div>
            </form>
        </div>
    )
}
