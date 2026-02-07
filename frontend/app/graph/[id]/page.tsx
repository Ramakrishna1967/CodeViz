'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import { getGraph, explainCode } from '@/lib/api'
import { GraphNode, GraphEdge } from '@/lib/types'
import GraphViewer from '@/components/GraphViewer'
import ChatPanel from '@/components/ChatPanel'
import SearchBar from '@/components/SearchBar'
import CodePreview from '@/components/CodePreview'

export default function GraphPage() {
    const params = useParams()
    const repoId = params.id as string

    const [nodes, setNodes] = useState<GraphNode[]>([])
    const [edges, setEdges] = useState<GraphEdge[]>([])
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState('')
    const [selectedNode, setSelectedNode] = useState<any>(null)
    const [explanation, setExplanation] = useState('')
    const [showChat, setShowChat] = useState(true)

    useEffect(() => {
        async function loadGraph() {
            try {
                const data = await getGraph(repoId)
                setNodes(data.nodes)
                setEdges(data.edges)
            } catch (err) {
                setError('Failed to load graph data')
            } finally {
                setIsLoading(false)
            }
        }

        loadGraph()
    }, [repoId])

    const handleNodeClick = async (nodeId: string, nodeData: any) => {
        setSelectedNode({ id: nodeId, ...nodeData })

        try {
            const result = await explainCode(repoId, nodeId)
            setExplanation(result.explanation)
        } catch (err) {
            setExplanation('Unable to generate explanation')
        }
    }

    const handleSearchResult = (result: any) => {
        setSelectedNode({
            id: result.name,
            label: result.name,
            fullPath: result.file_path,
            startLine: result.start_line,
            endLine: result.end_line,
        })
    }

    if (isLoading) {
        return (
            <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center">
                <div className="text-center">
                    <div className="mb-4 h-8 w-8 animate-spin rounded-full border-4 border-primary-500 border-t-transparent mx-auto" />
                    <p className="text-gray-400">Loading graph...</p>
                </div>
            </div>
        )
    }

    if (error) {
        return (
            <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center">
                <div className="rounded-lg border border-red-500/30 bg-red-500/10 px-6 py-4 text-red-400">
                    {error}
                </div>
            </div>
        )
    }

    return (
        <div className="flex h-[calc(100vh-4rem)]">
            <div className="flex flex-1 flex-col">
                <div className="flex items-center justify-between border-b border-gray-800 px-4 py-3">
                    <div className="flex items-center space-x-4">
                        <h2 className="font-semibold">Codebase Graph</h2>
                        <span className="rounded-full bg-gray-800 px-2 py-1 text-xs text-gray-400">
                            {nodes.length} nodes
                        </span>
                    </div>
                    <div className="flex items-center space-x-4">
                        <SearchBar repoId={repoId} onResultClick={handleSearchResult} />
                        <button
                            onClick={() => setShowChat(!showChat)}
                            className={`rounded-lg px-3 py-1.5 text-sm transition-colors ${showChat
                                ? 'bg-primary-500 text-white'
                                : 'bg-gray-800 text-gray-400 hover:text-white'
                                }`}
                        >
                            Chat
                        </button>
                    </div>
                </div>

                <div className="flex flex-1 overflow-hidden">
                    <div className={`${selectedNode ? 'w-2/3' : 'w-full'} h-full transition-all`}>
                        <GraphViewer nodes={nodes} edges={edges} onNodeClick={handleNodeClick} />
                    </div>

                    {selectedNode && (
                        <div className="w-1/3 border-l border-gray-800">
                            <CodePreview
                                fileName={selectedNode.fullPath || selectedNode.label}
                                code={`[Code for ${selectedNode.label}]`}
                                startLine={selectedNode.startLine}
                                endLine={selectedNode.endLine}
                                explanation={explanation}
                                onClose={() => setSelectedNode(null)}
                            />
                        </div>
                    )}
                </div>
            </div>

            {showChat && (
                <div className="w-80 border-l border-gray-800 bg-gray-900/50">
                    <ChatPanel repoId={repoId} />
                </div>
            )}
        </div>
    )
}
