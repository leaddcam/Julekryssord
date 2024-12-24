document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input[type="text"]');

    inputs.forEach(input => {
        input.addEventListener('keydown', function(e) {
            const currentInput = e.target;
            const [row, col] = currentInput.name.replace('cell-', '').split('-').map(Number);

            switch (e.key) {
                case 'ArrowUp':
                    navigateTo(row - 1, col);
                    break;
                case 'ArrowDown':
                    navigateTo(row + 1, col);
                    break;
                case 'ArrowLeft':
                    navigateTo(row, col - 1);
                    break;
                case 'ArrowRight':
                    navigateTo(row, col + 1);
                    break;
            }
        });
    });

    function navigateTo(row, col) {
        const nextInput = document.querySelector(`input[name="cell-${row}-${col}"]`);
        if (nextInput) {
            nextInput.focus();
        }
    }
});
