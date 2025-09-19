document.addEventListener('DOMContentLoaded', () => {

    const API_URL = 'http://127.0.0.1:5000/api';

    const elements = {
        authSection: document.getElementById('auth-section'),
        tasksSection: document.getElementById('tasks-section'),
        loginForm: document.getElementById('login-form'),
        registerForm: document.getElementById('register-form'),
        loginFormContainer: document.getElementById('login-form-container'),
        registerFormContainer: document.getElementById('register-form-container'),
        showRegisterLink: document.getElementById('show-register-link'),
        showLoginLink: document.getElementById('show-login-link'),
        logoutBtn: document.getElementById('logout-btn'),
        taskList: document.getElementById('task-list'),
        taskModal: document.getElementById('task-modal'),
        taskForm: document.getElementById('task-form'),
        addTaskBtn: document.getElementById('add-task-btn'),
        closeModalBtn: document.querySelector('.close-btn'),
        modalTitle: document.getElementById('modal-title'),
        paginationContainer: document.getElementById('pagination-container'),
        searchInput: document.getElementById('search-input'),
        statusFilter: document.getElementById('status-filter'),
        priorityFilter: document.getElementById('priority-filter'),
        totalTasksSpan: document.getElementById('total-tasks'),
        pageInfoSpan: document.getElementById('page-info'),
    };

    let currentPage = 1;
    const tasksPerPage = 5;
    let allTasksCache = []; // Cache para guardar a lista de tarefas da página atual

    async function apiRequest(endpoint, method = 'GET', body = null) {
        const token = localStorage.getItem('accessToken');
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        try {
            const response = await fetch(`${API_URL}${endpoint}`, {
                method, headers, body: body ? JSON.stringify(body) : null,
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.msg || 'Ocorreu um erro.');
            }
            if (response.status === 204 || (response.status === 200 && method === 'DELETE')) return {};
            return response.json();
        } catch (error) {
            console.error('API Error:', error);
            alert(`Erro: ${error.message}`);
            if (String(error.message).includes("Token")) handleLogout();
            return null;
        }
    }

    async function handleLogin(e) {
        e.preventDefault();
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-senha').value;
        const data = await apiRequest('/auth/login', 'POST', { email, senha: password });
        if (data && data.access_token) {
            localStorage.setItem('accessToken', data.access_token);
            elements.loginForm.reset();
            showTasksView();
        }
    }

    async function handleRegister(e) {
        e.preventDefault();
        const nome = document.getElementById('register-nome').value;
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-senha').value;
        const data = await apiRequest('/auth/register', 'POST', { nome, email, senha: password });
        if (data) {
            alert(data.msg);
            elements.registerForm.reset();
            showLoginView();
        }
    }

    function handleLogout() {
        localStorage.removeItem('accessToken');
        showAuthView();
    }

    function showAuthView() {
        elements.tasksSection.classList.add('hidden');
        elements.authSection.classList.remove('hidden');
        showLoginView();
    }

    function showLoginView() {
        elements.loginFormContainer.classList.remove('hidden');
        elements.registerFormContainer.classList.add('hidden');
    }

    function showRegisterView() {
        elements.loginFormContainer.classList.add('hidden');
        elements.registerFormContainer.classList.remove('hidden');
    }

    function showTasksView() {
        elements.authSection.classList.add('hidden');
        elements.tasksSection.classList.remove('hidden');
        currentPage = 1;
        loadTasks();
    }

    async function loadTasks() {
        const params = new URLSearchParams({
            page: currentPage, per_page: tasksPerPage,
            q: elements.searchInput.value, status: elements.statusFilter.value,
            prioridade: elements.priorityFilter.value,
        });
        const response = await apiRequest(`/tarefas?${params.toString()}`);
        if (response) {
            allTasksCache = response.data; // Armazena a lista atual
            renderTasks(response.data);
            renderPagination(response.totalPages);
            updateStats(response.total, response.page, response.totalPages);
        }
    }

    function renderTasks(tasks) {
        elements.taskList.innerHTML = '';
        if (tasks.length === 0) {
            elements.taskList.innerHTML = '<p style="text-align: center; color: #6c757d;">Nenhuma tarefa encontrada para os filtros selecionados.</p>';
            return;
        }
        tasks.forEach(task => {
            const taskItem = document.createElement('div');
            taskItem.className = 'task-item';
            taskItem.dataset.id = task.id;
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

    function renderPagination(totalPages) {
        elements.paginationContainer.innerHTML = '';
        for (let i = 1; i <= totalPages; i++) {
            const button = document.createElement('button');
            button.innerText = i;
            if (i === currentPage) button.classList.add('active');
            button.addEventListener('click', () => {
                currentPage = i;
                loadTasks();
            });
            elements.paginationContainer.appendChild(button);
        }
    }

    function updateStats(total, page, totalPages) {
        elements.totalTasksSpan.textContent = `Total: ${total}`;
        elements.pageInfoSpan.textContent = `Página ${page} de ${totalPages}`;
    }

    function openModalForCreate() {
        elements.taskForm.reset();
        document.getElementById('task-id').value = '';
        elements.modalTitle.textContent = 'Adicionar Tarefa';
        elements.taskModal.classList.remove('hidden');
    }

    function openModalForEdit(task) {
        elements.taskForm.reset();
        document.getElementById('task-id').value = task.id;
        document.getElementById('task-title').value = task.titulo;
        document.getElementById('task-description').value = task.descricao;
        document.getElementById('task-status').value = task.status;
        document.getElementById('task-priority').value = task.prioridade;
        elements.modalTitle.textContent = 'Editar Tarefa';
        elements.taskModal.classList.remove('hidden');
    }

    function closeModal() {
        elements.taskModal.classList.add('hidden');
    }

    async function handleTaskFormSubmit(e) {
        e.preventDefault();
        const id = document.getElementById('task-id').value;
        const taskData = {
            titulo: document.getElementById('task-title').value,
            descricao: document.getElementById('task-description').value,
            status: document.getElementById('task-status').value,
            prioridade: document.getElementById('task-priority').value,
        };
        if (id) {
            await apiRequest(`/tarefas/${id}`, 'PUT', taskData);
        } else {
            await apiRequest('/tarefas', 'POST', taskData);
        }
        closeModal();
        loadTasks();
    }

    function handleTaskListClick(e) {
        const target = e.target;
        const taskItem = target.closest('.task-item');
        if (!taskItem) return;
        const taskId = taskItem.dataset.id;
        
        if (target.classList.contains('btn-edit')) {
            const task = allTasksCache.find(t => t.id == taskId);
            if (task) {
                openModalForEdit(task);
            }
        }

        if (target.classList.contains('btn-delete')) {
            if (confirm('Tem certeza que deseja deletar esta tarefa?')) {
                apiRequest(`/tarefas/${taskId}`, 'DELETE').then(() => loadTasks());
            }
        }
    }

    function initialize() {
        if (localStorage.getItem('accessToken')) {
            showTasksView();
        } else {
            showAuthView();
        }
    }

    elements.loginForm.addEventListener('submit', handleLogin);
    elements.registerForm.addEventListener('submit', handleRegister);
    elements.logoutBtn.addEventListener('click', handleLogout);
    elements.showRegisterLink.addEventListener('click', (e) => { e.preventDefault(); showRegisterView(); });
    elements.showLoginLink.addEventListener('click', (e) => { e.preventDefault(); showLoginView(); });
    elements.addTaskBtn.addEventListener('click', openModalForCreate);
    elements.closeModalBtn.addEventListener('click', closeModal);
    elements.taskForm.addEventListener('submit', handleTaskFormSubmit);
    elements.taskList.addEventListener('click', handleTaskListClick);
    
    const debounce = (func, delay) => {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    };
    
    const debouncedLoadTasks = debounce(() => {
        currentPage = 1;
        loadTasks();
    }, 500); // 500ms de atraso

    elements.searchInput.addEventListener('input', debouncedLoadTasks);
    elements.statusFilter.addEventListener('change', () => { currentPage = 1; loadTasks(); });
    elements.priorityFilter.addEventListener('change', () => { currentPage = 1; loadTasks(); });
    
    window.addEventListener('click', (e) => { if (e.target === elements.taskModal) closeModal(); });

    initialize();
});