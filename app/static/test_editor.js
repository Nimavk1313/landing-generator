document.addEventListener('DOMContentLoaded', function () {
    const output = document.getElementById('test-output');

    function assert(condition, message) {
        const p = document.createElement('p');
        p.textContent = message;
        p.style.color = condition ? 'green' : 'red';
        output.appendChild(p);
    }

    // Test 1: Add a link block
    document.getElementById('add-link-block').click();
    let block = document.querySelector('.block[data-type="link"]');
    assert(block !== null, 'Test 1 Passed: Link block added.');

    // Test 2: Add a text block
    document.getElementById('add-text-block').click();
    block = document.querySelector('.block[data-type="text"]');
    assert(block !== null, 'Test 2 Passed: Text block added.');

    // Test 3: Remove a block
    const firstBlock = document.querySelector('.block');
    if (firstBlock) {
        firstBlock.querySelector('.remove-block').click();
        assert(!document.contains(firstBlock), 'Test 3 Passed: Block removed.');
    } else {
        assert(false, 'Test 3 Failed: No block to remove.');
    }
});
