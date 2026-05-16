// Redireciona para o login se não houver token no localStorage
// Inclua este script no <head> de TODAS as páginas protegidas (dashboard, empresas, projetos, etc)

(function() {
    const token = localStorage.getItem("token");
    const currentPath = window.location.pathname;
    const publicPages = ['/login', '/cadastro', '/esqueceu-senha', '/criar-senha'];

    // Se não tem token e não está numa página pública
    if (!token && !publicPages.some(page => currentPath.includes(page))) {
        // Se a página atual for um arquivo HTML direto (ex: /telas/templates/dashboard.html), 
        // direcionamos pro login.html
        if (window.location.href.includes('.html')) {
             const basePath = window.location.href.substring(0, window.location.href.lastIndexOf('/'));
             window.location.href = basePath + '/login.html';
        } else {
             window.location.href = "/login";
        }
    }
})();
