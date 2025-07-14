// gift-form.js
// 控制送禮紀錄表單送出與 localStorage 操作

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('giftForm');
    if (!form) return;
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        // TODO: 取得表單資料，存入 localStorage
        // 之後可加上驗證與提示
        alert('送禮紀錄功能尚未實作');
    });
});
