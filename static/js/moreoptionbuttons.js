
function updateLang() {
    lang_ids = ["btn-lang-English", "btn-lang-Spanish", "btn-lang-Unknown"];
    for (id of lang_ids) {
        let lang_btn = document.getElementById(id);
        console.log(lang_btn);
        if (lang_btn.hasAttribute("checked")) {
            lang_btn.removeAttribute("checked");
        }
    }
    
    // $('.language').val("");
}


function setup() {
    $('#lang-more-options').on('click', updateLang);
}

$('document').ready(setup);