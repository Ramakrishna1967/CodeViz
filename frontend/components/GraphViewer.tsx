'use client'

import { useCallback, useEffect, useState } from 'react'
import {
    ReactFlow,
    MiniMap,
    Controls,
    Background,
    useNodesState,
    useEdgesState,
    Node,
    Edge,
    BackgroundVariant,
} from '@xyflow/react'
import '@xyflow/react/dist/style.css'

interface GraphViewerProps {
    nodes: Array<{
        id: string
        data: { label: string; fullPath?: string }
        type: string
        style?: Record<string, string>
    }>
    edges: Array<{
        id: string
        source: string
        target: string
        type: string
    }>
    onNodeClick?: (nodeId: string, nodeData: any) => void
}

const NODE_COLORS: Record<string, string> = {
    repo: '#6366f1',
    file: '#22c55e',
    function: '#eab308',
    class: '#ef4444',
    module: '#8b5cf6',
}

function layoutNodes(nodes: any[]): any[] {
    const nodesByType: Record<string, any[]> = {}

    nodes.forEach(node => {
        const type = node.type || 'default'
        if (!nodesByType[type]) {
            nodesByType[type] = []
        }
        nodesByType[type].push(node)
    })

    const typeOrder = ['repo', 'file', 'class', 'function', 'module']
    let yOffset = 0
    const layoutedNodes: any[] = []

    typeOrder.forEach(type => {
        const typeNodes = nodesByType[type] || []
        const nodesPerRow = type === 'repo' ? 1 : type === 'file' ? 4 : 6

        typeNodes.forEach((node, index) => {
            const row = Math.floor(index / nodesPerRow)
            const col = index % nodesPerRow
            const xSpacing = type === 'file' ? 250 : 180
            const centerOffset = typeof window !== 'undefined' ? window.innerWidth / 2 - 400 : 400
            const xOffset = -(nodesPerRow * xSpacing) / 2 + col * xSpacing

            layoutedNodes.push({
                ...node,
                position: { x: xOffset + centerOffset, y: yOffset + row * 100 },
                style: {
                    ...node.style,
                    backgroundColor: NODE_COLORS[type] || '#6b7280',
                    color: '#fff',
                    padding: '10px 15px',
                    borderRadius: '8px',
                    fontSize: '12px',
                    fontWeight: 500,
                },
            })
        })

        if (typeNodes.length > 0) {
            const rows = Math.ceil(typeNodes.length / nodesPerRow)
            yOffset += rows * 100 + 80
        }
    })

    return layoutedNodes
}

export default function GraphViewer({ nodes, edges, onNodeClick }: GraphViewerProps) {
    const layoutedNodes = layoutNodes(nodes)
    const [flowNodes, setNodes, onNodesChange] = useNodesState(layoutedNodes)
    const [flowEdges, setEdges, onEdgesChange] = useEdgesState(edges)

    useEffect(() => {
        setNodes(layoutNodes(nodes))
        setEdges(edges)
    }, [nodes, edges, setNodes, setEdges])

    const handleNodeClick = useCallback(
        (_: React.MouseEvent, node: Node) => {
            if (onNodeClick) {
                onNodeClick(node.id, node.data)
            }
        },
        [onNodeClick]
    )

    return (
        <div className="h-full w-full">
            <ReactFlow
                nodes={flowNodes}
                edges={flowEdges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onNodeClick={handleNodeClick}
                fitView
                minZoom={0.1}
                maxZoom={2}
                defaultEdgeOptions={{
                    style: { stroke: '#6366f1', strokeWidth: 2 },
                    animated: true,
                }}
            >
                <Controls className="bg-gray-900 border-gray-700" />
                <MiniMap
                    nodeColor={(node) => NODE_COLORS[node.type as string] || '#6b7280'}
                    className="bg-gray-900 border border-gray-700 rounded-lg"
                />
                <Background variant={BackgroundVariant.Dots} gap={20} size={1} color="#333" />
            </ReactFlow>
        </div>
    )
}
