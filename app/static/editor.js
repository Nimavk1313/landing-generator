document.addEventListener('DOMContentLoaded', function () {
    const pageBlocks = document.getElementById('page-blocks');
    const addLinkBlockBtn = document.getElementById('add-link-block');
    const addTextBlockBtn = document.getElementById('add-text-block');
    const addVideoBlockBtn = document.getElementById('add-video-block');
    const savePageBtn = document.getElementById('save-page');

    // Initialize SortableJS
    new Sortable(pageBlocks, {
        animation: 150,
        ghostClass: 'blue-background-class'
    });

    // Add new blocks
    addLinkBlockBtn.addEventListener('click', () => addBlock('link'));
    addTextBlockBtn.addEventListener('click', () => addBlock('text'));
    addVideoBlockBtn.addEventListener('click', () => addBlock('video'));

    function addBlock(type) {
        const block = document.createElement('div');
        block.classList.add('block');
        block.dataset.type = type;

        let content = '';
        if (type === 'link') {
            content = `<input type="text" placeholder="Link Title">
                       <input type="url" placeholder="https://example.com">`;
        } else if (type === 'text') {
            content = `<textarea placeholder="Enter your text here..."></textarea>`;
        } else if (type === 'video') {
            content = `<input type="url" placeholder="YouTube or Vimeo URL">`;
        }
        block.innerHTML = content + '<button class="remove-block">Remove</button>';
        pageBlocks.appendChild(block);
    }

    // Remove blocks
    pageBlocks.addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-block')) {
            e.target.parentElement.remove();
        }
    });

    // Save page
    savePageBtn.addEventListener('click', function () {
        const blocksData = [];
        const blocks = pageBlocks.querySelectorAll('.block');
        blocks.forEach(block => {
            const type = block.dataset.type;
            let data = { type };
            if (type === 'link') {
                data.title = block.querySelector('input[type="text"]').value;
                data.url = block.querySelector('input[type="url"]').value;
            } else if (type === 'text') {
                data.text = block.querySelector('textarea').value;
            } else if (type === 'video') {
                data.url = block.querySelector('input[type="url"]').value;
            }
            blocksData.push(data);
        });

        fetch('/api/save_page', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content: blocksData })
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                alert('Page saved successfully!');
            } else {
                alert('Error saving page.');
            }
        });
    });
});
