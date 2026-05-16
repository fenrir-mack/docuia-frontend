// Configurações das URLs dos microserviços (usa global CONFIG se existir, senão usa localhost)
const API_URLS = window.API_CONFIG || {
    auth: "http://localhost:8001",
    empresas: "http://localhost:8002",
    projetos: "http://localhost:8003"
};

// Funções de utilidade para o Token
function getToken() {
    return localStorage.getItem("token");
}

function setToken(token) {
    localStorage.setItem("token", token);
}

function removeToken() {
    localStorage.removeItem("token");
}

// Cabeçalhos padrão para requisições autenticadas
function authHeaders() {
    const token = getToken();
    const headers = {
        "Content-Type": "application/json"
    };
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }
    return headers;
}

// Função genérica para tratar erros da API
async function handleResponse(response) {
    if (response.status === 401) {
        // Token inválido ou expirado
        removeToken();
        window.location.href = "/login"; // Redireciona pro login
        throw new Error("Sessão expirada. Faça login novamente.");
    }
    
    const data = await response.json().catch(() => null);
    
    if (!response.ok) {
        let errorMsg = "Ocorreu um erro na requisição.";
        if (data && data.detail) {
            if (Array.isArray(data.detail)) {
                // Erros de validação do FastAPI (422) vêm em uma lista
                errorMsg = data.detail.map(err => `${err.loc.join('.')}: ${err.msg}`).join('\n');
            } else {
                errorMsg = data.detail;
            }
        }
        throw new Error(errorMsg);
    }
    
    return data;
}
