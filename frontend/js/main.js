document.addEventListener('DOMContentLoaded', () => {
    // ... (código para mapear elementos da DOM, incluindo os novos filtros) ...
    const searchInput = document.getElementById('search-input');
    const statusFilter = document.getElementById('status-filter');
    const priorityFilter = document.getElementById('priority-filter');
    const totalTasksSpan = document.getElementById('total-tasks');
    const pageInfoSpan = document.getElementById('page-info');

    let currentPage = 1;
    const tasksPerPage = 5;

    // --- FUNÇÃO DE API (não muda) ---
    // ... (função apiRequest) ...

    // --- LÓGICA DE TAREFAS (ATUALIZADA) ---

    /**
     * Busca as tarefas na API com base nos filtros e página atuais.
     */
    async function loadTasks() {
        const searchTerm = searchInput.value;
        const status = statusFilter.value;
        const priority = priorityFilter.value;

        // Constrói a URL com os parâmetros
        const params = new URLSearchParams({
            page: currentPage,
            per_page: tasksPerPage,
            q: searchTerm,
            status: status,
            prioridade: priority,
        });
        
        const response = await apiRequest(`/tarefas?${params.toString()}`);
        
        if (response) {
            renderTasks(response.data);
            renderPagination(response.totalPages);
            updateStats(response.total, response.page, response.totalPages);
        }
    }

    /**
     * Renderiza a lista de tarefas na tela.
     * @param {Array} tasks - A lista de tarefas a ser renderizada.
     */
    function renderTasks(tasks) {
        // ... (limpa a task-list) ...
        
        tasks.forEach(task => {
            const taskItem = document.createElement('div');
            taskItem.className = 'task-item';
            taskItem.dataset.id = task.id;
            // ATUALIZADO: HTML do item para incluir badges
            taskItem.innerHTML = `
                <div class="task-details">
                    <h3>${task.titulo}</h3>
                    <p>${task.descricao || 'Sem descrição.'}</p>
                    <div class="task-meta">
                        <span class="badge status-${task.status.replace('_', '-')}">${task.status.replace('_', ' ')}</span>
                        <span class="badge priority-${task.prioridade}">Prioridade ${task.prioridade}</span>
                    </div>
                </div>
                <div class="task-actions">
                    <button class="btn-edit">Editar</button>
                    <button class="btn-delete">Deletar</button>
                </div>
            `;
            elements.taskList.appendChild(taskItem);
        });
    }
    
    /**
     * ATUALIZADO: Renderiza a paginação com base no total de páginas da API.
     * @param {number} totalPages - O número total de páginas.
     */
    function renderPagination(totalPages) {
        // ... (lógica para criar botões de página) ...
    }

    /**
     * NOVO: Atualiza as estatísticas de tarefas.
     */
    function updateStats(total, page, totalPages) {
        totalTasksSpan.textContent = `Total: ${total}`;
        pageInfoSpan.textContent = `Página ${page} de ${totalPages}`;
    }

    // --- LÓGICA DO MODAL (ATUALIZADA) ---
    function openModalForEdit(task) {
        // ... (preenche título e descrição) ...
        document.getElementById('task-status').value = task.status;
        document.getElementById('task-priority').value = task.prioridade;
        // ... (abre o modal) ...
    }

    async function handleTaskFormSubmit(event) {
        event.preventDefault();
        const taskData = {
            titulo: document.getElementById('task-title').value,
            descricao: document.getElementById('task-description').value,
            status: document.getElementById('task-status').value,
            prioridade: document.getElementById('task-priority').value,
        };
        // ... (lógica para POST ou PUT) ...
    }

    // --- EVENT LISTENERS ---
    // ... (listeners para login, logout, modal, etc.) ...

    // NOVO: Listeners para os filtros
    searchInput.addEventListener('input', () => {
        currentPage = 1; // Reseta para a primeira página ao buscar
        loadTasks();
    });
    statusFilter.addEventListener('change', () => {
        currentPage = 1; // Reseta para a primeira página ao filtrar
        loadTasks();
    });
    priorityFilter.addEventListener('change', () => {
        currentPage = 1; // Reseta para a primeira página ao filtrar
        loadTasks();
    });

    // ... (chamada inicial para initialize()) ...
});