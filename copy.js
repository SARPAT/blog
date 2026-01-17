document.addEventListener('DOMContentLoaded', function () {
    var codeBlocks = document.querySelectorAll('pre');

    codeBlocks.forEach(function (block) {
        var wrapper = document.createElement('div');
        wrapper.className = 'code-block';
        block.parentNode.insertBefore(wrapper, block);
        wrapper.appendChild(block);

        var button = document.createElement('button');
        button.className = 'copy-btn';
        button.setAttribute('aria-label', 'Copy code');
        wrapper.appendChild(button);

        button.addEventListener('click', function () {
            var code = block.textContent;
            navigator.clipboard.writeText(code).then(function () {
                button.classList.add('copied');
                setTimeout(function () {
                    button.classList.remove('copied');
                }, 2000);
            });
        });
    });
});
