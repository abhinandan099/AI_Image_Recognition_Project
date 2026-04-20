const revealElements = document.querySelectorAll(".scroll-reveal");
const fileInput = document.getElementById("image");
const uploadZone = document.getElementById("upload-zone");
const fileName = document.getElementById("file-name");
const previewPanel = document.getElementById("preview-panel");
const imagePreview = document.getElementById("image-preview");
const modeCards = document.querySelectorAll(".mode-card");
const submitButton = document.getElementById("submit-button");
const analysisForm = document.getElementById("analysis-form");

const compareRange = document.getElementById("compare-range");
const compareOverlay = document.getElementById("compare-overlay");
const compareDivider = document.getElementById("compare-divider");

const focusCompareRange = document.getElementById("focus-compare-range");
const focusCompareOverlay = document.getElementById("focus-compare-overlay");
const focusCompareDivider = document.getElementById("focus-compare-divider");

const focusButton = document.getElementById("focus-button");
const focusOverlay = document.getElementById("focus-overlay");
const focusBackdrop = document.getElementById("focus-backdrop");
const closeFocus = document.getElementById("close-focus");
const fullscreenToggle = document.getElementById("fullscreen-toggle");
const zoomIn = document.getElementById("zoom-in");
const zoomOut = document.getElementById("zoom-out");

const toggleBoxes = document.getElementById("toggle-boxes");
const toggleOverlays = document.getElementById("toggle-overlays");
const objectRows = document.querySelectorAll(".object-row[data-target-box]");
const detectionBoxes = document.querySelectorAll(".detection-box[data-target-id]");

const viewerFrame = document.getElementById("pan-zoom-frame");
const focusViewerFrame = document.getElementById("focus-pan-zoom-frame");

let scale = 1;
let translateX = 0;
let translateY = 0;
let isDragging = false;
let dragStartX = 0;
let dragStartY = 0;
let boxesVisible = true;
let overlaysVisible = true;

function updateRevealStates() {
    revealElements.forEach((element) => {
        const rect = element.getBoundingClientRect();
        element.classList.toggle("is-visible", rect.top < window.innerHeight * 0.88);
    });
}

function updateModeCards() {
    modeCards.forEach((card) => {
        const input = card.querySelector("input[type='radio']");
        card.classList.toggle("is-selected", input.checked);
    });
}

function updatePreview(file) {
    if (!file) {
        fileName.textContent = "No file selected yet";
        previewPanel.classList.remove("has-image");
        imagePreview.classList.remove("is-visible");
        imagePreview.removeAttribute("src");
        return;
    }

    fileName.textContent = file.name;
    previewPanel.classList.add("has-image");

    const reader = new FileReader();
    reader.onload = (event) => {
        imagePreview.src = event.target.result;
        imagePreview.classList.add("is-visible");
    };
    reader.readAsDataURL(file);
}

function updateCompare(rangeElement, overlayElement, dividerElement) {
    if (!rangeElement || !overlayElement || !dividerElement) {
        return;
    }

    const width = `${rangeElement.value}%`;
    overlayElement.style.width = width;
    dividerElement.style.left = width;
}

function openFocusOverlay() {
    if (!focusOverlay) {
        return;
    }

    focusOverlay.classList.add("is-open");
    focusOverlay.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
}

function closeFocusOverlay() {
    if (!focusOverlay) {
        return;
    }

    focusOverlay.classList.remove("is-open");
    focusOverlay.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
}

function applyPanZoom(target) {
    if (!target) {
        return;
    }

    target.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
}

function resetPanZoom() {
    scale = 1;
    translateX = 0;
    translateY = 0;
    applyPanZoom(viewerFrame);
    applyPanZoom(focusViewerFrame);
}

function setBoxVisibility() {
    detectionBoxes.forEach((box) => {
        box.style.display = boxesVisible ? "block" : "none";
    });

    if (toggleBoxes) {
        toggleBoxes.classList.toggle("is-active", boxesVisible);
    }
}

function setOverlayVisibility() {
    const overlayTargets = [compareOverlay, focusCompareOverlay].filter(Boolean);
    const dividerTargets = [compareDivider, focusCompareDivider].filter(Boolean);

    overlayTargets.forEach((element) => {
        element.style.display = overlaysVisible ? "block" : "none";
    });

    dividerTargets.forEach((element) => {
        element.style.display = overlaysVisible ? "block" : "none";
    });

    if (toggleOverlays) {
        toggleOverlays.classList.toggle("is-active", overlaysVisible);
    }
}

function highlightTarget(targetId) {
    objectRows.forEach((row) => {
        row.classList.toggle("is-active", row.id === targetId);
    });

    detectionBoxes.forEach((box) => {
        box.classList.toggle("is-active", box.dataset.targetId === targetId);
        box.classList.toggle("is-dimmed", targetId && box.dataset.targetId !== targetId);
    });
}

