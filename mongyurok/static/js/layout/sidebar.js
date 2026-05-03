// =====================================================
//  sidebar.js
// =====================================================

const sidebar  = document.getElementById('sidebar');
const toggleBtn = document.getElementById('toggle-btn');

// ── 사이드바 접기/펼치기 ──
if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
    });
}

// ── 모드 탭 전환 ──
document.querySelectorAll('.menu-item').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.menu-item').forEach(el => el.classList.remove('active'));
        btn.classList.add('active');

        const mode = btn.dataset.mode;
        const charHistory  = document.getElementById('char-history');
        const storyHistory = document.getElementById('story-history');

        if (!charHistory || !storyHistory) return;

        if (mode === 'char') {
            charHistory.classList.remove('hidden');
            storyHistory.classList.add('hidden');
        } else {
            storyHistory.classList.remove('hidden');
            charHistory.classList.add('hidden');
        }
    });
});

// ── 이어하기 클릭 (아이템 클릭 → 채팅방 이동) ──
document.querySelectorAll('.sidebar-items-group').forEach(item => {
    item.addEventListener('click', (e) => {
        // 삭제 버튼 클릭은 무시
        if (e.target.classList.contains('sidebar-delete-btn')) return;

        const roomId = item.dataset.roomId;
        const mode   = item.dataset.mode;

        if (!roomId) return;

        if (mode === 'char') {
            location.href = `/rooms/${roomId}/`;
        } else {
            location.href = `/scenarios/chats/${roomId}/`;
        }
    });
});

// ── 삭제 버튼 ──
let pendingDeleteRoomId = null;
let pendingDeleteMode   = null;
const deleteModal      = document.getElementById('delete-modal');
const deleteCancelBtn  = document.getElementById('delete-cancel-btn');
const deleteConfirmBtn = document.getElementById('delete-confirm-btn');

document.querySelectorAll('.sidebar-delete-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.stopPropagation(); // 부모 클릭(이어하기) 방지
        pendingDeleteRoomId = btn.dataset.roomId;
        pendingDeleteMode   = btn.dataset.mode;
        deleteModal.classList.add('open');
    });
});

// 취소
if (deleteCancelBtn) {
    deleteCancelBtn.addEventListener('click', () => {
        deleteModal.classList.remove('open');
        pendingDeleteRoomId = null;
        pendingDeleteMode   = null;
    });
}

// 모달 배경 클릭 취소
if (deleteModal) {
    deleteModal.addEventListener('click', (e) => {
        if (e.target === deleteModal) {
            deleteModal.classList.remove('open');
        }
    });
}

// 삭제 확인
if (deleteConfirmBtn) {
    deleteConfirmBtn.addEventListener('click', async () => {
        if (!pendingDeleteRoomId || !pendingDeleteMode) return;

        const url = pendingDeleteMode === 'char'
            ? `/rooms/${pendingDeleteRoomId}/delete/`
            : `/scenarios/chats/${pendingDeleteRoomId}/delete/`;

        const csrf = getCookie('csrftoken');

        try {
            const res = await fetch(url, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': csrf }
            });
            const data = await res.json();

            if (data.status === 'success') {
                // DOM에서 해당 아이템 제거
                const item = document.querySelector(
                    `.sidebar-items-group[data-room-id="${pendingDeleteRoomId}"]`
                );
                if (item) item.remove();
            } else {
                alert(data.message || '삭제 중 오류가 발생했습니다.');
            }
        } catch (err) {
            alert('통신 오류가 발생했습니다.');
        } finally {
            deleteModal.classList.remove('open');
            pendingDeleteRoomId = null;
            pendingDeleteMode   = null;
        }
    });
}

// CSRF 쿠키 읽기 유틸
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
}