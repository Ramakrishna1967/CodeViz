export interface GraphNode {
    id: string
    data: {
        label: string
        fullPath?: string
        startLine?: number
        endLine?: number
    }
    type: string
    style?: Record<string, string>
    position?: { x: number; y: number }
}

export interface GraphEdge {
    id: string
    source: string
    target: string
    type: string
}

export interface GraphData {
    nodes: GraphNode[]
    edges: GraphEdge[]
}

export interface ChatMessage {
    id: string
    role: 'user' | 'assistant'
    content: string
    references?: Array<{
        file: string
        start_line: number
        end_line: number
    }>
}
