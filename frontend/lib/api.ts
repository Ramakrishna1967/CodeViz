const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface AnalyzeResult {
    repo_id: string
    status: string
    node_count: number
}

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

export interface ChatResponse {
    response: string
    references: Array<{
        file: string
        start_line: number
        end_line: number
    }>
}

export interface SearchResult {
    name: string
    type: string
    file_path?: string
    start_line?: number
    end_line?: number
}

export async function analyzeRepository(githubUrl: string): Promise<AnalyzeResult> {
    const response = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ github_url: githubUrl }),
    })

    if (!response.ok) {
        let errorMsg = 'Failed to analyze repository'
        try {
            const error = await response.json()
            errorMsg = error.detail || errorMsg
        } catch {
            const text = await response.text()
            errorMsg = text || errorMsg
        }
        throw new Error(errorMsg)
    }

    return response.json()
}

export async function getGraph(repoId: string): Promise<GraphData> {
    const response = await fetch(`${API_URL}/graph/${repoId}`)

    if (!response.ok) {
        let errorMsg = 'Failed to fetch graph data'
        try {
            const error = await response.json()
            errorMsg = error.detail || errorMsg
        } catch {
            const text = await response.text()
            errorMsg = text || errorMsg
        }
        throw new Error(errorMsg)
    }

    return response.json()
}

export async function chatWithCodebase(repoId: string, message: string): Promise<ChatResponse> {
    const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ repo_id: repoId, message }),
    })

    if (!response.ok) {
        let errorMsg = 'Failed to get response'
        try {
            const error = await response.json()
            errorMsg = error.detail || errorMsg
        } catch {
            const text = await response.text()
            errorMsg = text || errorMsg
        }
        throw new Error(errorMsg)
    }

    return response.json()
}

export async function explainCode(repoId: string, nodeId: string): Promise<{ explanation: string; code: string }> {
    const response = await fetch(`${API_URL}/explain?repo_id=${repoId}&node_id=${nodeId}`)

    if (!response.ok) {
        let errorMsg = 'Failed to get explanation'
        try {
            const error = await response.json()
            errorMsg = error.detail || errorMsg
        } catch {
            const text = await response.text()
            errorMsg = text || errorMsg
        }
        throw new Error(errorMsg)
    }

    return response.json()
}

export async function searchCodebase(repoId: string, query: string): Promise<{ results: SearchResult[] }> {
    const response = await fetch(`${API_URL}/search?repo_id=${repoId}&query=${encodeURIComponent(query)}`)

    if (!response.ok) {
        let errorMsg = 'Failed to search'
        try {
            const error = await response.json()
            errorMsg = error.detail || errorMsg
        } catch {
            const text = await response.text()
            errorMsg = text || errorMsg
        }
        throw new Error(errorMsg)
    }

    return response.json()
}
