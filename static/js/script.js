// for add_edit buttons outside form to trigger hidden button inside the form
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('visible_submit').addEventListener('click', function() {
        document.getElementById('hidden_submit').click();
    });
});