function focusOnBox(boxElement) {
    if (!boxElement || !viewerFrame) {
        return;
    }

    const left = Number(boxElement.dataset.left || 0);
    const top = Number(boxElement.dataset.top || 0);
    const width = Number(boxElement.dataset.width || 0);
    const height = Number(boxElement.dataset.height || 0);

    scale = 1.7;
    translateX = (50 - (left + width / 2)) * 6;
    translateY = (50 - (top + height / 2)) * 6;
    applyPanZoom(viewerFrame);
    applyPanZoom(focusViewerFrame);
}

if (fileInput) {
    fileInput.addEventListener("change", (event) => {
        updatePreview(event.target.files[0]);
    });
}

if (uploadZone) {
    ["dragenter", "dragover"].forEach((eventName) => {
        uploadZone.addEventListener(eventName, (event) => {
            event.preventDefault();
            uploadZone.classList.add("is-dragover");
        });
    });

    ["dragleave", "drop"].forEach((eventName) => {
        uploadZone.addEventListener(eventName, (event) => {
            event.preventDefault();
            uploadZone.classList.remove("is-dragover");
        });
    });
}

modeCards.forEach((card) => {
    card.addEventListener("change", updateModeCards);
});
updateModeCards();

if (analysisForm && submitButton) {
    analysisForm.addEventListener("submit", () => {
        submitButton.classList.add("is-loading");
    });
}

if (compareRange) {
    compareRange.addEventListener("input", () => updateCompare(compareRange, compareOverlay, compareDivider));
    updateCompare(compareRange, compareOverlay, compareDivider);
}

if (focusCompareRange) {
    focusCompareRange.addEventListener("input", () => updateCompare(focusCompareRange, focusCompareOverlay, focusCompareDivider));
    updateCompare(focusCompareRange, focusCompareOverlay, focusCompareDivider);
}

if (focusButton) {
    focusButton.addEventListener("click", openFocusOverlay);
}

if (focusBackdrop) {
    focusBackdrop.addEventListener("click", closeFocusOverlay);
}

if (closeFocus) {
    closeFocus.addEventListener("click", closeFocusOverlay);
}

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        closeFocusOverlay();
    }
});

if (fullscreenToggle && focusOverlay) {
    fullscreenToggle.addEventListener("click", async () => {
        if (!document.fullscreenElement) {
            await focusOverlay.requestFullscreen();
        } else {
            await document.exitFullscreen();
        }
    });
}

if (toggleBoxes) {
    toggleBoxes.addEventListener("click", () => {
        boxesVisible = !boxesVisible;
        setBoxVisibility();
    });
}

if (toggleOverlays) {
    toggleOverlays.addEventListener("click", () => {
        overlaysVisible = !overlaysVisible;
        setOverlayVisibility();
    });
}

objectRows.forEach((row) => {
    row.addEventListener("mouseenter", () => highlightTarget(row.id));
    row.addEventListener("mouseleave", () => highlightTarget(null));
    row.addEventListener("click", () => {
        const targetBox = document.querySelector(`[data-box-id='${row.dataset.targetBox}']`);
        highlightTarget(row.id);
        focusOnBox(targetBox);
    });
});

detectionBoxes.forEach((box) => {
    box.addEventListener("mouseenter", () => highlightTarget(box.dataset.targetId));
    box.addEventListener("mouseleave", () => highlightTarget(null));
    box.addEventListener("click", () => {
        highlightTarget(box.dataset.targetId);
        focusOnBox(box);
    });
});

function attachPanZoom(target) {
    if (!target) {
        return;
    }

    target.addEventListener("mousedown", (event) => {
        isDragging = true;
        dragStartX = event.clientX - translateX;
        dragStartY = event.clientY - translateY;
        target.classList.add("is-dragging");
    });

    target.addEventListener("wheel", (event) => {
        event.preventDefault();
        const delta = event.deltaY < 0 ? 0.14 : -0.14;
        scale = Math.max(1, Math.min(3, scale + delta));
        applyPanZoom(viewerFrame);
        applyPanZoom(focusViewerFrame);
    });
}

attachPanZoom(viewerFrame);
attachPanZoom(focusViewerFrame);

window.addEventListener("mousemove", (event) => {
    if (!isDragging) {
        return;
    }

    translateX = event.clientX - dragStartX;
    translateY = event.clientY - dragStartY;
    applyPanZoom(viewerFrame);
    applyPanZoom(focusViewerFrame);
});

window.addEventListener("mouseup", () => {
    isDragging = false;
    if (viewerFrame) {
        viewerFrame.classList.remove("is-dragging");
    }
    if (focusViewerFrame) {
        focusViewerFrame.classList.remove("is-dragging");
    }
});

if (zoomIn) {
    zoomIn.addEventListener("click", () => {
        scale = Math.min(3, scale + 0.2);
        applyPanZoom(viewerFrame);
        applyPanZoom(focusViewerFrame);
    });
}

if (zoomOut) {
    zoomOut.addEventListener("click", () => {
        if (scale <= 1.1) {
            resetPanZoom();
            return;
        }
        scale = Math.max(1, scale - 0.2);
        applyPanZoom(viewerFrame);
        applyPanZoom(focusViewerFrame);
    });
}

window.addEventListener("scroll", updateRevealStates, { passive: true });
window.addEventListener("resize", updateRevealStates);

updateRevealStates();
setBoxVisibility();
setOverlayVisibility();
