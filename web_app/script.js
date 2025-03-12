let coins = 0;
let energy = 500;

// Обработка клика на крокодила
function tap() {
    if (energy > 0) {
        coins += 1;
        energy -= 1;
        updateUI();
    }
}

// Обновление интерфейса
function updateUI() {
    document.getElementById('energy').textContent = energy;
    document.getElementById('coins').textContent = coins;
}

// Восстановление энергии каждую минуту
setInterval(() => {
    if (energy < 500) {
        energy += 10;
        updateUI();
    }
}, 60000);

// Отправка данных в бот при закрытии Web App
Telegram.WebApp.onEvent('viewportChanged', () => {
    Telegram.WebApp.sendData(JSON.stringify({ coins, energy }));
});

// Инициализация Web App
Telegram.WebApp.ready();