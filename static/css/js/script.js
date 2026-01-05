// ===== ПЕРЕКЛЮЧЕНИЕ ТЕМЫ =====
const themeToggle = document.getElementById('themeToggle');
const themeIcon = themeToggle.querySelector('i');

themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('light-theme');
    if(document.body.classList.contains('light-theme')){
        themeIcon.classList.replace('fa-moon','fa-sun');
        localStorage.setItem('theme','light');
    }else{
        themeIcon.classList.replace('fa-sun','fa-moon');
        localStorage.setItem('theme','dark');
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    if(savedTheme==='light'){
        document.body.classList.add('light-theme');
        themeIcon.classList.replace('fa-moon','fa-sun');
    }
    initMatrixAnimation();
});

// ===== ВЫПАДАЮЩИЕ МЕНЮ =====
const notificationIcon = document.getElementById('notificationIcon');
const avatar = document.getElementById('avatar');
const notificationDropdown = notificationIcon.querySelector('.dropdown');
const avatarDropdown = avatar.querySelector('.dropdown');

notificationIcon.addEventListener('click', e=>{
    e.stopPropagation();
    notificationDropdown.classList.toggle('active');
    avatarDropdown.classList.remove('active');
});
avatar.addEventListener('click', e=>{
    e.stopPropagation();
    avatarDropdown.classList.toggle('active');
    notificationDropdown.classList.remove('active');
});
document.addEventListener('click', ()=>{
    notificationDropdown.classList.remove('active');
    avatarDropdown.classList.remove('active');
});
notificationDropdown.addEventListener('click', e=>e.stopPropagation());
avatarDropdown.addEventListener('click', e=>e.stopPropagation());

// ===== МАТРИЧНАЯ АНИМАЦИЯ =====
function initMatrixAnimation(){
    const matrixContainer = document.getElementById('matrixAnimation');
    if(!matrixContainer) return;
    const chars = '01abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ$+-*/=%"\'#&_(),.;:?!\\|{}<>[]^~';
    for(let i=0;i<30;i++){
        const line = document.createElement('div');
        line.className='code-line';
        line.style.left = `${Math.random()*100}%`;
        line.style.animationDelay = `${Math.random()*5}s`;
        line.style.animationDuration = `${5+Math.random()*10}s`;
        let text='';
        for(let j=0;j<10+Math.floor(Math.random()*20);j++){
            text+=chars[Math.floor(Math.random()*chars.length)];
        }
        line.textContent=text;
        matrixContainer.appendChild(line);
    }
}
