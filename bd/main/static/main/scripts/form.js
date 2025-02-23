const seeMoreButton = document.getElementById("see-more");
const arrow = document.querySelector(".arrow");
const upperLine = document.getElementById("upper-line");
const lowerLine = document.getElementById("lower-line");
let seeMore = false;
seeMoreButton.addEventListener("click", (event) => {
    document.querySelectorAll('[data-see="false"]').forEach(function(element) {
        element.style.display = seeMore ? "none": "table-cell";
    });
    seeMore = !seeMore;
    arrow.style.transform = seeMore ? "rotate(0deg)" : "rotate(180deg)";
    upperLine.style.display = seeMore ? "none" : "block";
    lowerLine.style.display = seeMore ? "block" : "none";
});

const inputs = document.querySelectorAll('.input-container input');
const selects = document.querySelectorAll('.input-container select');
const clearBtns = document.querySelectorAll('.input-container .clear-btn');

// Fonction pour afficher ou cacher la croix
function toggleClearBtn(input, clearBtn) {
    if (input.value) {
        clearBtn.style.display = 'block';
    } else {
        clearBtn.style.display = 'none';
    }
}

// Fonction pour effacer la valeur de l'input
function clearInput(input, clearBtn) {
    input.value = '';
    toggleClearBtn(input, clearBtn); // Met à jour la visibilité de la croix après effacement
}

window.onload = function () {
    const clearBtnAll = document.getElementById('clear-all');
    clearBtnAll.addEventListener('click', () => {
        inputs.forEach((input, index) => {
            const clearBtn = clearBtns[index];
            clearInput(input, clearBtn);
        });
        selects.forEach((select) => {
            select.value = "";
        })
    });

    inputs.forEach((input, index) => {
        const clearBtn = clearBtns[index];
        toggleClearBtn(input, clearBtn);
        input.addEventListener('input', () => toggleClearBtn(input, clearBtn));
        clearBtn.addEventListener('click', () => clearInput(input, clearBtn));
    });
}

