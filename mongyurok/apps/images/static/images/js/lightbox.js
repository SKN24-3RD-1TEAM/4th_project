/* 이미지 카드 클릭 → 라이트박스 (REQ-HIST-04 1-1 이미지 크게 보기) */
(function () {
  "use strict";
  const lightbox = document.getElementById("lightbox");
  if (!lightbox) return;

  const imgEl = lightbox.querySelector(".lightbox__img");
  const titleEl = lightbox.querySelector(".lightbox__title");
  const dateEl = lightbox.querySelector(".lightbox__date");
  const closeBtn = lightbox.querySelector(".lightbox__close");

  function open(card) {
    imgEl.src = card.dataset.src;
    imgEl.alt = card.dataset.title || "";
    titleEl.textContent = card.dataset.title || "";
    dateEl.textContent = card.dataset.created || "";
    lightbox.hidden = false;
    document.body.style.overflow = "hidden";
  }
  function close() {
    lightbox.hidden = true;
    imgEl.src = "";
    document.body.style.overflow = "";
  }

  document.querySelectorAll("[data-lightbox]").forEach(function (card) {
    card.addEventListener("click", function () { open(card); });
  });
  closeBtn.addEventListener("click", close);
  lightbox.addEventListener("click", function (e) {
    if (e.target === lightbox) close();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !lightbox.hidden) close();
  });
})();
