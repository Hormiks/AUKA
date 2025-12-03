// Estado global
let selectedProducts = [];
const WHATSAPP_NUMBER = '56975132176'; // Actualizar con número real
const EMAIL = 'romerodaniela957@gmail.com';

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    initializeTabs();
    loadSelectedProducts();
    updateSelectedBar();
    
    // Cerrar modal al hacer click fuera
    const modal = document.getElementById('requestModal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeRequestForm();
            }
        });
    }
    
    // Cerrar modal con ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeRequestForm();
        }
    });
});

// Sistema de pestañas
function initializeTabs() {
    const triggers = document.querySelectorAll('.tab-trigger');
    const contents = document.querySelectorAll('.tab-content');
    
    triggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            const tabId = trigger.getAttribute('data-tab');
            
            // Remover activos
            triggers.forEach(t => {
                t.classList.remove('active');
                t.setAttribute('aria-selected', 'false');
            });
            contents.forEach(c => c.classList.remove('active'));
            
            // Activar seleccionado
            trigger.classList.add('active');
            trigger.setAttribute('aria-selected', 'true');
            const content = document.getElementById(`tab-${tabId}`);
            if (content) {
                content.classList.add('active');
            }
        });
    });
}

// Toggle producto
function toggleProduct(productId, productName, category = 'General') {
    const index = selectedProducts.findIndex(p => p.id === productId);
    const card = document.querySelector(`[data-product-id="${productId}"]`);
    const button = card?.querySelector('.product-btn');
    const buttonText = button?.querySelector('.product-btn-text');
    
    if (index > -1) {
        // Deseleccionar
        selectedProducts.splice(index, 1);
        card?.classList.remove('selected');
        if (buttonText) buttonText.textContent = 'Seleccionar';
        if (button) {
            button.classList.remove('bg-green-600', 'text-white');
            button.classList.add('border-green-600', 'text-green-700');
        }
    } else {
        // Seleccionar
        selectedProducts.push({ 
            id: productId, 
            name: productName,
            category: category
        });
        card?.classList.add('selected');
        if (buttonText) buttonText.textContent = 'Seleccionado';
        if (button) {
            button.classList.add('bg-green-600', 'text-white');
            button.classList.remove('border-green-600', 'text-green-700');
        }
    }
    
    saveSelectedProducts();
    updateSelectedBar();
}

// Actualizar barra de seleccionados
function updateSelectedBar() {
    const bar = document.getElementById('selectedProductsBar');
    const count = document.getElementById('selectedCount');
    const text = document.getElementById('selectedText');
    
    if (selectedProducts.length > 0) {
        bar?.classList.add('show');
        if (count) count.textContent = selectedProducts.length;
        if (text) {
            text.textContent = selectedProducts.length === 1 
                ? 'producto seleccionado' 
                : 'productos seleccionados';
        }
    } else {
        bar?.classList.remove('show');
    }
}

// Guardar en localStorage
function saveSelectedProducts() {
    try {
        localStorage.setItem('aukaSelectedProducts', JSON.stringify(selectedProducts));
    } catch (e) {
        console.warn('No se pudo guardar en localStorage:', e);
    }
}

// Cargar de localStorage
function loadSelectedProducts() {
    try {
        const saved = localStorage.getItem('aukaSelectedProducts');
        if (saved) {
            selectedProducts = JSON.parse(saved);
            // Restaurar estado visual
            selectedProducts.forEach(product => {
                const card = document.querySelector(`[data-product-id="${product.id}"]`);
                if (card) {
                    card.classList.add('selected');
                    const button = card.querySelector('.product-btn');
                    const buttonText = button?.querySelector('.product-btn-text');
                    if (buttonText) buttonText.textContent = 'Seleccionado';
                    if (button) {
                        button.classList.add('bg-green-600', 'text-white');
                        button.classList.remove('border-green-600', 'text-green-700');
                    }
                }
            });
        }
    } catch (e) {
        console.warn('No se pudo cargar de localStorage:', e);
    }
}

// Abrir formulario
function openRequestForm() {
    if (selectedProducts.length === 0) {
        alert('Por favor selecciona al menos un producto');
        return;
    }
    
    const modal = document.getElementById('requestModal');
    const list = document.getElementById('selectedProductsList');
    
    // Mostrar productos seleccionados
    list.innerHTML = `
        <div>
            <h3 class="text-green-800 mb-3 font-semibold text-lg">Productos Seleccionados:</h3>
            <div class="space-y-2">
                ${selectedProducts.map((p, i) => `
                    <div class="selected-product-item">
                        <p>${i + 1}. ${escapeHtml(p.name)}</p>
                        ${p.category ? `<p class="category">${escapeHtml(p.category)}</p>` : ''}
                    </div>
                `).join('')}
            </div>
        </div>
    `;
    
    modal?.classList.add('show');
    document.body.style.overflow = 'hidden';
}

// Cerrar formulario
function closeRequestForm() {
    const modal = document.getElementById('requestModal');
    modal?.classList.remove('show');
    document.body.style.overflow = '';
    const form = document.getElementById('requestForm');
    if (form) form.reset();
    const errorMsg = document.getElementById('formError');
    if (errorMsg) errorMsg.style.display = 'none';
}

// Enviar formulario
function submitForm(method) {
    const name = document.getElementById('formName')?.value.trim();
    const email = document.getElementById('formEmail')?.value.trim();
    const phone = document.getElementById('formPhone')?.value.trim();
    const message = document.getElementById('formMessage')?.value.trim();
    const errorMsg = document.getElementById('formError');
    
    // Validar
    if (!name || !email || !phone) {
        if (errorMsg) errorMsg.style.display = 'block';
        return;
    }
    
    if (errorMsg) errorMsg.style.display = 'none';
    
    // Construir mensaje
    const productList = selectedProducts
        .map((p, i) => `${i + 1}. ${p.name}${p.category ? ` (${p.category})` : ''}`)
        .join('\n');
    
    const fullMessage = `Hola! Me gustaría solicitar información sobre los siguientes productos:

${productList}

Mis datos de contacto:
Nombre: ${name}
Email: ${email}
Teléfono: ${phone}

Mensaje adicional:
${message || 'Ninguno'}`;
    
    if (method === 'whatsapp') {
        const encodedMessage = encodeURIComponent(fullMessage);
        window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodedMessage}`, '_blank');
    } else {
        const subject = encodeURIComponent('Solicitud de Productos - Auka');
        const body = encodeURIComponent(fullMessage);
        window.location.href = `mailto:${EMAIL}?subject=${subject}&body=${body}`;
    }
    
    // Limpiar selección
    selectedProducts = [];
    saveSelectedProducts();
    updateSelectedBar();
    
    // Cerrar modal
    closeRequestForm();
    
    // Limpiar selecciones visuales
    document.querySelectorAll('.product-card.selected').forEach(card => {
        card.classList.remove('selected');
        const button = card.querySelector('.product-btn');
        const buttonText = button?.querySelector('.product-btn-text');
        if (buttonText) buttonText.textContent = 'Seleccionar';
        if (button) {
            button.classList.remove('bg-green-600', 'text-white');
            button.classList.add('border-green-600', 'text-green-700');
        }
    });
    
    // Mostrar mensaje de éxito
    alert('¡Solicitud enviada! Te contactaremos pronto.');
}

// Función auxiliar para escapar HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
