/**
 * VendaCerta - JavaScript Principal
 * Sistema de Gestão de Metas e Comissões
 */

// Inicialização quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    console.log('VendaCerta - Sistema carregado');
    
    // Inicializar tooltips do Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Inicializar popovers do Bootstrap
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-hide de alertas após 5 segundos
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Máscaras de formatação (se houver campos)
    formatCurrency();
    formatPhone();
    formatCPF();
    formatCNPJ();
});

/**
 * Formatar campos de moeda
 */
function formatCurrency() {
    const currencyInputs = document.querySelectorAll('input[data-format="currency"]');
    currencyInputs.forEach(function(input) {
        input.addEventListener('blur', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = (parseFloat(value) / 100).toFixed(2);
            e.target.value = 'R$ ' + value.replace('.', ',');
        });
    });
}

/**
 * Formatar campos de telefone
 */
function formatPhone() {
    const phoneInputs = document.querySelectorAll('input[data-format="phone"]');
    phoneInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length <= 10) {
                value = value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
            } else {
                value = value.replace(/(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
            }
            e.target.value = value;
        });
    });
}

/**
 * Formatar campos de CPF
 */
function formatCPF() {
    const cpfInputs = document.querySelectorAll('input[data-format="cpf"]');
    cpfInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{0,2})/, '$1.$2.$3-$4');
            e.target.value = value;
        });
    });
}

/**
 * Formatar campos de CNPJ
 */
function formatCNPJ() {
    const cnpjInputs = document.querySelectorAll('input[data-format="cnpj"]');
    cnpjInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{0,2})/, '$1.$2.$3/$4-$5');
            e.target.value = value;
        });
    });
}

/**
 * Confirmar ação (para botões de delete, etc)
 */
function confirmAction(message) {
    return confirm(message || 'Tem certeza que deseja realizar esta ação?');
}

/**
 * Mostrar loading
 */
function showLoading() {
    const loadingHtml = `
        <div class="position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center" 
             style="background: rgba(0,0,0,0.5); z-index: 9999;" id="globalLoading">
            <div class="spinner-border text-light" role="status">
                <span class="visually-hidden">Carregando...</span>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', loadingHtml);
}

/**
 * Esconder loading
 */
function hideLoading() {
    const loading = document.getElementById('globalLoading');
    if (loading) {
        loading.remove();
    }
}

/**
 * Copiar texto para clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showToast('Copiado para área de transferência!', 'success');
    });
}

/**
 * Mostrar toast notification
 */
function showToast(message, type = 'info') {
    const toastHtml = `
        <div class="toast align-items-center text-white bg-${type} border-0 position-fixed bottom-0 end-0 m-3" 
             role="alert" aria-live="assertive" aria-atomic="true" style="z-index: 9999;">
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', toastHtml);
    
    const toastElement = document.querySelector('.toast:last-child');
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

// Exportar funções globais
window.VendaCerta = {
    confirmAction,
    showLoading,
    hideLoading,
    copyToClipboard,
    showToast
};
