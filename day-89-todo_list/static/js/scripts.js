/*!
* Start Bootstrap - Clean Blog v6.0.9 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/
window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    const headerHeight = mainNav.clientHeight;
    window.addEventListener('scroll', function() {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        if ( currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                console.log(123);
                mainNav.classList.remove('is-visible', 'is-fixed');
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove(['is-visible']);
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }
        scrollPos = currentTop;
    });
})

window.addEventListener('DOMContentLoaded', () => {
  const checkboxes = document.querySelectorAll('input[type="checkbox"][id^="taskCheckbox-"]');

  checkboxes.forEach(checkbox => {
    const taskId = checkbox.id.replace('taskCheckbox-', '');
    const button = document.getElementById(`done-btn-${taskId}`);

    if (button) {
      checkbox.addEventListener('change', () => {
        button.style.display = checkbox.checked ? 'inline-block' : 'none';
      });
    }
  });
});

window.addEventListener('DOMContentLoaded', () => {
  // Handle due date and task title changes for showing Save buttons
  const tasks = document.querySelectorAll('input[id^="task-title-input-"]');

  tasks.forEach(titleInput => {
    const taskId = titleInput.id.replace('task-title-input-', '');
    const saveBtn = document.getElementById(`save-btn-${taskId}`);
    const dateInput = document.getElementById(`due-input-${taskId}`);

    const originalTitle = titleInput.value;
    const originalDate = dateInput ? dateInput.value : "";

    function maybeShowSave() {
      const titleChanged = titleInput.value !== originalTitle;
      const dateChanged = dateInput && dateInput.value !== originalDate;

      if (titleChanged || dateChanged) {
        saveBtn.style.display = 'inline-block';
      } else {
        saveBtn.style.display = 'none';
      }
    }

    if (saveBtn) {
      titleInput.addEventListener('input', maybeShowSave);
      if (dateInput) {
        dateInput.addEventListener('input', maybeShowSave);
      }
    }
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const authorSelect = document.getElementById('author');
  const sortSelect = document.getElementById('sort');
  const statusSelect = document.getElementById('status');
  const applyButton = document.getElementById('apply-filter-btn');

  const originalAuthor = authorSelect.value;
  const originalSort = sortSelect.value;
  const originalStatus = statusSelect.value;

  function checkForChanges() {
    const authorChanged = authorSelect.value !== originalAuthor;
    const sortChanged = sortSelect.value !== originalSort;
    const statusChanged = statusSelect.value !== originalStatus;

    if (authorChanged || sortChanged || statusChanged) {
      applyButton.style.display = 'inline-block';
    } else {
      applyButton.style.display = 'none';
    }
  }

  authorSelect.addEventListener('change', checkForChanges);
  sortSelect.addEventListener('change', checkForChanges);
  statusSelect.addEventListener('change', checkForChanges);
});