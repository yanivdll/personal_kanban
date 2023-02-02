// draggable cards
document.addEventListener('DOMContentLoaded', (event) => {
    let dragSrcEl = ''; //the element that is being dragged

    function handleDragStart(e) {
        this.style.opacity = '0.6';

        dragSrcEl = this;

        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/html', this.innerHTML);
    }

    function handleDragEnd(e) {
        this.style.opacity = '1';
        cards.forEach(function (card) {
            card.classList.remove('over');
        });
        columns.forEach(function (column) {
            column.classList.remove('over');
        });
    }

    function handleDragOver(e) {
        e.preventDefault();
        return false;
    }

    function handleDragEnter(e) {
        e.preventDefault();
        this.classList.add('over');
    }

    function handleDragLeave(e) {
        this.classList.remove('over');
    }

    function handleDrop(e) {
        const target = e.target;
        if (this) {
            e.stopPropagation(); // stops the browser from redirecting.
            dragSrcEl.parentNode.removeChild(dragSrcEl);
            dragSrcEl.style.opacity = '';
            target.appendChild(dragSrcEl);
            console.log('Column ID: ' + target.id);
            console.log('Task ID: ' + dragSrcEl.id);

            fetch("/update_task_ajax/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({
                    "task_id": dragSrcEl.id,
                    "column_id": target.id,
                }),
            })
                .then((response) => {
                    console.log(response);
                    return response.json();
                })
                .then((data) => console.log(data))
                .catch((error) => console.error(error));
        }
        return false;
    }

    let cards = document.querySelectorAll('.task.card');
    let columns = document.querySelectorAll('.column');
    cards.forEach(function (card) {
        card.addEventListener('dragstart', handleDragStart);
        card.addEventListener('dragend', handleDragEnd);
    });
    columns.forEach(function (column) {
        column.addEventListener('dragover', handleDragOver);
        column.addEventListener('dragenter', handleDragEnter);
        column.addEventListener('dragleave', handleDragLeave);
        column.addEventListener('drop', handleDrop);
    });

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
});