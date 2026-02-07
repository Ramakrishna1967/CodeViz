'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { searchCodebase, SearchResult } from '@/lib/api'

interface SearchBarProps {
    repoId: string
    onResultClick?: (result: SearchResult) => void
}

export default function SearchBar({ repoId, onResultClick }: SearchBarProps) {
    const [query, setQuery] = useState('')
    const [results, setResults] = useState<SearchResult[]>([])
    const [isSearching, setIsSearching] = useState(false)
    const [showResults, setShowResults] = useState(false)
    const searchRef = useRef<HTMLDivElement>(null)
    const debounceTimer = useRef<NodeJS.Timeout | null>(null);

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
                setShowResults(false)
            }
        }

        document.addEventListener('mousedown', handleClickOutside)
        return () => {
            document.removeEventListener('mousedown', handleClickOutside)
            if (debounceTimer.current) {
                clearTimeout(debounceTimer.current)
            }
        }
    }, [])

    const performSearch = useCallback(async (value: string) => {
        if (value.length < 2) {
            setResults([])
            setShowResults(false)
            return
        }

        setIsSearching(true)
        setShowResults(true)

        try {
            const response = await searchCodebase(repoId, value)
            setResults(response.results)
        } catch (error) {
            setResults([])
        } finally {
            setIsSearching(false)
        }
    }, [repoId])

    const handleSearch = (value: string) => {
        setQuery(value)

        if (debounceTimer.current) {
            clearTimeout(debounceTimer.current)
        }

        debounceTimer.current = setTimeout(() => {
            performSearch(value)
        }, 300)
    }

    const handleResultClick = (result: SearchResult) => {
        onResultClick?.(result)
        setShowResults(false)
        setQuery('')
    }

    return (
        <div ref={searchRef} className="relative">
            <input
                type="text"
                value={query}
                onChange={(e) => handleSearch(e.target.value)}
                onFocus={() => results.length > 0 && setShowResults(true)}
                placeholder="Search functions, classes..."
                className="w-64 rounded-lg border border-gray-700 bg-gray-900 px-4 py-2 text-sm text-white placeholder-gray-500 focus:border-primary-500 focus:outline-none"
            />

            {showResults && (
                <div className="absolute top-full left-0 z-50 mt-2 w-80 overflow-hidden rounded-lg border border-gray-700 bg-gray-900 shadow-xl">
                    {isSearching ? (
                        <div className="px-4 py-3 text-sm text-gray-400">Searching...</div>
                    ) : results.length === 0 ? (
                        <div className="px-4 py-3 text-sm text-gray-400">No results found</div>
                    ) : (
                        <div className="max-h-80 overflow-y-auto">
                            {results.map((result, index) => (
                                <button
                                    key={index}
                                    onClick={() => handleResultClick(result)}
                                    className="flex w-full items-start px-4 py-3 text-left hover:bg-gray-800"
                                >
                                    <span
                                        className={`mr-2 rounded px-1.5 py-0.5 text-xs font-medium ${result.type === 'Function'
                                            ? 'bg-yellow-500/20 text-yellow-400'
                                            : result.type === 'Class'
                                                ? 'bg-red-500/20 text-red-400'
                                                : 'bg-green-500/20 text-green-400'
                                            }`}
                                    >
                                        {result.type}
                                    </span>
                                    <div className="flex-1 overflow-hidden">
                                        <div className="truncate font-medium text-white">{result.name}</div>
                                        {result.file_path && (
                                            <div className="truncate text-xs text-gray-500">{result.file_path}</div>
                                        )}
                                    </div>
                                </button>
                            ))}
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}
